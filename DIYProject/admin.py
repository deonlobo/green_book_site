from django.contrib import admin

from DIYProject.models import ProjectCategory,Project,Thought, Favourite

admin.site.register(ProjectCategory)
admin.site.register(Project)
admin.site.register(Thought)
admin.site.register(Favourite)