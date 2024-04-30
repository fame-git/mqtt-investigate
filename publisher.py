import time
import paho.mqtt.client as mqtt


def on_connect(client, userdata, flag, rc):
    if rc == 0:
        print("Publisher 1 Connected to MQTT Broker!")
    else:
        print("Failed to connect, return code %d\n", rc)


def on_message(client, userdata, msg):
    pass


def publish(client: mqtt.Client, del_time: float, q: int, instance: int):
    client.on_connect = on_connect
    client.on_message = on_message
    # public broker connect
    client.username_pw_set(f"fame-f{instance}f", "33102023")
    client.connect('broker.emqx.io', 1883)

    # Local broker
    # client.username_pw_set(f"fame-f{instance}f", "33102023")
    # client.connect('100.90.169.82', 1883)
    # client.connect("10.28.107.139", 1883)
    # client.connect("10.1.1.27", 1883)
    # client.connect("10.28.15.26", 1883)
    # ? ============================Friend=====================================
    # client.username_pw_set(f"fame-f{instance}f", "33102023")
    # client.connect("172.20.10.2", 1883)
    # ? ====================================================================================
    client.loop_start()
    print(f"start publishing on publisher-f{instance}")
    # iteratively publish counter topic message until it finish
    timeout = 60
    timeout_start = time.time()
    msg_count = 0
    topic = "counter/" + str(instance) + "/" + str(q) + "/" + str(del_time)
    while time.time() < timeout_start+timeout:
        msg = msg_count
        result = client.publish(topic=topic, payload=msg, qos=q)

        status = result[0]
        if status == 0:
            print("Send " + str(msg) + " to " + topic)
        else:
            break
            # print("Failed to send message to " + topic)

        msg_count += 1
        time.sleep(del_time)





