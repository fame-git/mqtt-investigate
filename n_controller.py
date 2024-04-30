import paho.mqtt.client as mqtt
import publisher as p
import threading
import time
# Set Global variable for each mqtt client which in this case is publisher 1, 2, 3 and controller
publisher_1 = mqtt.Client(client_id='3310-1f', clean_session=True)
publisher_2 = mqtt.Client(client_id='3310-2f', clean_session=True)
publisher_3 = mqtt.Client(client_id='3310-3f', clean_session=True)
controller = mqtt.Client(client_id='3310-controllerf', clean_session=True)
qos = 0
delay = 0.0
instance = 0


# paho on_connect function to flag connection establishment for controller
def on_connect(client, userdata, flag, rc):
    if rc == 0:
        print("Controller Connected to MQTT Broker!")
    else:
        print("Failed to connect, return code %d\n", rc)


# paho on_message which will receive the subscription  message topics which based on requirement is
# "request/qos", "request/delay", "request/instancecount", "request/stop"
def on_message(client, userdata, msg):
    global qos, delay, instance
    # check topic on qos
    # set qos global parameter
    if msg.topic == "request/qos":
        print("------------------qos-change---------------")
        print("change to: " + str(msg.payload.decode('utf-8')))
        qos = int(msg.payload)
    # check topic on delay
    # set delay global parameter
    elif msg.topic == "request/delay":
        print("------------------delay-change-------------")
        print("change to: " + str(msg.payload.decode('utf-8')))
        delay = float(msg.payload)
    # check topic on instancecount
    # set instance global parameter
    # derived instance count and implement threading to target publish function inside publisher.py
    # run publisher depends on amount of instance and used input based on global variable instance
    elif msg.topic == "request/instancecount":
        print("------------------Change instances----------")
        print("change to: " + str(msg.payload.decode('utf-8')))
        instance = int(msg.payload.decode('utf-8'))
        if instance != 0:
            if instance == 1:
                print(1)
                p1_t = threading.Thread(target=p.publish, args=(publisher_1, delay, qos, 1,))
                p1_t.start()
            elif instance == 2:
                print(2)
                p1_t = threading.Thread(target=p.publish, args=(publisher_1, delay, qos, 1,))
                p1_t.start()
                p2_t = threading.Thread(target=p.publish, args=(publisher_2, delay, qos, 2,))
                p2_t.start()
            elif instance == 3:
                print(3)
                p1_t = threading.Thread(target=p.publish, args=(publisher_1, delay, qos, 1,))
                p1_t.start()
                p2_t = threading.Thread(target=p.publish, args=(publisher_2, delay, qos, 2,))
                p2_t.start()
                p3_t = threading.Thread(target=p.publish, args=(publisher_3, delay, qos, 3,))
                p3_t.start()
    # topic for kill signal which will end the process
    # disconnect every publisher
    # disconnect controller
    elif msg.topic == "request/stop":
        print("-----------------kill-signal---------------")
        publisher_1.disconnect()
        time.sleep(1)
        print("p1 disconnect")
        publisher_2.disconnect()
        time.sleep(1)
        print("p2 disconnect")
        publisher_3.disconnect()
        time.sleep(1)
        print("p3 disconnect")
        print("Finish")
        # caught error if didn't disconnect the controller somehow analyzer cannot receive another message
        controller.disconnect()


if __name__ == '__main__':
    # set controller client to tag on mqtt connection and message
    controller.on_connect = on_connect
    controller.on_message = on_message

    # choose the broker with set username and password
    #  =============================public test broker======================================
    controller.username_pw_set("fame-cf", "33102023")
    controller.connect("broker.emqx.io", 1883)
    #  ====================================================================================
    #  =============================local test broker======================================
    # controller.username_pw_set("fame-cf", "33102023")
    # controller.connect("100.90.169.82", 1883)
    # controller.connect("10.28.107.139", 1883)
    # controller.connect("10.1.1.27", 1883)
    # controller.connect("10.28.15.26", 1883)
    #  ====================================================================================
    # ? ============================Friend=====================================
    # controller.username_pw_set("fame-cf", "33102023")
    # controller.connect("172.20.10.2", 1883)
    # ? ====================================================================================

    # subscribe to request/# topic
    controller.subscribe("request/#", qos=0)
    controller.subscribe("request/#", qos=1)
    controller.subscribe("request/#", qos=2)
    print("subscribe finish")
    time.sleep(1)
    controller.loop_forever()
    print("Controller - Shutdown")


