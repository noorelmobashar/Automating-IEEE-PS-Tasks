from requests import Session
from bs4 import BeautifulSoup
from getDegrees import getDegree


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


Level0 = getDegree(session, "GROUP_LINK")

