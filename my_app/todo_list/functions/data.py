
#data API calls to managebac

from todo_list.functions import key

import json
import requests
#to use reload function
import importlib



def studentData(id):
    headers = {
        'auth-token': key.keyToken(),}
    response = requests.get('https://api.managebac.com/v2/students/'+id, headers=headers)
    
    # converts to python dict
    return json.loads(response.content)

def mbClasses():
    headers = {
        'auth-token': key.keyToken(),}
    response = requests.get('https://api.managebac.com/v2/classes?archived=true', headers=headers)
    
    # converts to python dict
    return json.loads(response.content)


def academicYears():
    headers = {
    'auth-token': key.keyToken(),}
    response = requests.get('https://api.managebac.com/v2/school/academic-years', headers=headers)

    return json.loads(response.content)

# class studentClasses(id):
#     if not archived:
#         archived = 'false'
#     headers = {
#     'auth-token': keyToken(),}
#     response = requests.get('https://api.managebac.com/v2/students/'+id+'/memberships?archived='+archived, headers=headers)

#     return json.loads(response.content)



def studentClasses(id,archived):
    if not archived:
        archived = 'false'
    headers = {
    'auth-token': key.keyToken(),}
    response = requests.get('https://api.managebac.com/v2/students/'+id+'/memberships?archived='+archived, headers=headers)

    return json.loads(response.content)

def allClasses(archived):
    headers = {
    'auth-token': key.keyToken(),}
    response = requests.get('https://api.managebac.com/v2/classes?per_page=1000&archived='+archived, headers=headers)

    return json.loads(response.content)
    

def classTermGrades(classId,termId):
    headers = {
    'auth-token': key.keyToken(),}
    response = requests.get('https://api.managebac.com/v2/classes/'+classId+'/assessments/term/'+termId+'/term-grades?include_archived_students=true', headers=headers)

    return json.loads(response.content)

#returns array of term ids in chronological order
#to be used for returning terms that class runs for
def terms(programme):
    termsofYears=[]
    years = academicYears()["academic_years"][programme]["academic_years"]

    for year in years:
        for termsInYear in year["academic_terms"]:
            termsofYears.append(termsInYear['id'])
    return termsofYears

#returns array of student classes and their terms [{classid:34324,terms:[324,3423,23423]},...]
def termsOfClasses(id):

    toc = []

    archived_student_Classes = studentClasses(str(id),'true')["memberships"]["classes"]
    current_student_Classes = studentClasses(str(id),'false')["memberships"]["classes"]
    all_student_classes=archived_student_Classes+current_student_Classes

    termsIds = terms('myp')+terms('diploma')
    
    for studentClass in all_student_classes:
        startIdIndex =  termsIds.index(studentClass['start_term_id'])
        endIdIndex =  termsIds.index(studentClass['end_term_id'])
        classTermsIds = []
        for classTermIdIndex in range (startIdIndex,endIdIndex+1):
            classTermsIds.append(termsIds[classTermIdIndex])
        toc.append({'classId':studentClass['id'], 'termsIds':classTermsIds})

    return toc

def studentTranscript(id, studentStart):
        mypyears = []
        dpyears = []
        #returns array of class objects
        all_archived_Classes=allClasses('true')["classes"]
        all_active_Classes=allClasses('false')["classes"]
        all_Classes=all_archived_Classes+all_active_Classes

        
        
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
                                        transcriptData.append({'subject_name':all_Classes[i]['subject_name'],'subject_group':all_Classes[i]['subject_group'], 'grade':str(student['term_grade']['grade'])})
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
                                        transcriptData.append({'classData':all_Classes[i],'grade':str(student['term_grade']['grade'])})
                            except:
                                print("oops "+str(i))
                    if hasGrade:
                        terms.append({'termID':term['id'], 'termName':term['name'], 'classGrades':transcriptData})
                        hasyearGrades = True
                if hasyearGrades:
                    dpyears.append({'yearName':year["name"],'terms':terms})

        years = [mypyears, dpyears] 

        return years