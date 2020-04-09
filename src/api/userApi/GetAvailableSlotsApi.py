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

# from models.ModelHandler import ModelHandler

class GetAvailableSlotsApi(Resource):

    def create_connection(self, db_file):
        """ create a database connection to the SQLite database
            specified by db_file
        :param db_file: database file
        :return: Connection object or None
        """
        conn = None
        try:
            conn = sqlite3.connect(db_file)
            return conn
        except Error as e:
            print(e)

        return conn

    def post(self):
        try:

            database = "/Users/panssing/Downloads/generate_pass_2.0/covid19Hack/src/utils/covid4New.db"
            data = request.data
            merchant_id = data['merchant_id']

            conn = self.create_connection(database)
            #max_slots = self.getMaxSlots(conn, int(merchant_id))
            merchant=Merchant.query.get(merchant_id)
            # max_slots= db.session.query(Merchant.maxPeoplePerSlot).filter(Merchant.merchant_id==int(merchant_id))
            # print(max_slots)
            available_slots = []
            available_slots = self.get_available_slots(conn, int(merchant_id), int(merchant.maxPeoplePerSlot))
            conn.close()
            return self.response("200", "success", available_slots)
        except threading.ThreadError as err:
            logging.error(str(err))
            result = None


    def response(self, responseCode,message,data):
        response = {}
        response['responseCode'] = responseCode
        response['message'] = message
        response['data'] = data
        return response

    def getMaxSlots(self, conn, merchant_id):
        query = "select maxPeoplePerSlot from Merchant where merchant_id = " + str(merchant_id)
        cursor = conn.cursor()
        cursor.execute(query)
        max_slots = cursor.fetchall()
        return max_slots[0][0]

    def get_available_slots(self, conn, merchant_id, max_slots):
        #now = datetime.today().strftime('%Y-%m-%d-%H:%M:%S')
        now2 = datetime.now()
        #now = datetime.today().strftime('%Y-%m-%d-%H:%M:%S')

        hour = now2.hour

        query = "Select startime, COUNT(*) from slot where merchant_id = " + str(merchant_id) + \
                " and booking_date = date('now') and startime > " + str(hour) + " and status = 'active' group by startime having COUNT(*) >= " + str(max_slots)
        print(query)
        total_slots = []
        for i in range(max(8, hour + 1), 16):
            total_slots.append(i)

        cursor = conn.cursor()
        cursor.execute(query)
        starttimes = cursor.fetchall()
        unavailable_slots = []
        for starttime in starttimes:
            unavailable_slots.append(starttime)

        available_slots = np.setdiff1d(total_slots, unavailable_slots)
        available_slots_to_send = []
        if len(available_slots) >= max_available_slots:
            available_slots = available_slots[0:max_available_slots]

            for slot in available_slots:
                available_slots_to_send.append({"date": now2.strftime('%Y-%m-%d'), "starttime": int(slot), "endtime": int(slot) + 1})
            return available_slots_to_send

        for slot in available_slots:
            available_slots_to_send.append(
                {"date": now2.strftime('%Y-%m-%d'), "starttime": int(slot), "endtime": int(slot) + 1})
        #diff = len(available_slots) - max_available_slots

        a = 1

        while a > 0:
            query = "Select startime, COUNT(*) from Slot where merchant_id = " + str(merchant_id) + \
                    " and booking_date = date('now', '" + str(a) +" day')  and status = 'active' group by startime having COUNT(*) >= " + str(max_slots)
            print(query)
            total_slots = []
            for i in range(8, 16):
                total_slots.append(i)
            cursor = conn.cursor()
            cursor.execute(query)
            starttimes = cursor.fetchall()
            unavailable_slots = []
            for starttime in starttimes:
                unavailable_slots.append(starttime)
            available_slots = np.setdiff1d(total_slots, unavailable_slots)
            for slot in available_slots:
                available_slots_to_send.append({"date": (now2 + timedelta(days=a)).strftime('%Y-%m-%d'), "starttime": int(slot), "endtime": int(slot) + 1})
            if len(available_slots_to_send) >= max_available_slots:
                return available_slots_to_send[:max_available_slots]
            a = a + 1









