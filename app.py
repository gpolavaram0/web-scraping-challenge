import numpy as np

from bs4 import BeautifulSoup
import requests

import pandas as pd
import time
from flask_pymongo import PyMongo

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify, render_template

from pandas.core.common import flatten
from pymongo import MongoClient

import time
import importlib



# myclient = pymongo.MongoClient("mongodb://localhost:27017/")


test_dict = {"key2":"value"}

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

#################################################
# Flask Routes
#################################################

@app.route("/")

def welcome():
    
    col = MongoClient('mongodb://localhost:27017').mars_app.mars
    result = col.find( {} )
    print(result)

    reader_dict = {}

    for doc in result:
        reader_dict.update(doc)
        
    return render_template("index.html", content = reader_dict)


@app.route("/scrape")

def dict_function():
   
   from scrape_mars import scrape
   #mars_data = scrape()
   #mmongo replace.
   
   mars = mongo.db.mars
   mars_data = scrape()
   mars.replace_one({}, mars_data, upsert = True)
   return mars_data 


if __name__ == "__main__":
    app.run(debug=True)
