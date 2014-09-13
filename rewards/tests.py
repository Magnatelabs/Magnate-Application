"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from .models import *
from django.contrib.auth.models import User
import datetime


class SimpleTest(TestCase):
	def setUp(self):
		self.user = User.objects.create(username='a')

	def test_agenda(self):
		self.assertEquals(Agenda.objects.count(), 0)
		self.assertEquals(HangoutAgenda.objects.count(), 0)
		self.assertEquals(FundraisingAgenda.objects.count(), 0)
		
		ha = HangoutAgenda.objects.create(user=self.user, date=datetime.datetime(2014,7,15))

		self.assertEquals(Agenda.objects.count(), 1)
		self.assertEquals(HangoutAgenda.objects.count(), 1)
		self.assertEquals(FundraisingAgenda.objects.count(), 0)

		fa = FundraisingAgenda.objects.create(user=self.user, date=datetime.datetime(2014,8,14))

		self.assertEquals(Agenda.objects.count(), 2)
		self.assertEquals(HangoutAgenda.objects.count(), 1)
		self.assertEquals(FundraisingAgenda.objects.count(), 1)

		self.assertEquals(HangoutAgenda.objects.all()[0].pk, ha.pk)
		self.assertEquals(FundraisingAgenda.objects.all()[0].pk, fa.pk)

		aa = Agenda.objects.create(user=self.user, date=datetime.datetime(2015,5,15))
		self.assertEquals(Agenda.objects.count(), 3)
		self.assertEquals(HangoutAgenda.objects.count(), 1)
		self.assertEquals(FundraisingAgenda.objects.count(), 1)
