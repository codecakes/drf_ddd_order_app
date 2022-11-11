from rest_framework import viewsets, exceptions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status as http_status

from order_app.infrastructure import bootstrap
from order_app.services.user_service import UserService, UserMgmtAppService
from order_app.utility.jwt import JWT_TOKEN

from order_app.infrastructure.user_mgmt.models import UserModel


class UserRegisterView(APIView):
    http_method_names = [
        "post",
    ]

    def post(self, request, format=None):
        # TODO: Implement this method
        data = request.data
        try:
            token: JWT_TOKEN = UserMgmtAppService.register_user(
                bootstrap.start_bootstrap.uow,
                username=data["username"],
                password=data["password"],
            )
            return Response(
                {"jwt": token.decode("utf-8")}, status=http_status.HTTP_201_CREATED
            )
        except UserModel.DoesNotExist as e:
            raise exceptions.AuthenticationFailed(detail=e) from e
        except ValueError as e:
            raise exceptions.PermissionDenied(detail=e) from e


class UserLoginViewSet(viewsets.ViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    http_method_names = [
        "post",
    ]

    def create(self, request, *args, **kwargs):
        """
        Return a logged in user token.
        """

        data = request.data
        try:
            token: JWT_TOKEN = UserMgmtAppService.start_session(
                bootstrap.start_bootstrap.uow,
                username=data["username"],
                password=data["password"],
            )
            return Response({"jwt": token.decode("utf-8")})
        except (ValueError, UserModel.DoesNotExist) as e:
            raise exceptions.AuthenticationFailed(detail=e) from e
