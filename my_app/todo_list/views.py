from django.shortcuts import render, redirect
from .models import List
from .forms import ListForm
from django.contrib import messages
from django.http import HttpResponseRedirect
from .key import keyToken

import json
import requests
    #managebac API call test
headers = {
    'auth-token': keyToken(),}
response = requests.get('https://api.managebac.com/v2/classes', headers=headers)
    
global mbClasses
# converts to python dict
mbClasses = json.loads(response.content)


def academicYears():
    headers = {
    'auth-token': keyToken(),}
    response = requests.get('https://api.managebac.com/v2/school/academic-years', headers=headers)

    return json.loads(response.content)


def studentClasses(id):
    headers = {
    'auth-token': keyToken(),}
    response = requests.get('https://api.managebac.com/v2/students/'+id+'/memberships', headers=headers)

    return json.loads(response.content)

def allClasses():
    headers = {
    'auth-token': keyToken(),}
    response = requests.get('https://api.managebac.com/v2/classes', headers=headers)

    return json.loads(response.content)
    

def classTermGrades(classId,termId):
    headers = {
    'auth-token': keyToken(),}
    response = requests.get('https://api.managebac.com/v2/classes/'+classId+'/assessments/term/'+termId+'/term-grades?include_archived_students=true', headers=headers)

    return json.loads(response.content)


def home(request):
    
    return render(request,'home.html',{'mbClasses' : mbClasses['classes']})

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

        for classes in mbClasses["classes"]:
            if filterTerm in classes['name']:
                filteredList.append({'name':classes['name']})

        messages.success(request,('Courses containing '+filterTerm))
        return render(request,'home.html',{'mbClasses' : filteredList})
    
    return render(request,'home.html',{'mbClasses' : mbClasses['classes']})

def student(request):
    
    if request.method == 'POST':
        id = request.POST['studentID']
        years = []
        
        student_Classes = studentClasses(id)["memberships"]["classes"]
        # termID = 168734
        yearsData = academicYears()["academic_years"]["diploma"]["academic_years"]
        
        
        for year in yearsData:
            hasyearGrades = False
            terms = []
            for term in year["academic_terms"]:               
                transcriptData = []
                hasGrade = False
                for classes in student_Classes:
                    classGrades = classTermGrades(str(classes['id']),str(term['id']))
                    for student in classGrades["students"]:
                        if student['id'] == int(id) and student['term_grade']['grade']!=None:
                            hasGrade = True
                            transcriptData.append({'name':classes['name'],'grade':student['term_grade']['grade']})
                if hasGrade:
                    terms.append({'termID':term['id'], 'termName':term['name'], 'classGrades':transcriptData})
                    hasyearGrades = True
            if hasyearGrades:
                years.append({'yearName':year["name"],'terms':terms})
        messages.success(request,('Student Classes'))
        return render(request,'student.html',{'years' : years})
    
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

# def delete(request, list_id):
#     item = List.objects.get(pk=list_id)
#     item.delete()
#     messages.success(request,('Item deleted'))
#     return redirect('home')

# def cross_off(request, list_id):
#     item = List.objects.get(pk=list_id)
#     item.completed = True
#     item.save()
#     return redirect('home')

# def uncross(request, list_id):
#     item = List.objects.get(pk=list_id)
#     item.completed = False
#     item.save()
#     return redirect('home')

# def edit(request,list_id):

#     if request.method == 'POST':
#         item = List.objects.get(pk=list_id)

#         form = ListForm(request.POST or None, instance=item)

#         if form.is_valid():
#             form.save()
#             messages.success(request,('Item edited'))
#             return redirect('home')

#     else:

#         item = List.objects.get(pk=list_id)
#         return render(request,'edit.html',{'item' : item})