from django.db import models
from django.contrib.auth.models import User
from users.models import Profile

class Tools_List(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User,null=True,blank=True,related_name='create2user',on_delete=models.SET_NULL)
    tool_name = models.CharField(max_length=300)
    tool_description = models.TextField()
    dev_by = models.CharField(max_length=300)
    used_by = models.TextField(null=True,blank=True)
    location = models.CharField(max_length=500,null=True,blank=True)
    url = models.CharField(max_length=300,null=True,blank=True)

    def __str__(self):
        return self.tool_name,self.dev_by

# class Tools_list_export(models.View):
#     res = Profile.team
#     tool_name = Tools_List.tool_name


