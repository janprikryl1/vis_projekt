import datetime

from django.http import HttpResponse
from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response


# Create your views here.
def index(request):
    return HttpResponse("This is api for test web")


"""class UserRegister(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = (SessionAuthentication,)

    def post(self, request):
        email = request.data['email'].strip()
        if not email or UserModel.objects.filter(email=email).exists():
            return Response({"error": "already_used"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.create(request.data)
            if user:
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class UserLogin(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = (SessionAuthentication,)

    ##
    def post(self, request):
        data = request.data
        assert validate_email(data)
        assert validate_password(data)
        serializer = UserLoginSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.check_user(data)
            login(request, user)
            return Response(serializer.data, status=status.HTTP_200_OK)


class UserLogout(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()

    def post(self, request):
        logout(request)
        return Response(status=status.HTTP_200_OK)


class UserView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (SessionAuthentication,)

    ##
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response({'user': serializer.data}, status=status.HTTP_200_OK)
"""


class TestsView(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()

    ##
    def get(self, request):
        data = [
            {"test_id": 1, "title": "Sčítání", "description": "Sčítání 1+1", "subject": "Math",
             "datetime": datetime.datetime.now(), "sequence": False, "max_time": None},
            {"test_id": 2, "title": "Základní Chemie", "description": "Identifikace základních prvků",
             "subject": "Chemistry", "datetime": datetime.datetime.now(), "sequence": True, "max_time": 60},
            {"test_id": 3, "title": "Čtení s porozuměním", "description": "Krátký text a otázky",
             "subject": "Language Arts", "datetime": datetime.datetime.now(), "sequence": False, "max_time": 45},
            {"test_id": 4, "title": "Geometrie", "description": "Výpočet obvodu a plochy", "subject": "Math",
             "datetime": datetime.datetime.now(), "sequence": True, "max_time": 30},
            {"test_id": 5, "title": "První světová válka", "description": "Historie událostí a důsledky",
             "subject": "History", "datetime": datetime.datetime.now(), "sequence": False, "max_time": 50},
            {"test_id": 6, "title": "Základy programování", "description": "Úvod do Pythonu",
             "subject": "Computer Science", "datetime": datetime.datetime.now(), "sequence": True, "max_time": 90},
            {"test_id": 7, "title": "Fyzika – pohyb", "description": "Výpočet rychlosti a zrychlení",
             "subject": "Physics", "datetime": datetime.datetime.now(), "sequence": True, "max_time": 40},
            {"test_id": 8, "title": "Biologie – buňka", "description": "Struktura a funkce buněk", "subject": "Biology",
             "datetime": datetime.datetime.now(), "sequence": False, "max_time": 70},
            {"test_id": 9, "title": "Základy podnikání", "description": "Co je to podnikání?", "subject": "Economics",
             "datetime": datetime.datetime.now(), "sequence": False, "max_time": None},
            {"test_id": 10, "title": "Umělecké směry", "description": "Přehled hlavních směrů v umění",
             "subject": "Art", "datetime": datetime.datetime.now(), "sequence": False, "max_time": 60},
            {"test_id": 11, "title": "Základy psychologie", "description": "Chování a osobnost",
             "subject": "Psychology", "datetime": datetime.datetime.now(), "sequence": False, "max_time": 80},
        ]
        return Response(data, status=status.HTTP_200_OK)


class TestView(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()

    def get(self, request, test_id):
        print(test_id)
        return Response({"test_id": 1, "title": "Sčítání", "description": "Sčítání 1+1", "subject": "Math",
                         "datetime": datetime.datetime.now(), "sequence": False, "max_time": None},
                        status=status.HTTP_200_OK)
