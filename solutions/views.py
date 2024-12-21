import json
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from .models import Solution
from django.contrib.auth.decorators import login_required
from collections import Counter

def solution_list(request):
    solutions = Solution.objects.all().order_by('published_date')
    return render(request, 'solutions/solution_list.html', {'solutions':solutions})

def user_solutions(request, username):
    solutions = Solution.objects.all().order_by('published_date')
    return render(request, 'solutions/user_solution_list.html', {'solutions':solutions})

def solution_detail(request, username, slug):
    solution = get_object_or_404(Solution, author__username=username, slug=slug)
    solution.tags_list = [tag.strip() for tag in solution.tags.split(',')] if solution.tags else []

    solution.views_count += 1
    solution.save()

    # Use json.dumps to escape the content safely
    solution_content = json.dumps(solution.content)
    return render(request, 'solutions/solution_detail.html', {'solution':solution, 'solution_content':solution_content})

@login_required(login_url='/login')
def solution_create(request):
    return render(request, 'solutions/solution_create.html')

def tag_list(request):
    # Retrieve all tags from the database as a list of strings
    all_tags = Solution.objects.values_list('tags', flat=True)
    
    # Split tags into individual items
    tag_list = []
    for tags in all_tags:
        if tags:  # Skip empty tags
            tag_list.extend(tags.split(','))  # Split tags by commas and add to the list
    
    # Count occurrences of each tag using Counter
    tag_counter = Counter(tag_list)
    
    # Sort tags by usage count in descending order
    sorted_tags = tag_counter.most_common()
    
    # Pass the sorted tag list to the template
    return render(request, 'solutions/tags.html', {'tags': sorted_tags})