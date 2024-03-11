from requests import Session
from bs4 import BeautifulSoup
from makeTask import makeTask

#intiate a session authenticating with codeforces

session = Session()
auth = session.get(f"https://codeforces.com/enter").content

soup = BeautifulSoup(auth, 'html.parser')
form_data = {}

for field in ['csrf_token' ]:

    field_value = soup.find('input', {'name': field}).get('value', '')
    form_data[field] = field_value
        
headers = {
    'X-Csrf-Token': form_data['csrf_token']
}

login_data = {
    'csrf_token': form_data['csrf_token'],
    'action': 'enter',
    'handleOrEmail': "YOUR_USERNAME",
    'password': "YOUR_PASSWORD",
    'remember': 'on',
    '_tta': '135'
}


result = session.post('https://codeforces.com/enter', data=login_data,headers=headers)

Level0 = makeTask(session, "Level0DB", 3, "GROUP_LINK", "Loops and Functions - Task 5")
Level1 = makeTask(session, "Level1DB", 2, "GROUP_LINK", "Number Theory - Task 4")
Level2 = makeTask(session, "Level2DB", 1, "GROUP_LINK", "Backtracking - Task 5")

print(f"LEVEL 0 ---------> {Level0}")
print(f"LEVEL 1 ---------> {Level1}")
print(f"LEVEL 2 ---------> {Level2}")



