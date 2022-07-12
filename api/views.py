from rest_framework import viewsets, permissions, status
from django.contrib.auth import get_user_model
from . import serializers
from rest_framework.response import Response
from .permissions import IsCreatorOrAdminReadOnly


UserModel = get_user_model()

# Create your views here.


class UserViewSet(viewsets.ModelViewSet):
    queryset = UserModel.objects.all()
    default_serializer_class = serializers.UserOutputSerializer

    serializers_classes = {"create": serializers.UserInputSerializer}

    def create(self, request, *args, **kwargs):
        """
        user SignUp
            - Allow anyone to signup with out authentication
        """
        self.check_permissions(request)
        serializer = serializers.UserInputSerializers(data=request.POST)
        serializer.is_valid(raise_exception=True)

        user = UserModel.objects.create_user(
            email=serializer.validated_data["email"],
            first_name=serializer.validated_data["first_name"],
            last_name=serializer.validated_data["last_name"],
            password=serializer.validated_data["password"],
        )
        response = serializers.UserOutputSerializer(user).data
        return Response(response, status=status.HTTP_201_CREATED)

    def get_permissions(self):
        if self.action == "create":  # create, update, retrieve and destroy
            permission_classes = [permissions.AllowAny]
        elif self.action == "retrieve":
            permission_classes = [permissions.IsAuthenticated]
        elif self.action in ["update", "partial_update", "destroy"]:
            permission_classes = [IsCreatorOrAdminReadOnly, permissions.IsAuthenticated]
        elif self.action == "list":
            permission_classes = [permissions.IsAdminUser]
        else:
            permission_classes = [permissions.IsAdminUser]

        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        return self.serializers_classes.get(self.action, self.default_serializer_class)
