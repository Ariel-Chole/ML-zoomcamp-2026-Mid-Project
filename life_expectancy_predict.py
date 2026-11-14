# Load the model
import pickle
import xgboost as xgb
from flask import Flask
from flask import request
from flask import jsonify

output_file= "life-expectancy-model.bin"

app = Flask("life_expectancy")

with open (output_file,"rb") as f_in:
    pipeline = pickle.load(f_in)

#sparsing the pipeline
model = pipeline["model"]
dv = pipeline["dv"]

@app.route('/life_expectancy', methods = ['POST'])
def predict():
    data = request.get_json()
    data_train = dv.transform([data])
    ddata = xgb.DMatrix(data_train,feature_names=list(dv.get_feature_names_out()))
    predictions = model.predict(ddata)
    result = {
        "Predicted Life_expectancy": float(predictions[0])
    }
    return jsonify(result)
@app.route('/health',methods=["GET"])
def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    app.run(debug=True, host="localhost", port = 9696)