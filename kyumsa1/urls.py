from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns =[
    path('',views.home, name="home"),
    path('register',views.register, name="register"),
    path('login',views.login, name="login"),
    path('logout', views.logout, name="logout"),

    #Alumin urls
    path('alumin_register', views.alumin_register, name='alumin_register'),
    path('alumin_profile', views.alumin_profile, name='alumin_profile'),
    path("alumin_update/<str:pk>/", views.alumin_update, name="alumin_update"),


    path('student_register', views.student_register, name="student_register"),
    path('student_profile', views.student_profile, name='student_profile'),
    path("student_update/<str:pk>/", views.student_update, name="student_update"),

        path('reset_password/',
     auth_views.PasswordResetView.as_view(template_name="password/reset_password.html"),
      name="reset_password"),

    path('reset_password_sent/',
     auth_views.PasswordResetDoneView.as_view(template_name="password/reset_password_sent.html"),
     name="password_reset_done"),

    path('reset/<uidb64>/<token>/',
     auth_views.PasswordResetConfirmView.as_view(template_name="password/reset.html"),
      name="password_reset_confirm"),


    path('reset_password_complete/',
     auth_views.PasswordResetCompleteView.as_view(template_name="password/password_reset_complete.html"), 
     name="password_reset_complete"),

    


]