
from django.core.validators import RegexValidator
from django.utils import timezone
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from post_app.models import User, Post, Comment


class EmailValidator:
    def __call__(self, value):
        allowed_domains = ('mail.ru', 'yandex.ru')
        domain = value.split('@')[-1]
        if domain not in allowed_domains:
            raise serializers.ValidationError("Разрешены домены: mail.ru, yandex.ru")


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(validators=[
        RegexValidator(r'(?=.*[0-9])(?=.*[a-z]){8,}', message="Пароль не менее 8 символов и должен содержать цифры")])
    # phone = serializers.IntegerField(validators=[PhoneValidator()])
    email = serializers.EmailField(validators=[EmailValidator()])
    phone = serializers.IntegerField(validators=[RegexValidator(r'^[7]\d{10}$',
                                                                message="Формат номера должен иметь вид "
                                                                        "79998887766, и состоять из 11 цифр.")])

    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        reader = super().create(validated_data)
        reader.set_password(reader.password)
        reader.save()
        return reader


class TitleValidator:
    def __call__(self, value):
        forbidden_words = ['ерунда', 'глупость', 'чепуха']
        for word in forbidden_words:
            if word in value:
                raise serializers.ValidationError('запрещенные слова: ерунда, глупость, чепуха')


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='username')

    class Meta:
        model = Comment
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.all())
    comment = serializers.SlugRelatedField(slug_field='text', queryset=Comment.objects.all(), many=True)
    title = serializers.CharField(validators=[TitleValidator()])

    class Meta:
        model = Post
        fields = '__all__'

    def validate_author(self, value):
        if not value.is_staff:
            if value.dob is None:
                raise serializers.ValidationError("Вы не указали дату рождения.")
            age = (timezone.now().date() - value.dob).days // 365
            if age < 18:
                raise serializers.ValidationError("Только лица достигшие 18 лет могу создавать посты.")
            return value
        return value
