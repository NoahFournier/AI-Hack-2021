from flask import Flask, request, jsonify, render_template
from tensorflow import keras
from sklearn.preprocessing import StandardScaler
import pandas as pd
import requests
import json
import numpy as np

app = Flask(__name__)

df = pd.read_csv("../boston_corrected.csv")

input_vars = ["LON", "LAT"]

output_vars = ['DIS', "RM", "TOWNNO", "NOX", 'PTRATIO',
               'TAX', "INDUS", "RAD", "AGE", "LSTAT", 'CMEDV']

scoring_uri = 'http://0ee13a32-fe8d-47f0-b758-f748edfd54f8.uksouth.azurecontainer.io/score'

all_batchsize = [150, 200, 200, 200, 200, 200, 200, 200, 200, 400, 300]
INPUT_SCALER = StandardScaler()
INPUT_SCALER.fit(df[input_vars].values)

input_scalers = {"LAT": INPUT_SCALER}
current_vars = ["LON", "LAT"]
for output in output_vars:
    current_vars.append(output)
    INPUT_SCALER_n = StandardScaler()
    INPUT_SCALER_n.fit(df[current_vars].values)

    input_scalers[output] = INPUT_SCALER_n
    print("Input scaler: ", len(input_scalers),
          " is ", current_vars, " with key: ", output)


def getValsFromLngLat(lon, lat):

    vals = [lon, lat]
    current_scale = ["LAT"] + output_vars
    results = {}
    for i, var in enumerate(output_vars):
        model = keras.models.load_model('../model'+str(i)+'/')
        print('worked')
        scaler = input_scalers[current_scale[i]]
        vals_2 = np.array(vals)

        predict = model.predict(scaler.transform([vals_2]))[0, 0]
        vals.append(predict)
        results[var] = predict
    return results


@app.route('/')
def main():
    return render_template('index.html')


@app.route('/api', methods=['POST'])
def api():

    jsdata = json.loads(request.get_json())
    print(jsdata)

    resp = getValsFromLngLat(jsdata['LON'], jsdata['LAT'])

    data = {
        "TOWNNO": resp["TOWNNO"]*1.,
        "LON": jsdata['LON']*1.,
        "LAT": jsdata['LAT']*1.,
        "DIS": resp["DIS"]*1.,
        "RM": resp["RM"]*1.,
        "NOX": resp["NOX"]*1.,
        "PTRATIO": resp["PTRATIO"]*1.,
        "TAX": resp["TAX"]*1.,
        "INDUS": resp["INDUS"]*1.,
        "RAD": resp["RAD"]*1.,
        "AGE": resp["AGE"]*1.,
        "CMEDV": resp["CMEDV"]*1.,
    }

    #input_data = json.dumps(data)
    #headers = {'Content-Type': 'application/json'}
    #resp = requests.post(scoring_uri, input_data, headers=headers)

    return jsonify(json.dumps(data))


if __name__ == "__main__":
    app.run(debug=True)
