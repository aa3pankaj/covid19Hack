import subprocess, os, time
import re
from flask_restful import Resource, Api, reqparse
from flask import request
import logging, threading
import shutil
import math
import sqlite3
from sqlite3 import Error
from utils.Constants import radius
import datetime
import numpy as np
from utils.Constants import max_available_slots
from datetime import timedelta
from datetime import datetime
from utils.database import db
from models.model import Merchant
from models.model import Slot
from sqlalchemy.sql.expression import func
from sqlalchemy import and_
from sqlalchemy import or_
from datetime import date 

# from models.ModelHandler import ModelHandler

class GetAvailableSlotsApi(Resource):

    # def create_connection(self, db_file):
    #     """ create a database connection to the SQLite database
    #         specified by db_file
    #     :param db_file: database file
    #     :return: Connection object or None
    #     """
    #     conn = None
    #     try:
    #         conn = sqlite3.connect(db_file)
    #         return conn
    #     except Error as e:
    #         print(e)

    #     return conn

    def post(self):
        try:

            #database = "/Users/panssing/Downloads/generate_pass_2.0/covid19Hack/src/utils/covid4New.db"
            data = request.data
            merchant_id = data['merchantId']
            user_id= data['userId']
            #conn = self.create_connection(database)
            #max_slots = self.getMaxSlots(conn, int(merchant_id))
            merchant=Merchant.query.get(merchant_id)
            # max_slots= db.session.query(Merchant.maxPeoplePerSlot).filter(Merchant.merchant_id==int(merchant_id))
            # print(max_slots)
            available_slots = []
            available_slots = self.get_available_slots(int(merchant_id), int(merchant.maxPeoplePerSlot),int(user_id))
            #conn.close()
            return self.response("200","false", "success", available_slots)
        except Exception as err:
            logging.error(str(err))
            return self.response("200","true",str(err), "")


    def response(self, responseCode,hasError,message,data):
        response = {}
        response['responseCode'] = responseCode
        response['hasError'] = hasError
        response['message'] = message
        response['data'] = data
        return response

    # def getMaxSlots(self, conn, merchant_id):
    #     query = "select maxPeoplePerSlot from Merchant where merchant_id = " + str(merchant_id)
    #     cursor = conn.cursor()
    #     cursor.execute(query)
    #     max_slots = cursor.fetchall()
    #     return max_slots[0][0]

    def get_available_slots(self, merchant_id, max_slots,user_id):
        now2 = datetime.now()
        hour = now2.hour
        today_date=datetime.today().strftime('%Y-%m-%d')
        query1=db.session.query(Slot.startime).filter(and_(Slot.merchant_id==int(merchant_id),Slot.booking_date==today_date,Slot.startime>int(hour),Slot.status=="active")).group_by(Slot.startime).having(or_(func.count(Slot.slot_id)>=int(max_slots)))
        query2=db.session.query(Slot.startime).filter(and_(Slot.booking_date==today_date,Slot.user_id==user_id))
        query= query1.union(query2)
        # query = "Select startime, COUNT(*) from slot where merchant_id = " + str(merchant_id) + \
        #         " and booking_date = date('now') and startime > " + str(hour) + " and status = 'active' group by startime having COUNT(*) >= " + str(max_slots)
        total_slots = []
        for i in range(max(8, hour + 1), 23):
            total_slots.append(i)
        unavailable_slots = []
        for row in query:
            unavailable_slots.append(row.startime)
        available_slots = np.setdiff1d(total_slots, unavailable_slots)
        available_slots_to_send = []
        if len(available_slots) >= max_available_slots:
            available_slots = available_slots[0:max_available_slots]

            for slot in available_slots:
                available_slots_to_send.append({"date": now2.strftime('%Y-%m-%d'), "startTime": int(slot), "endTime": int(slot) + 1})
            return available_slots_to_send

        for slot in available_slots:
            available_slots_to_send.append(
                {"date": now2.strftime('%Y-%m-%d'), "startTime": int(slot), "endTime": int(slot) + 1})
        diff = len(available_slots) - max_available_slots

        a = 1

        while a > 0:
            today_date=date.today()
            print(type(today_date))
            querySql=db.session.query(Slot.startime).filter(and_(Slot.user_id!=user_id, Slot.merchant_id==int(merchant_id),Slot.booking_date==today_date+timedelta(days=a),Slot.status=="active")).group_by(Slot.startime).having(or_(func.count(Slot.slot_id)>=int(max_slots)))
            query2=db.session.query(Slot.startime).filter(and_(Slot.booking_date==today_date+timedelta(days=a),Slot.user_id==user_id))
            query1= querySql.union(query2)

            # query = "Select startime, COUNT(*) from Slot where merchant_id = " + str(merchant_id) + \
            #         " and booking_date = date('now', '" + str(a) +" day')  and status = 'active' group by startime having COUNT(*) >= " + str(max_slots)
            
            total_slots = []
            for i in range(8, 23):
                total_slots.append(i)
            unavailable_slots = []

            for row in query1:
                unavailable_slots.append(row.startime)

            available_slots = np.setdiff1d(total_slots, unavailable_slots)
            for slot in available_slots:
                available_slots_to_send.append({"date": (now2 + timedelta(days=a)).strftime('%Y-%m-%d'), "startTime": int(slot), "endTime": int(slot) + 1})
            if len(available_slots_to_send) >= max_available_slots:
                return available_slots_to_send[:max_available_slots]
            a = a + 1









