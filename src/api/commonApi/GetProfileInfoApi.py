import subprocess, os, time
import re
from flask_restful import Resource, Api, reqparse
from flask import request
import logging, threading
import shutil
import math
import sqlite3
from sqlite3 import Error

class GetProfileInfoApi(Resource):
    
    def post(self):
        try:
            data = request.data
            
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

