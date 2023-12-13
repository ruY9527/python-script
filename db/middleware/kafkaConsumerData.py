# kafka 消费数据
from kafka import KafkaProducer, KafkaConsumer
from kafka.errors import kafka_errors
import traceback
import json


consumer = KafkaConsumer(
    'pyTest', 
    bootstrap_servers='172.21.129.215:9092',
    group_id='pyTestConsumer'
)

def consumerData():
    for message in consumer:
        print("receive, key: {}, value: {}".format(
            json.loads(message.key.decode()),
            json.loads(message.value.decode())
            )
        )



if __name__ == '__main__':
    consumerData()
    