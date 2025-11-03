from django.urls import path
from . import views

urlpatterns=[path('', views.entries_home, name='entries_home'),
             path('entry/<int:pk>/', views.entry_detail, name='entry_detail'),
             path('entry/<int:pk>/edit/', views.entry_update, name='entry_update'),
             path('entry/<int:pk>/delete/', views.entry_delete, name='entry_delete'),
              path('login/', views.login_view, name='login'),
               path('logout/', views.logout_view, name='logout'),
                path('signup/', views.signup_view, name='signup'), ]