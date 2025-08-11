# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated
# from rest_framework import status
# from rest_framework_simplejwt.tokens import RefreshToken
# from .serializers import RegisterSerializer, LoginSerializer, UserProfileSerializer
# from .models import CustomUser

# class RegisterView(APIView):
#     def post(self, request):
#         serializer = RegisterSerializer(data=request.data)
#         if serializer.is_valid():
#             user = serializer.save()
#             return Response({"message": "User registered successfully"}, status=201)
#         return Response(serializer.errors, status=400)

# class LoginView(APIView):
#     def post(self, request):
#         serializer = LoginSerializer(data=request.data)
#         if serializer.is_valid():
#             user = serializer.validated_data['user']
#             refresh = RefreshToken.for_user(user)
#             return Response({
#                 'refresh': str(refresh),
#                 'access': str(refresh.access_token),
#                 'role': user.role,
#                 'username': user.username
#             })
#         return Response(serializer.errors, status=401)

# class LogoutView(APIView):
#     permission_classes = [IsAuthenticated]
#     def post(self, request):
#         try:
#             refresh_token = request.data["refresh"]
#             token = RefreshToken(refresh_token)
#             token.blacklist()
#             return Response({"message": "Logout successful"}, status=205)
#         except Exception as e:
#             return Response({"error": str(e)}, status=400)

# class ProfileView(APIView):
#     permission_classes = [IsAuthenticated]
    
#     def get(self, request):
#         serializer = UserProfileSerializer(request.user)
#         return Response(serializer.data)

#     def put(self, request):
#         serializer = UserProfileSerializer(request.user, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({"message": "Profile updated", "data": serializer.data})
#         return Response(serializer.errors, status=400)





from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken,AccessToken
from .serializers import RegisterSerializer, LoginSerializer, UserProfileSerializer
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import CustomUser

# Route: POST /api/register/
# Auth Required: No
class RegisterView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):  # Accepts only POST
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "User registered successfully"}, status=201)
        return Response(serializer.errors, status=400)


# Route: POST /api/login/
# Auth Required:  No

from rest_framework_simplejwt.tokens import RefreshToken

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    refresh["role"] = user.role  # 👈 Add role to token
    refresh["email"] = user.email
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class LoginView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            tokens = get_tokens_for_user(user)
            return Response({
                **tokens,
                'role': user.role,
                'username': user.username
            })
        return Response(serializer.errors, status=401)


# class LoginView(APIView):
#     permission_classes = [AllowAny]
#     def post(self, request):  # Accepts only POST
#         serializer = LoginSerializer(data=request.data)
#         if serializer.is_valid():
#             user = serializer.validated_data['user']
#             refresh = RefreshToken.for_user(user)
#             return Response({
#                 'refresh': str(refresh),
#                 'access': str(refresh.access_token),
#                 'role': user.role,
#                 'username': user.username
#             })
#         return Response(serializer.errors, status=401)
# class LoginView(APIView):
#     def post(self, request):
#         serializer = LoginSerializer(data=request.data)
#         if serializer.is_valid():
#             user = serializer.validated_data['user']
#             access_token = AccessToken.for_user(user)
#             return Response({
#                 'access': str(access_token),
#                 'role': user.role,
#                 'username': user.username
#             })
#         return Response(serializer.errors, status=401)


# Route: POST /api/logout/
# Auth Required: Yes
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]  # JWT token required

    def post(self, request):  # Accepts only POST
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()  # Blacklist the token..blacklist the token means it will prevents  new access token to be issued   
            return Response({"message": "Logout successful"}, status=205)
        except Exception as e:
            return Response({"error": str(e)}, status=400)


# Route: GET /api/profile/   (to view profile)
#        PUT /api/profile/   (to update profile)
# Auth Required: Yes
class ProfileView(APIView):#this route supports both get req and put req when select get req pass jwt token to header then req willbe granted and you can able to view your profile but on put req pass jwt token on header but also passed updated body on json body so that ,profile data will be updated
    permission_classes = [IsAuthenticated]  # JWT token required

    def get(self, request):  # Accepts GET request
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)

    def put(self, request):  # Accepts PUT request (partial update)
        serializer = UserProfileSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Profile updated", "data": serializer.data})
        return Response(serializer.errors, status=400)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ResetPasswordSerializer

class ResetPasswordAPIView(APIView):
    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Password reset successful'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated, AllowAny
# from rest_framework import status
# from rest_framework_simplejwt.tokens import RefreshToken
# from .serializers import RegisterSerializer, LoginSerializer, UserProfileSerializer
# from .models import CustomUser
# from .models import EmailOTP  # new model for OTP
# from django.core.mail import send_mail
# import random
# import random
# import smtplib
# import ssl
# from django.http import JsonResponse
# from rest_framework.views import APIView
# from rest_framework.permissions import AllowAny
# from .models import EmailOTP

# class SendOTPView(APIView):
#     permission_classes = [AllowAny]

#     def post(self, request):
#         email = request.data.get('email')
#         if not email:
#             return JsonResponse({"error": "Email is required"}, status=400)

#         otp = str(random.randint(100000, 999999))

#         # Save OTP to DB
#         EmailOTP.objects.update_or_create(email=email, defaults={'otp': otp})

#         # Send OTP using smtplib with SSL context (unsafe: skips verification)
#         smtp_server = 'smtp.gmail.com'
#         smtp_port = 587
#         sender_email = 'kurkurerahul798@gmail.com'
#         app_password = 'ramlakhan345'  # Generate from Google account

#         context = ssl._create_unverified_context()

#         try:
#             server = smtplib.SMTP(smtp_server, smtp_port)
#             server.starttls(context=context)
#             server.login(sender_email, app_password)
#             subject = "Your OTP Code"
#             body = f"Your OTP is: {otp}"
#             message = f"Subject: {subject}\n\n{body}"

#             server.sendmail(sender_email, email, message)
#             server.quit()
#         except Exception as e:
#             return JsonResponse({"error": f"Failed to send email: {str(e)}"}, status=500)

#         return JsonResponse({"message": "OTP sent to email"})


# # Route: POST /api/verify-otp/
# class VerifyOTPView(APIView):
#     permission_classes = [AllowAny]

#     def post(self, request):
#         email = request.data.get('email')
#         otp = request.data.get('otp')

#         if not email or not otp:
#             return Response({"error": "Email and OTP are required"}, status=400)

#         try:
#             otp_entry = EmailOTP.objects.get(email=email)
#             if otp_entry.otp == otp:
#                 return Response({"message": "OTP verified. You can now register."})
#             else:
#                 return Response({"error": "Invalid OTP"}, status=400)
#         except EmailOTP.DoesNotExist:
#             return Response({"error": "OTP not found for this email"}, status=400)


# # Route: POST /api/register/
# class RegisterView(APIView):
#     permission_classes = [AllowAny]

#     def post(self, request):
#         email = request.data.get('email')

#         # Check if email is verified via OTP
#         try:
#             otp_obj = EmailOTP.objects.get(email=email)
#         except EmailOTP.DoesNotExist:
#             return Response({"error": "Email not verified via OTP."}, status=400)

#         serializer = RegisterSerializer(data=request.data)
#         if serializer.is_valid():
#             user = serializer.save()
#             otp_obj.delete()  # Clean up OTP after registration
#             return Response({"message": "User registered successfully"}, status=201)
#         return Response(serializer.errors, status=400)


# # Route: POST /api/login/
# class LoginView(APIView):
#     permission_classes = [AllowAny]

#     def post(self, request):
#         serializer = LoginSerializer(data=request.data)
#         if serializer.is_valid():
#             user = serializer.validated_data['user']
#             refresh = RefreshToken.for_user(user)
#             return Response({
#                 'access': str(refresh.access_token),
#                 'role': user.role,
#                 'username': user.username
#             })
#         return Response(serializer.errors, status=401)


# # Route: POST /api/logout/
# class LogoutView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         try:
#             refresh_token = request.data["refresh"]
#             token = RefreshToken(refresh_token)
#             token.blacklist()
#             return Response({"message": "Logout successful"}, status=205)
#         except Exception as e:
#             return Response({"error": str(e)}, status=400)


# # Route: GET /api/profile/   (view)
# #        PUT /api/profile/   (update)
# class ProfileView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         serializer = UserProfileSerializer(request.user)
#         return Response(serializer.data)

#     def put(self, request):
#         serializer = UserProfileSerializer(request.user, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({"message": "Profile updated", "data": serializer.data})
#         return Response(serializer.errors, status=400)

