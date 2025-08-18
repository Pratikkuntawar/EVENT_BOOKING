
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated
# from rest_framework import status
# from rest_framework_simplejwt.tokens import RefreshToken,AccessToken
# from .serializers import RegisterSerializer, LoginSerializer, UserProfileSerializer
# from rest_framework.permissions import AllowAny
# from .serializers import ResetPasswordSerializer
# from rest_framework_simplejwt.tokens import RefreshToken
# from rest_framework_simplejwt.views import TokenObtainPairView
# from .models import CustomUser

# # Route: POST /api/register/
# class RegisterView(APIView):
#     permission_classes = [AllowAny]#this route can be accesed by everyone
#     def post(self, request):  # Accepts only POST
#         serializer = RegisterSerializer(data=request.data)#this is where json data is passed into registerseialiser in serializers.py
#         if serializer.is_valid():
#             user = serializer.save()#here create method is called defined in Registerserialize(serializers.py)
#             return Response({"message": "User registered successfully"}, status=201)
#         return Response(serializer.errors, status=400)


# # Route: POST /api/login/

# def get_tokens_for_user(user):
#     refresh = RefreshToken.for_user(user)
#     refresh["role"] = user.role 
#     refresh["email"] = user.email
#     return {
#         'refresh': str(refresh),
#         'access': str(refresh.access_token),
#     }

# class LoginView(APIView):
#     permission_classes = [AllowAny]
#     def post(self, request):
#         serializer = LoginSerializer(data=request.data)
#         if serializer.is_valid():
#             user = serializer.validated_data['user']
#             tokens = get_tokens_for_user(user)
#             return Response({
#                 **tokens,# ** token expands into refresh token and access token
#                 'role': user.role,
#                 'username': user.username
#             })
#         return Response(serializer.errors, status=401)


# # Route: POST /api/logout/
# # Auth Required: Yes
# class LogoutView(APIView):
#     permission_classes = [IsAuthenticated]  # JWT token required

#     def post(self, request):  # Accepts only POST
#         try:
#             refresh_token = request.data["refresh"]
#             token = RefreshToken(refresh_token)
#             token.blacklist()  # Blacklist the token..blacklist the token means it will prevents  new access token to be issued   
#             return Response({"message": "Logout successful"}, status=205)
#         except Exception as e:
#             return Response({"error": str(e)}, status=400)


# # Route: GET /api/profile/   (to view profile)
# #        PUT /api/profile/   (to update profile)
# # Auth Required: Yes
# class ProfileView(APIView):#this route supports both get req and put req when select get req pass jwt token to header then req willbe granted and you can able to view your profile but on put req pass jwt token on header but also passed updated body on json body so that ,profile data will be updated
#     permission_classes = [IsAuthenticated]  # JWT token required

#     def get(self, request):  # Accepts GET request
#         serializer = UserProfileSerializer(request.user)
#         return Response(serializer.data)

#     def put(self, request):  # Accepts PUT request (partial update)
#         serializer = UserProfileSerializer(request.user, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({"message": "Profile updated", "data": serializer.data})
#         return Response(serializer.errors, status=400)


# class ResetPasswordAPIView(APIView):
#     def post(self, request):
#         serializer = ResetPasswordSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({'message': 'Password reset successful'}, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer, LoginSerializer, UserProfileSerializer, ResetPasswordSerializer
from .models import CustomUser


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    refresh["role"] = user.role
    refresh["email"] = user.email
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


class AuthView(APIView):
    """
    Single endpoint `/auth/`
    - POST    → Register (username, email, password, role) OR Login (email, password)
    - GET     → Get profile (auth required)
    - PUT     → Update profile (auth required)
    - DELETE  → Logout (auth required)
    - PATCH   → Reset password (auth required)
    """

    def get_permissions(self):
        if self.request.method == "POST":  
            return [AllowAny()]   # Register & Login don’t need auth
        return [IsAuthenticated()]  # profile, update, logout, reset-password need JWT

    def post(self, request):
        # Distinguish Register vs Login by keys
        if all(k in request.data for k in ["username", "email", "password", "role"]):
            # ---- REGISTER ----
            serializer = RegisterSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "User registered successfully"}, status=201)
            return Response(serializer.errors, status=400)

        elif all(k in request.data for k in ["email", "password"]):
            # ---- LOGIN ----
            serializer = LoginSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.validated_data["user"]
                tokens = get_tokens_for_user(user)
                return Response({
                    **tokens,
                    "role": user.role,
                    "username": user.username,
                })
            return Response(serializer.errors, status=401)

        return Response({"error": "Invalid payload"}, status=400)

    def get(self, request):
        # ---- PROFILE ----
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)

    def put(self, request):
        # ---- UPDATE PROFILE ----
        serializer = UserProfileSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Profile updated", "data": serializer.data})
        return Response(serializer.errors, status=400)

    def delete(self, request):
        # ---- LOGOUT ----
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Logout successful"}, status=205)
        except Exception as e:
            return Response({"error": str(e)}, status=400)

    def patch(self, request):
        # ---- RESET PASSWORD ----
        serializer = ResetPasswordSerializer(data=request.data, context={"user": request.user})
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Password reset successful"}, status=200)
        return Response(serializer.errors, status=400)
