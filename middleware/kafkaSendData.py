from kafka import KafkaProducer, KafkaConsumer
from kafka.errors import kafka_errors
import traceback
import json


# 依赖安装  pip install kafka-python

producer = KafkaProducer(
    bootstrap_servers=['172.21.129.215:9092'], 
    key_serializer=lambda k: json.dumps(k).encode(),
    value_serializer=lambda v: json.dumps(v).encode())

def sendDataToKafka():
    for i in range(200,300):
        future  = producer.send(
            topic='pyTest',
            key=str(i),
            value=str(i)
        )
        print("send {}".format(str(i)))
        try:
            future.get(timeout=10)
        except kafka_errors:
            traceback.format_exc()


if __name__ == '__main__':
    sendDataToKafka()
    