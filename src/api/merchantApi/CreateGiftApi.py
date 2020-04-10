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


class CreateGiftApi(Resource):

    def post(self):
        request_data = request.data
        merchant_id = request_data["merchant_id"]
        amount = request_data["amount"]
        gift_name = request_data["gift_name"]
    
        try:    
            gifts=Merchant_Gift.query.filter_by(gift_name=gift_name)
            if(gifts.count()>0):
               message="Gift already exist"
               return self.response("200","true","",message)
            gift=Merchant_Gift(merchant_id=merchant_id,gift_name=gift_name,amount=amount)
            db.session.add(gift)
            db.session.commit()
            message = "Success"
            return self.response("200","false",{"gift_id":gift.id,"gift_name":gift.gift_name,"amount":gift.amount},message)
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