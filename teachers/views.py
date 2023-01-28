from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from .models import Teacher

def home(request):
    teachers = Teacher.objects.order_by('name')
    return render(request, 'teachers/teachers_home.html', {'teachers':teachers})

def detail(request, teacher_id):
    teacher = get_object_or_404(Teacher, pk=teacher_id)
    return render(request, 'teachers/detail.html', {'teacher':teacher})

def search(request):
    if request.method == 'POST':
        search = request.POST['search']
        if search:
            match = Teacher.objects.filter(Q(name__icontains=search) | Q(subject__icontains=search))
            if match:
                return render(request, 'teachers/search.html', {'match':match})
            else:
                return render(request, 'teachers/search.html', {'error':'No Results Found'})
        else:
            return HttpResponseRedirect('teachers/teachers_home.html')
    return render(request, 'teachers/teachers_home.html')

def add(request):
    if request.method == 'POST':
        if request.POST['name'] and request.POST['subject'] and request.POST['email']:
            teacher = Teacher()
            teacher.name = request.POST['name']
            teacher.subject = request.POST['subject']
            teacher.email = request.POST['email']
            teacher.save()
            return redirect('/teachers/' + str(teacher.id))
        else:
            return render(request, 'teachers/add.html', {'error':'All fields are required.'})

    return render(request, 'teachers/add.html')

def delete(request, teacher_id):
    if request.method == 'POST':
        teacher = get_object_or_404(Teacher, pk=teacher_id)
        teacher.delete()
        return HttpResponseRedirect("/teachers/") 

def edit(request, teacher_id):
    teacher = get_object_or_404(Teacher, pk=teacher_id)
    if request.method == 'POST':
        if request.POST['name'] and request.POST['subject'] and request.POST['email']:
            teacher.name = request.POST['name']
            teacher.subject = request.POST['subject']
            teacher.email = request.POST['email']
            teacher.save()
            return render(request, 'teachers/detail.html', {'teacher':teacher})
        else:
            return render(request, 'teachers/edit.html', {'error': 'All fields are required.'})
    return render(request, 'teachers/edit.html', {'teacher':teacher})