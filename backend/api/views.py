#//ideálně transaction script nebo table module
from datetime import datetime
from django.http import HttpResponse
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from data.ProfileData import get_user_info_by_token
from domain.CheckAuthenticated import CheckAuthenticated
from domain.LatestTests import LatestTests
from domain.Login import Login
from domain.Register import Register
from domain.Tests import TestsService


# Create your views here.
def index(request):
    return HttpResponse("This is api for test web")


class RegisterView(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()

    def post(self, request):
        name = request.data.get('name')
        surname = request.data.get('surname')
        email = request.data.get('email')
        password = request.data.get('password')

        register_service = Register()
        result = register_service.register_user(name, surname, email, password)

        if result['status'] == 'error':
            return Response(result, status=status.HTTP_400_BAD_REQUEST)

        return Response(result, status=status.HTTP_201_CREATED)
class LoginView(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        login_service = Login()
        result = login_service.login_user(email, password)

        return Response(result, status=status.HTTP_200_OK)

class IsAuthenticatedView(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()

    def get(self, request):
        # Get the token from the Authorization header
        auth_header = request.headers.get('Authorization')
        token = auth_header.split(" ")[1] if auth_header else None

        if not token:
            return Response({'error': 'Authorization token not provided'}, status=status.HTTP_401_UNAUTHORIZED)

        is_authenticated_service = CheckAuthenticated()
        result = is_authenticated_service.is_authenticated(token)

        if not result['user_id']:
            return Response({'error': 'Invalid or expired token'}, status=status.HTTP_401_UNAUTHORIZED)

        return Response(result, status=status.HTTP_200_OK)


class LatestTestsView(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()

    def get(self, request):
        tests_service = LatestTests(request.headers.get('Authorization'))
        if tests_service.error:
            return Response(tests_service.error, status=status.HTTP_401_UNAUTHORIZED)
        result = tests_service.get_latest_tests()
        return Response(result, status=status.HTTP_200_OK)


class TestsView(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()

    def get(self, request):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith("Bearer "):
            return Response("Authorization token not provided", status=status.HTTP_401_UNAUTHORIZED)

        tests_service = TestsService(auth_header)
        if tests_service.error:
            return Response(tests_service.error, status=status.HTTP_401_UNAUTHORIZED)

        result = tests_service.get_tests()
        return Response(result, status=status.HTTP_200_OK)


class TestView(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()

    def get(self, request, test_id):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith("Bearer "):
            return Response("Authorization token not provided", status=status.HTTP_401_UNAUTHORIZED)

        test_service = TestDetailService(auth_header)
        if test_service.error:
            return Response(test_service.error, status=status.HTTP_401_UNAUTHORIZED)

        if test_service.user_type == "P":
            result = get_filled_test_detail_for_student(test_service.user_id, test_id)
        elif test_service.user_type == "T":
            result = get_test_detail_for_teacher(test_service.user_id, test_id)
        else:
            result = {}

        return Response(result, status=status.HTTP_200_OK)

class NewTest(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()

    def post(self, request):
        auth_header = request.headers.get('Authorization')
        create_test_service = CreateTestService(auth_header)

        if create_test_service.error:
            return Response(create_test_service.error, status=status.HTTP_401_UNAUTHORIZED)

        if not create_test_service.is_teacher():
            return Response("Permission denied: Only teachers can access this endpoint.",
                            status=status.HTTP_403_FORBIDDEN)

        title = request.data.get('title')
        description = request.data.get('description')
        subject = request.data.get('subject')
        sequence = request.data.get('sequence')
        max_time = request.data.get('max_time')

        result = create_test_service.save(title, description, subject, sequence, max_time)
        return Response(result, status=status.HTTP_201_CREATED)