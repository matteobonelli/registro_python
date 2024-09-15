import requests
import configparser
import re
from datetime import datetime
import matplotlib.pyplot as plt
from unhautorizedException import UnhautorizedException
import logging
from logging.handlers import TimedRotatingFileHandler
import os


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

def get_current_date():
    now = datetime.now()
    return now.strftime('%Y-%m-%d')

def getLogger():
    try:
        # Define the log directory
        log_directory = 'C:\\Users\\bonel\\Desktop\\logs'
        os.makedirs(log_directory, exist_ok=True)

        # Define log files with today's date
        app_log_file = os.path.join(log_directory, f'{get_current_date()}_app_python.log')

        # Create a logger for general application logs
        app_logger = logging.getLogger('app_logger')
        app_logger.setLevel(logging.INFO)

        # Create a handler for writing application log files with daily rotation
        app_handler = TimedRotatingFileHandler(app_log_file, when='midnight', interval=1, backupCount=30)
        app_handler.suffix = "%Y-%m-%d"  # Log file name will have date suffix

        # Create a formatter and set it to the handler
        formatter = logging.Formatter('%(asctime)s.%(msecs)03d %(levelname)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        app_handler.setFormatter(formatter)

        # Add the handler to the logger
        app_logger.addHandler(app_handler)

        return app_logger
    except Exception as e:
        logError(str(e))

def logError(message):
    # Define the log directory
    log_directory = 'C:\\Users\\bonel\\Desktop\\logs'
    os.makedirs(log_directory, exist_ok=True)

    # Define the error log file with today's date
    error_log_file = os.path.join(log_directory, f'error_python_{get_current_date()}.log')

    # Create a logger for error logs
    error_logger = logging.getLogger('error_logger')
    error_logger.setLevel(logging.ERROR)

    # Create a handler for writing error log files with daily rotation
    error_handler = TimedRotatingFileHandler(error_log_file, when='midnight', interval=1, backupCount=30)
    error_handler.suffix = "%Y-%m-%d"  # Log file name will have date suffix

    # Create a formatter and set it to the handler
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    error_handler.setFormatter(formatter)

    # Add the handler to the logger
    error_logger.addHandler(error_handler)

    # Log the error message
    error_logger.error(message)
