from django.http import HttpResponse
from django.shortcuts import render
from openpyxl import load_workbook
from assigner.models import PastList

def homepage(request):
    past_list = PastList.objects
    return render(request, 'home.html', {'past_list':past_list})
    