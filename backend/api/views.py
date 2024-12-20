import json
from django.http import HttpResponse
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from domain.DetailTestService import TestDetailService
from domain.CheckAuthenticated import CheckAuthenticated
from domain.FilledQuestionStatisticsService import FilledQuestionStatisticsService
from domain.LatestTestsService import LatestTests
from domain.LoginService import LoginDTO, LoginService
from domain.RegisterService import Register
from domain.TablesService import Tables
from domain.TestStatisticsService import TestStatisticsService
from domain.TestsService import TestsService
from domain.TestService import TestService


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

        login_service = LoginService()
        result = login_service.login_user(email, password)
        print(result)
        if not result:
            return Response({'error': 'Invalid email or password'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(result, status=status.HTTP_200_OK)


class IsAuthenticatedView(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()

    def get(self, request):
        is_authenticated_service = CheckAuthenticated(request.headers.get('Authorization'))
        if is_authenticated_service.error:
            return Response({"error": is_authenticated_service.error}, status=status.HTTP_401_UNAUTHORIZED)

        result = is_authenticated_service.is_authenticated()
        if not result['user_id']:
            return Response({'error': 'Invalid or expired token'}, status=status.HTTP_401_UNAUTHORIZED)

        return Response(result, status=status.HTTP_200_OK)


class LatestTestsView(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()

    def get(self, request):
        tests_service = LatestTests(request.headers.get('Authorization'))
        if tests_service.error:
            return Response({"error": tests_service.error}, status=status.HTTP_401_UNAUTHORIZED)
        result = tests_service.get_latest_tests()
        return Response(result, status=status.HTTP_200_OK)


class TestsView(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()

    def get(self, request):
        tests_service = TestsService(request.headers.get('Authorization'))
        if tests_service.error:
            return Response({"error": tests_service.error}, status=status.HTTP_401_UNAUTHORIZED)

        result = tests_service.get_tests()
        return Response(result, status=status.HTTP_200_OK)


class TestView(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()

    def get(self, request, test_id):
        test_service = TestDetailService(request.headers.get('Authorization'))
        if test_service.error:
            return Response({"error": test_service.error}, status=status.HTTP_401_UNAUTHORIZED)

        return Response(test_service.get_test_detail(test_id), status=status.HTTP_200_OK)


class NewTest(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()

    def post(self, request):
        test_service = TestService(request.headers.get('Authorization'))

        if test_service.error:
            return Response({"error": test_service.error}, status=status.HTTP_401_UNAUTHORIZED)

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

        if not test_id:  # New test
            test_id = test_service.save_new_test(title, description, subject, sequence, max_time, questions)
        else:  # Update test
            test_service.update_test(test_id, title, description, subject, sequence, max_time, questions)
        return Response({'test_id': test_id}, status=status.HTTP_201_CREATED)


class TestStatistics(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()

    def get(self, request, test_id):
        auth_header = request.headers.get('Authorization')
        test_service = TestStatisticsService(auth_header)
        if test_service.error:
            return Response({"error": test_service.error}, status=status.HTTP_401_UNAUTHORIZED)

        return Response(test_service.get_test_statistics(test_id), status=status.HTTP_200_OK)


class QuestionStatistics(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()

    def get(self, request, question_id):
        question_service = FilledQuestionStatisticsService(request.headers.get('Authorization'))
        if question_service.error:
            return Response({"error": question_service.error}, status=status.HTTP_401_UNAUTHORIZED)

        return Response(question_service.get_question_statistics(question_id), status=status.HTTP_200_OK)


class EvaluateTest(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()

    def post(self, request):
        test_service = TestService(request.headers.get('Authorization'))

        if test_service.error:
            return Response({'error': test_service.error}, status=status.HTTP_401_UNAUTHORIZED)

        filled_test_id = request.data.get('filled_test_id')
        question_id = request.data.get('question_id')
        solution = request.data.get('solution')

        if not (filled_test_id and question_id and solution is not None):
            return Response(
                {'error': 'Missing required parameters: filled_test_id, question_id, solution'},
                status=status.HTTP_400_BAD_REQUEST
            )

        filled_question_id, is_correct = test_service.evaulate(question_id, solution, filled_test_id)
        return Response({
            'filled_question_id': filled_question_id,
            'is_correct': is_correct
        }, status=status.HTTP_200_OK)


class TablesView(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()

    def get(self, request):
        table = Tables(request.headers.get('Authorization'))
        tables = table.get_tables()
        return Response({'tables': tables}, status=status.HTTP_200_OK)


class GetAllData(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()

    def get(self, request, table_name):
        table = Tables(request.headers.get('Authorization'))
        if table.error:
            return Response({"error": table.error}, status=status.HTTP_401_UNAUTHORIZED)
        tables = table.get_table_data(table_name)
        return Response(tables, status=status.HTTP_200_OK)
