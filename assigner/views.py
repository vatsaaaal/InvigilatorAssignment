from os import remove
from django.shortcuts import render, get_object_or_404, redirect
from teachers.models import Teacher
from .models import PastList, Room, SingleSubject
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from datetime import datetime
import openpyxl, random
from django.http import HttpResponse, HttpResponseRedirect

def home(request):
    return render(request, 'assigner/assigner_home.html')

def rooms(request):
    rooms = Room.objects.order_by('number')
    return render(request, 'assigner/rooms.html', {'rooms':rooms})

def detail(request, room_id):
    room = get_object_or_404(Room, pk=room_id)
    return render(request, 'assigner/room_detail.html', {'room':room})

def search(request):
    if request.method == 'POST':
        search = request.POST['search']
        if search:
            match = Room.objects.filter(Q(number__icontains=search) | Q(capacity__icontains=search))
            if match:
                return render(request, 'assigner/search.html', {'match':match})
            else:
                return render(request, 'assigner/search.html', {'error':'No Results Found'})
        else:
            return HttpResponseRedirect('assigner/rooms.html')
    return render(request, 'assigner/rooms.html')

def add(request):
    if request.method == 'POST':
        if request.POST['number'] and request.POST['capacity']:
            room = Room()
            room.number = request.POST['number']
            room.capacity = request.POST['capacity']
            room.save()
            return redirect('/assigner/rooms/' + str(room.id))
        else:
            return render(request, 'assigner/room_add.html', {'error':'All fields are required.'})

    return render(request, 'assigner/room_add.html')

def delete(request, room_id):
    if request.method == 'POST':
        room = get_object_or_404(Room, pk=room_id)
        room.delete()
        return HttpResponseRedirect("/assigner/rooms/")
    
def edit(request, room_id):
    room = get_object_or_404(Room, pk=room_id)
    if request.method == 'POST':
        if request.POST['number'] and request.POST['capacity']:
            room.number = request.POST['number']
            room.subject = request.POST['capacity']
            room.save()
            return render(request, 'assigner/room_detail.html', {'room':room})
        else:
            return render(request, 'assigner/room_edit.html', {'error': 'All fields are required.'})
    return render(request, 'assigner/room_edit.html', {'room':room})

def manual(request):
    if request.method == 'POST':
        number = int(request.POST['number'])
        global num_list
        num_list = [x for x in range(1, number+1)]
        teachers = Teacher.objects.all()
        subjects = Teacher.objects.values('subject').order_by('subject')
        return render(request, 'assigner/manual.html', {'teachers': teachers, 'num_list':num_list, 'subjects': subjects})
    return render(request, 'assigner/manual.html')

def assigned(request):
    if request.method == 'POST':
        sub_teacher = []
        for num in num_list:
            sub_teacher.append([request.POST['subject' + str(num)], request.POST['teacher' + str(num)]])
        now = datetime.datetime.now()
        assigned_list = AssignedList()
        assigned_list.name = now.strftime("%d-%m-%Y")
        assigned_list.assigned = sub_teacher
        assigned_list.save()
        return redirect('/assigner/' + str(assigned_list.id))
    return render(request, 'assigner/manual.html')

def list_detail(request, list_id):
    past_list = get_object_or_404(PastList, pk=list_id)
    subs = list(SingleSubject.objects.filter(pastList=past_list))
    data = []
    for x in subs:
        temp = []
        temp.extend([x.subject, x.duration, x.start_time, x.end_time, x.num_of_students, x.room_num, x.invigi_name])
        data.append(temp)
    print(data)      
    return render(request, 'assigner/list_detail.html', {'past_list':past_list, 'subs':subs, 'data':data})

def automatic(request):
    if request.method == 'POST' and request.FILES['schedule']:
        schedule = request.FILES['schedule']
        wb = openpyxl.load_workbook(schedule)
        worksheet = wb.active
        data = list()
        for row in worksheet.iter_rows():
            row_data = list()
            for cell in row:
                row_data.append(str(cell.value))
            data.append(row_data)
        data.pop(0)
        teachers_object = list(Teacher.objects.all())
        invigi_assignment = []     
        subject_list = [i[0] for i in data]
        # del subject_list[0]
        capacity = [int(i[4]) for i in data]
        print("CAPACITY:", capacity)
        rooms_object = list(Room.objects.all())
        rooms = []
        eighty_rooms = []
        thirty_rooms = []
        for room in rooms_object:
            rooms.append([room.number, room.capacity])
            if room.capacity > 30:
                eighty_rooms.append([room.number, room.capacity])
            else:
                thirty_rooms.append([room.number, room.capacity])
        print("INITIAL EIGHTY ROOMS:", eighty_rooms)
        print("INITIAL THIRTY ROOMS:", thirty_rooms)
        assinged_rooms = []
        removed_rooms = []
        teachers = []
        for teacher in teachers_object:
            teachers.append([teacher.name, teacher.subject, teacher.email])
        print(teachers)
        for ida, a in enumerate(capacity):
            print("CAPACITY", a)
            temp_assigned = []
            print("TEMP ASSIGNED:", temp_assigned)
            while a >= 80:
                print("IN WHILE A >= 80")
                print("IN WHILE A:", a)
                if len(eighty_rooms) > 0:
                    for x in eighty_rooms:
                        temp_assigned.append(x)
                        assinged_rooms.append(x)
                        eighty_rooms.pop(eighty_rooms.index(x))
                        a -= 80
                        break
                else:
                    while a > 30:
                        for x in thirty_rooms:
                            temp_assigned.append(x)
                            assinged_rooms.append(x)
                            thirty_rooms.pop(thirty_rooms.index(x))
                            a -= 30
                            break
                print("TEMP ASSIGNED:", temp_assigned)
            if a > 30 and a <= 80:
                print("IN IF A > 30 AND A<= 80")
                print("IN IF A > 30 AND A <= 80:", a)
                if len(eighty_rooms) > 0:
                    temp1 = eighty_rooms[0]
                    temp_assigned.append(temp1)
                    assinged_rooms.append(temp1)
                    eighty_rooms.remove(temp1)
                    a = 0
                else:
                    while a > 30:
                        for x in thirty_rooms:
                            temp_assigned.append(x)
                            assinged_rooms.append(x)
                            thirty_rooms.pop(thirty_rooms.index(x))
                            a -= 30
                            break
                print("TEMP ASSIGNED:", temp_assigned)
            if a <= 30 and a > 0:
                print("IN IF A <= 30")
                print("IN IF A <= 30", a)
                print("TEMP ASSIGNED:", temp_assigned)
                for x in thirty_rooms:
                    temp_assigned.append(x)                
                    assinged_rooms.append(x)
                    thirty_rooms.pop(thirty_rooms.index(x))
                    a = 0
                    break
            temp_rooms_string = ""
            for idx, x in enumerate(temp_assigned):
                temp2 = str(x[0])
                temp3 = str(x[1])
                if idx == 0:
                    temp_rooms_string = temp2 + " : " + temp3
                else:
                    temp_rooms_string += ", " + temp2 + " : " + temp3
            print(temp_rooms_string)
            data[ida].append(temp_rooms_string)
            print("EIGHTY ROOMS:", eighty_rooms)
            print("THIRTY ROOMS:", thirty_rooms)
            print("ASSIGNED ROOMS:", assinged_rooms)
            print("TEMP ROOMS:", temp_assigned)
            temp_teachers = []
            for idx, room_num in enumerate(temp_assigned):
                print(idx)
                invigilators = []
                removed_teachers = []
                for count, teacher in enumerate(teachers):
                    if data[ida][0] == teacher[1]:
                        removed_teacher = teachers.pop(count)
                        removed_teachers.append(removed_teacher)
                assigned_teacher = random.choice(teachers)
                teachers.pop(teachers.index(assigned_teacher))
                invigilators.append(assigned_teacher)
                temp_teachers.append(assigned_teacher[0])
                if len(removed_teachers) == 0:
                    pass
                else:
                    for item in removed_teachers:
                        teachers.append(item)
                print("SUBJECT: ", data[ida][0])
                print("ASSIGNED TEACHER: ", assigned_teacher)
                print("REMOVED TEACHERS: ", removed_teachers)
                print("INVIGILATORS", invigilators)
                print("TEACHERS: ", teachers)
                invigi_assignment.append([data[ida][0], assigned_teacher[0], assigned_teacher[1], assigned_teacher[2]])
            temp_teachers_string = ""
            for idx, teacher_name in enumerate(temp_teachers):
                temp4 = str(teacher_name)
                if idx == 0:
                    temp_teachers_string += temp4
                else:
                    temp_teachers_string += ", " + temp4
            data[ida].append(temp_teachers_string)
        print(subject_list)
        print(data)
        file_name = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        pastlist = PastList(date=file_name)
        pastlist.save()
        for i in data:
            singlesub = SingleSubject(subject=i[0], pastList=pastlist, duration=i[1], start_time=i[2], end_time=i[3], num_of_students=i[4], room_num=i[5], invigi_name=i[6])
            singlesub.save()
        
        return render(request, 'assigner/automatic.html', {'list':invigi_assignment, 'data':data, 'filename':file_name})
    return render(request, 'assigner/automatic.html')