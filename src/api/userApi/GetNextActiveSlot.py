import subprocess, os, time
import re
from flask_restful import Resource, Api, reqparse
from flask import request
import logging, threading
import shutil
import math
import sqlite3
from sqlite3 import Error
from models.model import Merchant
from models.model import Users
from models.model import NormalUser
from models.model import Slot
from sqlalchemy import and_
from sqlalchemy import or_
from datetime import date 
from datetime import timedelta
from datetime import datetime
from utils.Constants import max_total_slots_return
from utils.database import db

class GetNextActiveSlot(Resource):
    def getActiveSlotOfUser(self,normal_user_id):
        """Returns next active slot details of the user
        """
        today_date=date.today()
        now2 = datetime.now()
        hour = now2.hour
        
        active_slots = db.session.query(Slot).filter(and_(Slot.user_id==normal_user_id,Slot.status=="active",Slot.booking_date==today_date,Slot.endTime>int(hour))).order_by(Slot.startime).all()
        if(len(active_slots)==0):
            active_slots =  db.session.query(Slot).filter(and_(Slot.user_id==normal_user_id,Slot.status=="active",Slot.booking_date>today_date)).order_by(Slot.booking_date,Slot.startime).all()
               
        slotInfo={}
        merchantInfo={}
        data={}
        if(len(active_slots)>0):   
             
                slotInfo["bookingDate"]=str(active_slots[0].booking_date.date()) 
                slotInfo["startTime"]=active_slots[0].startime
                slotInfo["endTime"]=active_slots[0].endTime
                slot_user_id=active_slots[0].user_id
                merchant_id=active_slots[0].merchant_id
                merchant=Merchant.query.get(merchant_id)
                merchantInfo["merchantId"]=merchant_id
                merchantInfo["shopName"]=merchant.shopName
                merchantInfo["shopCategory"]=merchant.shopCategory
                merchantInfo["maxPeoplePerSlot"]=merchant.maxPeoplePerSlot
                merchantInfo["lat"]=str(merchant.lat)
                merchantInfo["lng"]=str(merchant.lng)
                data["merchantInfo"]=merchantInfo
                data["slotInfo"]=slotInfo
                
                message="valid"
                return self.response("200","false",message,data)
            
        return self.response("200","true","No Active Slot","")

    def post(self):
        try:
            request_data = request.data
            normal_user_id = request_data["userId"]
            data={}
            return self.getActiveSlotOfUser(normal_user_id)
            
        except Exception as err:
            logging.error(str(err))
            return self.response("200", "false",str(err), {})


    def response(self, responseCode,hasError,message,data):
        response = {}
        response['responseCode'] = responseCode
        response['message'] = message
        response['data'] = data
        response['hasError'] = hasError
        return response

