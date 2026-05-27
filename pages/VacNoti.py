import streamlit as st
import hotel_logic
from datetime import datetime
from zoneinfo import ZoneInfo
import json
import os
from twilio.rest import Client

# Securely pull the values from the secrets system
account_sid = st.secrets["TWILIO_ACCOUNT_SID"]
auth_token = st.secrets["TWILIO_AUTH_TOKEN"]

if not st.session_state.get("logged_in", False):
    st.error("Please login first!")
    st.switch_page("main.py")
    st.stop()

# st.balloons()
st.image("logo.png", width=400)
st.write(hotel_logic.hello())
st.title("🏨 Room Dispatcher")
st.write("Welcome, Supervisor. Please use the template below")


# Tell Python to look inside the pages folder
with open("room_schedule_template.xlsx", "rb") as file:
    btn = st.download_button(
        label="Download the Room Schedule Template Excel File",
        data=file,
        file_name="room_schedule_template.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )


persistent_file = "persistent_schedule.xlsx"
schedule = st.file_uploader("Please upload today schedule", type=".xlsx", 
                            accept_multiple_files=False, max_upload_size=10)

currTime = datetime.now(ZoneInfo("America/Halifax")).strftime("%D, %H:%M:%S")
# st.info(currTime)

# checking if no logger
if "msg_logger" not in st.session_state:
    # creating an empty logger list
    st.session_state.msg_logger = []
    
# function to append new messages to msg_logger
def add_message(text, msg_type="info"):
    st.session_state.msg_logger.insert(0, {"text": text, "type": msg_type})



if schedule is not None:
    with open (persistent_file, "wb") as f:
        f.write(schedule.getbuffer())
    st.success(f"New schedule saved locally as {schedule.name}")
    with open("schedule_name.txt", "w")as a:
        a.write(f"{schedule.name}")
        a.close()
    schedule = persistent_file
    run = True
elif os.path.exists(persistent_file):
    schedule = persistent_file
    b = open("schedule_name.txt", "r")
    st.info(f"Using previously saved schedule. {b.read()}")
    b.close()
    run = True
else:
    schedule = None
    run = False

# checking if schedule has been uploaded
if run:   
    # initialize a json data
    if not os.path.exists("simple.json"):
        initial_data = {"message": [], "type": []}
        with open("simple.json", "w") as f:
            json.dump(initial_data, f)

    # hotel_logic.schedule_rn(schedule)
    mess_type = st.radio("Service Type", ["Check out", "Stayover"], horizontal=True) 
    sms = st.checkbox("SMS send?")
    # st.info(mess_type)
    # using form function
    with st.form("notification"):
        room_number = st.text_input("Enter Room Number:", placeholder="room number")

        send = st.form_submit_button("Send")
        if send:
            try:
                int_room_number = int(room_number)
                # Checking if inputed room number valid 
                if int_room_number in hotel_logic.schedule_rn(schedule).values:
                    # checking if inputed room number assigned
                    if int_room_number in hotel_logic.schedule_rl(schedule).values:
                        # checking if depluating assigned to room attentant
                        if hotel_logic.roomCount(int_room_number, schedule) == 1:
                            # finding the inputed room number in the schedule
                            for row in hotel_logic.schedule_ws(schedule).iter_rows():
                                for cell in row:
                                    # text and adding success message if found the right room number and room attendant
                                    if cell.value == int_room_number:
                                        ra_name = hotel_logic.schedule_ws(schedule).cell(row=cell.row, column=1).value
                                        ra_number = str(hotel_logic.schedule_ws(schedule).cell(row=cell.row, column=2).value)
                                        client = Client(account_sid, auth_token)
                                        if mess_type == "Check out":
                                            ##### SMS senting part
                                            if sms:
                                                try: 
                                                    message = client.messages.create(
                                                        from_=hotel_logic.twilio_number,
                                                        body= f"From supervisor. Hi, room {room_number} is vacant now, thank you",
                                                        to=ra_number
                                                    )
                                                    success_mess = f"{currTime} Notification sent to {ra_name} {ra_number} for room {room_number}!"
                                                    type_mess = "success"
                                                    hotel_logic.update_json(success_mess, type_mess, "simple.json")                                      
                                                    add_message(f"{currTime} Notification sent to {ra_name} {ra_number} for room {room_number}!", "success")   
                                                except Exception as e:
                                                    st.error(f"Failed to send SMS: {e}")
                                            else:
                                                try: 
                                                    success_mess = f"{currTime} Notification sent to {ra_name} {ra_number} for room {room_number}!"
                                                    type_mess = "success"
                                                    hotel_logic.update_json(success_mess, type_mess, "simple.json")                                      
                                                    add_message(f"{currTime} Notification sent to {ra_name} {ra_number} for room {room_number}!", "success")   
                                                except Exception as e:
                                                    st.error(f"Failed to send SMS: {e}")
                                          
                                        elif mess_type == "Stayover":
                                            ###### SMS senting part
                                            if sms:
                                                try: 
                                                    message = client.messages.create(
                                                        from_=hotel_logic.twilio_number,
                                                        body= f"From supervisor. Hi, room {room_number} needs service, thank you",
                                                        to=ra_number
                                                    )
                                                    success_mess = f"{currTime} STAYOVER notification  sent to {ra_name} {ra_number} for room {room_number}!"
                                                    type_mess = "success"
                                                    hotel_logic.update_json(success_mess, type_mess, "simple.json")                                      
                                                    add_message(f"{currTime} STAYOVER notification sent to {ra_name} {ra_number} for room {room_number}!", "success")    
                                                except Exception as e:
                                                    st.error(f"Failed to send SMS: {e}")
                                            else:
                                                try: 

                                                        success_mess = f"{currTime} STAYOVER notification  sent to {ra_name} {ra_number} for room {room_number}!"
                                                        type_mess = "success"
                                                        hotel_logic.update_json(success_mess, type_mess, "simple.json")                                      
                                                        add_message(f"{currTime} STAYOVER notification sent to {ra_name} {ra_number} for room {room_number}!", "success")    
                                                except Exception as e:
                                                    st.error(f"Failed to send SMS: {e}")

                        else:
                            error_mess = f"{currTime} Room {room_number} is assigned to more than one room attendants."
                            type_mess = "error"
                            hotel_logic.update_json(error_mess, type_mess, "simple.json")                        
                            add_message(f"{currTime} Room {room_number} is assigned to more than one room attendants.", "error")
                    else:
                        error_mess = f"{currTime} Room {room_number} is not assigned yet."
                        type_mess = "error"
                        hotel_logic.update_json(error_mess, type_mess, "simple.json")                         
                        add_message(f"{currTime} Room {room_number} is not assigned yet.", "error")                       
                else:
                    # error if input invalid room number
                    error_mess = f"{currTime} Please input a valid room number."
                    type_mess = "error"
                    hotel_logic.update_json(error_mess, type_mess, "simple.json")    
                    add_message(f"{currTime} Please input a valid room number.", "error")

            # error if input other than integer
            except ValueError:
                error_mess = f"{currTime} Please input a valid room number."
                type_mess = "error"
                hotel_logic.update_json(error_mess, type_mess, "simple.json")    
                add_message(f"{currTime} Please input a valid room number.", "error")
            
# Create a button to clear the JSON data
clear = st.button("Clear Message History")
if clear:
    # Define the empty template
    empty_message = {
        "message": [],
        "type": []
    }
    
    # Overwrite the file with the empty template
    with open("simple.json", "w") as f:
        json.dump(empty_message, f)
    
    # Clear the session state logger as well so the UI updates immediately
    st.session_state.msg_logger = []
    
    st.success("History cleared!")
    st.rerun() # Refresh the app to show the empty state


st.divider()

st.subheader("Message History")
for msg in st.session_state.msg_logger:
    if msg["type"] == "success":
        st.success(msg["text"])
    elif msg["type"] == "error":
        st.error(msg["text"])

st.subheader("JSON Data")

with open("simple.json", "r") as f:
    data = json.load(f)
    
    # Loop through the length of the message list
    for i in range(len(data["message"])):
        msg_text = data["message"][i]
        msg_type = data["type"][i]
        
        # Display based on the type stored at the same index
        if msg_type == "success":
            st.success(msg_text)
        elif msg_type == "error":
            st.error(msg_text)





    # SMS senting part
    # account_sid = functions.account_sid
    # account_token = functions.auth_token

    # client = Client(account_sid, account_token)

    # message = client.messages.create(
    #     from_=functions.twilio_number,
    #     body= f"From supervisor. Hi, room {room_number} is vacant now, thank you",
    #     to=functions.my_phone_number
    # )
    # print(message.sid)

