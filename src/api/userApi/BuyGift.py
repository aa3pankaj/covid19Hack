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
from models.model import User_Gift

class BuyGift(Resource):

    def post(self):
        data = request.data
        gift_id = data["gift_id"]
        normal_user_id = data["normal_user_id"]
        try:
            
            # datetime_object = datetime.strptime(booking_date, "%Y-%m-%d")
            #secretKey = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(16))
            # gift = User_Gift(user_id = normal_user_id,merchant_id = merchant_id,startime=int(start_time),endTime=int(end_time),booking_date=datetime_object,status="active",qrCode="weff")
            gift = User_Gift(gift_id = gift_id,booking_date=datetime.now(), normal_user_id = normal_user_id)
            
            db.session.add(gift)
            db.session.commit()

            data = {"user_gift_id":gift.id}
            message = "ok"
            return self.response("200","false",data,message)
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