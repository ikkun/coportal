from django.contrib import admin
from .models import Tools_List

class HomeAdmin(admin.ModelAdmin):
    list_display = ('tool_name','created_by','tool_description','dev_by')

admin.site.register(Tools_List,HomeAdmin)

# Register your models here.
