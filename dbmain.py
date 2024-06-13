
from db import DBClass
import utilModule

dbInstance = DBClass()

dbInstance.connect()

try:
    query = '''
    SELECT
        SUM(http_response_code = '100') AS '100',
        SUM(http_response_code = '200') AS '200',
        SUM(http_response_code = '400') AS '400',
        COUNT(*) as count
    FROM request_log
    '''

                
    procedure = 'CALL registro.GetHttpResponseCodeSummary()'
    
    
    result, columns =  dbInstance.execute_query(procedure)#dbInstance.execute_query(query)
    results = [{arr[i]: arr[i+1] for i in range(0, len(arr), 2)} for arr in result]
    print(results)
    

except Exception as e:
    print(f"Query Error {e}")    

finally:
    dbInstance.disconnect()        