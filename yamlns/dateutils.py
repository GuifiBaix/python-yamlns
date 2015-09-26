#!/usr/bin/env python3

import datetime


def date(*adate):
	"""Transforms almost anything into a datetime.date"""
	return Date(*adate)

def slashDate(adate) :
	"""Turns date into common Spanish 31/01/2015 format"""
	return Date(adate).slashDate

def isoDate(adate) :
	"""Turns a date in almost any format into a iso formated date string"""
	return str(Date(adate))

def compactDate(adate) :
	"""Turns a date in almost any format into a iso formated date string"""
	return Date(adate).compact

def catalanDate(adate) :
	"""Turns a date in almost any format into a catalan string like '25 de desembre'"""
	return Date(adate).catalanDate

def isoToTime(iso):
	return datetime.time(*(int(t) for t in iso.split(':')))

class Date(datetime.date) :
	"""An extension of datetime.date that provides, both
	flexible initialization and flexible formatting via
	special attributes for common representation formats.

	>> "Això va passar el dia {.catalanDate}.".format(date(2013,3,4))
	Això va passar el dia 3 de març de 2013.
	>> "Birth date: {.iso}".format(date.today())
	"""

	def __new__(cls, *args) :
		"""
		Takes as arguments either:
			- an actual datetime.date
			- a tupple (yyyy,mm,dd) or (dd,mm,yyyy)
			- strings in 'yyyy-mm-dd', 'yyyy/mm/dd', 'dd-mm-yyyy', 'dd/mm/yyyy', 'yyyymmdd'
		"""
		dateTuple = cls._extractDataTuple(*args)
		return datetime.date.__new__(cls,*dateTuple)

	@classmethod
	def _extractDataTuple(cls, *args):
		if len(args) != 1:
			return cls._extractDataTuple(tuple(args))

		adate = args[0]

		if hasattr(adate, 'strftime') :
			return adate.timetuple()[:3]

		# formated string
		for separator in '-/':
			if separator in adate:
				adate = [x for x in adate.split(separator)]

		if len(adate)==8:
			adate = adate[:4],adate[4:6],adate[6:8] 

		if len(adate) != 3:
			raise ValueError("Invalid date initializator '{}'"
				.format(args[0]))

		adate = [int(x) for x in adate]

		# reverse date
		if adate[-1]>31 and adate[0]<31:
			adate = adate[::-1]

		return adate

	@property
	def isoDate(self):
		return str(self)
	@property
	def slashDate(self):
		return self.strftime("%d/%m/%Y")
	@property
	def catalanDate(self):
		catalanMonths= (
			"gener febrer març abril maig juny "
			"juliol agost setembre octubre novembre desembre"
			).split()
		monthName = catalanMonths[self.month-1]
		de = "d'" if monthName[0] in 'aeiou' else 'de '
		return "{} {}{}".format(self.day, de, monthName)
	@property
	def compact(self):
		return self.strftime('%Y%m%d')

import unittest

unittest.TestCase.__str__ = unittest.TestCase.id

class DateUtils_Test(unittest.TestCase):

	def test_date_withDate(self):
		self.assertEqual(
			datetime.date(2015,10,30),
			date(datetime.date(2015,10,30)),
			)

	def test_date_withIso(self):
		self.assertEqual(
			datetime.date(2015,10,30),
			date('2015-10-30'),
			)

	def test_date_withTuple(self):
		self.assertEqual(
			datetime.date(2015,10,30),
			date((2015,10,30)),
			)

	def test_date_withYearMonthDay(self):
		self.assertEqual(
			datetime.date(2015,10,30),
			date((2015,10,30)),
			)

	def test_date_withTupleReversed(self):
		self.assertEqual(
			datetime.date(2015,10,30),
			date(30,10,2015),
			)

	def test_date_withSlashDate(self):
		self.assertEqual(
			datetime.date(2015,10,30),
			date('2015/10/30'),
			)

	def test_date_withCompact(self):
		self.assertEqual(
			datetime.date(2015,10,30),
			date('20151030'),
			)

	def test_date_withBadCompact(self):
		with self.assertRaises(ValueError) as e:
			date('201510303')

		self.assertEqual(e.exception.args[0],
			"Invalid date initializator '201510303'")

	def test_isoDate_withIso(self):
		self.assertEqual(
			"2015-10-30",
			isoDate('2015-10-30'),
			)

	def test_isoDate_withSlashDate(self):
		self.assertEqual(
			"2015-10-30",
			isoDate('2015/10/30'),
			)

	def test_isoDate_withDate(self):
		self.assertEqual(
			"2015-10-30",
			isoDate(datetime.date(2015,10,30)),
			)

	def test_isoDate_withTuple(self):
		self.assertEqual(
			"2015-10-30",
			isoDate((2015,10,30)),
			)

	def test_slashDate_withIso(self) :
		self.assertEqual(
			slashDate("2014-09-01"),
			"01/09/2014")

	def test_slashDate_withDate(self) :
		self.assertEqual(
			slashDate(datetime.date(2014,9,1)),
			"01/09/2014")

	def test_slashDate_withDate(self) :
		self.assertEqual(
			slashDate((2014,9,1)),
			"01/09/2014")


	def test_catalanDate_withTuple(self) :
		self.assertEqual(
			catalanDate((2014,1,1)),
			"1 de gener")

	def test_catalanDate(self) :
		self.assertEqual(
			catalanDate("2014-01-01"),
			"1 de gener")

	def test_catalanDate_whenMonthStartsWithVowel(self) :
		self.assertEqual(
			catalanDate("2014-08-01"),
			"1 d'agost")

	def test_Date_catalan(self) :
		aDate = Date("2014-01-01")
		self.assertEqual(
			aDate.catalanDate,
			"1 de gener")

	def test_Date_format(self) :
		aDate = Date("2014-01-02")
		self.assertEqual(
			"hola {} tu".format(aDate),
			"hola 2014-01-02 tu")

	def test_Date_format_catalan(self) :
		aDate = Date("2014-01-02")
		self.assertEqual(
			"hola {.catalanDate} tu".format(aDate),
			"hola 2 de gener tu")

	def test_Date_format_slash(self) :
		aDate = Date("2014-01-02")
		self.assertEqual(
			"hola {.slashDate} tu".format(aDate),
			"hola 02/01/2014 tu")

	def test_Date_format_compact(self) :
		aDate = Date("2014-01-02")
		self.assertEqual(
			aDate.isoDate,
			"2014-01-02")

	def test_Date_init_threeArgs(self) :
		aDate = Date(2014,1,2)
		self.assertEqual(
			"hola {.compact} tu".format(aDate),
			"hola 20140102 tu")

	def test_isoToTime(self):
		self.assertEqual(
			isoToTime('01:02:03:0004'),
			datetime.time(1,2,3,4))

	def test_isoToTime_zero(self):
		self.assertEqual(
			isoToTime('00:00:00:0000'),
			datetime.time(0,0))

	def test_Date_today(self) :
		aDate = Date.today()
		self.assertEqual(
			aDate.isoDate,
			str(datetime.date.today()))

class Period() :

	def __init__(self, first, lastIncluded) :
		"""
		Constructs a time period including 'first' day and 'lastIncluded' day,
		being 'first' and 'lastIncluded' strings representing ISO dates YYYY-MM-DD,
		Ie. Period from '2000-01-01' to '2000-01-02' has 2 days.
		When the last day happens before the first day it is considered an empty
		period with zero days.
		"""
		self.first = first
		self.last = lastIncluded

	def __iter__(self) :
		"Iterates on first and last"
		yield self.first
		yield self.last

	def intersect(self, other) :
		"""Returns the intersection of the receiver with other.
		If they do not overlap an empty period is returned.
		"""
		first = max(self.first, other.first)
		last = min(self.last, other.last)
		return Period(first, last)

	def empty(self) :
		"""Returns true if the period is empty, that is the
		first day is later than the last day.
		"""
		return self.last < self.first

	@property
	def days(self) :
		"""The number of days of the period"""
		return max((date(self.last)-date(self.first)).days+1,0)

	@classmethod
	def trimester(cls, year, trimester) :
		"""Returns a period of a trimester.
		Payment trimesters start the 10th of january, april, july and october.
		"""
		invoicingMonths = ['01','04','07','10']
		initialDate = '{}-{}-10'.format(
				year,
				invoicingMonths[trimester-1],
				)
		finalDate = '{}-{}-09'.format(
				year+1 if trimester==4 else year,
				invoicingMonths[trimester % 4],
				)
		return Period(initialDate, finalDate)

	def notUntil(self, start) :
		"Returns the period retained until 'start'"
		return Period(max(start, self.first), self.last)

	def notAfter(self, end) :
		"Returns the period shortened after 'end'"
		return Period(self.first, min(end, self.last))

	@property
	def t(self) :
		"Returns the period as a tuple of iso date strings"
		return tuple(self)

class Period_Test(unittest.TestCase):

	def test_trimesterPeriod_t1(self) :
		self.assertEqual(
			Period.trimester(2015, 1).t,
			('2015-01-10', '2015-04-09'))

	def test_trimesterPeriod_t2(self) :
		self.assertEqual(
			Period.trimester(2015, 2).t,
			('2015-04-10', '2015-07-09'))
		
	def test_trimesterPeriod_t3(self) :
		self.assertEqual(
			Period.trimester(2015, 3).t,
			('2015-07-10', '2015-10-09'))
		
	def test_trimesterPeriod_t4(self) :
		self.assertEqual(
			Period.trimester(2015, 4).t,
			('2015-10-10', '2016-01-09'))

	def test_empty_whenOrdered(self) :
		self.assertFalse(
			Period('2015-01-10', '2015-01-11').empty())

	def test_empty_whenSame(self) :
		self.assertFalse(
			Period('2015-01-10', '2015-01-10').empty())

	def test_empty_whenInverted(self) :
		self.assertTrue(
			Period('2015-01-10', '2015-01-09').empty())

	def test_notUntil_whenEarly(self) :
		p = Period.trimester(2015, 1)
		self.assertEqual(
			p.notUntil('2014-05-06').t,
			('2015-01-10', '2015-04-09'))

	def test_notUntil_whenInside(self) :
		p = Period.trimester(2014, 2)
		self.assertEqual(
			p.notUntil('2014-05-06').t,
			('2014-05-06', '2014-07-09'))

	def test_notUntil_whenLater(self) :
		p = Period.trimester(2012, 2)
		self.assertEqual(
			p.notUntil('2014-05-06').t,
			('2014-05-06', '2012-07-09'))
	
	def test_notAfter_whenEarly(self) :
		p = Period.trimester(2015, 1)
		self.assertEqual(
			p.notAfter('2014-05-06').t,
			('2015-01-10', '2014-05-06'))

	def test_notAfter_whenInside(self) :
		p = Period.trimester(2014, 2)
		self.assertEqual(
			p.notAfter('2014-05-06').t,
			('2014-04-10', '2014-05-06'))

	def test_notAfter_whenLater(self) :
		p = Period.trimester(2012, 2)
		self.assertEqual(
			p.notAfter('2014-05-06').t,
			('2012-04-10', '2012-07-09'))


	def test_periodDays(self) :
		self.assertEqual(
			Period("2014-05-06","2014-05-08").days,
			3)

	def test_periodDays_singleDay(self) :
		self.assertEqual(
			Period("2014-05-06","2014-05-06").days,
			1)

	def test_periodDays_leapYear(self) :
		self.assertEqual(
			Period("2012-02-01","2012-03-01").days,
			30)

	def test_periodDays_emptyPeriod(self) :
		self.assertEqual(
			Period("2014-02-01","2012-02-01").days,
			0)

	def test_periodIntersect_whenIncluded(self) :
		p1 = Period("2014-01-01","2014-03-20")
		p2 = Period("2013-01-01","2015-03-20")
		self.assertEqual(
			p1.intersect(p2).t,
			("2014-01-01","2014-03-20"))

	def test_periodIntersect_whenIncludes(self) :
		p1 = Period("2013-01-01","2015-03-20")
		p2 = Period("2014-01-01","2014-03-20")
		self.assertEqual(
			p1.intersect(p2).t,
			("2014-01-01","2014-03-20"))

	def test_periodIntersect_whenDifers(self) :
		p1 = Period("2013-01-01","2014-03-20")
		p2 = Period("2015-01-01","2016-03-20")
		self.assertEqual(
			p1.intersect(p2).t,
			("2015-01-01","2014-03-20"))

	def test_periodIntersect_whenPartiallyOverlap(self) :
		p1 = Period("2013-01-01","2015-03-20")
		p2 = Period("2015-01-01","2016-03-20")
		self.assertEqual(
			p1.intersect(p2).t,
			("2015-01-01","2015-03-20"))





def load_tests(loader, tests, ignore):
	import doctest
	tests.addTests(doctest.DocTestSuite())
	return tests

if __name__ == '__main__' :
	import sys
	if '--test' in sys.argv :
		sys.argv.remove('--test')
		sys.exit(unittest.main())

	sys.exit(main())



