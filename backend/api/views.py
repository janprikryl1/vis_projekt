#//ideálně transaction script nebo table module
import json

from django.http import HttpResponse
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from data.DetailTest import TestDetailService
from data.TestData import get_filled_test_detail_for_student, get_test_detail_for_teacher
from domain.CheckAuthenticated import CheckAuthenticated
from domain.LatestTests import LatestTests
from domain.Login import Login
from domain.Register import Register
from domain.Tables import Tables
from domain.Tests import TestsService
from domain.TestService import TestService

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

        return Response(test_service.get_test_detail(test_id), status=status.HTTP_200_OK)

class NewTest(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()

    def post(self, request):
        auth_header = request.headers.get('Authorization')
        test_service = TestService(auth_header)

        if test_service.error:
            return Response(test_service.error, status=status.HTTP_401_UNAUTHORIZED)

        if not test_service.is_teacher():
            return Response("Permission denied: Only teachers can access this endpoint.",
                            status=status.HTTP_403_FORBIDDEN)
        test_id = request.data.get('test_id')
        title = request.data.get('test_title')
        description = request.data.get('description')
        subject = request.data.get('subject')
        sequence = request.data.get('sequence')
        max_time = request.data.get('max_time')
        questions_json = request.data.get('questions')
        questions = json.loads(questions_json)

        if not test_id: #New test
            test_id = test_service.save_new_test(title, description, subject, sequence, max_time, questions)
        else: #Update test
            test_service.update_test(test_id, title, description, subject, sequence, max_time, questions)
        return Response({'test_id': test_id}, status=status.HTTP_201_CREATED)


class EvaluateTest(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()

    def post(self, request):
        auth_header = request.headers.get('Authorization')
        test_service = TestService(auth_header)

        filled_test_id = request.data.get('filled_test_id')
        question_id = request.data.get('question_id')
        solution = request.data.get('solution')

        is_correct = test_service.evaluate_test(question_id, solution)
        existing_filled_question_id = test_service.filled_question_exists(filled_test_id, question_id)
        if existing_filled_question_id:
            test_service.update_filled_question_result(existing_filled_question_id, solution, is_correct)
            filled_question_id = existing_filled_question_id
        else:
            filled_question_id = test_service.save_filled_question_result(filled_test_id, question_id, solution, is_correct)

        return Response({
            'filled_question_id': filled_question_id,
            'is_correct': is_correct
        }, status=status.HTTP_200_OK)


class TablesView(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()

    def get(self, request):
        tables = Tables().get_tables()
        return Response({'tables': tables}, status=status.HTTP_200_OK)

class GetAllData(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()

    def get(self, request, table_name):
        tests_service = TestsService(request.headers.get('Authorization'))
        if tests_service.error:
            return Response(tests_service.error, status=status.HTTP_401_UNAUTHORIZED)
        tables = Tables().get_table_data(table_name)
        return Response(tables, status=status.HTTP_200_OK)