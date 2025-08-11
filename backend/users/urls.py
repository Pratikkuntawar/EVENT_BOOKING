from django.urls import path
from .views import RegisterView, LoginView, LogoutView, ProfileView,ResetPasswordAPIView

urlpatterns = [
    # path('send-otp/', SendOTPView.as_view(), name='send_otp'),
    # path('verify-otp/', VerifyOTPView.as_view(), name='verify_otp'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', ProfileView.as_view(), name='get_profile'),
    path('profile/update/', ProfileView.as_view(), name='update_profile'),
     path('reset-password/', ResetPasswordAPIView.as_view(), name='reset-password'),
]
