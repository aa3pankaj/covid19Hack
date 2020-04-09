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


class BookSlotApi(Resource):

    def post(self):
        data = request.data
        start_time = data["start_time"]
        end_time = data["end_time"]
        booking_date= data["booking_date"]
        user_id = data["user_id"]
        merchant_id = data["merchant_id"]
        try:
            
            datetime_object = datetime.strptime(booking_date, "%Y-%m-%d")
            #secretKey = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(16))
            slot = Slot(user_id = user_id,merchant_id = merchant_id,startime=int(start_time),endTime=int(end_time),booking_date=datetime_object,status="active",qrCode="weff")
            db.session.add(slot)
            db.session.commit()

            data = {"slot_id":slot.slot_id}
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