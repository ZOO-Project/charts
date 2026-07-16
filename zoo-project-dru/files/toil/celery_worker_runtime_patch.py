import os
from pathlib import Path


def patch_file(path, replacements):
    target = Path(path)
    if not target.exists():
        return
    source = target.read_text(encoding='utf-8')
    for old, new in replacements:
        source = source.replace(old, new)
    target.write_text(source, encoding='utf-8')


patch_file(
    '/usr/local/lib/python3.13/dist-packages/toil/server/wes/tasks.py',
    [
        ('import celery.states  # type: ignore', 'from celery import states as celery_states  # type: ignore'),
        ('celery.result.AsyncResult(task_id)', 'celery.AsyncResult(task_id)'),
        ('celery.states.FAILURE', 'celery_states.FAILURE'),
        ('celery.states.READY_STATES', 'celery_states.READY_STATES'),
        ('run_wes.apply_async(args=args, task_id=task_id, ignore_result=True)', 'run_wes.apply_async(args=args, task_id=task_id, ignore_result=False)'),
    ],
)

patch_file(
    '/usr/local/lib/python3.13/dist-packages/toil/server/celery_app.py',
    [
        ('app = Celery("toil_wes", broker=broker)', 'app = Celery("toil_wes", broker=broker, backend=os.environ.get("TOIL_WES_RESULT_BACKEND", "rpc://"))'),
    ],
)

if {{ ternary "True" "False" (not .Values.toilWes.s3.realaws) }}:
    patch_file(
        '/usr/local/lib/python3.13/dist-packages/toil/lib/aws/utils.py',
        [
            ('    s3_client.delete_public_access_block(Bucket=bucket_name)', '    return'),
            ('    s3_client.put_bucket_encryption(\n        Bucket=bucket_name,\n        ServerSideEncryptionConfiguration={\n            "Rules": [\n                {"BlockedEncryptionTypes": {"EncryptionType": ["NONE"]}},\n            ],\n        },\n    )', '    return'),
        ],
    )
