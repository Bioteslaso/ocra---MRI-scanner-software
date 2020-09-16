#!/usr/bin/env python

# import general packages
import sys
import struct
import time

# import calculation and plot packages
import numpy as np

# import private packages
from globalsocket import gsocket
from assembler import Assembler
from PyQt5.QtNetwork import QAbstractSocket, QTcpSocket

idle = True  # state variable: True-stop, False-start
seq_filename = '/Users/thomaswitzel/oss_ocra/ocra/Applications/ocra/sequence/basic/cw_pulse_2ms.txt'


# setup buffer and offset for incoming data
buffer_size = 50000  # total data received (defined by the server code)
buffer = bytearray(8 * buffer_size)
data = np.frombuffer(buffer, np.complex64)

def socket_connected():
    print("Socket Connected!")

def socket_error(socketError):
    print('Socket Error: %s.' % gsocket.errorString())

def receive_data():
    print("\tAcquiring data.")
    while True:  # Read data
        gsocket.waitForReadyRead()
        datasize = gsocket.bytesAvailable()
        #print(datasize)
        if datasize == 8 * buffer_size:
            print("Readout finished : ", datasize)
            buffer[0:8 * buffer_size] = gsocket.read(8 * buffer_size)
            break
        else:
            continue

# start the FID app on the server by sending the command over the socket
print("Starting MRI_FID_Widget")
gsocket = QTcpSocket()
gsocket.connected.connect(socket_connected)
gsocket.error.connect(socket_error)

gsocket.connectToHost("10.10.2.39", 1001)
gsocket.waitForConnected(1000)
if gsocket.state() == QAbstractSocket.ConnectedState:
    print("Connection to host established.")
elif gsocket.state() == QAbstractSocket.UnconnectedState:
    print("Conncection to host failed.")
else:
    print("TCP socket in state : ", gsocket.state())

time.sleep(1)
# send 1 as signal to start MRI_FID_Widget
gsocket.write(struct.pack('<I', 1))
gsocket.flush()

# setup global socket for receive data
gsocket.setReadBufferSize(8 * buffer_size)


# send the sequence to the backend
ass = Assembler()
seq_byte_array = ass.assemble(seq_filename)
print(len(seq_byte_array))
gsocket.write(struct.pack('<I', len(seq_byte_array)))
gsocket.write(seq_byte_array)
gsocket.flush()

# Set frequency
print("Setting frequency.")
freq = 15.62 # MHz
gsocket.write(struct.pack('<I', 1 << 28 | int(1.0e6 * freq)))
gsocket.flush()
receive_data()

for attenuation in np.arange(24.0,0.0,-0.25):
    # Set attenuation
    print("Setting attenuation %f\n" % attenuation)
    gsocket.write(struct.pack('<I', 3 << 28 | int(attenuation / 0.25)))
    gsocket.flush()
    # Acquire data
    #gsocket.write(struct.pack('<I', 2 << 28 | 0 << 24))
    #gsocket.flush()
    receive_data()

    time.sleep(2)

# stopping the backend app on the server
print("Stopping MRI_FID_Widget")

# send 0 as signal to stop MRI_FID_Widget
gsocket.write(struct.pack('<I', 0))
gsocket.flush()


