from django.shortcuts import render
from .models import List
from django.contrib import messages
from .key import keyToken
from .doc_output import outputDoc

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
        mypyears = []
        dpyears = []
        #returns array of class objects
        all_archived_Classes=allClasses('true')["classes"]
        all_active_Classes=allClasses('false')["classes"]
        all_Classes=all_archived_Classes+all_active_Classes

        studentObject = studentData(id)["student"]
        studentStart = studentObject["created_at"]
        
        # termID = 168734
        mypyearsData = academicYears()["academic_years"]["myp"]["academic_years"]
        dpyearsData = academicYears()["academic_years"]["diploma"]["academic_years"]
        toc = termsOfClasses(id)

        for year in mypyearsData:
            hasyearGrades = False
            terms = []
            
            if int(year["starts_on"][0:4]) >= int(studentStart[0:4]):
                for term in year["academic_terms"]:               
                    transcriptData = []
                    hasGrade = False
                    for t in toc:
                        if term['id'] in t['termsIds']:
                            classGrades = classTermGrades(str(t['classId']),str(term['id']))
                            try:
                                for student in classGrades["students"]:
                                    if student['id'] == int(id) and student['term_grade']['grade']!=None:
                                        hasGrade = True
                                        i=0
                                        while t['classId'] != all_Classes[i]['id'] and i+1<len(all_Classes):
                                            i=i+1
                                        print (str(i)+"class "+all_Classes[i]['subject_name'])
                                        transcriptData.append({'classData':all_Classes[i],'grade':student['term_grade']['grade']})
                            except:
                                print("oops "+str(i))
                    if hasGrade:
                        terms.append({'termID':term['id'], 'termName':term['name'], 'classGrades':transcriptData})
                        hasyearGrades = True
                if hasyearGrades:
                    mypyears.append({'yearName':year["name"],'terms':terms})
        
        for year in dpyearsData:
            hasyearGrades = False
            terms = []
            #only checks in years since student joined
            if int(year["starts_on"][0:4]) >= int(studentStart[0:4]):
                for term in year["academic_terms"]:               
                    transcriptData = []
                    hasGrade = False
                    for t in toc:
                        if term['id'] in t['termsIds']:
                            classGrades = classTermGrades(str(t['classId']),str(term['id']))
                            try:
                                for student in classGrades["students"]:
                                    if student['id'] == int(id) and student['term_grade']['grade']!=None:
                                        hasGrade = True
                                        i=0
                                        while t['classId'] != all_Classes[i]['id'] and i+1<len(all_Classes):
                                            i=i+1
                                        print (str(i)+"class "+all_Classes[i]['subject_name'])
                                        transcriptData.append({'classData':all_Classes[i],'grade':student['term_grade']['grade']})
                            except:
                                print("oops "+str(i))
                    if hasGrade:
                        terms.append({'termID':term['id'], 'termName':term['name'], 'classGrades':transcriptData})
                        hasyearGrades = True
                if hasyearGrades:
                    dpyears.append({'yearName':year["name"],'terms':terms})

        years = [mypyears, dpyears]    
        
        messages.success(request,('Student Classes'))
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

def genDoc(data):

    outputDoc(data)
    messages.success(request,('Transcript generated'))
    return render(request,'student.html')



