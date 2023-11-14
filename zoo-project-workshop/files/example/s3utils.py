import os
import sys
import zoo

# don't remove this import, it's needed for the botocore session
import boto3  # noqa: F401
import botocore
from botocore.exceptions import ClientError
import yaml
from urllib.parse import urljoin, urlparse
from loguru import logger
import requests
import subprocess

def s3_read(conf,inputs,outputs):
    import json
    source=inputs["s3_ref"]["value"]
    parsed = urlparse(inputs["s3_ref"]["value"])
    if parsed.scheme == "s3":
        with open('/assets/additional_inputs.yaml', 'r') as file:
                s3_settings = yaml.safe_load(file)
        for i in s3_settings.keys():
            os.environ[i]=s3_settings[i]

        session = botocore.session.Session()
        s3_client = session.create_client(
            service_name="s3",
            region_name=os.environ.get("STAGEOUT_AWS_REGION"),
            use_ssl=True,
            endpoint_url=os.environ.get("STAGEOUT_AWS_SERVICEURL"),
            aws_access_key_id=os.environ.get("STAGEOUT_AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.environ.get("STAGEOUT_AWS_SECRET_ACCESS_KEY"),
        )

        bucket = parsed.netloc
        key = parsed.path[1:]

        try:
            outputs["result"]["value"] = (
                s3_client.get_object(Bucket=bucket, Key=key)["Body"]
                .read()
                .decode("utf-8")
            )
            return zoo.SERVICE_SUCCEEDED
        except ClientError as ex:
            if ex.response["Error"]["Code"] == "NoSuchKey":
                logger.error(f"Error reading {source}: {ex}")
                conf["lenv"]["message"]+=f"\nError reading {source}: {ex}"
                return zoo.SERVICE_FAILED
    else:
        conf["lenv"]["message"]="Unable to find any S3 URI from your string"
        return zoo.SERVICE_FAILED

def s3_download(conf,inputs,outputs):
    fileName=conf["main"]["tmpPath"]+"/file-"+conf["lenv"]["usid"]+".tif"
    oldOutFd = os.dup(sys.stdout.fileno())
    oldOut = sys.stdout
    os.dup2(sys.stderr.fileno(),1)
    out = subprocess.run('s3cmd get '+inputs["s3_ref"]["value"]+" "+fileName, shell=True)
    sys.stdout.flush()
    os.dup2(oldOutFd, oldOut.fileno())
    sys.stdout = oldOut
    outputs["result"]["generated_file"]=fileName
    return zoo.SERVICE_SUCCEEDED

