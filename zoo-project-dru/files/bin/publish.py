#!/usr/bin/python3
import os
import sys
import configparser
import osgeo.ogr as ogr
{{- if .Values.notifications.enabled }}
import requests
import json
import configparser
from cloudevents.http import CloudEvent
from cloudevents.conversion import to_binary
{{- end }}
import redis
data = sys.stdin.read();

print('Content-Type: text/html')
print('')
print('')

#print(data)

from urllib import parse

# Ensure that only the zoofpm pod is allowed to invoke the publish CGI script
config = configparser.ConfigParser()
config.read("/usr/lib/cgi-bin/main.cfg")
driver = ogr.GetDriverByName("PostgreSQL")
connection_string=""
for key in config["database"]:
    if key != "type" and key != "schema":
        connection_string += f"{key}={config['database'][key]} "
ds=driver.Open(f"PG:{connection_string}")
layer=ds.ExecuteSQL("SELECT host from servers")
if layer is not None and layer.GetFeatureCount() > 0:
    hasAddress = False
    for i in range(layer.GetFeatureCount()):
        host = layer.GetFeature(i).GetFieldAsString("host")
        if os.environ["REMOTE_ADDR"] == host:
            print("You are allowed to publish this job", file=sys.stderr)
            hasAddress = True
            break
    if not(hasAddress):
        print("You are not allowed to publish this job", file=sys.stderr)
        sys.exit(0)
else:
    print("You are not allowed to publish this job", file=sys.stderr)
    sys.exit(0)

{{- if .Values.redis.enabled }}
try:
    params=parse.parse_qs(os.environ["QUERY_STRING"])
    r=None
    if "ZOO_REDIS_HOST" in os.environ:
        r = redis.Redis(host=os.environ["ZOO_REDIS_HOST"], port=6379, db=0)
    else:
        r = redis.Redis(host='{{ .Release.Name }}-redis-master', port=6379, db=0)
    print(params,file=sys.stderr)
    r.publish(params["jobid"][0],data)
except Exception as e:
	print(e,file=sys.stderr)
{{- end }}

{{- if .Values.notifications.enabled }}
k_sink = os.environ.get("K_SINK", None)
k_ce_overrides_str = os.environ.get("K_CE_OVERRIDES", None)
configp = configparser.ConfigParser()
configp.read("/usr/lib/cgi-bin/oas.cfg")
try:
    if k_sink is not None:
        params=parse.parse_qs(os.environ["QUERY_STRING"])
        #print(params,file=sys.stderr)
        #print(f"k_sink: {k_sink}",file=sys.stderr)
        # TODO: detect the userid and add it to the URLs
        data = json.loads(data)
        host_name = configp["openapi"]["rootUrl"]
        root_path = configp["openapi"]["rootPath"]
        try:
            job_id = data["id"]
            attributes = {
                "type": "org.eoepca.ogc-api-processes-notification.job.update",
                "source": f"{host_name}/{root_path}/job/{job_id}",
                "datacontenttype": "application/json",
                "dataschema": "https://schemas.opengis.net/ogcapi/processes/part1/1.0/openapi/schemas/statusInfo.yaml",
                "jobid": job_id
            }
        except:
            data = data["stac"]["value"]
            job_id = data["id"]
            attributes = {
                "type": "org.eoepca.ogc-api-processes-notification.job.result",
                "source": f"{host_name}/{root_path}/job/{job_id}/results",
                "datacontenttype": "application/json",
                #"dataschema": "https://schemas.opengis.net/ogcapi/processes/part1/1.0/openapi/schemas/results.yaml",
                "dataschema": "https://schemas.opengis.net/ogcapi/features/part1/1.0/openapi/schemas/featureCollectionGeoJSON.yaml",
                "jobid": job_id
            }

        event = CloudEvent(attributes, data)
        headers, body = to_binary(event)
        #print(f"k_sink send {body}",file=sys.stderr)
        requests.post(k_sink, data=body, headers=headers)
        #print(f"k_sink received {body}",file=sys.stderr)
    else:
        print(f"k_sink is undefined",file=sys.stderr)
except Exception as e:
	print(e,file=sys.stderr)

{{- end }}


