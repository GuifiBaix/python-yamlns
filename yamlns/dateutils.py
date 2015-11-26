#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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
	"""Turns a string representing an iso time into a time"""
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
		"""Returns the period as a tuple of iso date strings
		>>> Period("2015-02-20", "2015-03-02").t
		('2015-02-20', '2015-03-02')
		"""
		return tuple(self)


def load_tests(loader, tests, ignore):
	import doctest
	tests.addTests(doctest.DocTestSuite())
	return tests



