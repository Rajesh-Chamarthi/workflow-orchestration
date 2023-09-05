import logging
from dataclasses import dataclass

logging.basicConfig(
    filename='orchestrator.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


@dataclass
class EventDetails:
    batch_id: int
    task_name: str
    task_status: str
    error_message: str


def parse_event(event):
    try:
        # TODO check if dead queue needs to be maintained for faulty events.
        evt = EventDetails(
            batch_id=event['batchId'],
            task_name=event['taskName'],
            task_status=event['taskStatus'],
            error_message=event['errorMessage']
        )
        return evt
    except Exception as e:
        logging.error("An error occurred while parsing event %s , Error Details: %s", event, str(e))
