from bs4 import BeautifulSoup
import pandas
global cnt
cnt = 0
global trainee
trainee = {
    "TraineeName": ["NAME"],
}

level0 = {
    "TraineeName": ["NAME"],
}

level1 = {
    "TraineeName": ["NAME"],
}

level2 = {
    "TraineeName": ["NAME"],
}

def getDegree(session, group):
    global cnt
    global trainee

    data = session.get(group)
    soup = BeautifulSoup(data.text, 'html.parser')
    table = soup.find_all('tr', class_='highlighted-row')

    rows = []
    for tr in table:
        row = tr['data-contestid']
        rows.append(row)


    current = rows[1]

    standingLink = group[:-1] + f"/{current}/standings"

    data = session.get(standingLink)

    table = BeautifulSoup(data.text, "html.parser")

    rows = []
    for tr in table.find_all('tr'):
        row = [td.text.strip() for td in tr.find_all('td')]
        rows.append(row)



    for row in rows:
        if len(row) > 2 and row[1].split()[0] in trainee:
            name = row[1].split()[0]
            if '*' in name: continue
            correct = 0
            total = 0
            for answer in row[4:]:
                if '+' in answer:
                    correct+=1
                total += 1
            
            if name in trainee and ((cnt == 0 and name in level0) or (cnt == 1 and name in level1) or (cnt == 2 and name in level2)):

                result = round((correct/total) * 20)
                if result: result += 20
                else: result = "00"
                trainee[name].append(f"{result}/40")

    cnt += 1
    if cnt == 1:
        getDegree(session, "GROUP_LINK")
    elif cnt == 2:
        getDegree(session, "GROUP_LINK")
    else:
        printResults()

def printResults():

    filePath = "Task Results.xlsx"
    data = pandas.DataFrame({
        'Name': [],
        'Degree': [],
    })

    for i in trainee.keys():
        if len(trainee[i]) == 1:
            trainee[i].append("00/40")
        
        data.loc[len(data)] = trainee[i]

    data.to_excel(filePath, index=False)



            
