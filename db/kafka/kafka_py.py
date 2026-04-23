# -*- coding: utf-8 -*-
"""
Kafka 生产者和消费者工具类
支持生产 JSON 数据到 Kafka 和从 Kafka 消费数据
"""

import json
import logging
from typing import Optional, Dict, Any, List, Callable
from kafka import KafkaProducer, KafkaConsumer
from kafka.errors import KafkaError
from kafka.admin import KafkaAdminClient, NewTopic

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class KafkaProducerClient:
    """Kafka 生产者客户端"""
    
    def __init__(self, config: Dict[str, Any]):
        """
        初始化 Kafka 生产者
        
        Args:
            config: Kafka 配置字典，包含以下键:
                - bootstrap_servers: Kafka 服务器地址列表，如 ['localhost:9092']
                - value_serializer: 序列化函数 (可选，默认使用 JSON 序列化)
                - key_serializer: 键序列化函数 (可选)
                - 其他 kafka-python 支持的参数
        """
        self.config = config.copy()
        self.config.setdefault('value_serializer', lambda v: json.dumps(v, ensure_ascii=False).encode('utf-8'))
        self.config.setdefault('key_serializer', lambda k: k.encode('utf-8') if k else None)
        self.config.setdefault('acks', 'all')  # 等待所有副本确认
        self.config.setdefault('retries', 3)  # 重试次数
        
        self.producer: Optional[KafkaProducer] = None
    
    def connect(self) -> KafkaProducer:
        """建立 Kafka 连接"""
        try:
            self.producer = KafkaProducer(**self.config)
            logger.info(f"成功连接到 Kafka: {self.config['bootstrap_servers']}")
            return self.producer
        except KafkaError as e:
            logger.error(f"连接 Kafka 失败：{e}")
            raise
    
    def close(self):
        """关闭生产者连接"""
        if self.producer:
            self.producer.flush()
            self.producer.close()
            self.producer = None
            logger.info("Kafka 生产者连接已关闭")
    
    def send_message(self, topic: str, message: Dict, key: Optional[str] = None) -> bool:
        """
        发送单条消息
        
        Args:
            topic: 主题名称
            message: 消息内容 (字典)
            key: 消息键 (可选)
            
        Returns:
            发送成功返回 True，失败返回 False
        """
        if not self.producer:
            self.connect()
        
        try:
            future = self.producer.send(topic, value=message, key=key)
            record_metadata = future.get(timeout=10)
            logger.info(
                f"消息发送成功 - topic: {record_metadata.topic}, "
                f"partition: {record_metadata.partition}, "
                f"offset: {record_metadata.offset}"
            )
            return True
        except KafkaError as e:
            logger.error(f"发送消息失败：{e}")
            return False
    
    def send_batch(self, topic: str, messages: List[Dict]) -> int:
        """
        批量发送消息
        
        Args:
            topic: 主题名称
            messages: 消息列表
            
        Returns:
            成功发送的消息数量
        """
        if not self.producer:
            self.connect()
        
        success_count = 0
        for message in messages:
            try:
                self.producer.send(topic, value=message)
                success_count += 1
            except KafkaError as e:
                logger.error(f"批量发送消息失败：{e}")
        
        # 确保所有消息都已发送
        self.producer.flush()
        logger.info(f"批量发送完成，成功：{success_count}/{len(messages)}")
        return success_count
    
    def create_topic(self, topic_name: str, num_partitions: int = 1, replication_factor: int = 1) -> bool:
        """
        创建 Kafka 主题
        
        Args:
            topic_name: 主题名称
            num_partitions: 分区数
            replication_factor: 复制因子
            
        Returns:
            创建成功返回 True
        """
        try:
            admin_client = KafkaAdminClient(
                bootstrap_servers=self.config['bootstrap_servers']
            )
            topic = NewTopic(
                name=topic_name,
                num_partitions=num_partitions,
                replication_factor=replication_factor
            )
            admin_client.create_topics([topic])
            admin_client.close()
            logger.info(f"主题 {topic_name} 创建成功")
            return True
        except KafkaError as e:
            logger.error(f"创建主题失败：{e}")
            return False


class KafkaConsumerClient:
    """Kafka 消费者客户端"""
    
    def __init__(self, config: Dict[str, Any]):
        """
        初始化 Kafka 消费者
        
        Args:
            config: Kafka 配置字典，包含以下键:
                - bootstrap_servers: Kafka 服务器地址列表
                - group_id: 消费者组 ID
                - value_deserializer: 反序列化函数 (可选，默认使用 JSON 反序列化)
                - key_deserializer: 键反序列化函数 (可选)
                - auto_offset_reset: 偏移量重置策略 (earliest/latest)
                - enable_auto_commit: 是否自动提交偏移量
                - 其他 kafka-python 支持的参数
        """
        self.config = config.copy()
        self.config.setdefault('value_deserializer', lambda m: json.loads(m.decode('utf-8')))
        self.config.setdefault('key_deserializer', lambda k: k.decode('utf-8') if k else None)
        self.config.setdefault('auto_offset_reset', 'earliest')
        self.config.setdefault('enable_auto_commit', True)
        
        self.consumer: Optional[KafkaConsumer] = None
        self.topics: List[str] = []
    
    def connect(self, topics: List[str]) -> KafkaConsumer:
        """
        建立 Kafka 连接并订阅主题
        
        Args:
            topics: 要订阅的主题列表
        """
        try:
            self.consumer = KafkaConsumer(**self.config)
            self.topics = topics
            self.consumer.subscribe(topics)
            logger.info(f"成功订阅主题：{topics}")
            return self.consumer
        except KafkaError as e:
            logger.error(f"连接 Kafka 失败：{e}")
            raise
    
    def close(self):
        """关闭消费者连接"""
        if self.consumer:
            self.consumer.close()
            self.consumer = None
            logger.info("Kafka 消费者连接已关闭")
    
    def consume(self, callback: Callable[[Dict], None], max_messages: Optional[int] = None):
        """
        消费消息
        
        Args:
            callback: 处理消息的回调函数
            max_messages: 最大消费消息数 (None 表示持续消费)
        """
        if not self.consumer:
            raise RuntimeError("请先调用 connect() 方法")
        
        message_count = 0
        try:
            for message in self.consumer:
                try:
                    data = message.value
                    logger.info(
                        f"收到消息 - topic: {message.topic}, "
                        f"partition: {message.partition}, "
                        f"offset: {message.offset}, "
                        f"key: {message.key}"
                    )
                    callback(data)
                    message_count += 1
                    
                    if max_messages and message_count >= max_messages:
                        logger.info(f"已达到最大消费数量：{max_messages}")
                        break
                except Exception as e:
                    logger.error(f"处理消息失败：{e}")
                    continue
        except KeyboardInterrupt:
            logger.info("消费者被中断")
        finally:
            self.close()
    
    def consume_one(self, timeout_ms: int = 1000) -> Optional[Dict]:
        """
        消费单条消息
        
        Args:
            timeout_ms: 超时时间 (毫秒)
            
        Returns:
            消息内容或 None
        """
        if not self.consumer:
            raise RuntimeError("请先调用 connect() 方法")
        
        messages = self.consumer.poll(timeout_ms=timeout_ms)
        for topic_partition, records in messages.items():
            if records:
                message = records[0]
                logger.info(f"收到消息 - topic: {message.topic}, offset: {message.offset}")
                return message.value
        return None
    
    def get_consumer_lag(self) -> Dict[str, int]:
        """
        获取消费者延迟
        
        Returns:
            各分区的延迟字典
        """
        if not self.consumer:
            raise RuntimeError("请先调用 connect() 方法")
        
        lag_dict = {}
        assigned = self.consumer.assignment()
        for tp in assigned:
            committed = self.consumer.committed(tp)
            end = self.consumer.position(tp)
            if committed and end:
                lag_dict[f"{tp.topic}-{tp.partition}"] = end - committed
        return lag_dict


# 默认配置
DEFAULT_PRODUCER_CONFIG = {
    'bootstrap_servers': ['localhost:9092'],
    'acks': 'all',
    'retries': 3
}

DEFAULT_CONSUMER_CONFIG = {
    'bootstrap_servers': ['localhost:9092'],
    'group_id': 'my_consumer_group',
    'auto_offset_reset': 'earliest',
    'enable_auto_commit': True
}


if __name__ == "__main__":
    # 使用示例
    
    # 1. 生产者示例
    print("=" * 50)
    print("Kafka 生产者示例")
    print("=" * 50)
    
    producer_config = DEFAULT_PRODUCER_CONFIG.copy()
    producer = KafkaProducerClient(producer_config)
    
    try:
        producer.connect()
        
        # 创建主题 (可选)
        # producer.create_topic('test_topic', num_partitions=3, replication_factor=1)
        
        # 发送单条消息
        message_data = {
            'id': 1,
            'name': '测试数据',
            'timestamp': '2026-04-17 10:00:00',
            'value': 100.5
        }
        success = producer.send_message('test_topic', message_data, key='message_key_1')
        print(f"单条消息发送成功：{success}")
        
        # 批量发送消息
        batch_messages = [
            {'id': i, 'name': f'批量数据_{i}', 'timestamp': '2026-04-17'}
            for i in range(5)
        ]
        count = producer.send_batch('test_topic', batch_messages)
        print(f"批量发送成功数量：{count}")
        
    except Exception as e:
        print(f"生产者错误：{e}")
    finally:
        producer.close()
    
    # 2. 消费者示例
    print("\n" + "=" * 50)
    print("Kafka 消费者示例")
    print("=" * 50)
    
    consumer_config = DEFAULT_CONSUMER_CONFIG.copy()
    consumer = KafkaConsumerClient(consumer_config)
    
    def process_message(data: Dict):
        """消息处理回调函数"""
        print(f"处理消息：{data}")
    
    try:
        consumer.connect(['test_topic'])
        
        # 消费消息 (持续消费)
        # consumer.consume(process_message)
        
        # 消费指定数量的消息
        consumer.consume(process_message, max_messages=10)
        
        # 消费单条消息
        # message = consumer.consume_one()
        # if message:
        #     print(f"收到消息：{message}")
        
    except Exception as e:
        print(f"消费者错误：{e}")
    finally:
        consumer.close()
