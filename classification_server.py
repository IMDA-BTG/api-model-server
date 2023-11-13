from flask import Flask
from flask import jsonify
from flask import request
from flask import Response
from flask import make_response
import pandas
import json
import pprint
import base64
import os

import pickle

pp = pprint.PrettyPrinter(width=120, compact=True)

app = Flask(__name__)
UPLOAD_FOLDER = os.path.join(os.getcwd(), "uploaded_data")
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def load_model(location):
  """This model assumes that the data is unprocessed yet"""
  model = pickle.load(open(location, "rb"))
  print("[+]\t Model loaded")
  return model
  

# load this once, if not very slow
model = load_model("model/sample_bc_credit_sklearn_linear.LogisticRegression.sav")

def predict_result(df):
  prediction = model.predict(df)
  return int(prediction[0])

def get_single_row(request_dict):
  age = request_dict["age"]
  gender = request_dict["gender"]
  income = request_dict["income"]
  race = request_dict["race"]
  home_ownership = request_dict["home_ownership"]
  prior_count = request_dict["prior_count"]
  loan_amount = request_dict["loan_amount"]
  loan_interests = request_dict["loan_interests"]
  df = pandas.DataFrame([[age, gender, income, race, home_ownership, prior_count, loan_amount, loan_interests]])
  return df

def validate_input(input):
  try:
    input = int(input)
  except:
    print("except")
    return False

  return input

@app.route("/")
def index():
  return "Hello World"

#
# Test cases
#
def log_request(request):
  print("\n[+]\t Request received.")
  print("==========================================================================================================================================")  
  print("request:", request)
  print("------------------------------------------------------------------------------------------------------------------------------------------")
  print("request_url", request.url)
  print("------------------------------------------------------------------------------------------------------------------------------------------")
  print("request_headers", request.headers)
  print("------------------------------------------------------------------------------------------------------------------------------------------")
  print("request_form", request.form)
  print("------------------------------------------------------------------------------------------------------------------------------------------")
  print("request_data", request.data)
  print("==========================================================================================================================================\n")

def log_and_return_response(response):
  print("[+]\t Response.")
  print("response_status:", response.status)
  print("response_headers:", response.headers)
  print("response_data:", response.get_data())
  return response;

BEARER_TOKEN = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjYyMmY4MTJiNmJlM2IzMjEyMTQzMjBjZiIsImlhdCI6MTY2MDE5Nzg3MCwiZXhwIjoxNjYyNzg5ODcwfQ.cebsoHVMzV4GGwX-QjHFc5CcTkEy7jLQQLaaHlvN2JU"
BASIC_TOKEN = "Basic " + base64.b64encode(b'test:p@ssword').decode("utf-8") 

def validate_headers(request, ar):
  for item in ar:
    value = request.headers.get(item["param"])
    if value is None:
      return Response(item["msg"], item["status"], mimetype='text/plain')
    if value != item["value"]:
      return Response(item["msg"], item["status"], mimetype='text/plain')
  return None

def validate_multipart_form_data_header(request):
  value = request.headers.get("Content-Type")
  if value is None:
    return False
  print("value of multipart form:", value)
  return value.startswith("multipart/form-data; boundary=")

def validate_form_input(request):
  
  keys = request.form.keys();
  if 'age' not in keys:
    return False
  if 'gender' not in keys:
    return False
  if 'income' not in keys:
    return False
  if 'race' not in keys:
    return False
  if 'home_ownership' not in keys:
    return False
  if 'prior_count' not in keys:
    return False
  if 'loan_amount' not in keys:
    return False
  if 'loan_interests' not in keys:
    return False
  return True

def predict_array(data):
  ar = []
  for row in data:
    keys = row.keys();
    if 'age' not in keys:
      continue
    if 'gender' not in keys:
      continue
    if 'income' not in keys:
      continue
    if 'race' not in keys:
      continue
    if 'home_ownership' not in keys:
      continue
    if 'prior_count' not in keys:
      continue
    if 'loan_amount' not in keys:
      continue
    if 'loan_interests' not in keys:
      continue
    age = row["age"]
    gender = row["gender"]
    income = row["race"]
    race = row["race"]
    home_ownership = row["home_ownership"]
    prior_count = row["prior_count"]
    loan_amount = row["loan_amount"]
    loan_interests = row["loan_interests"]
    a = [age, gender, income, race, home_ownership, prior_count, loan_amount, loan_interests]
    ar.append(a)
  df = pandas.DataFrame(ar)
  p = predict_result(df)
  return p

def get_array_form_input(request):
  keys = request.form.keys();
  if 'data' not in keys:
    return False
  payload = request.form["data"]
  data = json.loads("["+payload+"]")
  return predict_array(data)

def get_array_parameter_query(request):
  keys = request.args.keys();
  if 'data' not in keys:
    return False
  payload = request.args["data"].replace('\\n','').replace('\\r','')
  data1 = json.loads(payload)
  if isinstance(data1,list):
    data = []
    for row in data1:
      data.append(json.loads(row))
    return predict_array(data)
  else:
    return predict_array([data1])

def get_array_parameter_path(pathdata):
  payload = pathdata.replace('\\n','').replace('\\r','')
  data1 = json.loads(payload)
  if isinstance(data1,list):
    data = []
    for row in data1:
      data.append(json.loads(row))
    return predict_array(data)
  else:
    return predict_array([data1])

def validate_request_parameters(request):
  keys = request.args.keys()
  if 'age' not in keys:
    return False
  if 'gender' not in keys:
    return False
  if 'income' not in keys:
    return False
  if 'race' not in keys:
    return False
  if 'home_ownership' not in keys:
    return False
  if 'prior_count' not in keys:
    return False
  if 'loan_amount' not in keys:
    return False
  if 'loan_interests' not in keys:
    return False
  return True

@app.route('/predict/tc001', methods=["POST"])
def predict_tc001():  
  log_request(request)
  retVal = validate_headers(request, [
    { "param":"Content-Type", "value":"application/x-www-form-urlencoded", "msg":"Invalid Content-Type", "status":400 },
    { "param":"Authorization", "value":BEARER_TOKEN, "msg":"Unauthorized", "status":401 },
  ])
  if retVal is not None:
    return log_and_return_response(retVal)
  if not validate_form_input(request):
    return log_and_return_response(Response("Invalid or missing form data", 400))
  df = get_single_row(request.form)
  result = predict_result(df)
  response = Response(str(result), status=200, mimetype='text/plain')
  return log_and_return_response(response)

@app.route('/predict/tc002', methods=["POST"])
def predict_tc002():  
  log_request(request)
  retVal = validate_headers(request, [
    { "param":"Content-Type", "value":"application/x-www-form-urlencoded", "msg":"Invalid Content-Type", "status":400 },
    { "param":"Authorization", "value":BASIC_TOKEN, "msg":"Unauthorized", "status":401 },
  ])
  if retVal is not None:
    return log_and_return_response(retVal)
  if not validate_form_input(request):
    return log_and_return_response(Response("Invalid or missing form data", 400))
  df = get_single_row(request.form)
  result = predict_result(df)
  response = Response(str(result), status=200, mimetype='text/plain')
  return log_and_return_response(response)

@app.route('/predict/tc003', methods=["POST"])
def predict_tc003():  
  log_request(request)
  retVal = validate_headers(request, [
    { "param":"Content-Type", "value":"application/x-www-form-urlencoded", "msg":"Invalid Content-Type", "status":400 },
  ])
  if retVal is not None:
    return log_and_return_response(retVal)
  if not validate_form_input(request):
    return log_and_return_response(Response("Invalid or missing form data", 400))
  df = get_single_row(request.form)
  result = predict_result(df)
  response = Response(str(result), status=200, mimetype='text/plain')
  return log_and_return_response(response)

@app.route('/predict/tc004', methods=["POST"])
def predict_tc004():  
  log_request(request)
  if not validate_multipart_form_data_header(request):
    return log_and_return_response(Response("Invalid Content-Type", 400))
  if not validate_form_input(request):
    return log_and_return_response(Response("Invalid or missing form data", 400))
  df = get_single_row(request.form)
  result = predict_result(df)
  response = Response(str(result), status=200, mimetype='text/plain')
  return log_and_return_response(response)

@app.route('/predict/tc005', methods=["GET"])
def predict_tc005():  
  log_request(request)
  if not validate_request_parameters(request):
    return log_and_return_response(Response("Invalid or missing parameters", 405))
  df = get_single_row(request.args)
  result = predict_result(df)
  response = Response(str(result), status=200, mimetype='text/plain')
  return log_and_return_response(response)

@app.route('/predict/tc006/<age>/<gender>/<income>/<race>/<home_ownership>/<prior_count>/<loan_amount>/<loan_interests>', methods=["GET"])
def predict_tc006(age, gender, income, race, home_ownership, prior_count, loan_amount, loan_interests):  
  log_request(request)
  df = pandas.DataFrame([[age, gender, race, income, home_ownership, prior_count, loan_amount, loan_interests]])
  result = predict_result(df)
  response = make_response(jsonify({'data': result}), 200)
  response = Response(str(result), status=200, mimetype='text/plain')
  return log_and_return_response(response)

@app.route('/predict/tc007', methods=["POST"])
def predict_tc007():  
  log_request(request)
  retVal = validate_headers(request, [
    { "param":"Content-Type", "value":"application/x-www-form-urlencoded", "msg":"Invalid Content-Type", "status":400 },
  ])
  if retVal is not None:
    return log_and_return_response(retVal)
  if not validate_form_input(request):
    return log_and_return_response(Response("Invalid or missing form data", 400))
  df = get_single_row(request.form)
  result = predict_result(df)
  response = make_response(jsonify({'data': result}), 200)
  return log_and_return_response(response)

@app.route('/predict/tc008', methods=["POST"])
def predict_tc008():  
  log_request(request)
  retVal = validate_headers(request, [
    { "param":"Content-Type", "value":"application/x-www-form-urlencoded", "msg":"Invalid Content-Type", "status":400 },
    { "param":"foo", "value":"bar", "msg":None, "status":418 },
  ])
  if retVal is not None:
    return log_and_return_response(retVal)
  if not validate_form_input(request):
    return log_and_return_response(Response("Invalid or missing form data", 400))
  df = get_single_row(request.form)
  result = predict_result(df)
  response = Response(str(result), status=200, mimetype='text/plain')
  return log_and_return_response(response)

@app.route('/predict/tc009', methods=["POST"])
def predict_tc009():  
  log_request(request)
  if not validate_form_input(request):
    return log_and_return_response(Response("Invalid or missing form data", 400))
  df = get_single_row(request.form)
  result = predict_result(df)
  response = Response(str(result), status=200, mimetype='text/plain')
  return log_and_return_response(response)

@app.route('/predict/tc010', methods=["POST"])
def predict_tc010():  
  log_request(request)
  retVal = validate_headers(request, [
    { "param":"Content-Type", "value":"application/x-www-form-urlencoded", "msg":"Invalid Content-Type", "status":400 },
  ])
  if retVal is not None:
    return log_and_return_response(retVal)
  result = get_array_form_input(request)
  response = Response(str(result), status=200, mimetype='text/plain')
  return log_and_return_response(response)

@app.route('/predict/tc011', methods=["GET"])
def predict_tc011():  
  log_request(request)
  retVal = validate_headers(request, [
    { "param":"Content-Type", "value":"application/x-www-form-urlencoded", "msg":"Invalid Content-Type", "status":400 },
  ])
  if retVal is not None:
    return log_and_return_response(retVal)
  result = get_array_parameter_query(request)
  response = Response(str(result), status=200, mimetype='text/plain')
  return log_and_return_response(response)

@app.route('/predict/tc012/<data>', methods=["GET"])
def predict_tc012(data):  
  log_request(request)
  retVal = validate_headers(request, [
    { "param":"Content-Type", "value":"application/x-www-form-urlencoded", "msg":"Invalid Content-Type", "status":400 },
  ])
  if retVal is not None:
    return log_and_return_response(retVal)
  result = get_array_parameter_path(data)
  response = Response(str(result), status=200, mimetype='text/plain')
  return log_and_return_response(response)


def get_single_batched_request(request):
  age =  request.form.getlist('age')
  gender =  request.form.getlist('gender')
  income =  request.form.getlist('income')
  race =  request.form.getlist('race')
  home_ownership =  request.form.getlist('home_ownership')
  prior_count =  request.form.getlist('prior_count')
  loan_amount =  request.form.getlist('loan_amount')
  loan_interests =  request.form.getlist('loan_interests')
  hr_lst  = list(zip(age, gender, income, race, home_ownership, prior_count, loan_amount, loan_interests))
  df = pandas.DataFrame(hr_lst)
  return df

def predict_batched_result(list_of_dict):
    df = pandas.DataFrame.from_dict(list_of_dict)
    prediction_results = model.predict(df)
    return prediction_results



@app.route('/predict/tc013', methods=["POST"])
def predict_tc013():  
  request_json = request.json
  print("request_json:", request_json)
  result = predict_batched_result(request_json)
  print("results from prediction:", result, type(result))
  jsonified_results = pandas.Series(result).to_json(orient='values')
  print("results from prediction(jsonified)", jsonified_results, type(result))
  response = make_response(jsonify({'data': jsonified_results}), 200)
  return log_and_return_response(response)



def predict_proba_batched_result(list_of_dict):
    df = pandas.DataFrame.from_dict(list_of_dict)
    prediction_results = model.predict_proba(df)

    print("prediction_results_batched", prediction_results)
    return prediction_results


@app.route('/predict/tc014', methods=["POST"])
def predict_tc014():  
  request_json = request.json
  print("request_json:", request_json)
  result = predict_batched_result(request_json)
  jsonified_results = pandas.Series(result).to_json(orient='values')
  print("RESULTZ:", jsonified_results, type(result))
  response = make_response(jsonify({'data': jsonified_results}), 200)
  return log_and_return_response(response)

