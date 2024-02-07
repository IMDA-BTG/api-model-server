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

# simple way to get our model
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
model = load_model("model/regression_mock_donation_sklearn.linear_model._base.LinearRegression.sav")

def predict_result(df):
  
  prediction = model.predict(df)
  return int(prediction[0])

def get_single_row(request_dict):
  age = request_dict["age"]
  gender = request_dict["gender"]
  race = request_dict["race"]
  income = request_dict["income"]
  employment = request_dict["employment"]
  employment_length = request_dict["employment_length"]
  total_donated = request_dict["total_donated"]
  num_donation = request_dict["num_donation"]
  df = pandas.DataFrame([[age, gender, race, income, employment, employment_length, total_donated, num_donation]])
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
  if 'race' not in keys:
    return False
  if 'income' not in keys:
    return False
  if 'employment' not in keys:
    return False
  if 'employment_length' not in keys:
    return False
  if 'total_donated' not in keys:
    return False
  if 'num_donation' not in keys:
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
    if 'race' not in keys:
      continue
    if 'income' not in keys:
      continue
    if 'employment' not in keys:
      continue
    if 'employment_length' not in keys:
      continue
    if 'total_donated' not in keys:
      continue
    if 'num_donation' not in keys:
      continue
    age = row["age"]
    gender = row["gender"]
    race = row["race"]
    income = row["income"]
    employment = row["employment"]
    employment_length = row["employment_length"]
    total_donated = row["total_donated"]
    num_donation = row["num_donation"]
    a = [age, gender, race, income, employment, employment_length, total_donated, num_donation]
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
  # print(payload)
  return predict_array(data)

def get_array_json(request):
  payload = request.get_json()
  results = []
  for row in payload:
    df = get_single_row(row)
    result = predict_result(df)
    results.append(result)
  return results

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
  if 'race' not in keys:
    return False
  if 'income' not in keys:
    return False
  if 'employment' not in keys:
    return False
  if 'employment_length' not in keys:
    return False
  if 'total_donated' not in keys:
    return False
  if 'num_donation' not in keys:
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
  # response = make_response(jsonify({'data': result}), 200)
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
  # response = make_response(jsonify({'data': result}), 200)
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
  # response = make_response(jsonify({'data': result}), 200)
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

@app.route('/predict/tc006/<gender>/<race>/<age>/<income>/<employment>/<employment_length>/<total_donated>/<num_donation>', methods=["GET"])
def predict_tc006(gender, race, age, income, employment, employment_length, total_donated, num_donation):  
  log_request(request)
  df = pandas.DataFrame([[age, gender, race, income, employment, employment_length, total_donated, num_donation]])
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
  # response = make_response(jsonify({'data': result}), 200)
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
  # # response = make_response(jsonify({'data': result}), 200)
  response = Response(str(result), status=200, mimetype='text/plain')
  return log_and_return_response(response)

@app.route('/predict/tc011', methods=["GET"])
def predict_tc011():  
  log_request(request)
  # retVal = validate_headers(request, [
  #   { "param":"Content-Type", "value":"application/x-www-form-urlencoded", "msg":"Invalid Content-Type", "status":400 },
  # ])
  # if retVal is not None:
  #   return log_and_return_response(retVal)
  result = get_array_parameter_query(request)
  # response = make_response(jsonify({'data': result}), 200)
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
  # # response = make_response(jsonify({'data': result}), 200)
  response = Response(str(result), status=200, mimetype='text/plain')
  return log_and_return_response(response)

@app.route('/predict/tc013', methods=["POST"])
def predict_tc013():  
  log_request(request)
  retVal = validate_headers(request, [
    { "param":"Content-Type", "value":"application/json", "msg":"Invalid Content-Type", "status":400 },
  ])
  if retVal is not None:
    return log_and_return_response(retVal)
  results = get_array_json(request)
  # # response = make_response(jsonify({'data': result}), 200)
  # response = Response(str(result), status=200, mimetype='text/plain')
  response = make_response(jsonify(results), 200)
  return log_and_return_response(response)

@app.route('/predict/tc014', methods=["POST"])
def predict_tc014():  
  log_request(request)
  retVal = validate_headers(request, [
    { "param":"Content-Type", "value":"application/json", "msg":"Invalid Content-Type", "status":400 },
  ])
  if retVal is not None:
    return log_and_return_response(retVal)
  results = get_array_json(request)
  results = list(map(lambda row: { "data": row }, results))
  response = make_response(jsonify(results), 200)
  return log_and_return_response(response)

@app.route('/predict/tc015', methods=["POST"])
def predict_tc015():  
  log_request(request)
  retVal = validate_headers(request, [
    { "param":"Content-Type", "value":"application/json", "msg":"Invalid Content-Type", "status":400 },
  ])
  if retVal is not None:
    return log_and_return_response(retVal)
  results = get_array_json(request)
  results = {
    "data": results
  }
  response = make_response(jsonify(results), 200)
  return log_and_return_response(response)

@app.route('/predict/tc016', methods=["POST"])
def predict_tc016():  
  log_request(request)
  retVal = validate_headers(request, [
    { "param":"Content-Type", "value":"application/json", "msg":"Invalid Content-Type", "status":500 },
  ])
  if retVal is not None:
    return log_and_return_response(retVal)
  results = get_array_json(request)
  results = {
    "data": results
  }
  response = make_response(jsonify(results), 200)
  return log_and_return_response(response)

@app.route('/predict/tc017', methods=["POST"])
def predict_tc017():  
  log_request(request)
  retVal = validate_headers(request, [
    { "param":"Content-Type", "value":"application/json", "msg":"Invalid Content-Type", "status":502 },
  ])
  if retVal is not None:
    return log_and_return_response(retVal)
  results = get_array_json(request)
  results = {
    "data": results
  }
  response = make_response(jsonify(results), 200)
  return log_and_return_response(response)

@app.route('/predict/tc018', methods=["POST"])
def predict_tc018():  
  log_request(request)
  retVal = validate_headers(request, [
    { "param":"Content-Type", "value":"application/json", "msg":"Invalid Content-Type", "status":503 },
  ])
  if retVal is not None:
    return log_and_return_response(retVal)
  results = get_array_json(request)
  results = {
    "data": results
  }
  response = make_response(jsonify(results), 200)
  return log_and_return_response(response)

@app.route('/predict/tc019', methods=["POST"])
def predict_tc019():  
  log_request(request)
  retVal = validate_headers(request, [
    { "param":"Content-Type", "value":"application/json", "msg":"Invalid Content-Type", "status":504},
  ])
  if retVal is not None:
    return log_and_return_response(retVal)
  results = get_array_json(request)
  results = {
    "data": results
  }
  response = make_response(jsonify(results), 200)
  return log_and_return_response(response)

@app.route('/predict/tc020', methods=["POST"])
def predict_tc020():  
  log_request(request)
  retVal = validate_headers(request, [
    { "param":"Content-Type", "value":"application/json", "msg":"Invalid Content-Type", "status":429 },
  ])
  if retVal is not None:
    return log_and_return_response(retVal)
  results = get_array_json(request)
  results = {
    "data": results
  }
  response = make_response(jsonify(results), 200)
  return log_and_return_response(response)

# def get_single_batched_request(request):
#   age =  request.form.getlist('age')
#   gender =  request.form.getlist('gender')
#   race =  request.form.getlist('race')
#   income =  request.form.getlist('income')
#   employment =  request.form.getlist('employment')
#   employment_length =  request.form.getlist('employment_length')
#   total_donated =  request.form.getlist('total_donated')
#   num_donation =  request.form.getlist('num_donation')
#   hr_lst  = list(zip(age, gender, race, income, employment, employment_length, total_donated, num_donation))
#   df = pandas.DataFrame(hr_lst)
#   return df

# def predict_batched_result(df):
#   prediction_list = model.predict(df)
#   print("--------------------------------------")
#   final_prediction_list = []
#   for prediction in prediction_list:
#     final_prediction_list.append(int(prediction[0]))
#   return final_prediction_list

# def get_single_batched_request(request):
#   age =  request.form.getlist('age')
#   gender =  request.form.getlist('gender')
#   race =  request.form.getlist('race')
#   income =  request.form.getlist('income')
#   employment =  request.form.getlist('employment')
#   employment_length =  request.form.getlist('employment_length')
#   total_donated =  request.form.getlist('total_donated')
#   num_donation =  request.form.getlist('num_donation')
#   hr_lst  = list(zip(age, gender, race, income, employment, employment_length, total_donated, num_donation))
#   df = pandas.DataFrame(hr_lst)
#   return df

# def predict_batched_result(df):
#   prediction_list = model.predict(df)
#   print("--------------------------------------")
#   final_prediction_list = []
#   for prediction in prediction_list:
#     final_prediction_list.append(int(prediction[0]))
#   return final_prediction_list


# @app.route('/predict/tc013', methods=["POST"])
# def predict_tc013():  
#   request_data = request.form
#   print("age:", request_data.getlist('age'))
#   print("gender:", request_data.getlist('gender'))
#   print("race:", request_data.getlist('race'))
#   print("income:", request_data.getlist('income'))
#   print("employment:", request_data.getlist('employment'))
#   print("employment_length:", request_data.getlist('employment_length'))
#   print("total_donated:", request_data.getlist('total_donated'))
#   print("num_donation:", request_data.getlist('num_donation'))
#   if not validate_multipart_form_data_header(request):
#     return log_and_return_response(Response("Invalid Content-Type", 400))
#   if not validate_form_input(request):
#     return log_and_return_response(Response("Invalid or missing form data", 400))
#   df = get_single_batched_request(request)

#   result = predict_batched_result(df)
#   # jsonify_result = jsonify({"test": result})
#   ast_result = repr(result)
#   response = Response(ast_result, status=200, mimetype='text/plain')
#   # response = Response(json.dumps(result), status=200, mimetype='text/plain')
#   return log_and_return_response(response)


# def get_single_batched_request(request):
#   age =  request.form.getlist('age')
#   gender =  request.form.getlist('gender')
#   race =  request.form.getlist('race')
#   income =  request.form.getlist('income')
#   employment =  request.form.getlist('employment')
#   employment_length =  request.form.getlist('employment_length')
#   total_donated =  request.form.getlist('total_donated')
#   num_donation =  request.form.getlist('num_donation')
#   hr_lst  = list(zip(age, gender, race, income, employment, employment_length, total_donated, num_donation))
#   df = pandas.DataFrame(hr_lst)
#   return df

# def predict_batched_result(list_of_dict):
#     prediction_results_list = []
#     df = pandas.DataFrame.from_dict(list_of_dict)
#     prediction_results = model.predict(df)
#     for prediction_result in prediction_results:
#       prediction_results_list.append(int(prediction_result[0]))
#     return prediction_results_list

# @app.route('/predict/tc013', methods=["POST"])
# def predict_tc013():  
#   request_json = request.json
#   print("request_json:", request_json)
#   result = predict_batched_result(request_json)
#   jsonified_results = pandas.Series(result).to_json(orient='values')
#   response = make_response(jsonify({'data': jsonified_results}), 200)
#   return log_and_return_response(response)