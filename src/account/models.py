from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.db import models, IntegrityError
import uuid
import uuid


class UserManager(BaseUserManager):
    def get_or_create_for_cognito(self, payload):
        print(payload,'paylooooooooooooooooooooooooooooooooooooooooooodd')
        # """Get any value from payload here
        #     ipdb> pprint(payload)
        #     {'aud': '159ufjrihgehb67sn373aotli7',
        #     'auth_time': 1583503962,
        #     'cognito:username': 'john-rambo',
        #     'email': 'foggygiga@gmail.com',
        #     'email_verified': True,
        #     'event_id': 'd92a99c2-c49e-4312-8a57-c0dccb84f1c3',
        #     'exp': 1583507562,
        #     'iat': 1583503962,
        #     'iss': 'https://cognito-idp.us-west-2.amazonaws.com/us-west-2_flCJaoDig',
        #     'sub': '2e4790a0-35a4-45d7-b10c-ced79be22e94',
        #     'token_use': 'id'}
        # """
        cognito_id = payload['sub']
        try:
            user = self.get(cognito_id=cognito_id)
            print(user,'userrrrrrrrrrrrrrr')
            return self.get(cognito_id=cognito_id)
        except self.model.DoesNotExist:
            pass
        try:
            user = self.create(
                cognito_id=cognito_id,
                email=payload['email'],
                is_active=True)
        except Exception as e:
            print(e)
            print('HHHHHHHHH')
            user = self.get(email=payload['email'])
            user.cognito_id = cognito_id
            user.save()

        return user

    def create_user(self, email, password=None, **extra_fields):
        print('inside create_user')
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    cognito_id = models.UUIDField(default=uuid.uuid4, editable=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
