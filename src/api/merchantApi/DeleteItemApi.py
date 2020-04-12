import subprocess, os, time
import re
from flask_restful import Resource, Api, reqparse
from flask import request
import logging, threading
import shutil
from models.model import Slot
from utils.database import db
import json
import copy
from sqlalchemy import or_
import random,string
import calendar;
import time;
from datetime import datetime,timedelta
from sqlalchemy import and_
from models.model import Shop_Item

class DeleteItemApi(Resource):

    def post(self):
        try: 
            data = request.data
            item_id = data["id"]
            item=Shop_Item.query.filter_by(id=item_id, status = "active").first()
            if item:
                item.status = "inactive"
                message = "success"
                db.session.add(item)
                db.session.commit()
            else:
                message = "No such item found."    
            return self.response("200","false","",message)
        except Exception as err:
            message = str(err)
            return self.response("503", "true",{}, message)


    def response(self, responseCode,hasError,data,message):
        response = {}
        response['responseCode'] = responseCode
        response['message'] = message
        response['hasError'] = hasError
        response['data'] = data
        return response