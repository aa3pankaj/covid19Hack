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
        user_id = data["user_id"]
        merchant_id = data["merchant_id"]
        try:
            secretKey = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(16))
            slot = Slot(user_id = user_id,merchant_id = merchant_id,startTime=start_time,endTime=end_time,status="active",qrCode=secretKey)
            db.session.add(slot)
            db.session.commit()
            data = {"qr_code":secretKey}
            message = "ok"
            return self.response("200",data,message)
        except threading.ThreadError as err:
            message = "Error in booking slot"
            return self.response("503", {}, message)


    def response(self, responseCode,data,message):
        response = {}
        response['responseCode'] = responseCode
        response['message'] = message
        response['data'] = data
        return response