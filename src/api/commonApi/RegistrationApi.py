import subprocess, os, time
import re
from flask_restful import Resource, Api, reqparse
from flask import request
import logging, threading
import shutil
import math
import sqlite3
from sqlite3 import Error

class RegistrationApi(Resource):


    def post(self):
        try:
            data = request.data

            shopName = db.Column(db.String, nullable=False)
            gstNumber = db.Column(db.String, nullable=False)
            shopCategory = db.Column(db.String, nullable=False)
            avgTime = db.Column(db.String, nullable=False)
            maxPeoplePerSlot = db.Column(db.String, nullable=False)
            # user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
            lat = db.Column(db.String, nullable=False)
            long = db.Column(db.String, nullable=False)


            phone = data['phone_number']
            name = data['shop_name']
            type = data['shop_category']
            gst = data['gst_number']
            lat = data['lat']
            long = data['long']
            max_slots = data['max_slots']

            #Duplicate electricity bill number check
            query = "select * from Merchants where gst_in = '" + gst + "'"
            conn = self.create_connection(database)

            cursor = conn.cursor()
            cursor.execute(query)
            normal_users = cursor.fetchall()
            merchant_id_ToSend = []
            if len(normal_users) > 0:
                return self.response("200", "Duplicate GST IN number", merchant_id_ToSend)

            # Duplicate phone number check
            query = "select * from Merchants where phone_number = '" + phone + "'"
            cursor = conn.cursor()
            cursor.execute(query)
            normal_users = cursor.fetchall()
            if len(normal_users) > 0:
                return self.response("200", "Duplicate phone number", merchant_id_ToSend)

            #Insert user if everything is unique
            insertQuery2 = "Insert into Merchants(name, type, max_slots, gst_in, phone_number, lat, long) " \
                           "values(?,?,?,?,?,?,?)"
            values = (name, type, max_slots, gst, phone, lat, long)
            cursor = conn.cursor()
            cursor.execute(insertQuery2, values)
            conn.commit()
            merchant_id = cursor.lastrowid
            cursor.close()
            conn.close()
            merchant_id_ToSend = {
                "merchant_id": merchant_id
            }
            return self.response("200", "success", merchant_id_ToSend)
        except threading.ThreadError as err:
            logging.error(str(err))
            result = None


    def response(self, responseCode,message,data):
        response = {}
        response['responseCode'] = responseCode
        response['message'] = message
        response['data'] = data
        return response

