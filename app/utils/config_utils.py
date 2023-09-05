import json
from dataclasses import dataclass


@dataclass
class AwsConfigDetails:
    region: str
    endpoint_url: str
    cmd_queue_url: str
    event_queue_url: str
    aws_access_key_id: str
    aws_secret_access_keys: str


@dataclass
class DatabaseConfigDetails:
    db_name: str
    user: str
    password: str
    host: str
    port: int


@dataclass
class TableDetails:
    job_log: str
    pipeline_ref: str
    feed_config_ref: str


@dataclass
class ConfigDetails:
    database: DatabaseConfigDetails
    aws: AwsConfigDetails
    tables: TableDetails


def parse_config(config_file):
    with open(config_file, 'r') as f:
        config = json.load(f)

    db_details = DatabaseConfigDetails(
        db_name=config['database']['dbName'],
        user=config['database']['user'],
        password=config['database']['password'],
        host=config['database']['host'],
        port=config['database']['port']

    )

    table_details = TableDetails(
        job_log=config['tables']['jobLog'],
        pipeline_ref=config['tables']['pipelineRef'],
        feed_config_ref=config['tables']['dataFeedRef']
    )

    aws_details = AwsConfigDetails(
        region=config['aws']['region'],
        endpoint_url=config['aws']['endpointUrl'],
        cmd_queue_url=config['aws']['cmdQueueUrl'],
        event_queue_url=config['aws']['eventQueueUrl'],
        aws_access_key_id=config['aws']['awsAccessKeyId'],
        aws_secret_access_keys=config['aws']['awsSecretAccessKeys']
    )

    config_details = ConfigDetails(
        database=db_details,
        aws=aws_details,
        tables=table_details
    )

    return config_details
