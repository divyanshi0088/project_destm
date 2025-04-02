from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User, Teacher, Student
from .serializers import UserSerializer, UserLoginSerializer, TeacherSerializer, StudentSerializer

# Helper function to generate access & refresh tokens
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
#function to register user
@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    serializer = UserSerializer(data=request.data)

    if serializer.is_valid():
        user = serializer.save()

        # Check if user is a teacher
        if user.role == 'teacher':
            teacher = Teacher.objects.create(user=user)
            return Response({'message': 'Teacher registered successfully', 'teacher_id': teacher.id}, 
                             status=status.HTTP_201_CREATED)

        # Check if user is a student
        elif user.role == 'student':
            teacher_id = request.data.get('teacher_id')

            if not teacher_id:
                return Response({'error': 'Teacher ID is required for students'}, status=status.HTTP_400_BAD_REQUEST)

            try:
                teacher = Teacher.objects.get(id=teacher_id)
                Student.objects.create(user=user, teacher=teacher)
                return Response({'message': 'Student registered successfully'}, status=status.HTTP_201_CREATED)
            except Teacher.DoesNotExist:
                return Response({'error': 'Teacher not found. Please register a teacher first.'}, status=status.HTTP_400_BAD_REQUEST)

        # If user is neither teacher nor student, return a success response
        return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)







#  LOGIN API (Returns Access & Refresh Token)
@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    serializer = UserLoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        tokens = get_tokens_for_user(user)  # Generate JWT Tokens
        return Response({'tokens': tokens, 'role': user.role}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#  DASHBOARD API (Fetch User Details)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_dashboard(request):
    user = request.user

    if user.role == 'teacher':
        teacher_profile = Teacher.objects.get(user=user)
        students = Student.objects.filter(teacher=teacher_profile)
        students_data = StudentSerializer(students, many=True).data
        return Response({
            'role': 'teacher',
            'email': user.email,
            'username': user.username,
            'students': students_data
        }, status=status.HTTP_200_OK)

    elif user.role == 'student':
        student_profile = Student.objects.get(user=user)
        teacher_data = TeacherSerializer(student_profile.teacher).data
        return Response({
            'role': 'student',
            'email': user.email,
            'username': user.username,
            'teacher': teacher_data
        }, status=status.HTTP_200_OK)

    return Response({'error': 'Invalid user role'}, status=status.HTTP_400_BAD_REQUEST)
