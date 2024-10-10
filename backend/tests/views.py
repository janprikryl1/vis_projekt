import datetime
from django.http import HttpResponse
from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication

# Create your views here.
def index(request):
    return HttpResponse("This is api for test web")


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