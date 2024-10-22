# -*- coding: utf-8 -*-
###############################################################################
#  Author:   Gérald Fenoy, gerald.fenoy@geolabs.fr
#  Copyright (c) 2020-2023, GeoLabs SARL.
###############################################################################
#  Permission is hereby granted, free of charge, to any person obtaining a
#  copy of this software and associated documentation files (the "Software"),
#  to deal in the Software without restriction, including without limitation
#  the rights to use, copy, modify, merge, publish, distribute, sublicense,
#  and/or sell copies of the Software, and to permit persons to whom the
#  Software is furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included
#  in all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
#  OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
#  THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
#  FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
#  DEALINGS IN THE SOFTWARE.
################################################################################
import zoo
from loguru import logger


def workspaceApi(conf, inputs, outputs):
    conf["additional_parameters"] = {}
    conf["additional_parameters"]["APP"] = "zoo-project-dru"
    conf["additional_parameters"]["STAGEIN_AWS_REGION"] = "RegionOne"
    conf["additional_parameters"]["STAGEIN_AWS_ACCESS_KEY_ID"] = "minio-admin"
    conf["additional_parameters"][
        "STAGEIN_AWS_SECRET_ACCESS_KEY"
    ] = "minio-secret-password"
    conf["additional_parameters"][
        "STAGEIN_AWS_SERVICEURL"
    ] = "http://s3-service.zoo.svc.cluster.local:9000"
    conf["additional_parameters"]["STAGEOUT_AWS_REGION"] = "RegionOne"
    conf["additional_parameters"]["STAGEOUT_AWS_ACCESS_KEY_ID"] = "minio-admin"
    conf["additional_parameters"][
        "STAGEOUT_AWS_SECRET_ACCESS_KEY"
    ] = "minio-secret-password"
    conf["additional_parameters"][
        "STAGEOUT_AWS_SERVICEURL"
    ] = "http://s3-service.zoo.svc.cluster.local:9000"
    conf["additional_parameters"]["STAGEOUT_OUTPUT"] = "s3://processingresults"
    return zoo.SERVICE_SUCCEEDED


def securityIn(conf, inputs, outputs):
    import sys, os, shutil

    if "servicesNamespace" in conf and "debug" in conf["servicesNamespace"]:
        logger.info("securityIn!")
    workspaceApi(conf, inputs, outputs)
    conf["pod_env_vars"] = {"A": "1", "B": "2"}
    conf["pod_node_selector"] = {} #{"C": "3"}
    try:
        if (
            "has_jwt_service" in conf["servicesNamespace"]
            and conf["servicesNamespace"]["has_jwt_service"] == "true"
        ):
            import jwts.security_service as s

            res = s.securityIn(conf, inputs, outputs)
            s.addHeader(conf, "dru.securityIn")
            if res == zoo.SERVICE_FAILED:
                logger.error("dru.securityIn has failed")
                return res
    except Exception as e:
        if "servicesNamespace" in conf and "debug" in conf["servicesNamespace"]:
            logger.error(f"No JWT service available: {str(e)}")
    rPath = conf["servicesNamespace"]["path"] + "/"
    for i in conf["renv"]:
        if i.count("SERVICES_NAMESPACE"):
            rPath += conf["renv"][i]
            if "auth_env" not in conf:
                conf["auth_env"] = {"user": conf["renv"][i], "cwd": rPath}
            else:
                conf["auth_env"]["user"] = conf["renv"][i]
                conf["auth_env"]["cwd"] = rPath
            conf["lenv"]["fpm_user"] = conf["renv"][i]
            conf["lenv"]["fpm_cwd"] = rPath
            # conf["lenv"]["cwd"]=rPath
            conf["zooServicesNamespace"] = {"namespace": conf["renv"][i], "cwd": rPath}
            conf["main"]["tmpPath"] = rPath + "/temp"
        if i.count("REDIRECT_QUERY_STRING") and conf["renv"][i].count("/package"):
            if conf["renv"]["HTTP_ACCEPT"] == "application/cwl+json":
                print(
                    "Conversion to cwl+json should happen in securityOut",
                    file=sys.stderr,
                )
                conf["renv"]["HTTP_ACCEPT"] = "application/cwl"
                conf["lenv"]["require_conversion_to_json"] = "true"
    if not (os.path.isdir(rPath)):
        logger.info(f"Creating directory {rPath}")
        os.mkdir(rPath)
        os.mkdir(rPath + "/temp")
        if "required_files" in conf["servicesNamespace"]:
            rFiles = conf["servicesNamespace"]["required_files"].split(",")
            for i in range(len(rFiles)):
                logger.info(f"Copy file {rFile[i]}")
                shutil.copyfile(
                    conf["renv"]["CONTEXT_DOCUMENT_ROOT"] + "/" + rFiles[i],
                    rPath + "/" + rFiles[i],
                )
    try:
        print(conf["auth_env"], file=sys.stderr)
    except Exception as e:
        print(e, file=sys.stderr)
    return zoo.SERVICE_SUCCEEDED


def securityOut(conf, inputs, outputs):
    import sys

    try:
        if (
            "has_jwt_service" in conf["servicesNamespace"]
            and conf["servicesNamespace"]["has_jwt_service"] == "true"
        ):
            import jwts.security_service as s

            s.addHeader(conf, "dru.securityOut")
    except Exception as e:
        if "servicesNamespace" in conf and "debug" in conf["servicesNamespace"]:
            print("No JWT service available: " + str(e), file=sys.stderr)
    if "servicesNamespace" in conf and "debug" in conf["servicesNamespace"]:
        print("securityOut!", file=sys.stderr)
    if (
        "require_conversion_to_json" in conf["lenv"]
        and conf["lenv"]["require_conversion_to_json"] == "true"
    ):
        import json
        import yaml

        if "require_conversion_to_ogcapppkg" in conf["lenv"]:
            conf["lenv"]["json_response_object"] = json.dumps(
                {
                    "executionUnit": {
                        "value": yaml.safe_load(conf["lenv"]["json_response_object"]),
                        "mediaType": "application/cwl+json",
                    }
                },
                indent=2,
            )
        else:
            conf["lenv"]["json_response_object"] = json.dumps(
                yaml.safe_load(conf["lenv"]["json_response_object"]), indent=2
            )
    return zoo.SERVICE_SUCCEEDED


def runDismiss(conf, inputs, outputs):
    import sys

    import json
    import os
    from loguru import logger
    from zoo_calrissian_runner import ZooCalrissianRunner
    from pycalrissian.context import CalrissianContext

    logger.remove()
    logger.add(sys.stderr, level="INFO")
    try:
        if "param" in inputs:
            print(inputs, file=sys.stderr)
            json_object = json.loads(inputs["param"]["value"])
            session = CalrissianContext(
                namespace=ZooCalrissianRunner.shorten_namespace(
                    json_object["processID"].replace("_", "-")
                    + "-"
                    + conf["lenv"]["gs_usid"]
                ),
                storage_class=os.environ.get("STORAGE_CLASS", "openebs-nfs-test"),
                volume_size="10Mi",
            )
        logger.info(f"Dispose namespace {session.namespace}")
        session.dispose()
    except Exception as e:
        logger.error(str(e))

    return zoo.SERVICE_SUCCEEDED


def browse(conf, inputs, outputs):
    import sys

    f = open(
        conf["servicesNamespace"]["path"]
        + "/"
        + conf["renv"]["REDIRECT_REDIRECT_SERVICES_NAMESPACE"]
        + "/temp/"
        + inputs["directory"]["value"],
        "r",
        encoding="utf-8",
    )
    if f is not None:
        if "result" not in outputs:
            outputs["result"] = {}
        outputs["result"]["value"] = f.read()
        return zoo.SERVICE_SUCCEEDED
    conf["lenv"]["message"] = "Unable to access the file"
    return zoo.SERVICE_FAILED
