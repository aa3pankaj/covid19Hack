import subprocess, os, time
import re
from flask_restful import Resource, Api, reqparse
from flask import request
import logging, threading
from utils.database import db
from models.model import Users
from models.model import Roles
from models.model import User_Roles

class Authenticate(Resource):

    def post(self):
        data = request.data
        phoneNumber = data["phonenumber"]
        password = data["password"]

        try:
            user = db.session.query(Users).filter(Users.phonenumber == phoneNumber).filter(Users.passwordhash == password).all()
            if len(user) > 0:
                userId = user[0].id
                role = db.session.query(User_Roles).filter(User_Roles.user_id == userId).all()
                if(len(role)) > 0:
                    roleName = db.session.query(Roles).filter(Roles.id== role[0].role_id).all()
                    message = "ok"
                    role = roleName[0].roleType
                    return self.response("200",message, role)
            message = "Invalid User"
            role = "Not applicable"
            return self.response("501", message, role)
        except threading.ThreadError as err:
            message = str(err)
            return self.response("500", message)


    def response(self, responseCode,message, role):
        response = {}
        response['responseCode'] = responseCode
        response['message'] = message
        response['role'] = role
        return response
