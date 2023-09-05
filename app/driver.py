import multiprocessing

import tasks.task_executor as task_executor
import tasks.task_monitor as task_monitor
import tasks.task_planner as task_planner
from utils.config_utils import parse_config
from db.db_utils import DatabaseConnector

config_file = 'config.json'
config_details = parse_config(config_file)
db_connector = DatabaseConnector(config_details)


def execute_task():
    task_executor.TaskExecutor(config_details).execute()


def execute_plan():
    task_planner.TaskPlanner(config_details).create_plan()


def execute_monitor():
    task_monitor.TaskMonitor(config_details).monitor_events()


if __name__ == '__main__':
    multiprocessing.Process(target=execute_task).start()
    multiprocessing.Process(target=execute_plan).start()
    multiprocessing.Process(target=execute_monitor).start()
