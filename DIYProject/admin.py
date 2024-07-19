from django.contrib import admin

from DIYProject.models import ProjectCategory,Project,Thought

admin.site.register(ProjectCategory)
admin.site.register(Project)
admin.site.register(Thought)