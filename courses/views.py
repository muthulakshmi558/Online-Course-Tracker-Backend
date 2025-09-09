from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Course, Instructor
from .serializers import CourseSerializer, InstructorSerializer

# Courses: ModelViewSet gives list/create/retrieve/update/destroy (CBV).
class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all().select_related('instructor').prefetch_related('lessons')
    serializer_class = CourseSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        instructor_id = self.request.query_params.get('instructor_id')
        if instructor_id:
            qs = qs.filter(instructor_id=instructor_id)
        return qs

@api_view(['GET', 'POST'])
def instructors_list_create(request):
    if request.method == 'GET':
        instructors = Instructor.objects.all()
        serializer = InstructorSerializer(instructors, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        # Detect if it's a single object or list
        many = isinstance(request.data, list)
        serializer = InstructorSerializer(data=request.data, many=many)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
