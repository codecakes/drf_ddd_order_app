from order_app.domain.user.user import User
from order_app.infrastructure.user_mgmt.models import UserModel, Session
from order_app.repository.user_repository import AbstractUserRepository, UserOrNone
from order_app.utility.jwt import JWTPayload
from order_app.utility.singleton import Singleton


@Singleton
class UserRepo(AbstractUserRepository):
    """User repository.

    Any number of this can be created as a singleton
    on multiple machine instances. Each instance will be
    unique but it will not corrupt any
    underlying instantiated dependencies. Each is an
    individual and unbounded adapter.
    """

    def get_user(self, username: str, password: str) -> UserOrNone:
        queryset = UserModel.objects.filter(username=username)
        if not queryset.exists():
            return None

        user_obj = queryset.first()
        if user_obj.password != password:
            raise ValueError("Password does not match.")

        return User.store(
            username=user_obj.username,
            encrypted_password=user_obj.password,
        )

    def save_user(self, user: User) -> User:
        user_model = UserModel(username=user.username, password=user.encrypted_password)
        user_model.save()
        return user

    def store_user_session(self, username: str, session_token: bytes, jwk_header_dict: dict) -> None:
        user_obj = UserModel.objects.get(username=username)
        ttl = JWTPayload.decode_exp_tm_datetime(session_token, jwk_header_dict)
        # TODO: should store the jwk header for caching & rotating
        #  multi-device session mgmt.
        session = Session(token=session_token, ttl=ttl, user=user_obj)
        session.save()
