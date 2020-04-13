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
from models.model import User_Roles
from models.model import Roles

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
            phone = data['phoneNumber']
            firstname = data['firstName']
            lastname = data['lastName']
            lat = data['lat']
            lng = data['lng']
            password=data['password']
            electricity_bill_number=data['electricityBillNumber']
            #bunit=data['bunit']
            #ctype=data['ctype']

            #validates electricity_bill_number with mahadiscom api
            # if not self.isElectricityBillNumberValid(electricity_bill_number,bunit,ctype):
            #     return self.response("200","true","Invalid electricity_bill_number, Please verify with your bill", "")

            #Duplicate electricity bill number check
            normal_user=NormalUser.query.filter_by(electricity_bill_number=electricity_bill_number)
            merchant_id_ToSend = []

            #-----------------------
            # role=Roles(roleType='merchant')
            # role2=Roles(roleType='normalUser')
            # role3=Roles(roleType='police')
            # db.session.add(role)

            # db.session.commit()
            # db.session.add(role2)

            # db.session.commit()
            # db.session.add(role3)

            # db.session.commit()
            #-----------------------
            #Test comment




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
            user_role1=User_Roles(user_id=new_user.id,role_id=2)
            db.session.add(user_role1)
            db.session.commit()

            print("new user created")
            print(new_user.id)
            new_normal_user=NormalUser(user_id=new_user.id,electricity_bill_number=electricity_bill_number,lat=lat,lng=lng)
            db.session.add(new_normal_user)
            db.session.commit()
            data={}
            # userInfo = {
            #     "userId": new_normal_user.normal_user_id
            # }  
            #data['userInfo']=userInfo
            data= {"userId":new_normal_user.normal_user_id}
            return self.response("200","false","success", data)
            print(userInfo)
            
    def registerPoliceUser(self,data):
            phone = data['phoneNumber']
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

            user_role1=User_Roles(user_id=new_user.id,role_id=3)
            db.session.add(user_role1)
            db.session.commit()

            print("new user created")
            print(new_user.id)
            data={}
            # userInfo = {
            #     "userId": new_user.id
            # }  
            #data['userInfo']=userInfo
            data= {"userId":new_user.id}
            return self.response("200","false","success", data)
            print(userInfo)
    def registerMerchant(self,data):
            phone = data['phoneNumber']
            name = data['shopName']
            shopType = data['shopCategory']
            gst = data['gstNumber']
            lat = data['lat']
            lng = data['lng']
            max_slots = data['maxSlots']
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


            user_role1=User_Roles(user_id=new_user.id,role_id=1)
            db.session.add(user_role1)
            db.session.commit()

            print("new user created")
            print(new_user.id)
            new_merchant=Merchant(shopName=name,gstNumber=gst,shopCategory=shopType,avgTime="",maxPeoplePerSlot=max_slots,user_id=new_user.id,lat=lat,lng=lng)
            db.session.add(new_merchant)
            db.session.commit()
            data={}
            # merchantInfo = {
            #     "merchantId": new_merchant.merchant_id
            # }  
            #data['merchantInfo']=merchantInfo
            data= {"userId":new_merchant.merchant_id}
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

