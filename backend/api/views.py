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


# Create your views here.
def index(request):
    return HttpResponse("This is api for test web")


class RegisterView(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()

    def post(self, request):
        data = request.data
        name = data.get('name')
        surname = data.get('surname')
        email = data.get('email')
        password = data.get('password')

        register_service = Register()
        result = register_service.register_user(name, surname, email, password)

        if result['status'] == 'error':
            return Response(result, status=status.HTTP_400_BAD_REQUEST)

        return Response(result, status=status.HTTP_201_CREATED)
class LoginView(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()

    def post(self, request):
        data = request.data
        email = data.get('email')
        password = data.get('password')

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

        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith("Bearer "):
            return Response({'error': 'Authorization token not provided'}, status=status.HTTP_401_UNAUTHORIZED)

        token = auth_header.split(" ")[1]

        user_data = get_user_info_by_token(token)
        if not user_data:
            return Response({'error': 'Invalid token'}, status=status.HTTP_401_UNAUTHORIZED)

        user_id = user_data['user_id']
        user_type = user_data['user_type']

        tests_service = LatestTests()
        result = tests_service.get_latest_tests(user_id, user_type)

        return Response(result, status=status.HTTP_200_OK)


class TestsView(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()

    def get(self, request):
        data = [
            {
                "test_id": 1,
                "title": "Sčítání",
                "description": "Sčítání 1+1",
                "subject": "Math",
                "datetime": datetime.datetime.now(),
                "sequence": False,
                "max_time": None,
                "date_time_creation": str(datetime.datetime.now()),
                "author": "John Doe",
                "questions": [
                    {
                        "id": 1,
                        "title": "Sčítání",
                        "description": "Jednoduché sčítání",
                        "task": "Kolik je 1 + 1?",
                        "corrects": ["2"],
                        "show_correct": True
                    },
                    {
                        "id": 2,
                        "title": "Sčítání",
                        "description": "Pokročilé sčítání",
                        "task": "Kolik je 2 + 2?",
                        "corrects": ["4"],
                        "show_correct": True
                    }
                ]
            },
            {
                "test_id": 2,
                "title": "Základní Chemie",
                "description": "Identifikace základních prvků",
                "subject": "Chemistry",
                "datetime": datetime.datetime.now(),
                "sequence": True,
                "max_time": 60,
                "date_time_creation": str(datetime.datetime.now()),
                "author": "Jane Smith",
                "questions": [
                    {
                        "id": 1,
                        "title": "Chemie",
                        "description": "Základní chemické prvky",
                        "task": "Jaký je symbol pro vodík?",
                        "corrects": ["H"],
                        "show_correct": True
                    },
                    {
                        "id": 2,
                        "title": "Chemie",
                        "description": "Základní chemické prvky",
                        "task": "Jaký je symbol pro kyslík?",
                        "corrects": ["O"],
                        "show_correct": True
                    }
                ]
            }
        ]
        return Response(data, status=status.HTTP_200_OK)


class TestView(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()

    def get(self, request, test_id):
        data = {
            "test_id": test_id,
            "test": {
                "test_id": 1,
                "title": "Sčítání",
                "description": "Sčítání 1+1",
                "subject": "Math",
                "datetime": str(datetime.datetime.now()),
                "sequence": False,
                "max_time": None,
                "date_time_creation": str(datetime.datetime.now()),
                "author": "John Doe",
                "questions": [
                    {
                        "id": 1,
                        "title": "Sčítání",
                        "description": "Jednoduché sčítání",
                        "task": "Kolik je 1 + 1?",
                        "corrects": ["2"],
                        "show_correct": True
                    },
                    {
                        "id": 2,
                        "title": "Sčítání",
                        "description": "Pokročilé sčítání",
                        "task": "Kolik je 2 + 2?",
                        "corrects": ["4"],
                        "show_correct": True
                    }
                ]
            },
            "date_time_filled": str(datetime.datetime.now()),
            "questions": [
                {
                    "id": 1,
                    "date_time_filled": str(datetime.datetime.now()),
                    "question": {
                        "id": 1,
                        "title": "Sčítání",
                        "description": "Jednoduché sčítání",
                        "task": "Kolik je 1 + 1?",
                        "corrects": ["2"],
                        "show_correct": True
                    },
                    "solution": "2",
                    "is_correct": True
                },
                {
                    "id": 2,
                    "date_time_filled": str(datetime.datetime.now()),
                    "question": {
                        "id": 2,
                        "title": "Sčítání",
                        "description": "Pokročilé sčítání",
                        "task": "Kolik je 2 + 2?",
                        "corrects": ["4"],
                        "show_correct": True
                    },
                    "solution": "4",
                    "is_correct": True
                }
            ]
        }
        return Response(data, status=status.HTTP_200_OK)


class NewTests(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()

    def get(self, request):
        data = [
            {
                "test_id": 3,
                "title": "Marketing Basics",
                "description": "Introduction to Marketing",
                "subject": "Business",
                "datetime": str(datetime.datetime.now()),
                "sequence": False,
                "max_time": 60,
                "date_time_creation": str(datetime.datetime.now()),
                "author": "John Doe",
                "questions": [
                    {
                        "id": 1,
                        "title": "Marketing",
                        "description": "Základy marketingu",
                        "task": "Co je marketing?",
                        "corrects": ["Propagace"],
                        "show_correct": True
                    },
                    {
                        "id": 2,
                        "title": "Marketing",
                        "description": "Základy marketingu",
                        "task": "Co je 4P marketingu?",
                        "corrects": ["Cena", "Produkt", "Distribuce", "Propagace"],
                        "show_correct": True
                    }
                ]
            },
            {
                "test_id": 4,
                "title": "Basic French",
                "description": "Simple French phrases and grammar",
                "subject": "Languages",
                "datetime": str(datetime.datetime.now()),
                "sequence": True,
                "max_time": 90,
                "date_time_creation": str(datetime.datetime.now()),
                "author": "Jane Smith",
                "questions": [
                    {
                        "id": 1,
                        "title": "Francouzština",
                        "description": "Základy francouzštiny",
                        "task": "Jak se řekne 'Ahoj' francouzsky?",
                        "corrects": ["Bonjour"],
                        "show_correct": True
                    },
                    {
                        "id": 2,
                        "title": "Francouzština",
                        "description": "Základy francouzštiny",
                        "task": "Jaké je francouzské slovo pro 'jablko'?",
                        "corrects": ["Pomme"],
                        "show_correct": True
                    }
                ]
            }
        ]
        return Response(data, status=status.HTTP_200_OK)

class UserView(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()

    def put(self, request):
        # This endpoint returns a status change message
        print(request)
        return Response({"status": "changes made successfully"}, status=status.HTTP_200_OK)