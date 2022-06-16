import json

import localstack_client.session as boto3


class QueueService:

    def __init__(self, queue_url):
        # Create the client once so we don't need to be instantiated every time we poll the queue
        self.sqs_client = boto3.client('sqs')
        self.queue_url = queue_url

    # Gets a message from the SQS queue. Returns an array of JSON message bodies.
    def get_messages(self, max_request_messages):
        if self.sqs_client is None or self.queue_url is None:
            return []

        # Array to hold return values
        return_bodies = []

        # Array to hold messages that need deleted after being read
        messages_to_delete = []
        messages_object = self.sqs_client.receive_message(
            QueueUrl=self.queue_url,
            MaxNumberOfMessages=max_request_messages)

        if 'Messages' not in messages_object:
            return []
        for message in messages_object['Messages']:

            # Ensure that the response is properly filled out
            if any(subscript not in message for subscript in ['ReceiptHandle', 'Body', 'MessageId']):
                continue

            # Fill response object with message body JSON
            return_bodies.append(json.loads(message['Body']))

            # Add message to be deleted
            messages_to_delete.append(
                {
                    'Id': message['MessageId'],
                    'ReceiptHandle': message['ReceiptHandle']
                }
            )

        # Delete retrieved messages
        self.sqs_client.delete_message_batch(
            QueueUrl=self.queue_url,
            Entries=messages_to_delete)

        return return_bodies
