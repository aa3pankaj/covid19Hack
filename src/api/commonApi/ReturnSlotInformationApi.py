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
from datetime import datetime,date,timedelta
from sqlalchemy import and_
from models.model import Merchant

class ReturnSlotInformationApi(Resource):

    def post(self):
        request_data = request.data
        slot_id = request_data["slotId"]
       
        try:
            slot = Slot.query.get(slot_id)
            slotInfo={}
            if(slot):   
               
                slotInfo["bookingDate"]=str(slot.booking_date.date()) 
                slotInfo["startTime"]=slot.startime
                slotInfo["endTime"]=slot.endTime
               
                slot_user_id=slot.user_id
                merchant_id=slot.merchant_id 
                #check for qr not valid for this merchant
                if "merchantId" in request_data:
                    if merchant_id!=int(request_data["merchantId"]):
                        return self.response("200","true","","invalid for this merchant")

                hourNow=datetime.now().hour
                now = datetime.now().date()
                #timestamp = datetime.now()
               
                merchantInfo={}
                if "merchantId" in request_data:
                    if(slot.booking_date.date()<now):
                        return self.response("200","true","","invalid")
                    elif slot.booking_date.date()==now:
                        if slot.endTime < hourNow:
                            return self.response("200","true","","invalid")
            
                merchant=Merchant.query.get(merchant_id)
                merchantInfo["merchantId"]=merchant_id
                merchantInfo["shopName"]=merchant.shopName
                merchantInfo["shopCategory"]=merchant.shopCategory
                merchantInfo["maxPeoplePerSlot"]=merchant.maxPeoplePerSlot
                merchantInfo["lat"]=str(merchant.lat)
                merchantInfo["lng"]=str(merchant.lng)
                  
                data={}
                
                data["merchantInfo"]=merchantInfo
                data["slotInfo"]=slotInfo
                message="valid"
                return self.response("200","false",data,message)
            else:
                return self.response("200","true","","invalid")
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