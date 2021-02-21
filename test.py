import requests
import json

scoring_uri = 'http://bbf0d4a5-957f-4281-9332-e356a8298cfc.uksouth.azurecontainer.io/score'

data = {
    "data": [
        {
            "TOWN": "example_value",
            "LON": -70.95,
            "LAT": 42.2875,
            "TOWNNO": 0,
            "TRACT": 0,
            "MEDV": 0,
            "CRIM": 0,
            "ZN": 0,
            "INDUS": 0,
            "CHAS": 0,
            "NOX": 0,
            "RM": 0,
            "AGE": 0,
            "DIS": 0,
            "RAD": 0,
            "TAX": 0,
            "PTRATIO": 0,
            "B": 0,
            "LSTAT": 0
        }
    ]
}

input_data = json.dumps(data)

headers = {'Content-Type': 'application/json'}

resp = requests.post(scoring_uri, input_data, headers=headers)
print(resp.text)
