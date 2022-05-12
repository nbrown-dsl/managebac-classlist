
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
    print(termsofYears)

#returns array of student classes and their terms [{classid:34324,terms:[324,3423,23423]},...]
def termsOfClasses(id):

    pass
