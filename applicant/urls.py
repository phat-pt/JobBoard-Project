from django.urls import path, include
from . import views
from .views import ResetPasswordVerificationView, VerificationView

urlpatterns = [
    #Account
    path('login', views.login, name = 'login'),
    path('register', views.register, name = 'register'),
    path('logout', views.logout, name = 'logout'),
    path('profile', views.profile, name='profile'),
    path('activate/<uidb64>/<token>', VerificationView.as_view(), name='activate'), 
    path('forgot_password', views.forgot_password, name = 'forgot_password'),
    path('resetpassword/<uidb64>/<token>', ResetPasswordVerificationView.as_view(), name='resetpassword'), 
    path('reset_password', views.reset_password, name= 'reset_password'),
    path('delete_CV', views.delete_CV, name = 'delete_CV'),
]