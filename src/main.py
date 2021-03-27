import logging
from cloud_formation_remover import delete_old_cloud_formation_stacks


logging.getLogger().setLevel(logging.INFO)

def lambda_handler(event, context):
    logging.info("Start")
    delete_old_cloud_formation_stacks()
    logging.info("Finish")
