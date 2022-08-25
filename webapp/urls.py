from django.urls import path
from . import views

urlpatterns = [
    path('', views.EmployeesListAPIView.as_view()),
    path('<int:id>/', views.EmployeeDetailAPIView.as_view())
]