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

class GetProfileInfoApi(Resource):
    def getAllActiveSlotOfUser(self,normal_user):
        """Returns next 5 days active slots of the user
        """
        today_date=date.today()
        now2 = datetime.now()
        hour = now2.hour
        active_slots = db.session.query(Slot.slot_id).filter(and_(Slot.user_id==normal_user.normal_user_id,Slot.status=="active",Slot.booking_date==today_date,Slot.endTime>int(hour))).all()
        a=1
        slotInfo=[]
        for slot in active_slots:
            slotInfo.append(int(slot[0]))
       
        while a > 0:
                active_slots_other = db.session.query(Slot.slot_id).filter(and_(Slot.user_id==normal_user.normal_user_id,Slot.status=="active",Slot.booking_date==today_date+timedelta(days=a))).all()
                for slot in active_slots_other:
                    slotInfo.append(int(slot[0]))
                if a == max_total_slots_return-1:
                    return slotInfo
                a = a + 1

        return slotInfo

    def getNormalUserProfile(self,normal_user_id):
       
        normal_user = NormalUser.query.get(normal_user_id)
        user = Users.query.get(normal_user.user_id)
        activeSlots = self.getAllActiveSlotOfUser(normal_user)
        normalUserInfo={}
        normalUserInfo["user_id"]=normal_user_id
        normalUserInfo["phoneNumber"]=user.phonenumber
        normalUserInfo["firstName"]=user.firstname
        normalUserInfo["lastName"]=user.lastname
        normalUserInfo["electricity_bill_number"]=normal_user.electricity_bill_number
        normalUserInfo["lat"]=str(normal_user.lat)
        normalUserInfo["lng"]=str(normal_user.lng)
        normalUserInfo["activeSlots"] = activeSlots
        return normalUserInfo

    def getMerchantUserProfile(self,merchant_id):
        merchant=Merchant.query.get(merchant_id)
        user_id=merchant.user_id
        user=Users.query.get(user_id)
        merchantInfo={}
        merchantInfo["merchant_id"]=merchant_id
        merchantInfo["phoneNumber"]=user.phonenumber
        merchantInfo["shopName"]=merchant.shopName
        merchantInfo["gstNumber"]=merchant.gstNumber
        merchantInfo["shopCategory"]=merchant.shopCategory
        merchantInfo["maxPeoplePerSlot"]=merchant.maxPeoplePerSlot
        merchantInfo["lat"]=str(merchant.lat)
        merchantInfo["lng"]=str(merchant.lng)
        return merchantInfo

    def getGeneralProfileInfo(self,user_id):
        user=Users.query.get(user_id)
        userInfo={}
        userInfo["user_id"]=user_id
        userInfo["phoneNumber"]=user.phonenumber
        userInfo["firstName"]=user.firstname
        userInfo["lastName"]=user.lastname
        return userInfo

    def post(self):
        try:
            request_data = request.data
            data={}
            if(request_data["userType"]=="merchant"):
                data =self.getMerchantUserProfile(request_data["merchant_id"])
            elif(request_data["userType"]=="normalUser"):
                data =self.getNormalUserProfile(request_data["normal_user_id"])
            elif(request_data["userType"]=="police"):
                data =self.getGeneralProfileInfo(request_data["police_user_id"])
            return self.response("200", "false","success", data)
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

