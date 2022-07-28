import subprocess, os, time
import re
from flask_restful import Resource, Api, reqparse
from flask import request
import logging, threading
import shutil
from models.model import Slot
from models.model import Merchant
from utils.database import db
import json
import copy
from sqlalchemy import or_
from utils.database import db
import calendar;
import time;
from datetime import datetime, timedelta
from sqlalchemy import and_
from datetime import datetime, timedelta
from sqlalchemy.sql.expression import func


class GetNextSlot(Resource):

    def post(self):
        data = request.data
        user_id = data["user_id"]
        merchant_id = data["shop_id"]
        try:
            # Merchant.query.delete()
            # Slot.query.delete()
            # shope = Merchant(user_id = 2324,merchant_id = merchant_id,lattitute="32434",longitude="663643",shopName="test",maxPeoplePerSlot=3)
            # db.session.add(shope)
            # slot1 = Slot(user_id = 1,current_count=1,merchant_id = 1,startTime="2020-04-05 21:11:32.658670",endTime="2020-04-05 22:11:32.658670",status="active",qrCode="qrCode4")
            # slot2 = Slot(user_id = 2,current_count=2,merchant_id = 1,startTime="2020-04-05 21:11:32.658670",endTime="2020-04-05 22:11:32.658670",status="active",qrCode="qrCode4")
            # db.session.add(slot1)
            # db.session.add(slot2)
            # db.session.commit()

            maxSlotID = db.session.query(func.max(Slot.slot_id)).filter(Slot.merchant_id == merchant_id)
            lastSlot = Slot.query.filter_by(slot_id=maxSlotID).all()
            print("lastSlot: %s"%lastSlot)
            shop = Merchant.query.filter_by(merchant_id=merchant_id)
            out = []
            print("Executing...!")
            startTimeStr = lastSlot[0].startTime
            endTimeStr = lastSlot[0].endTime
            startTime = time.strptime(lastSlot[0].startTime, '%Y-%m-%d %H:%M:%S.%f')
            endTime = time.strptime(lastSlot[0].endTime, '%Y-%m-%d %H:%M:%S.%f')
            print(startTime)
            print(endTime)
            if (lastSlot[0].current_count < shop[0].maxPeoplePerSlot):
                out.append({startTime, endTime})
                slot = Slot(user_id=user_id, merchant_id=merchant_id, current_count=lastSlot[0].current_count + 1,
                            startTime=startTime, endTime=endTime, status="active", qrCode="null")
                db.session.add(slot)
            else:
                out.append({startTime + timedelta(hours=1), endTime + timedelta(hours=1)})
                slot = Slot(user_id=user_id, merchant_id=merchant_id, current_count=1,
                            startTime=startTime + timedelta(hours=1), endTime=endTime + timedelta(hours=1),
                            status="active", qrCode="null")
                db.session.add(slot)

            db.session.commit()
            data = out
            message = "true"
            return self.response("200", data, message)
        except threading.ThreadError as err:
            logging.error(str(err))
            result = None

    def response(self, responseCode, data, message):
        response = {}
        response['responseCode'] = responseCode
        response['message'] = message
        response['data'] = data
        return response