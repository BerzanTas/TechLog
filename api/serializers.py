from rest_framework import serializers
from solutions.models import Solution, Comment

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field='username', read_only=True)
    solution_author = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'content', 'author', 'created_date', 'solution_author']
        read_only_fields = ['author', 'created_date']

    def get_solution_author(self, obj):
        return obj.solution.author.username # Add solutions author


class SolutionSerializer(serializers.ModelSerializer):
    snippet = serializers.SerializerMethodField()
    author = serializers.SlugRelatedField(slug_field='username', read_only=True)
    comments = CommentSerializer(many=True, read_only=True, source='comments.all')

    class Meta:
        model = Solution
        fields = ['id', 'title', 'slug', 'content', 'content_html', 'published_date', 'modified_date', 'thumb', 'author', 'snippet', 'comments', 'tags']
        read_only_fields = ['content_html', 'published_date', 'modified_date', 'slug']
        extra_kwargs = {
            'thumb': {'required': False},
        }

    def get_snippet(self, obj):
        return obj.snippet()