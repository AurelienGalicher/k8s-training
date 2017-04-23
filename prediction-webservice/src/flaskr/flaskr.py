# -*- coding: utf-8 -*-
"""
    Flaskr
    ~~~~~~

    A microblog example application written as Flask tutorial with
    Flask and sqlite3.

    :copyright: (c) 2015 by Armin Ronacher.
    :license: BSD, see LICENSE for more details.
"""


from pymongo import MongoClient
import gridfs
from flask import Flask, request, session, g, redirect, url_for
from flask import abort,render_template, flash
import json
from bson import json_util
#from bson.json_util import dumps
import pickle
#import sklearn
import pandas as pd

# create our little application :)
app = Flask(__name__)

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE_URL="mongodb://mongo:27017",
    MONGO_REPLICASET="rs0",
    DATABASE_NAME = 'modeldb',
    COLLECTION_NAME = 'models',
    DEBUG=True
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

def connect_db():
    """Connects to the specific database."""
    mongo = MongoClient(app.config['DATABASE_URL'],replicaset=app.config['MONGO_REPLICASET'])
    return mongo

def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'mongo_db'):
        g.mongo_db = connect_db()
    return g.mongo_db

def load_model(model_name, version):
    #filename = "%s_v%s.p" % (model_name, version)
    mongo = get_db()
    fs = gridfs.GridFS(mongo[app.config['DATABASE_NAME']], collection=app.config['COLLECTION_NAME'])
    if fs.exists({'model_name':model_name,'version':version}):
        model = pickle.load(fs.find_one({'model_name':model_name,'version':version}))
        return model
    else:
        return None

def get_model(model_name, version):
    filename = "%s_v%s.p" % (model_name, version)
    if not hasattr(g, 'models'):
        g.models= {}
    model = load_model(model_name, version)
    if filename not in g.models.keys() and model is not None:
        g.models.update({filename:load_model(model_name, version)})
        return g.models[filename]
    else:
        return None

def get_last_version(model_name):
    mongo = get_db()
    files = mongo.modeldb.models.files
    res = mongo[app.config['DATABASE_NAME']][app.config['COLLECTION_NAME']]\
                .files.find({"model_name":model_name}).sort("version",-1).limit(1)
    try:
        version = res.next()['version']
    except:
        version = -1
    return version

@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'mongo_db'):
        g.mongo_db.close()
    #if hasattr(g, 'models'):
    #    for model in g.models.keys():
    #      del(g.models[model])
    #    del(g.models)
## TODO: delete models stored in memory


@app.route("/models")
def get_models():
    mongo = get_db()
    collection = mongo[app.config['DATABASE_NAME']][app.config['COLLECTION_NAME']]
    FIELDS = {}
    #fs = gridfs.GridFS(mongo[app.config['DATABASE_NAME']], collection=app.config['COLLECTION_NAME'])
    models = collection.files.find(FIELDS,limit=1000)
    json_models = []
    for model in models:
        json_models.append(model)
    return json.dumps(json_models, default=json_util.default)

@app.route("/predict/<string:model_name>/<int:version>/",methods=['POST'])
def predict(model_name,version):
      #    g['%s_%s' % (model,version)] = model
    model = get_model(model_name, version)
    if model is None:
        return ("failed to load the model")
    
    data = json.loads(request.form['data'])
    print(data)
    df = pd.DataFrame(data).set_index('timestamp').fillna(0.)
    prediction = model.predict(df)
    res = pd.DataFrame(prediction, index=df.index, columns=['prediction']).reset_index()
    res.columns = ['timestamp','prediction']
    res['version'] = version
    res['model'] = model_name
    res = list(res.T.to_dict().values())
    print(res)
    #app.log(data)
    return json.dumps(res, default=json_util.default)

@app.route("/predict/<string:model_name>/latest/",methods=['POST'])
def predictLatest(model_name):
      #    g['%s_%s' % (model,version)] = model
    version = get_last_version(model_name)
    return predict(model_name,version)
   
      
app.run(host='0.0.0.0', debug=True)
