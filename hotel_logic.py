import pandas as pd
import time 
from openpyxl import load_workbook


account_sid = "YOUR_SID_HERE"
auth_token = "YOUR_TOKEN_HERE"
twilio_number = "+19027018815"
my_phone_number = "+17826410444"

ct = time.time()
currTime = time.ctime(ct)
# roomSchedule = pd.ExcelFile('pages/room_schedule.xlsx')
# df = roomSchedule.parse('roomNum')
# rl = roomSchedule.parse('roomList')
# wb = load_workbook('pages/room_schedule.xlsx')
# ws = wb['roomList']

def schedule_rn(file):
    roomSchedule = pd.ExcelFile(file)
    rn = roomSchedule.parse('roomNum')
    return rn

def schedule_rl(file):
    roomSchedule = pd.ExcelFile(file)
    rl = roomSchedule.parse('roomList')
    return rl

def schedule_ws(file):
    wb = load_workbook(file)
    ws = wb['roomList']
    return ws

def hello():
    return "Hello, this is Alex's summer project"

def sentSuccess(text):
    return f"sentSuccess: {text}"




