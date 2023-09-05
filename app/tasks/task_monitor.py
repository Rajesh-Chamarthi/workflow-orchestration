import json
import logging

import boto3
from botocore.exceptions import NoCredentialsError
import utils.logging_config as logging_config
from utils.batch_utils import JobHandler
from tasks.event_model import parse_event


class TaskMonitor:
    def __init__(self, config_details):
        self.config_details = config_details
        self.job_handler = JobHandler(config_details)
        self.logger = logging.getLogger(__name__)

    def monitor_events(self):
        aws_config = self.config_details.aws
        sqs = boto3.client('sqs',
                           region_name=aws_config.region,
                           endpoint_url=aws_config.endpoint_url,
                           aws_access_key_id=aws_config.aws_access_key_id,
                           aws_secret_access_key=aws_config.aws_secret_access_keys)
        while True:
            try:
                response = sqs.receive_message(
                    QueueUrl=aws_config.event_queue_url,
                    MaxNumberOfMessages=1,
                    WaitTimeSeconds=20
                )

                if 'Messages' in response:
                    for msg in response['Messages']:
                        event = parse_event(json.loads(msg['Body']))
                        self.job_handler.update_task(event.batch_id, event.task_name, event.task_status, event.error_message)
                        self.logger.info(f"[{event.batch_id},{event.task_name}] Clearing the event queue")
                        sqs.delete_message(
                            QueueUrl=aws_config.event_queue_url,
                            ReceiptHandle=msg['ReceiptHandle']
                        )
            except NoCredentialsError:
                self.logger.error("AWS credentials are invalid or missing for %s", aws_config.event_queue_url)
                raise
            except Exception as e:
                self.logger.error("An error occurred while processing SQS messages %s with error %s",
                                  aws_config.event_queue_url, str(e))

