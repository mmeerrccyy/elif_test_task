from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

# Create your models here.


class ExpenseInfo(models.Model):
    expense_name = models.CharField(max_length=20)
    cost = models.FloatField()
    date_added = models.DateField()
    user_expense = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.expense_name

    def get_absolute_url(self):
        return reverse('expense-detail', args=(self.id,))

    @property
    def get_html_url(self):
        url = reverse('expense-detail', args=(self.id,))
        return f'<a href="{url}"> {self.expense_name} </a>'
