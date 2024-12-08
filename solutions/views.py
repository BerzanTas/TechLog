import json
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from .models import Solution
from django.contrib.auth.decorators import login_required

def solution_list(request):
    solutions = Solution.objects.all().order_by('published_date')
    return render(request, 'solutions/solution_list.html', {'solutions':solutions})

def user_solutions(request, username):
    solutions = Solution.objects.all().order_by('published_date')
    return render(request, 'solutions/user_solution_list.html', {'solutions':solutions})

def solution_detail(request, username, slug):
    solution = get_object_or_404(Solution, author__username=username, slug=slug)
    solution.tags_list = [tag.strip() for tag in solution.tags.split(',')] if solution.tags else []

    # Use json.dumps to escape the content safely
    solution_content = json.dumps(solution.content)
    return render(request, 'solutions/solution_detail.html', {'solution':solution, 'solution_content':solution_content})

@login_required(login_url='/login')
def solution_create(request):
    return render(request, 'solutions/solution_create.html')