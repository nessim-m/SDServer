import random
import socket
import threading
import time
import psutil

HOST = '192.168.1.139'
HEADER = 64
FORMAT = 'utf-8'
from gps import *
from flask import Flask, render_template, Response, send_from_directory

app = Flask(__name__)
# THREAD 1
def handle_robot_status_client(conn, addr):
    print(f"[ROBOT STATUS CLIENT] {addr} connected.")
    connected = True

    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            print(f"[{addr}] {msg}")
            conn.send(b"Ready")
            app.run(threaded=True,host='0.0.0.0', port=5000)
            # .......
        else:
            connected = False

    conn.close()


# THREAD 2
def handle_robot_distance_client(conn, addr):
    print(f"[ROBOT DISTANCE CLIENT] {addr} connected.")
    connected = True
    time.sleep(2)
    while connected:
        conn.send(get_udistance().encode('ASCII'))
        time.sleep(1)

    conn.close()


# THREAD 3
def handle_robot_cpu_temp_client(conn, addr):
    print(f"[ROBOT DISTANCE CLIENT] {addr} connected.")
    connected = True
    time.sleep(2)
    while connected:
        # msg= str('{get_cpu_temp_func()}\N{DEGREE SIGN}')
        msg = str(f"{get_cpu_temp_func()}C")
        # msg= str("0")
        conn.send(msg.encode('ASCII'))
        time.sleep(1)
        # conn.send(b"55%")
        # time.sleep(2)

    conn.close()


# THREAD 4
def handle_robot_cpu_usage_client(conn, addr):
    print(f"[ROBOT DISTANCE CLIENT] {addr} connected.")
    connected = True
    time.sleep(2)
    while connected:
        msg = str(f"{get_cpu_use()}%")
        conn.send(msg.encode('ASCII'))
        time.sleep(1)

    conn.close()


# THREAD 5
def handle_robot_ram_usage_client(conn, addr):
    print(f"[ROBOT DISTANCE CLIENT] {addr} connected.")
    connected = True
    time.sleep(2)
    while connected:
        msg = str(f"{get_ram_info()}%")
        conn.send(msg.encode('ASCII'))
        time.sleep(1)

    conn.close()


def start():
    status_server_port = 5001
    distance_server_port = 5002
    cpu_temp_server_port = 5003
    cpu_usage_server_port = 5004
    ram_usage_server_port = 5005

    status_addr = (HOST, status_server_port)
    distance_addr = (HOST, distance_server_port)
    cpu_temp_addr = (HOST, cpu_temp_server_port)
    cpu_usage_addr = (HOST, cpu_usage_server_port)
    ram_usage_addr = (HOST, ram_usage_server_port)

    status_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    status_server.bind(status_addr)
    status_server.listen()

    distance_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    distance_server.bind(distance_addr)
    distance_server.listen()

    cpu_temp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cpu_temp_server.bind(cpu_temp_addr)
    cpu_temp_server.listen()

    cpu_usage_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cpu_usage_server.bind(cpu_usage_addr)
    cpu_usage_server.listen()

    ram_usage_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ram_usage_server.bind(ram_usage_addr)
    ram_usage_server.listen()

    print(f"[LISTENING] Server is listening on {HOST}")

    while True:
        status_server_conn, status_server_addr = status_server.accept()
        distance_server_conn, distance_server_addr = distance_server.accept()
        cpu_temp_server_conn, cpu_temp_server_addr = cpu_temp_server.accept()
        cpu_usage_server_conn, cpu_usage_server_addr = cpu_usage_server.accept()
        ram_usage_server_conn, ram_usage_server_addr = ram_usage_server.accept()

        thread_count = threading.active_count() - 1

        status_server_thread = threading.Thread(target=handle_robot_status_client,
                                                args=(status_server_conn, status_server_addr))
        status_server_thread.start()
        distance_server_thread = threading.Thread(target=handle_robot_distance_client,
                                                  args=(distance_server_conn, distance_server_addr))
        distance_server_thread.start()
        cpu_temp_server_thread = threading.Thread(target=handle_robot_cpu_temp_client,
                                                  args=(cpu_temp_server_conn, cpu_temp_server_addr))
        cpu_temp_server_thread.start()
        cpu_usage_server_thread = threading.Thread(target=handle_robot_cpu_usage_client,
                                                   args=(cpu_usage_server_conn, cpu_usage_server_addr))
        cpu_usage_server_thread.start()
        ram_usage_server_thread = threading.Thread(target=handle_robot_ram_usage_client,
                                                   args=(ram_usage_server_conn, ram_usage_server_addr))
        ram_usage_server_thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")

    # port = 5001
    # addr = (HOST, pr)
    # server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # server.bind(ADDR)
    # server.listen()
    # print(f"[LISTENING] Server is listening on {HOST}")
    # while True:
    #     conn, addr = server.accept()
    #     thread_count = threading.active_count() - 1
    #     if thread_count == 0:
    #         thread = threading.Thread(target=handle_robot_status_client, args=(conn, addr))
    #         thread.start()
    #     elif thread_count == 1:
    #         thread = threading.Thread(target=handle_robot_distance_client, args=(conn, addr))
    #         thread.start()
    #     elif thread_count == 2:
    #         thread = threading.Thread(target=handle_robot_cpu_temp_client, args=(conn, addr))
    #         thread.start()
    #     elif thread_count == 3:
    #         thread = threading.Thread(target=handle_robot_cpu_usage_client, args=(conn, addr))
    #         thread.start()
    #     elif thread_count == 4:
    #         thread = threading.Thread(target=handle_robot_ram_usage_client, args=(conn, addr))
    #         thread.start()
    #
    #     print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")
    #

from obj import gen_frame
@app.route('/')
def video_feed():
    return Response(gen_frame(),

                    mimetype='multipart/x-mixed-replace; boundary=frame')


def get_cpu_use():
    """ Return CPU usage using psutil"""
    cpu_cent = psutil.cpu_percent()
    return str(cpu_cent)


def get_cpu_temp_func():
    """ Return CPU temperature """
    result = 0
    mypath = "/sys/class/thermal/thermal_zone0/temp"
    with open(mypath, 'r') as mytmpfile:
        for line in mytmpfile:
            result = line

    result = float(result) / 1000
    result = round(result, 1)
    return str(result)


def get_ram_info():
    """ Return RAM usage using psutil """
    ram_cent = psutil.virtual_memory()[2]
    return str(ram_cent)

def get_udistance():
    #path = 'C:\\Users\\Username\\Path\\To\\File'
    path = '\home\pi\adeept_picarpro\server\distData.txt'
    with open(path, 'r') as f:
        return str(f.read())

print("[STARTING] server is starting...")
start()
