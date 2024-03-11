from requests import Session
from bs4 import BeautifulSoup
import json
import time

global contestName
global groupLink

def getCSRF(info):

    auth = info
    soup = BeautifulSoup(auth, 'html.parser')
    form_data = {}
    for field in ['csrf_token' ]:
        field_value = soup.find('input', {'name': field}).get('value', '')

        form_data[field] = field_value 

    return form_data['csrf_token']


def makeTask(session: Session, problemSet: str, numQuestions: int, group: str, Name: str):

    global contestName, groupLink
    contestName = Name
    groupLink = group

    #Reading Level 0 DB
    file = open(f"{problemSet}.txt", "r")
    listOfProbs = file.readlines()
    file.close()

    #Get CSRF Token
    token = getCSRF(session.get("https://codeforces.com/mashup/new").content)

    #Getting Problems ID
        
    js = [] #JSON Payload

    for i in range(numQuestions):

        problem = listOfProbs.pop(0).strip()

        if "polygon" not in problem:         #Check if problem is a polygon link or not

            #Getting problems informations to be sent

            Payload = {
                "action": "problemQuery",
                "problemQuery": problem,
                "previouslyAddedProblemCount":"0",
                "csrf_token": token,
            }

            #Get information

            result = session.post("https://codeforces.com/data/mashup", data=Payload)
            data = result.json()

            #Making Payload
            place = data['problems'][0]
            dic = {"id": place['id'], "index": chr(ord('A') + i)}
        
        else:
            dic = {"url": problem, "index": chr(ord('A') + i)}

        js.append(dic)

    file = open(f"{problemSet}.txt", "w")
    file.writelines(listOfProbs)
    file.close()

    #Transform to JSON
    final = json.dumps(js)
    

    #Now Prepairing Payload to be sent


    Payload = {
        'action': 'saveMashup',
        'isCloneContest': 'false',
        'parentContestIdAndName': "",
        'parentContestId': "",
        'contestName': contestName,
        'contestDuration': "1440",
        'problemsJson': final,
        'csrf_token': token,

    }

    #Creating Mashup
    result = session.post("https://codeforces.com/data/mashup", data=Payload) 

    #Mashup ID
    mashNum = result.json()["newMashupContestId"]     

    return editSettings(session, mashNum)


def editSettings(session: Session, MashID):

    global contestName, groupLink
    mashNum = MashID

    #Get CSRF Token
    token = getCSRF(session.get(f"https://codeforces.com/gym/edit/{mashNum}").content)

    #Make Date
    date = time.asctime().split(" ")
    startDay = f"{date[1]}/{('0' + str(int(date[2]) + 1)) if len(str(int(date[2]) + 1)) == 1 else int(date[2]) + 1}/{date[-1]}"

    #Now Editing Mashup Settings
    print(startDay)
    Payload = {
        'csrf_token': token,
        "contestEditFormSubmitted": "true",
        "clientTimezoneOffset": "120",
        "englishName": contestName,
        "russianName": contestName,
        "untaggedContestType": "ICPC",
        "initialDatetime" : "",
        "startDay": startDay,
        "startTime": "00:00",
        "duration": "1440",
        "visibility": "PRIVATE",
        "participationType": "PERSONS_ONLY",
        "freezeDuration":"0",
        "initialUnfreezeTime": "",
        "unfreezeDay": "",
        "unfreezeTime": "",
        "allowedPractice": "on",
        "allowedVirtual": "on",
        "allowedSelfRegistration": "on",
        "allowedViewForNonRegistered": "on",
        "allowedCommonStatus": "on",
        "viewTestdataPolicy": "NONE",
        "submitViewPolicy": "NONE",
        "languages": "true",
        "useProgramTypeExtraTimeFactors": "on",
        "allowedStatements": "on",
        "allowedStandings": "on",
        "season": "2024-2025",
        "contestType": "Training Contest",
        "icpcRegion": "",
        "country": "Egypt",
        "city": "Damietta",
        "difficulty":"1",
        "websiteUrl":"",
        "englishDescription":"",
        "russianDescription":"",
        "englishRegistrationConfirmation":"",
        "russianRegistrationConfirmation":"",
        "englishLogo": "",
        "russianLogo": "",
        "_tta": "995",
    }

    params = {
        "csrf_token": token,
    }
    
    #Creating Mashup
    result = session.post(f"https://codeforces.com/gym/edit/{mashNum}", data=Payload, params=params) 

    return addToGroup(session, MashID)


def addToGroup(session: Session, MashID):

    global contestName, groupLink

    link = groupLink + ('/add' if groupLink[-1] != '/' else 'add')

    token = getCSRF(session.get(link).content)
    groupCode = link.split('/')[-3]

    destination = f"https://codeforces.com/data/manageGroupContest?groupCode={groupCode}"
    Payload = {
        "action": "addContest",
        "csrf_token": token,
        "contestId": MashID,
        "_tta": "995",
    }

    session.post(link, data=Payload)
    contestLink = f"https://codeforces.com/group/{groupCode}/contest/{MashID}"
    
    return contestLink
