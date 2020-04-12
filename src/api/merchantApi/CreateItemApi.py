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



class CreateItemApi(Resource):

    def post(self):
        
        try:
            data = request.data
            merchant_id = data["merchant_id"]
            item_value = data["item_value"]
            items=Shop_Item.query.filter_by(item_value=item_value, merchant_id = merchant_id, status = "active")
            itemsInactive=Shop_Item.query.filter_by(item_value=item_value, merchant_id = merchant_id, status = "inactive")
            if(items.count()>0):
                message="Item already exist"
                return self.response("200","true","",message)
            elif itemsInactive.count() > 0:
                item=itemsInactive.first()
                item.status = "active"
                message = 'success'
                db.session.add(item)
                db.session.commit()
                return self.response("200","true","",message)
            item=Shop_Item(merchant_id=merchant_id,item_value=item_value, status = "active")
            db.session.add(item)
            db.session.commit()
            message = "success"
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