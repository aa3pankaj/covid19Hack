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
            slot = db.session.query(Slot).filter(Slot.slot_id==slot_id).all()
            
            print("in")
            for s in slot:
              print(slot.slot_id)
              print("out")
            # print(slot.count())
            #print(str(slot[0].slot_id))
            print("------------0")
            # if(slot.count>0):   
            #     print("________1")
               
            #     slotInfo["booking_date"]=slot[0].booking_date
                
            #     slotInfo["start_time"]=slot[0].startTime
            #     slotInfo["end_time"]=slot[0].endTime
            #     #current_count

            #     slot_user_id=slot.user_id
            #     merchant_id=slot.merchant_id
            #     print("________2")
            #     now = datetime.now()
            #     print("________2")
            #     if(slotInfo["booking_date"]<now):
            #         print("________3")
            #         slotInfo["status"]="invalid"
            #     else:
            #         print("________4")
            #         slotInfo["status"]="valid"
            #         merchant=Merchant.query.filter(merchant_id=merchant_id)
            #         merchantInfo["merchant_id"]=merchant_id
            #         merchantInfo["shop_name"]=merchant[0].shopName
            #         merchantInfo["shop_category"]=merchant[0].shopCategory
            #         merchantInfo["max_people_per_slot"]=merchant[0].maxPeoplePerSlot
            #         merchantInfo["lat"]=merchant[0].lat
            #         merchantInfo["lng"]=merchant[0].long
            #     print(merchantInfo)
            #     data["merchant_details"]=merchantInfo
            #     data["slot_info"]=slotInfo
            #     print(data)
            data=""
            
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