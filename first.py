import utilModule
import sys

jokesResultList = []
try:
    response = utilModule.chuckHttpGetJokeWithSearch(utilModule.getPrompt())
    jokesResponse = response.json()
    if response.status_code == 200:
        jokesResultList = utilModule.mapJokesResulst(jokesResponse)
        utilModule.addJokesToFile(jokesResultList)

    elif response.status_code == 400:
        print(f"{jokesResponse['error']} : {jokesResponse['message']}")
    else:
        print(f"Error : {response.status_code}")
except Exception as e:
    print(f"An exception occured: {e}")


'''
response = utilModule.chuckHttpGetJoke()

if response.status_code == 200:
    joke = response.json()
    utilModule.addJokeToFile(joke['value'])
else:
    print("Error")

'''
