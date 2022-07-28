import subprocess, os, time
import re
from flask_restful import Resource, Api, reqparse
from flask import request
import logging, threading
from utils.database import db
from models.model import Users
from models.model import Roles
from models.model import User_Roles
from models.model import Merchant
from models.model import NormalUser

class Authenticate(Resource):

    def post(self):
        data = request.data
        phoneNumber = data["phoneNumber"]
        password = data["password"]

        try:
            user = db.session.query(Users).filter(Users.phonenumber == phoneNumber).filter(Users.passwordhash == password).all()
            if len(user) > 0:
                userId = user[0].id
                response_user_id=userId
                role = db.session.query(User_Roles).filter(User_Roles.user_id == userId).all()
                if(len(role)) > 0:
                    roleName = db.session.query(Roles).filter(Roles.id== role[0].role_id).all()
                   
                    message = "success"
                    role = roleName[0].roleType
                    if role=='merchant':
                        merchant=db.session.query(Merchant.merchant_id).filter(Merchant.user_id==userId ).all()
                        response_user_id= merchant[0].merchant_id
                    elif role=='normalUser':
                        normalUser=db.session.query(NormalUser.normal_user_id).filter(NormalUser.user_id==userId).all()
                        response_user_id=normalUser[0].normal_user_id
                    elif role=='police':
                        response_user_id=userId
                    else:
                        return self.response("501","true","", "invalid role")
                        
                    data={"userId":response_user_id,"role":role}
                    return self.response("200","false",message, data)
            message = "Invalid User"
            return self.response("501", "true",message, "")
        except Exception as err:
            message = str(err)
            return self.response("500","true", message,"")


    def response(self, responseCode,hasError,message, data):
        response = {}
        response['responseCode'] = responseCode
        response['message'] = message
        response['hasError'] = hasError
        response['data'] = data
        return response
