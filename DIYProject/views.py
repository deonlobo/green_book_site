from DIYProject.forms import NewProject, SearchProject, ThoughtForm
from DIYProject.models import Project, ProjectCategory, Thought, Favourite
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
    fav_projects = Favourite.objects.get(holder=request.user).fav_projects.all()
    SearchForm = SearchProject()
    projects = Project.objects.order_by('-posted_on')
    return render(request,'DIYProject/feed.html',{'projects':projects,'SearchForm':SearchForm, 'fav_projects':fav_projects})

def filterCategoryView(request, category_id):
    fav_projects = Favourite.objects.get(holder=request.user).fav_projects.all()
    SearchForm = SearchProject()
    category_name=ProjectCategory.objects.get(pk=category_id)
    projects = Project.objects.filter(project_category=category_name).order_by('-posted_on')
    return render(request, 'DIYProject/feed.html', {'projects': projects,'SearchForm':SearchForm, 'fav_projects':fav_projects})

@login_required(login_url='login')
def myProjectView(request):
    projects = Project.objects.filter(posted_by=request.user).order_by('-posted_on')
    return render(request,'DIYProject/my_projects.html',{'projects': projects})

def projectView(request,id):
    project = get_object_or_404(Project, pk=id)
    thoughts = Thought.objects.filter(project=project)
    tf = ThoughtForm()
    if request.method=='POST':
        tf = ThoughtForm(request.POST)
        if tf.is_valid():
            instance = tf.save(commit=False)
            instance.project = project
            instance.posted_by = request.user
            instance.save()
            return redirect('DIYProject:viewproject',project.id)

    return render(request,'DIYProject/view_project.html',{'project': project,'thoughts':thoughts,'ThoughtForm':tf})

@login_required(login_url='login')
def addToFavouriteView(request, project_id):
    try:
        MyBookmark = Favourite.objects.get(holder=request.user)
    except:
        MyBookmark = Favourite()
        MyBookmark.holder = request.user
        MyBookmark.save()
    TempProject = Project.objects.get(pk=project_id)
    if TempProject in MyBookmark.fav_projects.all():
        messages.error(request,'Project already saved')
        return redirect('DIYProject:bookmarks')
    else:
        MyBookmark.fav_projects.add(TempProject)
        MyBookmark.save()
        messages.success(request,'Project saved')
        return redirect('DIYProject:bookmarks')

@login_required(login_url='login')
def removeFromFavouriteView(request, project_id):
    MyBookmark = Favourite.objects.get(holder=request.user)
    MyBookmark.fav_projects.remove(project_id)
    MyBookmark.save()
    return redirect('DIYProject:bookmarks')

@login_required(login_url='login')
def bookmarkView(request):
    SearchForm = SearchProject()
    fav_projects = Favourite.objects.get(holder=request.user).fav_projects.all()
    try:
        MyBookmark = Favourite.objects.get(holder=request.user)
    except:
        MyBookmark = Favourite(holder=request.user)
        MyBookmark.save()
    AllProjects = MyBookmark.fav_projects.all()
    if not AllProjects:
        messages.error('No Projects saved yet')
        return redirect('DIYProject:feed')
    return render(request, 'DIYProject/feed.html', {'projects': AllProjects, 'SearchForm': SearchForm, 'fav_projects':fav_projects})

@login_required(login_url='login')
def deleteProjectView(request,project_id):
    temp_project = get_object_or_404(Project, pk=project_id)
    temp_project.delete()
    return redirect('DIYProject:myprojects')

@login_required(login_url='login')
def removeThoughtView(request,thought_id):
    temp_thought = get_object_or_404(Thought, pk=thought_id)
    temp_thought.delete()
    temp_project = temp_thought.project
    return redirect('DIYProject:viewproject',temp_project.id)

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
            fav_projects  = Favourite.objects.get(holder=request.user).fav_projects.all()
            return render(request, "DIYProject/feed.html", {'projects': projects, 'SearchForm': form, 'fav_projects':fav_projects})
        else:
            messages.error(request, 'Invalid search term')
            return redirect('DIYProject:feed')

