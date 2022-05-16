from django.shortcuts import render
from .models import List
from django.contrib import messages
from .key import keyToken
from .doc_output import mailmergeDoc

import json
import requests
#managebac API functions
from .data import *


def home(request):
    
    return render(request,'home.html',{'mbClasses' : mbClasses()['classes']})

    from .classroomList import main
    global courses
    courses = main()

    return render(request,'home.html',{'mbClasses' : courses})


def about(request):
    my_name ="Nick"
    return render(request,'about.html',{'name' : my_name})



def search(request):
    
    if request.method == 'POST' and len(request.POST['item'])>0:
        filterTerm = request.POST['item']
        filteredList = []

        for classes in mbClasses()["classes"]:
            if filterTerm in classes['name']:
                filteredList.append({'name':classes['name']})

        messages.success(request,('Courses containing '+filterTerm))
        return render(request,'home.html',{'mbClasses()' : filteredList})
    
    return render(request,'home.html',{'mbClasses' : mbClasses()['classes']})

def student(request):
    
    if request.method == 'POST':
        id = request.POST['studentID']

        studentObject = studentData(id)["student"]
        studentStart = studentObject["created_at"]

        years = studentTranscript(id, studentStart)

        # outputDoc(years)
        mailmergeDoc(years,studentObject)
                   
        messages.success(request,('Student Classes below and transcript doc generated'))
        return render(request,'student.html',{'years' : years,'student': studentObject})
    
    return render(request,'student.html')


#sort items alphabetically
def sortAlpha(request):
    
        sorted_items = List.objects.order_by('item')
        return render(request,'home.html',{'all_items' : sorted_items})

#sort items alphabetically
def filterDone(request,state):
    filterSwitch = ''
    if state == 'done':
        filterSwitch = True
    else:
        filterSwitch = False
    filtered_items = List.objects.filter(completed=filterSwitch)
    return render(request,'home.html',{'all_items' : filtered_items})

# def genDoc(request,id):

#     studentObject = studentData(id)["student"]
#     studentStart = studentObject["created_at"]

#     years = studentTranscript(id, studentStart)

#     outputDoc(years)
#     messages.success(request,('Transcript generated'))
#     return render(request,'student.html')



