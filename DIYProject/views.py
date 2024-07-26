from DIYProject.forms import NewProject, SearchProject, ThoughtForm
from DIYProject.models import Project, ProjectCategory, Thought, Favourite
from green_book_challenges.models import Points
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from marketplace.models import Category
from django.db.models.signals import post_delete
from django.db.models import Count
from django.dispatch import receiver
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.contrib import messages


def indexView(request):
    projects = Project.objects.annotate(upvotes_count=Count('upvotes')).order_by('-upvotes_count')
    categories = ProjectCategory.objects.all()
    return render(request,'DIYProject/index.html',{'projects':projects[:4], 'categories': categories})

@login_required(login_url='login')
def newProjectView(request):
    if request.method == 'POST':
        form = NewProject(request.POST, request.FILES)
        if form.is_valid():
            temp_project = form.save(commit=False)
            temp_project.posted_by = request.user
            temp_project.save()
            points_record, created = Points.objects.get_or_create(user=request.user)
            points_record.total_points += 2000
            points_record.save()
            messages.success(request,"2000 points have been added to your account")
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
    MyBookmark, created = Favourite.objects.get_or_create(holder=request.user)
    fav_projects = MyBookmark.fav_projects.all() or None
    visit_history = request.session.get('visit_history', [])
    SearchForm = SearchProject()
    projects = Project.objects.annotate(upvotes_count=Count('upvotes')).order_by('-upvotes_count')

    return render(request,'DIYProject/feed.html',{'projects':projects,'SearchForm':SearchForm, 'fav_projects':fav_projects, 'suggestions': visit_history[-5:]})


def upvotesView(request, project_id):
    MyBookmark, created = Favourite.objects.get_or_create(holder=request.user)
    fav_projects = MyBookmark.fav_projects.all() or None
    visit_history = request.session.get('visit_history', [])
    SearchForm = SearchProject()
    temp_project = get_object_or_404(Project,pk=project_id)

    if temp_project.upvotes.filter(id=request.user.pk).exists():
        temp_project.upvotes.remove(request.user)
    else:
        temp_project.upvotes.add(request.user)

    projects = Project.objects.annotate(upvotes_count=Count('upvotes')).order_by('-upvotes_count')

    return render(request,'DIYProject/feed.html',{'projects':projects,'SearchForm':SearchForm, 'fav_projects':fav_projects, 'suggestions': visit_history[-5:]})



def sortAscendingView(request):
    MyBookmark, created = Favourite.objects.get_or_create(holder=request.user)
    fav_projects = MyBookmark.fav_projects.all() or None
    SearchForm = SearchProject()
    projects = Project.objects.order_by('title')
    visit_history = request.session.get('visit_history', [])
    return render(request,'DIYProject/feed.html',{'projects':projects,'SearchForm':SearchForm, 'fav_projects':fav_projects, 'suggestions': visit_history[-5:]})

def sortDescendingView(request):
    MyBookmark, created = Favourite.objects.get_or_create(holder=request.user)
    fav_projects = MyBookmark.fav_projects.all() or None
    SearchForm = SearchProject()
    projects = Project.objects.order_by('-title')
    visit_history = request.session.get('visit_history', [])
    return render(request,'DIYProject/feed.html',{'projects':projects,'SearchForm':SearchForm, 'fav_projects':fav_projects,'suggestions':visit_history[-5:]})

def filterCategoryView(request, category_id):
    MyBookmark, created = Favourite.objects.get_or_create(holder=request.user)
    fav_projects = MyBookmark.fav_projects.all() or None
    SearchForm = SearchProject()
    category_name=ProjectCategory.objects.get(pk=category_id)
    projects = Project.objects.filter(project_category=category_name).order_by('-posted_on')
    visit_history = request.session.get('visit_history', [])
    return render(request, 'DIYProject/feed.html', {'projects': projects,'SearchForm':SearchForm, 'fav_projects':fav_projects, 'suggestions': visit_history[-5:]})

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
            points_record, created = Points.objects.get_or_create(user=request.user)
            points_record.total_points += 100
            points_record.save()
            messages.success(request, "100 points have been added to your account")
            return redirect('DIYProject:viewproject',project.id)

    return render(request,'DIYProject/view_project.html',{'project': project,'thoughts':thoughts,'ThoughtForm':tf})

@login_required(login_url='login')
def addToFavouriteView(request, project_id):
    MyBookmark, created = Favourite.objects.get_or_create(holder=request.user)
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
    MyBookmark, created = Favourite.objects.get_or_create(holder=request.user)
    if MyBookmark.fav_projects.filter(id=project_id).exists():
        MyBookmark.fav_projects.remove(project_id)
        MyBookmark.save()
        messages.success(request, "Project removed from Bookmarks")
    else:
        messages.error(request,"This project was never saved !")
    return redirect('DIYProject:bookmarks')

@login_required(login_url='login')
def bookmarkView(request):
    SearchForm = SearchProject()
    MyBookmark, created = Favourite.objects.get_or_create(holder=request.user)
    AllProjects = MyBookmark.fav_projects.all() or None
    if AllProjects is None:
        messages.error(request,'No Projects saved yet')
        return redirect('DIYProject:feed')
    visit_history = request.session.get('visit_history', [])
    return render(request, 'DIYProject/feed.html', {'projects': AllProjects, 'SearchForm': SearchForm, 'fav_projects':AllProjects,'suggestions':visit_history[-5:]})

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
    points_record, created = Points.objects.get_or_create(user=request.user)
    if points_record.total_points >= 100:
        points_record.total_points -=100
        points_record.save()
        messages.success(request, "100 points have been removed from your account")
    return redirect('DIYProject:viewproject',temp_project.id)

def SearchProjectView(request):
    if request.method == 'GET':
        form = SearchProject(request.GET)
        if form.is_valid():
            query = form.cleaned_data['term']

            visit_history = request.session.get('visit_history', [])

            if query not in visit_history:
                visit_history.append(query)
                request.session['visit_history'] = visit_history

            projects = Project.objects.filter(Q(title__icontains=query) | Q(tools__icontains=query) | Q(project_category__name__icontains=query)).order_by('-posted_on')
            if len(projects) == 0:
                messages.error(request,'No matching projects found')
                return redirect('DIYProject:feed')
                # projects = Project.objects.order_by('-posted_on')
            else:
                messages.success(request, 'Search completed successfully!')
                form = SearchProject()
                try:
                    fav_projects = Favourite.objects.get(holder=request.user).fav_projects.all()
                except:
                    fav_projects = None
                suggestions = visit_history[-5:]
                return render(request, "DIYProject/feed.html",
                              {'projects': projects, 'SearchForm': form, 'fav_projects': fav_projects,
                               'suggestions': suggestions})
        else:
            messages.error(request, 'Invalid search term')
            return redirect('DIYProject:feed')
    else:
        return redirect('DIYProject:feed')



