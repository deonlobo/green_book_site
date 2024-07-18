from DIYProject.forms import NewProject, SearchProject
from DIYProject.models import Project, ProjectCategory
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from marketplace.models import Category
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.contrib import messages


@login_required(login_url='login')
def newProjectView(request):
    if request.method == 'POST':
        form = NewProject(request.POST, request.FILES)
        if form.is_valid():
            temp_project = form.save(commit=False)
            temp_project.posted_by = request.user
            temp_project.save()
            return redirect('DIYProject:myprojects')
        else:
            for field in form:
                print("Field Error:", field.name, field.errors)
            return HttpResponse('Uploaded details are not valid')
    else:
        form = NewProject()
    return render(request,'DIYProject/new_project.html',{'form':form})

@login_required(login_url='login')
def editProjectView(request,project_id):
    temp_project = get_object_or_404(Project, pk=project_id)
    if request.method == 'POST':
        form = NewProject(request.POST, request.FILES, instance=temp_project)
        if form.is_valid():
            form.save()
            return redirect('DIYProject:myprojects')
        else:
            for field in form:
                print("Field Error:", field.name, field.errors)
                return HttpResponse('Uploaded details are not valid')
    else:
        form = NewProject(instance=temp_project)
    return render(request,'DIYProject/edit_project.html',{'form':form,'temp_project':temp_project})

def categoriesView(request):
    categories = ProjectCategory.objects.all()
    return render(request,'DIYProject/categories.html',{'categories':categories})

def feedView(request):
    SearchForm = SearchProject()
    projects = Project.objects.order_by('-posted_on')
    return render(request,'DIYProject/feed.html',{'projects':projects,'SearchForm':SearchForm})

def filterCategoryView(request, category_id):
    SearchForm = SearchProject()
    category_name=ProjectCategory.objects.get(pk=category_id)
    projects = Project.objects.filter(project_category=category_name).order_by('-posted_on')
    return render(request, 'DIYProject/feed.html', {'projects': projects,'SearchForm':SearchForm})

@login_required(login_url='login')
def myProjectView(request):
    projects = Project.objects.filter(posted_by=request.user).order_by('-posted_on')
    return render(request,'DIYProject/my_projects.html',{'projects': projects})

def projectView(request,id):
    project = get_object_or_404(Project, pk=id)
    return render(request,'DIYProject/view_project.html',{'project': project})

@login_required(login_url='login')
def deleteProjectView(request,project_id):
    temp_project = get_object_or_404(Project, pk=project_id)
    temp_project.delete()
    return redirect('DIYProject:myprojects')

def SearchProjectView(request):
    if request.method == 'GET':
        form = SearchProject(request.GET)
        if form.is_valid():
            query = form.cleaned_data['term']
            projects = Project.objects.filter(Q(title__icontains=query) | Q(tools__icontains=query) | Q(project_category__name__icontains=query)).order_by('-posted_on')
            if len(projects) == 0:
                messages.error(request,'No matching projects found')
                return redirect('DIYProject:feed')
            messages.success(request, 'Search completed successfully!')
            return render(request, "DIYProject/feed.html", {'projects': projects, 'SearchForm': form})
        else:
            messages.error(request, 'Invalid search term')
            return redirect('DIYProject:feed')

