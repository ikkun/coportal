from django.shortcuts import render
from django.views.generic import View,TemplateView,ListView
from .models import Tools_List
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse,HttpResponse
from users.models import Profile
from django.db.models import Q,F

import xlwt




def toollist(request):
    context = {
        'title': 'รายการเครื่องมือ'
    }
    return render(request, 'tools_inventory/toolslist.html', context)

class ToolsListView(LoginRequiredMixin,TemplateView):
    # model = ScanSchedule
    template_name='tools_inventory/toolslist.html'
    # context_object_name = 'tasks'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tools'] = Tools_List.objects.filter(created_by_id=self.request.user.id)
        context['title'] = 'รายการเครื่องมือ'
        
        return context

class CreateTool(LoginRequiredMixin,View):
    def get(self, request):
        createby1 = request.user.id
        toolname1 = request.GET.get('toolname', None)
        tooldesc1 = request.GET.get('tooldesc', None)
        devby1 = request.GET.get('devby', None)
        useby1 = request.GET.get('useby', None)  
        location1 = request.GET.get('location', None)
        url1 = request.GET.get('url', None)      

        obj = Tools_List.objects.create(
            tool_name = toolname1,
            tool_description = tooldesc1,
            dev_by = devby1,
            used_by = useby1,
            location = location1,
            url = url1,
            created_by_id = createby1

        )

        tool = {'id':obj.id,'tool_name':obj.tool_name,'tool_description':obj.tool_description}

        data = {
            'tool': tool
        }
        return JsonResponse(data)

class UpdateTool(LoginRequiredMixin,View):
    def get(self, request):
        id1 = request.GET.get('id', None)
        toolname1 = request.GET.get('toolname', None)
        tooldesc1 = request.GET.get('tooldesc', None)
        devby1 = request.GET.get('devby', None)
        useby1 = request.GET.get('useby', None)  
        location1 = request.GET.get('location', None)
        url1 = request.GET.get('url', None) 
        

        obj = Tools_List.objects.get(id=id1)        
        obj.tool_name = toolname1
        obj.tool_description = tooldesc1
        obj.dev_by = devby1
        obj.used_by = useby1
        obj.location = location1
        obj.url = url1        
        obj.save()

        tool = {'id':obj.id,'tool_name':obj.tool_name,'tool_description':obj.tool_description,'dev_by':obj.dev_by,
                'used_by':obj.used_by,'location':obj.location,'url':obj.url
                }

        data = {
            'tool': tool
        }
        return JsonResponse(data)

class DeleteTool(LoginRequiredMixin,View):
    def get(self, request):
        id1 = request.GET.get('id', None)
        Tools_List.objects.get(id=id1).delete()
        data = {
            'deleted': True
        }
        return JsonResponse(data)

class Echo:
    """An object that implements just the write method of the file-like
    interface.
    """
    def write(self, value):
        """Write the value by returning it, instead of storing in a buffer."""
        return value


class List_Tool_Filter(LoginRequiredMixin,ListView):
    
    model=Tools_List
    template_name='tools_inventory/toolslistfilter.html'
    context_object_name = 'tools'
    paginate_by=10
    def get_queryset(self):
        qs = Tools_List.objects.order_by('-created_by')
        res= self.request.GET.get('response')
        if res is not None and res != '':
            qs = Tools_List.objects.filter(Q(created_by_id__exact=res)).order_by('created_at')
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) 
        context['title']="Tools List"
        
        context['ress'] = Profile.objects.exclude(Q(user_id__exact=1)).values('team','user').distinct()
        
        # context.update(nav_count()) 
        return context

def export_tools_to_xlsx(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="listTools.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Tools')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.easyxf('pattern: pattern solid, fore_color light_blue;borders: top_color black, bottom_color black, right_color black, left_color black,left thin, right thin, top thin, bottom thin;')
    font_style.font.bold = True

    columns = ['Responsibilities Team', 'Tool', 'Description', 'Dev By','Used By','Location','URL' ]

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rowsx
    font_style = xlwt.easyxf('align:wrap 1;borders: top_color black, bottom_color black, right_color black, left_color black,left thin, right thin, top thin, bottom thin;')

    #rows = Tools_List.objects.select_related().values_list('created_by', 'tool_name', 'tool_description', 'dev_by','used_by','location','url')
    qtools = Tools_List.objects.select_related()
    # print(rows)
    listTools=[]
    for tool in qtools:
        listTools.append((tool.created_by.profile.get_team_display(),
        tool.tool_name,
        tool.tool_description,
        tool.dev_by,
        tool.used_by,
        tool.location,
        tool.url
        ))
    # print(listTools)
    # print(rows)
    for row in listTools:
        
        row_num += 1
        
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)
            
    # columnwidth = {}
    # row = 0
    # for rowdata in listTools:
    #     column = 0
    #     for colomndata in rowdata:
    #         if column in columnwidth:
    #             if len(colomndata) > columnwidth[column]:
    #                 columnwidth[column] = len(colomndata)
    #         else:
    #             columnwidth[column] = len(colomndata)
    #         ws.write(row, column, colomndata, font_style)
    #         column = column + 1
    #     row = row + 1
    # for column, widthvalue in columnwidth.items():
    #     ws.col(column).width = (widthvalue + 4) * 367
    ws.col(0).width=256*10
    ws.col(1).width=256*20
    ws.col(2).width=256*70
    ws.col(3).width=256*20
    ws.col(4).width=256*20
    ws.col(5).width=256*15
    ws.col(6).width=256*10
    wb.save(response)
    return response

def toollist_map(request):
    qloc_res=Tools_List.objects.select_related()
    map_tools=[]
    for row in qloc_res:
        if [row.location,row.created_by.profile.get_team_display()] not in map_tools:
            map_tools.append([row.location,row.created_by.profile.get_team_display()])
        if [row.created_by.profile.get_team_display(),row.tool_name] not in map_tools:
            map_tools.append([row.created_by.profile.get_team_display(),row.tool_name])
    map_dicts=[]
    for m in map_tools:
        map_dicts.append({'from':m[0],'to':m[1]})
    context = {
        'title': 'เครือข่ายเครื่องมือของ O&C',
        
    }
    context['map']=map_dicts
    return render(request, 'tools_inventory/toolsmap.html', context)

def toollist_plan(request):
    context = {
        'title': 'แผนงานรวบรวม Tools List',
        
    }
    return render(request,'tools_inventory/toolslistplan.html',context)

