import pandas as pd
from openpyxl import load_workbook

account_sid = "YOUR_SID_HERE"
auth_token = "YOUR_TOKEN_HERE"
twilio_number = "+19027018815"
my_phone_number = "+17826410444"

roomSchedule = pd.ExcelFile('pages/room_schedule.xlsx')
df = roomSchedule.parse('roomNum')
rl = roomSchedule.parse('roomList')
wb = load_workbook('pages/room_schedule.xlsx')
ws = wb['roomList']

def hello():
    return "Hello, this is Alex's summer project"

def sentSuccess(text):
    return f"sentSuccess: {text}"




