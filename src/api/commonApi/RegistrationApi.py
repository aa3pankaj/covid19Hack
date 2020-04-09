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
from utils.database import db
from api.commonApi.MahaDiscomApi import MahaDiscomApi

class RegistrationApi(Resource):
    def isElectricityBillNumberValid(self,electricity_bill_number,bunit,ctype):
            mahadiscom = MahaDiscomApi(cn=electricity_bill_number, bun=bunit, ct=ctype)
            billdetails = mahadiscom.get_bill_details()
            if len(billdetails)>0:
                return True
            else:
                return False
            #return mahadiscom.is_consumer_valid()

    def registerNormalUser(self,data):
            phone = data['phone_number']
            firstname = data['firstName']
            lastname = data['lastName']
            lat = data['lat']
            lng = data['long']
            password=data['password']
            electricity_bill_number=data['electricity_bill_number']
            #bunit=data['bunit']
            #ctype=data['ctype']

            #validates electricity_bill_number with mahadiscom api
            # if not self.isElectricityBillNumberValid(electricity_bill_number,bunit,ctype):
            #     return self.response("200","true","Invalid electricity_bill_number, Please verify with your bill", "")

            #Duplicate electricity bill number check
            normal_user=NormalUser.query.filter_by(electricity_bill_number=electricity_bill_number)
            merchant_id_ToSend = []
            if normal_user.count() > 0:
                return self.response("200","true","Duplicate electricity_bill_number", merchant_id_ToSend)

            # Duplicate phone number check
            user=Users.query.filter_by(phonenumber=phone)
            if user.count() > 0:
                return self.response("200","true","Duplicate phone number", merchant_id_ToSend)

            #Insert user if everything is unique
            new_user=Users(firstname=firstname,lastname=lastname,phonenumber=phone,passwordhash=password)
            db.session.add(new_user)
            db.session.commit()
            print("new user created")
            print(new_user.id)
            new_normal_user=NormalUser(user_id=new_user.id,electricity_bill_number=electricity_bill_number,lat=lat,lng=lng)
            db.session.add(new_normal_user)
            db.session.commit()
            data={}
            userInfo = {
                "user_id": new_user.id
            }  
            data['userInfo']=userInfo
            return self.response("200","false","success", data)
            print(userInfo)
            
    def registerPoliceUser(self,data):
            phone = data['phone_number']
            firstname = data['firstName']
            lastname = data['lastName']
            password=data['password']

            # Duplicate phone number check
            user=Users.query.filter_by(phonenumber=phone)
            if user.count() > 0:
                return self.response("200","true","Duplicate phone number", "")

            #Insert user if everything is unique
            new_user=Users(firstname=firstname,lastname=lastname,phonenumber=phone,passwordhash=password)
            db.session.add(new_user)
            db.session.commit()
            print("new user created")
            print(new_user.id)
            data={}
            userInfo = {
                "user_id": new_user.id
            }  
            data['userInfo']=userInfo
            return self.response("200","false","success", data)
            print(userInfo)
    def registerMerchant(self,data):
            phone = data['phone_number']
            name = data['shop_name']
            shopType = data['shop_category']
            gst = data['gst_number']
            lat = data['lat']
            lng = data['long']
            max_slots = data['max_slots']
            password=data['password']
            #Duplicate electricity bill number check
            merchant=Merchant.query.filter_by(gstNumber=gst)
            merchant_id_ToSend = []
            if merchant.count() > 0:
                return self.response("200","true","Duplicate GST IN number", merchant_id_ToSend)

            # Duplicate phone number check
            user=Users.query.filter_by(phonenumber=phone)
            if user.count() > 0:
                return self.response("200","true","Duplicate phone number", merchant_id_ToSend)

            #Insert user if everything is unique
            new_user=Users(phonenumber=phone,passwordhash=password)
            db.session.add(new_user)
            db.session.commit()
            print("new user created")
            print(new_user.id)
            new_merchant=Merchant(shopName=name,gstNumber=gst,shopCategory=shopType,avgTime="",maxPeoplePerSlot=max_slots,user_id=new_user.id,lat=lat,lng=lng)
            db.session.add(new_merchant)
            db.session.commit()
            data={}
            merchantInfo = {
                "merchant_id": new_merchant.merchant_id
            }  
            data['merchantInfo']=merchantInfo
            return self.response("200","false","success", data)
            print(merchantInfo)
            

    def post(self):
        try:
            request_data = request.data
            
            if(request_data["userType"]=="merchant"):
                return self.registerMerchant(request_data)
            elif(request_data["userType"]=="normalUser"):
                return self.registerNormalUser(request_data)
            elif(request_data["userType"]=="police"):
                return self.registerPoliceUser(request_data)
                
            #return self.response("200","false","success", data)
        except Exception as err:
            logging.error(str(err))
            return self.response("200","true",str(err), "")


    def response(self, responseCode,hasError,message,data):
        response = {}
        response['responseCode'] = responseCode
        response['message'] = message
        response['data'] = data
        response['hasError']=hasError
        return response

