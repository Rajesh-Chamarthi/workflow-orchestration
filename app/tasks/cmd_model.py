import logging
from dataclasses import dataclass

logging.basicConfig(
    filename='orchestrator.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


@dataclass
class CommandDetails:
    feed_id: int
    supplier_id: int
    batch_id: int
    file_name: str


def parse_command(command):
    try:
        # TODO check if dead queue needs to be maintained for faulty events.
        cmd = CommandDetails(
            feed_id=command['feedId'],
            supplier_id=command['supplierId'],
            batch_id=command['batchId'],
            file_name=command['fileName']
        )
        return cmd
    except Exception as e:
        logging.error("An error occurred while parsing command %s . Error details : %s", command, str(e))
