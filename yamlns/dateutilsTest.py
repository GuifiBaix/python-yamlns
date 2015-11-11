#!/usr/bin/env python3

from yamlns.dateutils import (
	Period, Date,
	date, slashDate, isoDate, catalanDate,
	isoToTime,
	)
import datetime

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

	def test_isoToTime_ellided(self):
		self.assertEqual(
			isoToTime('01:02'),
			datetime.time(1,2,0,0))

	def test_Date_today(self) :
		aDate = Date.today()
		self.assertEqual(
			aDate.isoDate,
			str(datetime.date.today()))

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



if __name__ == '__main__' :
	sys.exit(unittest.main())



