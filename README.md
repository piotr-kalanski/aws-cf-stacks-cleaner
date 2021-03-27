# aws-cf-stacks-cleaner

Python script to remove old CloudFormation stacks

## Customization

Modify function `_can_be_removed` at [cloud_formation_remover.py](./src/cloud_formation_remover.py) to provide business rules when Cloud Formation stack can be removed.
