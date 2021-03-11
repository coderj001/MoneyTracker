from django.contrib.auth.models import User
from django.test import TestCase
from expenses.models import Expense, Catagory

user = User.objects.get(username='admintest')


class ExpenseTestCase(TestCase):
    def setUp(self):
        self.expense = Expense.objects.create(
            amount=1000,
            description='test case',
            owner=user,
            category='BUSSINESS'
        )

    def test_expense_model(self):
        d = self.expense
        self.assertTrue(isinstance(d, Expense))


class CatagoryTestCase(TestCase):
    def setUp(self):
        self.category = Catagory.objects.create(
            name='TestCase'
        )

    def test_catagory_model(self):
        d = self.category
        self.assertTrue(isinstance(d, Catagory))
        self.assertEqual(str(d), 'TestCase')
