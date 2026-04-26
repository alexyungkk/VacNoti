import pandas as pd

account_sid = "YOUR_SID_HERE"
auth_token = "YOUR_TOKEN_HERE"
twilio_number = "+19027018815"
my_phone_number = "+17826410444"

roomSchedule = pd.ExcelFile('room_schedule.xlsx')
df = roomSchedule.parse('roomNum')


def hello():
    return "Hello, this is Alex summer project"

def sentSuccess(text):
    return f"sentSuccess: {text}"




