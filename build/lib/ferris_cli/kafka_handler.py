from logging import StreamHandler
from kafka import KafkaProducer
import json
from datetime import datetime

class KafkaConfig(object):
    def __init__(self, kafka_brokers, json=False):
        self.json = json
        if not json:
            self.producer = KafkaProducer(
                bootstrap_servers=kafka_brokers
            )
        else:
            self.producer = KafkaProducer(
                value_serializer=lambda v: json.dumps(v).encode('utf-8'),
                bootstrap_servers=kafka_brokers
            )
    def send(self, data, topic):
        if self.json:
            result = self.producer.send(topic, key=b'log', value=data)
        else:
            result = self.producer.send(topic, bytes(data, 'utf-8'))
        print("kafka send result: {}".format(result.get()))


class FerrisKafkaLoggingHandler(StreamHandler):

    def __init__(self, broker, topic):
        StreamHandler.__init__(self)
        self.broker = broker
        self.topic = topic
        # Kafka Broker Configuration
        self.kafka_broker = KafkaConfig(broker)
    def emit(self, record):
        msg = self.format(record)
        self.kafka_broker.send(msg, self.topic)

class MetricMessage(object):
    def __init__(self, metric_key, metric_value, update_time=None):
        self.metric_key = metric_key
        self.metric_value = metric_value
        if update_time == None:
            dateTimeObj = datetime.now()
            timestampStr = dateTimeObj.strftime("%d-%b-%Y (%H:%M:%S.%f)")
            self.update_time = timestampStr
        else:
            self.update_time = update_time

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)

class TaskTrackerMessage(object):
    def __init__(self, job_name,job_key,instance_id,job_status,status_message,update_time, correlation_id):  
        self.job_name = job_name
        self.job_key = job_key
        self.instance_id = instance_id
        self.job_status = job_status
        self.status_message = status_message
        self.update_time = update_time
        self.correlation_id = correlation_id
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)




