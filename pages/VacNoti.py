import streamlit as st
import hotel_logic
import datetime
from twilio.rest import Client


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

schedule = st.file_uploader("Please upload today schedule", type=".xlsx", accept_multiple_files=False, 
                            max_upload_size=10)

currTime = datetime.datetime.now().strftime("%D, %H:%M:%S")

# checking if no logger
if "msg_logger" not in st.session_state:
    # creating an empty logger list
    st.session_state.msg_logger = []
# function to append new messages to msg_logger
def add_message(text, msg_type="info"):
    st.session_state.msg_logger.insert(0, {"text": text, "type": msg_type})

# checking if schedule has been uploaded
if schedule is not None:
    # hotel_logic.schedule_rn(schedule)
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
                                        # SMS senting part
                                        # account_sid = hotel_logic.account_sid
                                        # account_token = hotel_logic.auth_token

                                        # client = Client(account_sid, account_token)

                                        # message = client.messages.create(
                                        #     from_=hotel_logic.twilio_number,
                                        #     body= f"From supervisor. Hi, room {room_number} is vacant now, thank you",
                                        #     to=ra_number
                                        # )                                      
                                        add_message(f"{currTime} Notification sent to {ra_name} {ra_number} for room {room_number}!", "success")                                       
                        else:
                            add_message(f"{currTime} Room {room_number} is assigned to more than one room attendants.", "error")
                    else:
                        add_message(f"{currTime} Room {room_number} is not assigned yet.", "error")                       
                else:
                    # error if input invalid room number
                    add_message(f"{currTime} Please input a valid room number.", "error")

            # error if input other than integer
            except ValueError:
                add_message(f"{currTime} Please input a valid room number.", "error")


st.divider()

st.subheader("Message History")
for msg in st.session_state.msg_logger:
    if msg["type"] == "success":
        st.success(msg["text"])
    elif msg["type"] == "error":
        st.error(msg["text"])






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

