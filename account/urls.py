from django.urls import path

from account.views import CreateAccountView,RetrieveUpdateDestroyAccountView, loginAccountView,SendPasswordResetEmailView,UserPasswordResetView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', CreateAccountView.as_view(), name="Create account"),
    path("my_account/<int:pk>/", RetrieveUpdateDestroyAccountView.as_view(), name=''),
    path('login/', loginAccountView.as_view(), name="login usr"),
    path('send-reset-password-mail/', SendPasswordResetEmailView.as_view(), name="reset_password_email"),
    path('reset-password/<uid>/<token>/', UserPasswordResetView.as_view(), name="reset-password"),

]