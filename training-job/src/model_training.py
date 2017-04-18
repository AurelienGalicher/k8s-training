# -*- coding: utf-8 -*-
import pickle
from pymongo import MongoClient
import gridfs
import pandas as pd
from sklearn.linear_model import RidgeCV
import sys
import datetime 

mongo = MongoClient("mongodb://mongo:27017",replicaset="rs0")
fs = gridfs.GridFS(mongo.modeldb, collection="models")
ts = mongo.mldb.ts

def register_model(sk_model, model_name="", version=0, description="",score=None ):
    pickle.dump(sk_model,open('save.p','wb'))
    fs.put(open('save.p','rb'),filename='%s_v%s.p' %(model_name,version),model_name=model_name,version=version, description=description, score=score)
    return

def retrieve_training_dataset(ts, start, end):
    data = [doc for doc in ts.find( {'time': {'$lt': end, '$gte': start}})]
    df = pd.DataFrame(data).drop('_id', axis=1).drop('time', axis=1).set_index('timestamp')
    return df

def train_model(df):
    y = df.target
    X = df.drop('target',axis=1).fillna(0)
    model = RidgeCV().fit(X,y)
    score = model.score(X,y)
    return model, score

def get_last_version(model_name):
    pipeline =[{"$match":{"metadata.modelname": model_name}}
              ,{"$group":
                    {"model_name" : "$metadata.model_name",
                     "lastVersion": { "$max": {"$metadata.version" } } }
               }]
    files = mongo.mldb.models.files
    res = files.aggregate(pipeline) 
    try:
        version = res[0]['lastVersion']
    except:
        version = -1
    return version

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: model_traing.py <period in min> <model_name> <version>", file=sys.stderr)
        sys.exit(-1)

    period, model_name, version = sys.argv[1:]
    period= int(period)
    if version == 'latest':
        version = max(0, get_last_version(model_name))
    else:
        version = int(version)
    end = datetime.datetime.now()
    start = end - datetime.timedelta(minutes=period)
    df = retrieve_training_dataset(ts, start, end).dropna()
    # restricting the schema
    cols = list(filter(lambda x: x.startswith('feat_') or x.startswith('target'),df.columns))
    #feat_cols.append('target')
    model, score = train_model(df[cols])
    print ("r^2 score: %s" % score)
    register_model(model, model_name=model_name, version=version, score=score, description="ridgeCV %s" % end.isoformat())

    
