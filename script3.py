import subprocess
import sqlalchemy as db
import pandas as pd
import numpy as np 
import h5py as h5

conn = db.create_engine('postgresql://mariam:1234@localhost/data_management')
conn.table_names()

Diabtes_batch = """
SELECT pregnancies,glucose,bloodpressure ,skinthickness ,insulin ,bmi,diabetespedigreefunction ,age
FROM Public."diabetes_unscored"
EXCEPT  
SELECT pregnancies,glucose,bloodpressure ,skinthickness ,insulin ,bmi,diabetespedigreefunction ,age
FROM Public."diabetes_scored";
"""
Batch = pd.read_sql(Diabtes_batch, con=conn)
Batch

import json
from keras.models import model_from_json
import pandas as pd
json_file = open('model.json', 'r')
model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(model_json)

loaded_model.load_weights("model.h5")

predictionData = pd.DataFrame(Batch)
predictionData = predictionData.iloc[:, :].values
Array = np.array(predictionData)

prediction = loaded_model.predict(Array)

prediction_list = []
for i in prediction:
    if i> 0.5:
        i=1
    else:
        i =0
    prediction_list.append(i)
Batch['outcome']=prediction_list

Batch.to_sql(name = 'diabetes_scored',                           
                con=conn,                                           
                schema = 'public',index = False ,                                 
                if_exists='append') 