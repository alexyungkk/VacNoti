import streamlit as st
import hotel_logic
from twilio.rest import Client

st.title(hotel_logic.hello())
st.title("🏨 Room Dispatcher")
st.write("Welcome, Supervisor. Select a room to notify an attendant.")

room_number = st.text_input("Enter Room Number:")

if st.button("Send Notification"):
    try:
        int_room_number = int(room_number)
        if int_room_number in hotel_logic.df.values:
            st.success(f"Notification sent for Room {room_number}!")
        else:
            st.error("Please input a valid room number.")
    except ValueError:
        st.error("Please input a valid room number.")
    




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

