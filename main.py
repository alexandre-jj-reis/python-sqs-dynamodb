# This is a sample Python scri
import json
import boto3

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


url_queue = "http://localhost:4566/queue/python"
region = "eu-west-1"
url_endpoint = "http://localhost:4566"
save = '{"id":1,"nome":"Alexandre Reis","endereco":"R. Qualquer"}'


def put_people_dynamo(id, nome, endereco):
    dynamodb = boto3.resource(
        'dynamodb', endpoint_url=url_endpoint)
    # Specify the table
    devices_table = dynamodb.Table('python')
    response = devices_table.put_item(
        Item={
            'pk': '1',
            'sk': '2',
            'id': id,
            'nome': nome,
            'endereco': endereco
        }
    )
    print(response)


def send_message():
    sqs_client = boto3.client("sqs", aws_access_key_id=None,
                              aws_secret_access_key=None,
                              region_name=region,
                              endpoint_url=url_endpoint)

    resp = sqs_client.send_message(
                QueueUrl=url_queue,
                MessageBody=(
                    save
                )
            )
    print(resp['MessageId'])


def receive_message():
    sqs_client = boto3.client("sqs", region_name=region, endpoint_url=url_endpoint)
    response = sqs_client.receive_message(
        QueueUrl=url_queue,
        MaxNumberOfMessages=1,
        WaitTimeSeconds=10,
    )

    print(f"Number of messages received: {len(response.get('Messages', []))}")

    for message in response.get("Messages", []):
        message_body = message["Body"]
        receipt_handle = message['ReceiptHandle']

        # Delete received message from queue
        sqs_client.delete_message(
            QueueUrl=url_queue,
            ReceiptHandle=receipt_handle
        )

        print(f"Message body: {json.loads(message_body)}")
        print(f"Receipt Handle: {message['ReceiptHandle']}")
        return message_body


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    send_message()
    people = receive_message()
    put_people_dynamo(
        json.loads(people)['id'],
        json.loads(people)['nome'],
        json.loads(people)['endereco']
    )


