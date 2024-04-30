import sys
import paho.mqtt.client as mqtt


analyse_data = {}
sys_a = mqtt.Client(client_id='3310-sysfriend', clean_session=True)


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Sys Analyser connected to MQTT Broker!")
    else:
        print("Failed to connect, return code %d\n", rc)


def on_message(client, userdata, msg):
    global analyse_data

    if msg.topic not in analyse_data:

        analyse_data[msg.topic] = [msg.payload]
    else:
        analyse_data[msg.topic].append(msg.payload)
    # if request stop show all sys data that gather from the broker
    if msg.topic == "request/stop":
        print("-----------------kill-signal---------------")
        print("-----------------show sys data---------------")
        for k, v in analyse_data.items():
            print(k + " : " + str(v))
        sys_a.disconnect()


def run():
    sys_a.on_connect = on_connect
    sys_a.on_message = on_message
    # choose the broker
    #  =============================public test broker======================================
    sys_a.username_pw_set("fame-sf", "33102023")
    sys_a.connect("broker.emqx.io", 1883)
    #  ====================================================================================
    #  =============================local test broker======================================
    # sys_a.username_pw_set("fame-sf", "33102023")
    # sys_a.connect("100.90.169.82", 1883)
    # sys_a.connect("10.28.107.139", 1883)
    # sys_a.connect("10.1.1.27", 1883)
    # sys_a.connect("10.28.15.26", 1883)
    #  ====================================================================================
    # ? ============================Friend=====================================
    # sys_a.username_pw_set(f"fame-sf", "33102023")
    # sys_a.connect("172.20.10.2", 1883)
    # ? ====================================================================================
    # subscribe to the sys topic
    sys_a.subscribe('$SYS/broker/load/messages/received/#', qos=0)
    sys_a.subscribe('$SYS/broker/messages/received/#', qos=0)
    sys_a.subscribe('$SYS/broker/heap/#', qos=0)
    sys_a.subscribe('$SYS/broker/clients/total/#', qos=0)
    sys_a.subscribe('$SYS/broker/load/messages/received/#', qos=1)
    sys_a.subscribe('$SYS/broker/messages/received/#', qos=1)
    sys_a.subscribe('$SYS/broker/heap/#', qos=1)
    sys_a.subscribe('$SYS/broker/clients/total/#', qos=1)
    sys_a.subscribe('$SYS/broker/load/messages/received/#', qos=2)
    sys_a.subscribe('$SYS/broker/messages/received/#', qos=2)
    sys_a.subscribe('$SYS/broker/heap/#', qos=2)
    sys_a.subscribe('$SYS/broker/clients/total/#', qos=2)
    sys_a.subscribe("request/stop", qos=0)
    sys_a.subscribe("request/stop", qos=1)
    sys_a.subscribe("request/stop", qos=2)
    sys_a.loop_start()