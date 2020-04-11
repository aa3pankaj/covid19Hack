import subprocess, os, time
import re
from flask_restful import Resource, Api, reqparse
from flask import request
import logging, threading
import shutil
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

class GetAllGifts(Resource):

    def post(self):
        data = request.data
        merchant_id = data["merchant_id"]

        try:
            
            gifts=Merchant_Gift.query.filter_by(merchant_id=merchant_id).all()
            data={}
            giftsToSend = []
            for gift in gifts:
                giftDict = {}
                giftDict["amount"] = gift.amount
                giftDict["gift_name"] = gift.gift_name
                giftDict["id"] = gift.id
                giftsToSend.append(giftDict)
            data['gifts']=giftsToSend
            message = "Success"
            return self.response("200","false",data,message)
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