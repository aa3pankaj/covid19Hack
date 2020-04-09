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

class ReturnSlotInformationApi(Resource):

    def post(self):
        data = request.data
        slot_id = data["slot_id"]
        police_user_id = data["police_user_id"]
       
        try:
            slot = Slot.query.get(slot_id)
            if(slot):   
                slotInfo["booking_date"]=str(slot.booking_date) 
                slotInfo["start_time"]=slot.startTime
                slotInfo["end_time"]=slot.endTime
                slot_user_id=slot.user_id
                merchant_id=slot.merchant_id 
                now = datetime.now()
                if(slot.booking_date<now):
                    slotInfo["status"]="invalid"
                else:
                    slotInfo["status"]="valid"
                    merchant=Merchant.query.get(merchant_id)
                    merchantInfo["merchant_id"]=merchant_id
                    merchantInfo["shop_name"]=merchant.shopName
                    merchantInfo["shop_category"]=merchant.shopCategory
                    merchantInfo["max_people_per_slot"]=merchant.maxPeoplePerSlot
                    merchantInfo["lat"]=merchant.lat
                    merchantInfo["lng"]=merchant.lng
                data={}
                data["merchantInfo"]=merchantInfo
                data["slot_info"]=slotInfo
                message="OK"
                return self.response("200","false",data,message)
        except Exception as err:
            message = err
            return self.response("503","true", {}, message)


    def response(self,responseCode,hasError,data,message):
        response = {}
        response['responseCode'] = responseCode
        response['message'] = message
        response['data'] = data
        response['hasError'] = hasError
        return response