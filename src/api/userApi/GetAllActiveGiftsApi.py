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
from models.model import User_Gift
from sqlalchemy.sql.expression import func
from sqlalchemy import and_

class GetAllActiveGiftsApi(Resource):

    def post(self):
        request_data = request.data
        normal_user_id = request_data["user_id"]
        try: 
            purchased_gifts = db.session.query(User_Gift.gift_id,func.count(User_Gift.gift_id)).filter(and_(User_Gift.user_id==normal_user_id,User_Gift.status=="active")).group_by(User_Gift.gift_id).all()
            print(purchased_gifts)
            
            giftList=[]
            for purchased_gift in purchased_gifts:
                giftInfo={}
                giftInfo["gift_id"]=purchased_gift[0]
                gift=Merchant_Gift.query.get(purchased_gift[0])
                giftInfo["gift_name"]=gift.gift_name
                giftInfo["amount"]=gift.amount
                giftInfo["count"]=purchased_gift[1]
                giftList.append(giftInfo)
            print(giftList)
            message = "Success"
            return self.response("200","false",giftList,message)
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