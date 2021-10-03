# python-sqs-dynamodb
Send message for a queue sqs, consumer and persiste in a dinamoDB

# Docker Compose for localstack

version: '2.1'
services:
  localstack:
    image: localstack/localstack-full
    network_mode: bridge
    ports:
      - "4566:4566"
      - "4571:4571"
      - "${PORT_WEB_UI-8080}:${PORT_WEB_UI-8080}"
    environment:
      - SERVICES=${SERVICES- }
      - DEBUG=${DEBUG- }
      - DATA_DIR=/home/silverlight/Projects/localstack
      - PORT_WEB_UI=${PORT_WEB_UI- }
      - LAMBDA_EXECUTOR=${LAMBDA_EXECUTOR- }
      - KINESIS_ERROR_PROBABILITY=${KINESIS_ERROR_PROBABILITY- }
      - DOCKER_HOST=unix:///var/run/docker.sock
      - HOST_TMP_FOLDER=${TMPDIR}
    volumes:
      - "${TMPDIR:-/tmp/localstack}:/home/silverlight/Projects/localstack"
      - "/var/run/docker.sock:/var/run/docker.sock"

# Commands for create topic, send message, receive message and create table in dynamo


aws --endpoint-url=http://localhost:4566 sqs send-message --queue-url http://localhost:4566/queue/teste --message-body "Mensagem de teste"

aws --endpoint-url=http://localhost:4566 sqs receive-message --queue-url http://localhost:4566/queue/teste --max-number-of-messages 10  

aws --endpoint-url=http://localhost:4566 sqs create-queue --queue-name test_queue


aws dynamodb create-table --table-name python --attribute-definitions AttributeName=pk,AttributeType=S AttributeName=sk,AttributeType=S --key-schema AttributeName=pk,KeyType=HASH AttributeName=sk,KeyType=RANGE --provisioned-throughput ReadCapacityUnits=5,WriteCapacityUnits=5 --endpoint-url http://localhost:4566