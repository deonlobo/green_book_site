from DIYProject.forms import NewProject
from DIYProject.models import Project, ProjectCategory
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from marketplace.models import Category


@login_required(login_url='login')
def newProjectView(request):
    if request.method == 'POST':
        form = NewProject(request.POST, request.FILES)
        if form.is_valid():
            temp_project = form.save(commit=False)
            temp_project.posted_by = request.user
            temp_project.save()
            return redirect('home')
        else:
            for field in form:
                print("Field Error:", field.name, field.errors)
            return HttpResponse('Uploaded details are not valid')
    else:
        form = NewProject()
    return render(request,'DIYProject/new_project.html',{'form':form})

@login_required(login_url='login')
def editProjectView(request,project_id):
    temp_project = Project.objects.get(pk=project_id)
    if request.method == 'POST':
        form = NewProject(request.POST, request.FILES, instance=temp_project)
        if form.is_valid():
            form.save()
            return redirect('home')
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
    projects = Project.objects.order_by('-posted_on')
    return render(request,'DIYProject/feed.html',{'projects':projects})

def filterCategoryView(request, category_id):
    category_name=ProjectCategory.objects.get(pk=category_id)
    projects = Project.objects.filter(project_category=category_name).order_by('-posted_on')
    return render(request, 'DIYProject/feed.html', {'projects': projects})
