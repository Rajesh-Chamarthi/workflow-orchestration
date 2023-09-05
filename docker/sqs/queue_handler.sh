#!/bin/bash
echo "## Setting up localstack profile"
aws configure set aws_access_key_id dummy --profile=localstack
aws configure set aws_secret_access_key dummy --profile=localstack
aws configure set region us-east-2 --profile=localstack

echo "## Setting default profile"
export AWS_DEFAULT_PROFILE=localstack

export CMD_QUEUE_NM=command-queue
export EVT_QUEUE_NM=event-queue

echo "## Creating queues"
aws --endpoint-url=http://localstack:4566 sqs create-queue --queue-name $CMD_QUEUE_NM
aws --endpoint-url=http://localstack:4566 sqs create-queue --queue-name $EVT_QUEUE_NM

echo "## Listing queues"
aws --endpoint-url=http://localhost:4566 sqs list-queues


echo "## Putting message to the queue form file"
aws --endpoint-url=http://localhost:4566 sqs send-message --queue-url http://localstack:4566/000000000000/command-queue --message-body '{"batchId" : 152, "supplierId": 179,"fileName" : "inovalon_rx_file1", "feedId" : 177 }'
aws --endpoint-url=http://localhost:4566 sqs send-message --queue-url http://localstack:4566/000000000000/command-queue --message-body '{"batchId" : 153, "supplierId": 100,"fileName" : "officeally_file1", "feedId" : 425 }'
#aws --endpoint-url=http://localhost:4566 sqs send-message --queue-url http://localstack:4566/000000000000/event-queue --message-body '{"batchId" : 152, "taskName": 179,"taskStatus" : "completed", "errorMessage" : "" }' --profile localstack | cat

