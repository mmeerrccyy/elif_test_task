from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView
from django.urls import path

from . import views

urlpatterns = [
    path('welcome/', views.WelcomeView.as_view(), name='welcome'),
    path('sign_up/', views.SignUpView.as_view(), name='sign_up'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('', login_required(views.LoggedIndex.as_view(), login_url='welcome'), name='index'),
    path('logout/', login_required(LogoutView.as_view(next_page="/"), login_url='welcome'), name='logout'),
    path('add_expense/', login_required(views.add_expense, login_url='welcome'), name='add_expense'),
    path('expense/<int:expense_id>/details/', login_required(views.expense_details, login_url='welcome'),
         name='expense-detail'),
    path('expense/<int:expense_id>/delete/', login_required(views.DeleteExpense.as_view(), login_url='welcome'),
         name='expense-delete'),
    path('expense/<int:pk>/edit/', login_required(views.EventEdit.as_view(), login_url='welcome'), name='expense-edit'),
]
