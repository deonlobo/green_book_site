from django.db import models
from django.contrib.auth.models import User


class ProjectCategory(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='images/DIYProjects/ProjectCategory')

    def __str__(self):
        return self.name


class Project(models.Model):
    title = models.CharField(max_length=200)
    tools = models.CharField(max_length=200)
    project_category = models.ForeignKey(ProjectCategory, on_delete=models.CASCADE)
    process = models.TextField()
    img_1 = models.ImageField(upload_to='images/DIYProjects/ProjectImages')
    img_2 = models.ImageField(upload_to='images/DIYProjects/ProjectImages', blank=True, null=True)
    posted_on = models.DateTimeField(auto_now_add=True)
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def getSteps(self):
        return self.process.splitlines()

class Thought(models.Model):
    content = models.TextField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE)
    posted_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content

class Favourite(models.Model):
    holder =models.OneToOneField(User, on_delete=models.CASCADE)
    fav_projects = models.ManyToManyField(Project, blank=True)

    def __str__(self):
        return str(self.holder)
