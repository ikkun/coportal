"""oc URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from users import views as user_views
from tools_inventory import views as tools_inventory_views

urlpatterns = [
    path('admin/', admin.site.urls),
    #users
    path('register/', user_views.register, name='register'),
    path('profile/', user_views.profile, name='profile'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    
    #tools list
    path('toolslist/',tools_inventory_views.ToolsListView.as_view(),name='toolslist'),
    path('toolslist/map/',tools_inventory_views.toollist_map,name='toolsmap'),
    path('toolcreate/create/',tools_inventory_views.CreateTool.as_view(), name='tool_create'),
    path('toolcreate/update/',tools_inventory_views.UpdateTool.as_view(), name='tool_update'),
    path('toolcreate/delete/',tools_inventory_views.DeleteTool.as_view(), name='tool_delete'),

    path('toolslistfilter/',tools_inventory_views.List_Tool_Filter.as_view(),name='toolslistfilter'),
    path('toolslistcsv/',tools_inventory_views.export_tools_to_xlsx,name='listtool_download'),

    path('',include('main.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)