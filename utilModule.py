import requests
import configparser
import re
from datetime import datetime
import matplotlib.pyplot as plt
from unhautorizedException import UnhautorizedException


config = configparser.ConfigParser()
config.read('config.ini')
chuckUrl = config['http']['chuck_url']

def fun1():
    return "a"

def fun2():
    return "c"

def chuckHttpGetJoke():
    return requests.get(chuckUrl, headers={
    'Content-Type' : 'application/json'
    })

def chuckHttpGetJokeWithSearch(search):
    return requests.get("{}{}".format(config['http']['search_url'], search) , headers={
    'Content-Type' : 'application/json'
    })

def addJokesToFile(jokes):
    with open(f'{datetime.now().time().strftime("%H-%M-%S_%f.txt")}', 'a') as file:
        for j in jokes:
            file.write("{}{}{}\n".format(j.title(), '###', len(j.strip())))

def addJokeToFile(joke):
    with open(config['file']['name'], 'a') as file:
        count = 0
        for w in enumerate(joke):
            count += 1
        file.write(joke.title() + '###' + str(count) + '\n')

def addSearchCountToFile(filename, searchTerm, count):
    with open(f'Ciao_{filename}.txt', 'a') as file:
        file.write("{}:{}\n".format(searchTerm, count))

def containsSpecialChars(string):
    pattern = r'[^\w\s]'
    match = re.search(pattern, string)
    return bool(match)

def getPrompt():
    search = input("{}\n".format(config['prompt']['text'])).strip()
    if(search in config['prompt']['bad_words']) or containsSpecialChars(search):
        raise Exception("You are a nasty guy!") 
    return search

def mapJokesResulst(jokesResponse):
    jokesList = []
    if not jokesResponse["total"]:
        raise Exception("No results found...")
    for res in enumerate(jokesResponse["result"]):
        jokesList.append(res[1]["value"]) 
    return jokesList

def ensure_keys_are_valid(data):
    if isinstance(data, list):
        return [ensure_keys_are_valid(item) for item in data]
    elif isinstance(data, dict):
        # Convert keys to str, if they are not already str, int, float, bool, or None
        return {str(key) if not isinstance(key, (str, int, float, bool, type(None))) else key: ensure_keys_are_valid(value) for key, value in data.items()}
    else:
        return data

def check_api_key(request):
    if 'X-API-Key' not in request.headers or request.headers['X-API-Key'] != config['http']['API_KEY']:
        raise UnhautorizedException("Unauthorized")

def generateGraphic(xValues, yValues):  
    plt.bar(xValues, yValues)
    # Step 4: Customize the chart (optional)
    plt.title('Sample Bar Chart')
    plt.xlabel('Categories')
    plt.ylabel('Values')

    # Step 5: Display the chart
    plt.show()