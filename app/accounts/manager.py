from django.contrib.auth.models import BaseUserManager, AbstractBaseUser





class UserManager(BaseUserManager):
    def create_user(self, email, username, phone, password=None):
        if not email:
            raise ValueError("Users must have an email address")

        if not username:
            raise ValueError("Users must have a username")

        if not phone:
            raise ValueError("Users must have a phone number")


        user = self.model(
            email=self.normalize_email(email),
            username=username,
            phone=phone,
)

        user.set_password(password)
        user.is_active = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, phone, password=None):

        user = self.create_user(
            email=self.normalize_email(email),
            phone=phone,
            password=password,
            username=username,
        )
        user.is_admin = True
        user.is_superuser = True
        user.is_active = True
        user.save(using=self._db)
        return user