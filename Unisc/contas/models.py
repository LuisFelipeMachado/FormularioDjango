from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, email, nome, password=None):
        if not email:
            raise ValueError("Usuário precisa de um email.")
        if not nome:
            raise ValueError("Usuário precisa de um nome.")

        email = self.normalize_email(email)
        user = self.model(email=email, nome=nome)
        user.set_password(password)
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser):
    nome = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    
    genero = models.CharField(
        max_length=1,
        choices=[('M', 'Masculino'), ('F', 'Feminino'), ('O', 'Outro')],
        null=True,
        blank=True
    )
    idade = models.PositiveIntegerField(null=True, blank=True)

    is_active = models.BooleanField(default=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nome']

    def __str__(self):
        return self.email


class SRQ20Resposta(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    respostas = models.JSONField()  # Ex: [1, 0, 1, ..., 0]
    data_resposta = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"SRQ-20 de {self.user.email} em {self.data_resposta.strftime('%d/%m/%Y %H:%M')}"
