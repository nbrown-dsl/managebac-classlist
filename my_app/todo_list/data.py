
#data API calls to managebac

from .key import keyToken

import json
import requests
#to use reload function
import importlib



def studentData(id):
    headers = {
        'auth-token': keyToken(),}
    response = requests.get('https://api.managebac.com/v2/students/'+id, headers=headers)
    
    # converts to python dict
    return json.loads(response.content)

def mbClasses():
    headers = {
        'auth-token': keyToken(),}
    response = requests.get('https://api.managebac.com/v2/classes?archived=true', headers=headers)
    
    # converts to python dict
    return json.loads(response.content)


def academicYears():
    headers = {
    'auth-token': keyToken(),}
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
    'auth-token': keyToken(),}
    response = requests.get('https://api.managebac.com/v2/students/'+id+'/memberships?archived='+archived, headers=headers)

    return json.loads(response.content)

def allClasses(archived):
    headers = {
    'auth-token': keyToken(),}
    response = requests.get('https://api.managebac.com/v2/classes?per_page=1000&archived='+archived, headers=headers)

    return json.loads(response.content)
    

def classTermGrades(classId,termId):
    headers = {
    'auth-token': keyToken(),}
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
def termsOfClasses(id='13618268'):

    toc = []

    archived_student_Classes = studentClasses(id,'true')["memberships"]["classes"]
    current_student_Classes = studentClasses(id,'false')["memberships"]["classes"]
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

