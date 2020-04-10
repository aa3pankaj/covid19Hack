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
from models.model import Merchant_Gift

class DeleteGiftApi(Resource):

    def post(self):
        data = request.data
        merchant_id = data["merchant_id"]
        gift_name = data["gift_name"]
        try: 
            gift=Merchant_Gift.query.filter_by(gift_name=gift_name).first()
            if gift:
               db.session.delete(gift)
            db.session.commit()
            message = "Success"
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