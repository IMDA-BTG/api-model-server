# sample-model-server

## Install the Requirement

Suggest to run this in a virtual environment then install the requirements.

```pip install -r requirements.txt```

## To Run a Prediction via a Web Browser

1. Fire up a terminal in this directory and run this command

    ```export FLASK_APP=app.py && flask run```
1.1 To run in https
    ```export FLASK_APP=app.py && flask run --cert=cert.pem --key=key.pem```

2. Then navigate to `localhost:5000/predict`

3. Upload the data file in `./data` (Suggest to try `pickle_scikit_lr_compas_xtest_pkl.sav`)

4. Wait for results

## To Start an API Server to Test Run Models With Inputs From an Algorithm
1. cd to api-model-server directory and run:
   
   ```source venv/bin/activate```
2. To run a regression model server, run:
 
   ```bash regression_run_http.sh``` to start a HTTP server on port 5000
   
   and 

   ```bash regression_run_https.sh``` to start a HTTPS server on port 5000

3. To run a classification model server, run:
 
   ```bash classification_run_http.sh```  to start a HTTP server on port 5001
   
   and 

   ```bash classification_run_https.sh``` to start a HTTPS server on port 5001
## To Run a Prediction via API

1. Fire up a terminal in this directory and run this command

    ```flask app```

2. Run this curl command (replace the file path accordingly)

    ```curl -X POST -F file=@"./data/pickle_scikit_lr_compas_xtest_pkl.sav" http://localhost:5000/predict```

3. Or run this curl command (replace the value accordingly)
   
   This will return 0
    ```curl -X POST http://localhost:5000/predict_one -H "Content-Type: application/x-www-form-urlencoded" -d "count=0&gender=0&race=5&charge=1&age=2"```

    This will return 1
    ```curl -X POST http://localhost:5000/predict_one -H "Content-Type: application/x-www-form-urlencoded" -d "count=10&gender=1&race=5&charge=1&age=2"```

4. Or run this curl command (replace the value accordingly) for mulitple dataset

    ```curl -X POST http://localhost:5000/predict_all -H 'Content-Type: application/json' -d '{"input": "[[0, 1, 0, 0, 0], [0, 1, 0, 0, 0], [0, 1, 3, 11, 1], [0, 1, 2, 0, 0], [0, 1, 5, 2, 0], [1, 0, 0, 1, 0], [0, 1, 5, 0, 0], [0, 1, 0, 1, 1], [0, 1, 0, 9, 0], [1, 1, 0, 1, 0]]"}'```

# Others

1. Note that this is not the only way to write a model server

   - The response might differ from server to server.
   - The way to upload the input data could differ too.

