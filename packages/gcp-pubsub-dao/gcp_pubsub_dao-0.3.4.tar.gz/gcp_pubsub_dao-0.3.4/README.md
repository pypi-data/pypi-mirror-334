# GCP Pub/Sub DAO
The library provides DAO classes for GCP pubsub publisher/subscriber.

## Installation

```python
pip install gcp-pubsub-dao
```

## Usage

- sync subscriber:
```python
from gcp_pubsub_dao import PubSubSubscriberDAO, Message

dao = PubSubSubscriberDAO(project_id="prodect-dev", subscription_id="subscription")
messages: Message = dao.get_messages(messages_count=2)

for message in messages:
    print(message.data)
    
dao.ack_messages(ack_ids=[message[0].ack_id])      
dao.nack_messages(ack_ids=[message[1].ack_id])     

dao.close()     # to clean up connections
```
- sync publisher:
```python
from gcp_pubsub_dao import PubSubPublisherDAO

dao = PubSubPublisherDAO(project_id="prodect-dev")
try:
    dao.publish_message(topic_name="topic", payload=b"asdfsdf", attributes={"kitId": "AW12345678"})
except Exception as ex:
    print(ex)
```
- async subscriber:
```python
from gcp_pubsub_dao import AsyncPubSubSubscriberDAO, Message

dao = AsyncPubSubSubscriberDAO(project_id="prodect-dev", subscription_id="subscription")
messages: Message = await dao.get_messages(messages_count=2)

for message in messages:
    print(message.data)
    
await dao.ack_messages(ack_ids=[message[0].ack_id])      
await dao.nack_messages(ack_ids=[message[1].ack_id])
```
- async publisher:
```python
from gcp_pubsub_dao import AsyncPubSubPublisherDAO

dao = AsyncPubSubPublisherDAO(project_id="prodect-dev")
try:
    await dao.publish_message(topic_name="topic", payload=b"asdfsdf", attributes={"kitId": "AW12345678"})
except Exception as ex:
    print(ex)
```
- async worker

```python
import asyncio
import sys

sys.path.append("./")

from gcp_pubsub_dao import AsyncPubSubSubscriberDAO
from gcp_pubsub_dao.worker_pool import WorkerPool, WorkerTask, HandlerResult
from gcp_pubsub_dao.entities import Message


async def handler1(message: Message):
    print(f"handler1: {message}")
    await asyncio.sleep(2)
    return HandlerResult(ack_id=message.ack_id, is_success=True)


async def handler2(message: Message):
    print(f"handler2: {message}")
    await asyncio.sleep(5)
    return HandlerResult(ack_id=message.ack_id, is_success=True)


async def main():
    tasks = [
        WorkerTask(
            subscriber_dao=AsyncPubSubSubscriberDAO(project_id="ash-dev-273120", subscription_id="http-sender-sub"),
            handler=handler1,
        ),
        WorkerTask(
            subscriber_dao=AsyncPubSubSubscriberDAO(project_id="ash-dev-273120", subscription_id="email-sender-sub"),
            handler=handler2,
        ),
    ]
    wp = WorkerPool()
    await wp.run(tasks=tasks)


if __name__ == "__main__":
    asyncio.run(main())
```