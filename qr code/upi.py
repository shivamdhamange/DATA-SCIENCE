import streamlit as st
import qrcode
import cv2
import numpy as np
from io import BytesIO

st.title("My UPI QR Scanner")

upi = st.text_input("Enter UPI ID")
name = st.text_input("Enter Name")

from urllib.parse import urlencode

if st.button("Generate QR"):

    if not upi or not name:
        st.error("Please enter UPI ID and Name")

    else:
        params = {
            "pa": upi.strip(),
            "pn": name.strip(),
            "cu": "INR"
        }

        link = "upi://pay?" + urlencode(params)

        st.write("UPI Payment Link:", link)

        qr = qrcode.make(link)

        img_buffer = BytesIO()
        qr.save(img_buffer, format="PNG")

        st.image(img_buffer.getvalue(), width=300)

        st.success("QR Generated!")

st.subheader("Scan QR")

file = st.camera_input("Open Camera")

if file:
    image = cv2.imdecode(
        np.frombuffer(file.getvalue(), np.uint8),
        cv2.IMREAD_COLOR
    )

    detector = cv2.QRCodeDetector()
    data, points, _ = detector.detectAndDecode(image)

    if data:
        st.success("QR Scanned!")
        st.write(data)
    else:
        st.error("QR Not Found")
