from flask import Flask, jsonify, request
from db import DBClass
import utilModule
from unhautorizedException import UnhautorizedException
import requests
import time

app = Flask(__name__)

dbInstance = DBClass()

dbInstance.connect()

query = '''
    SELECT
        SUM(http_response_code = '100') AS '100',
        SUM(http_response_code = '200') AS '200',
        SUM(http_response_code = '400') AS '400',
        COUNT(*) as count
    FROM request_log
    '''

procedure = 'CALL registro.GetHttpResponseCodeSummary()'
    
result, column =  dbInstance.execute_query(procedure)

results = [dict(zip(column, row)) for row in result]

print(results)

data = [
    {'id' : 1, 'name' : 'Pippetto', 'surname' : 'Pippettoz'},
    {'id' : 2, 'name' : 'Item 2', 'value' : 200}
]

@app.route('/')
def index():
    return 'Pippetto is alive'

@app.route('/propagateJWT', methods=['GET'])
def propagateJWT():
    response = {
        'message': 'OK'
    }
    return jsonify(response), 200

@app.route('/data', methods=['GET'])
def get_data():
    try:
        utilModule.check_api_key(request)
        return jsonify(data)
    except UnhautorizedException as e:
        return jsonify({'error': str(e)}), 401
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/results', methods=['GET'])
def get_results():
    try:
        utilModule.check_api_key(request)
        return jsonify(results)
    except UnhautorizedException as e:
        return jsonify({'error': str(e)}), 401
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

@app.route('/log', methods=['GET'])
def get_log():
    time.sleep(5)
    try:
        url = "http://127.0.0.1:3000/log"
        params = {
            "mario" : "Marietto",
            "200" : "Ok"
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
                print(response.json())
        else:
            print("Error:", response.text)
        
        return jsonify(response.json())

    except UnhautorizedException as e:
        return jsonify({'error': str(e)}), 401
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, port=8361)
