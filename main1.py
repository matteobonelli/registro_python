import utilModule
from datetime import datetime

counter = 0
dateTime = datetime.now().time().strftime("%H-%M-%S_%f.txt")
xvalues = []
yvalues = []

while counter < 5:
    try:
        searchTerm = utilModule.getPrompt()
        response = utilModule.chuckHttpGetJokeWithSearch(searchTerm)
        jokesResponse = response.json()
        if response.status_code == 200 and jokesResponse['total'] > 0:
            utilModule.addSearchCountToFile(dateTime, searchTerm, jokesResponse["total"])
            counter += 1
    except Exception as e:
        print(f"An exception occured: {e}")
