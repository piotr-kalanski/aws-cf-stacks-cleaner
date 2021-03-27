from cloud_formation_remover import _can_be_removed


def test_dev_env_can_not_be_removed():
    assert not _can_be_removed({
        'Tags': [
            {
                'Key': 'environment',
                'Value': 'dev'
            }
        ]
    })
