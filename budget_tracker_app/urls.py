from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView
from django.urls import path

from . import views

urlpatterns = [
    path('welcome/', views.WelcomeView.as_view(), name='welcome'),
    path('sign_up/', views.SignUpView.as_view(), name='sign_up'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('', login_required(views.LoggedIndex.as_view(), login_url='welcome'), name='index'),
    path('logout/', LogoutView.as_view(next_page="/"), name='logout'),
    path('add_expense/', views.add_expense, name='add_expense'),
    path('expense/<int:expense_id>/details/', views.expense_details, name='expense-detail'),
    path('expense/<int:expense_id>/delete/', views.DeleteExpense.as_view(), name='expense-delete'),
    # path('add_expense/', views.add_expense, name='add_expense'),
]
