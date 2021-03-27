import logging
from typing import List
from datetime import datetime, timezone

import boto3


_client = boto3.client('cloudformation')


def _get_cloud_formation_stacks() -> List[dict]:
    logging.info("Listing all Cloud Formation stacks")
    result = []
    response = _client.describe_stacks()
    result.extend(response.get('Stacks'))
    next_token = response.get('NextToken')
    while next_token:
        response = _client.describe_stacks(NextToken=next_token)
        result.extend(response.get('Stacks'))
        next_token = response.get('NextToken')
    return result


def __get_tag_value(tags: List[dict], key: str) -> str:
    r = [t['Value'] for t in tags if t['Key'] == key]
    if len(r) > 0:
        return r[0]
    else:
        return None


def _can_be_removed(stack: dict):
    stack_name = stack.get('StackName')
    tags = stack.get('Tags')
    last_updated_time = stack.get('LastUpdatedTime')

    environment_tag = __get_tag_value(tags, 'environment')

    now = datetime.now(timezone.utc)
    
    # this is example rule when stack can be removed, it can be adapted to needs
    if environment_tag == 'dev':
        if not stack_name.startswith("dev"):
            if last_updated_time:
                if (now - last_updated_time).days > 360:
                    return True

    return False


def _remove_stack(stack: dict):
    logging.info("Removing stack: " + str(stack))
    _client.delete_stack(
        StackName=stack.get('StackName')
    )


def delete_old_cloud_formation_stacks():
    logging.info("Start delete Cloud Formation stacks")
    for stack in _get_cloud_formation_stacks():
        if _can_be_removed(stack):
            _remove_stack(stack)
