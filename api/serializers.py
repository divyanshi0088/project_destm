# Serializer for User Registration (Creating a User)
from rest_framework import serializers

from .models import Teacher, Student,User

class UserSerializer(serializers.ModelSerializer):
    password_confirmation = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'password_confirmation',"role"]
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        """Ensure passwords match before saving."""
        password = data.get("password")
        password_confirmation = data.pop("password_confirmation", None)

        if password != password_confirmation:
            raise serializers.ValidationError({"password_confirmation": "Passwords do not match."})

        return data

    def create(self, validated_data):
        """Create user without password_confirmation field."""
        return User.objects.create_user(**validated_data)

# Serializer for User Login (Authentication)
class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        user = User.objects.filter(email=email).first()
        if user and user.check_password(password):
            return {'user': user}
        raise serializers.ValidationError("Invalid email or password")

# Serializer for Teacher Model
class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ['user', 'id']

# Serializer for Student Model
class StudentSerializer(serializers.ModelSerializer):
    teacher = TeacherSerializer(read_only=True)

    class Meta:
        model = Student
        fields = ['user', 'teacher', 'id']