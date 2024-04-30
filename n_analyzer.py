import threading
import time
import n_sys as n_sys
import paho.mqtt.client as mqtt
import numpy as np

analyse_data = {}  # storing dict with key of counter topic and counter value
analyse_time = {}  # timestamping corresponding with the counter topic
average_receive_message = {} # average received message for each topic
inter_msg_gap = {}  # dict for internal gap for each topic
out_order_msg = {}  # dict for out of order message
msg_loss = {}  # dict for message loss
mean_gap = {}  # dict mean value generate by numpy
median_gap = {}  # dict median value generate by numpy
INTERVAL = 60  # default interval time
delay = 0


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Analyser connected to MQTT Broker!")
    else:
        print("Failed to connect, return code %d\n", rc)


def on_message(client, userdata, msg):
    global analyse_data, analyse_time

    if msg.topic not in analyse_data:

        analyse_data[msg.topic] = [int(msg.payload)]
        analyse_time[msg.topic] = [float(msg.timestamp)]
    else:
        analyse_data[msg.topic].append(int(msg.payload))
        analyse_time[msg.topic].append(float(msg.timestamp))


def assignment3():
    global delay
    for topic, data in analyse_data.items():
        # calculate average messages for each topic
        average_receive_message[topic] = len(data) / INTERVAL
        # calculate the out-of-order message percentage
        out_order_count = 0
        for i in range(1, len(data)):
            if data[i] - data[i-1] != 1:
                out_order_count += 1
        if len(data) != 0:
            out_order_msg[topic] = out_order_count/len(data)
        else:
            out_order_msg[topic] = 0
        # calculate the loss message percentage
        topics = topic.split('/')
        rate = float(topics[3])
        if rate == delay:
            should_receive = 0
            for i in range(1, len(data)):
                should_receive += data[i] - data[i-1]
            if should_receive != 0 or should_receive >= len(data):
                msg_loss[topic] = abs(round((should_receive - len(data)) / should_receive, 4) * 100)
            else:
                msg_loss[topic] = 0
        else:
            total_msg = INTERVAL/rate
            if total_msg != 0 or total_msg >= len(data):
                msg_loss[topic] = abs(round((total_msg - len(data))/total_msg, 4) * 100)
            else:
                msg_loss[topic] = 0

        # find interval gap between each messages to find a mean and median
        internal_gap = []
        for i in range(1, len(data)):
            if data[i] == data[i-1] + 1:
                gap = round((analyse_time[topic][i] - analyse_time[topic][i-1]), 4)
                internal_gap.append(gap)
        inter_msg_gap[topic] = internal_gap

        median_gap[topic] = np.median(inter_msg_gap[topic])

        mean_gap[topic] = np.mean(inter_msg_gap[topic])

    # print all the result
    for key, value in average_receive_message.items():
        print(key + " : has =  " + str(value) + " msg/s of average receive message")
    print("-----------------------------------------------------------------------------------")
    for key, value in msg_loss.items():
        print(key + " : has = " + str(value) + "% of loss message")
    print("-----------------------------------------------------------------------------------")
    for key, value in out_order_msg.items():
        print(key + " : has = " + str(value) + "% of out-of-order messages.")
    print("-----------------------------------------------------------------------------------")
    for key, value in mean_gap.items():
        print(key + " : has = " + str(value) + " ms. of mean inter-message-gap value.")
    print("-----------------------------------------------------------------------------------")
    for key, value in median_gap.items():
        print(key + " : has = " + str(value) + " ms. of median inter-message-gap value.")


if __name__ == '__main__':
    # establish the analyzer client
    analyzer = mqtt.Client(client_id='3310-analyzerfriend', clean_session=True)
    analyzer.on_connect = on_connect
    analyzer.on_message = on_message
    # choose the broker
    #  =============================public test broker======================================
    analyzer.username_pw_set("fame-af", "33102023")
    analyzer.connect("broker.emqx.io", 1883)
    #  ====================================================================================
    #  =============================local test broker======================================
    # analyzer.username_pw_set("fame-af", "33102023")
    # analyzer.connect("100.90.169.82", 1883)
    # analyzer.connect("10.28.107.139", 1883)
    # analyzer.connect("10.1.1.27", 1883)
    # analyzer.connect("10.28.15.26", 1883)
    # ? ====================================================================================
    # ? ============================Friend=====================================
    # analyzer.username_pw_set("fame-af", "33102023")
    # analyzer.connect("172.20.10.2", 1883)
    # ? ====================================================================================
    print("----------Dear User Here is the QOS choice which is 0, 1, or 2 --------------------------------")
    qos = int(input("Please Enter your desired qos: "))
    print("----------Choose your delayed from [0.0, 0.01, 0.02, 0.04, 0.08, 0.16, 0.32]------------------")
    delay = float(input("Please Enter your desired delay: "))
    print("----------Choose the amount of instances you want from 1, 2, 3 --------------------------------")
    instance = int(input("Please Enter your instance count: "))
    # subscribe to counter topic for analyzed the data
    analyzer.subscribe('counter/1/0/#', qos=qos)
    analyzer.subscribe('counter/1/1/#', qos=qos)
    analyzer.subscribe('counter/1/2/#', qos=qos)
    analyzer.subscribe('counter/2/0/#', qos=qos)
    analyzer.subscribe('counter/2/1/#', qos=qos)
    analyzer.subscribe('counter/2/2/#', qos=qos)
    analyzer.subscribe('counter/3/0/#', qos=qos)
    analyzer.subscribe('counter/3/1/#', qos=qos)
    analyzer.subscribe('counter/3/2/#', qos=qos)

    time.sleep(1)
    # concurrently run the sys topic subscriber to track the $SYS topic data
    sys_thread = threading.Thread(target=n_sys.run)
    sys_thread.start()
    time.sleep(1)

    print("Analyzer publish")
    # publish the request/# topic to the broker which controller will receive and run the publisher based on input
    analyzer.publish(topic='request/qos', payload=qos, qos=qos)
    analyzer.publish(topic='request/delay', payload=delay, qos=qos)
    analyzer.publish(topic='request/instancecount', payload=instance, qos=qos)

    analyzer.loop_start()
    print("Analyze begin")
    time.sleep(INTERVAL)
    analyzer.publish(topic='request/stop', payload=instance, qos=qos)
    time.sleep(1)
    print('end of analyzer')
    assignment3()
    analyzer.disconnect()
