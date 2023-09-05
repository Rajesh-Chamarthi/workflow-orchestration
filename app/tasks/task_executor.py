import logging
import time

import utils.logging_config as logging_config
from utils.batch_utils import JobHandler


class TaskExecutor:
    def __init__(self, config_details):
        self.config_details = config_details
        self.job_handler = JobHandler(config_details)
        self.logger = logging.getLogger(__name__)

    def execute_plan(self):
        try:
            self.logger.info("Fetching pending tasks")
            pending_tasks = self.job_handler.fetch_pending_tasks()
            for pending_task in pending_tasks:
                self.logger.info(f"[{pending_task.batch_id},{pending_task.task_name}] Creating K8 Pod")
                # TODO need to create K8 pod
                self.job_handler.update_task(pending_task.batch_id, pending_task.task_name, 'running')
        except Exception as e:
            self.logger.error("An error occurred during task execution: %s", str(e))

    def execute(self):
        while True:
            self.execute_plan()
            time.sleep(10)
