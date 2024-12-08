from django.forms import ValidationError
from django.contrib.auth.models import User
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from solutions.models import Solution, Comment
from .serializers import SolutionSerializer, CommentSerializer

class SolutionListCreate(generics.ListCreateAPIView):
    queryset = Solution.objects.all().order_by('-published_date')
    serializer_class = SolutionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.request.method == 'POST':
            # POST requires login
            return [permissions.IsAuthenticated()]
        # GET allows everyone
        return [permissions.AllowAny()]

    def perform_create(self, serializer):
        # Add the user as an author of solution
        solution = serializer.save(author=self.request.user)
        self.created_solution = solution
    
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        # Dodanie do odpowiedzi URL szczegółów rozwiązania
        detail_url = f"/{self.created_solution.author.username}/{self.created_solution.slug}/"
        return Response({'detail_url': detail_url}, status=status.HTTP_201_CREATED)
    
class UserSolutionsList(generics.ListAPIView):
    serializer_class = SolutionSerializer
    permission_classes = [permissions.AllowAny]  # Dopuszczamy dostęp do rozwiązań innych użytkowników

    def get_queryset(self):
        # Pobranie identyfikatora użytkownika z URL
        user_slug = self.kwargs['username']
        
        # Pobranie użytkownika na podstawie sluga lub username
        try:
            user = User.objects.get(username=user_slug)
        except User.DoesNotExist:
            raise NotFound("User not found")
        
        # Filtracja rozwiązań po użytkowniku
        return Solution.objects.filter(author=user)



class SolutionRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Solution.objects.all()
    serializer_class = SolutionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class CommentListCreate(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        solution_id = self.request.query_params.get('solution', None)
        if solution_id:
            return self.queryset.filter(solution_id=solution_id)
        else:
            return self.queryset.none()

    def perform_create(self, serializer):
        solution_id = self.request.data.get('solution')
        
        if not solution_id:
            raise ValidationError({'solution': 'This field is required.'})

        try:
            solution = Solution.objects.get(pk=solution_id)
        except Solution.DoesNotExist:
            raise ValidationError({'solution': 'Solution does not exist.'})

        serializer.save(author=self.request.user, solution=solution)


class CommentDestroy(generics.DestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        obj = super().get_object()
        
        # Check if user is the owner of comment or solution
        if obj.author != self.request.user and obj.solution.author != self.request.user:
            raise permissions.PermissionDenied("You do not have permission to delete this comment.")
        
        return obj