import os
import sys
import traceback
import yaml
import json
import boto3  # noqa: F401
import botocore
from loguru import logger
from urllib.parse import urlparse
from botocore.exceptions import ClientError
from botocore.client import Config
from pystac import read_file
from pystac.stac_io import DefaultStacIO, StacIO
from pystac.item_collection import ItemCollection

logger.remove()
logger.add(sys.stderr, level="INFO")


class CustomStacIO(DefaultStacIO):
    """Custom STAC IO class that uses boto3 to read from S3."""

    def __init__(self):
        self.session = botocore.session.Session()
        self.s3_client = self.session.create_client(
            service_name="s3",
            region_name="it-rom",
            endpoint_url="{{ include "zoo-project-dru.argo.minio.endpoint" . }}",
            aws_access_key_id="{{ include "zoo-project-dru.argo.minio.accessKey" . }}",
            aws_secret_access_key="{{ include "zoo-project-dru.argo.minio.secretKey" . }}",
        )

    def read_text(self, source, *args, **kwargs):
        parsed = urlparse(source)
        if parsed.scheme == "s3":
            return (
                self.s3_client.get_object(Bucket=parsed.netloc, Key=parsed.path[1:])[
                    "Body"
                ]
                .read()
                .decode("utf-8")
            )
        else:
            return super().read_text(source, *args, **kwargs)

    def write_text(self, dest, txt, *args, **kwargs):
        parsed = urlparse(dest)
        if parsed.scheme == "s3":
            self.s3_client.put_object(
                Body=txt.encode("UTF-8"),
                Bucket=parsed.netloc,
                Key=parsed.path[1:],
                ContentType="application/geo+json",
            )
        else:
            super().write_text(dest, txt, *args, **kwargs)


StacIO.set_default(CustomStacIO)

s3_catalog_output = "{{`{{inputs.parameters.stac-catalog}}`}}"
logger.info("Post execution hook")

StacIO.set_default(CustomStacIO)

logger.info(f"Read catalog from STAC Catalog URI: {s3_catalog_output}")

cat = read_file(s3_catalog_output)

collection = next(cat.get_all_collections())

logger.info("Got collection {collection.id} from processing outputs")

item_collection = ItemCollection(items=collection.get_all_items())

logger.info("Created feature collection from items")

# save the feature collection to a file /tmp/output
with open("/tmp/output", "w") as f:
    f.write(json.dumps(item_collection.to_dict(), indent=2))
logger.info("Saved feature collection to /tmp/output")
