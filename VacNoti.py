import streamlit as st

st.title("🏨 Room Dispatcher")
st.write("Welcome, Supervisor. Select a room to notify an attendant.")

room_number = st.text_input("Enter Room Number:")
if st.button("Send Notification"):
    st.success(f"Notification sent for Room {room_number}!")