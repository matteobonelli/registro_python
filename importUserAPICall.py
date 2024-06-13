import pandas
import base64

data = pandas.read_csv("./importUsers.csv")
csv_string = data.to_csv(index=False)

csv_bytes = csv_string.encode('utf-8')
base64_bytes = base64.b64encode(csv_bytes)
base64_string = base64_bytes.decode('utf-8')

print(base64_string)