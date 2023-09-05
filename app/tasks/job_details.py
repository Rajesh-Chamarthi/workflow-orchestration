import logging


class JobDetails:
    def __init__(self, batch_id, file_name, supplier_id, feed_id, exec_order, task_name, load_status_cd):
        self.batch_id = batch_id
        self.file_name = file_name
        self.supplier_id = supplier_id
        self.feed_id = feed_id
        self.exec_order = exec_order
        self.task_name = task_name
        self.load_status_cd = load_status_cd
        self.logger = logging.getLogger(__name__)

    def __str__(self):
        return f"batch_id:{self.batch_id},file_name: {self.file_name}, supplier_id: {self.supplier_id}, feed_id: {self.feed_id}, exec_order: {self.exec_order}, task_name: {self.task_name}, task_status_cd: {self.load_status_cd}"