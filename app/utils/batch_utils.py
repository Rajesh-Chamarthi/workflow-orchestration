import logging

from db.db_utils import DatabaseConnector
import utils.logging_config as logging_config
from tasks.job_details import JobDetails


class JobHandler:
    def __init__(self, config_details):
        self.config_details = config_details
        self.table_details = config_details.tables
        self.db_connector = DatabaseConnector(config_details)
        self.db_connector.connect()
        self.logger = logging.getLogger(__name__)

    def fetch_pending_tasks(self):
        try:
            cursor = self.db_connector.get_connection().cursor()
            query = f"""select j.batch_id,j.file_name,j.supplier_id,j.feed_id,j.exec_order
                ,j.task_name, j.load_status_cd
                    from (select batch_id,file_name,supplier_id,feed_id,exec_order,task_name,
                    load_status_cd from {self.table_details.job_log}) j
                        join (select batch_id,
                        coalesce(max(case when load_status_cd = 'completed' then exec_order end),0) as completed_exec_order
                            from {self.table_details.job_log} group by batch_id
                            ) prev ON j.batch_id = prev.batch_id AND j.exec_order = prev.completed_exec_order + 1
                    where j.load_status_cd = 'pending'
            """
            cursor.execute(query)
            pending_tasks = cursor.fetchall()
            return [JobDetails(*task) for task in pending_tasks]
        except Exception as e:
            self.logger.error("Error occurred in fetching pending tasks: %s", str(e))
            return []

    def update_task(self, batch_id, task_name, status, error_message=None):
        try:
            con = self.db_connector.get_connection()
            cursor = con.cursor()
            query = f"""update job_log set load_status_cd = '{status}', error_msg = '{error_message}'
            where batch_id = {batch_id} and task_name='{task_name}'
            """
            cursor.execute(query)
            con.commit()
            cursor.close()
        except Exception as e:
            self.logger.error("[%s,%s] Error in updating task status to running: %s", batch_id, task_name, str(e))

    def persist_plan(self, batch_details):
        batch_id = batch_details.batch_id
        file_name = batch_details.file_name
        supplier_id = batch_details.supplier_id
        feed_id = batch_details.feed_id
        try:
            con = self.db_connector.get_connection()
            cursor = con.cursor()
            query = f"""insert into {self.table_details.job_log} (batch_id, feed_id, pipeline_id, supplier_id,
                        file_name, task_name, exec_order, load_status_cd,error_msg, cre_ts, updt_ts)
                        select {batch_id} as batch_id , dfc.feed_id ,dfc.pipeline_id ,dfc.supplier_id 
                        ,'{file_name}' as file_name , pd.task_name,pd.exec_order ,'pending' as load_status_cd
                        ,null as error_msg ,current_timestamp as cre_ts , current_timestamp as updt_ts 
                        from {self.table_details.feed_config_ref} dfc join {self.table_details.pipeline_ref} pd  
                        on dfc.pipeline_id = pd.pipeline_id 
                        and dfc.supplier_id = {supplier_id} and feed_id = {feed_id}  
            """
            cursor.execute(query)
            con.commit()
            cursor.close()
            self.logger.info(f"[{batch_id}] Created task plan for batch_id")
        except Exception as e:
            self.logger.error("An error occurred during status update: %s", str(e))

