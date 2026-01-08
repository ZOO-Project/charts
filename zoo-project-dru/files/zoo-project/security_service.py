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


def securityIn(conf, inputs, outputs):
    import os
    if "servicesNamespace" in conf and "debug" in conf["servicesNamespace"]:
        zoo.debug("securityIn")
    try:
        if (
            "has_jwt_service" in conf["servicesNamespace"]
            and conf["servicesNamespace"]["has_jwt_service"] == "true"
        ):
            import jwts.security_service as s

            res = s.securityIn(conf, inputs, outputs)
            s.addHeader(conf, "dru.securityIn")
            if res == zoo.SERVICE_FAILED:
                zoo.error("dru.securityIn has failed")
{{- if .Values.eoapi.enabled }}
                if conf["renv"]["REQUEST_URI"].count("/collections"):
                    pass
                else:
                    return res
{{- else }}
                return res
{{- end }}
    except Exception as e:
        if "servicesNamespace" in conf and "debug" in conf["servicesNamespace"]:
            zoo.debug(f"No JWT service available: {str(e)}")
    rPath = conf["servicesNamespace"]["path"] + "/"
    has_rpath=False
    for i in conf["renv"]:
        if i.count("SERVICES_NAMESPACE"):
            if not(has_rpath):
                rPath += conf["renv"][i]
                has_rpath=True
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
        if i.count("QUERY_STRING") and conf["renv"][i].count("/package"):
            if conf["renv"]["HTTP_ACCEPT"] == "application/cwl+json":
                zoo.info("Conversion to cwl+json should happen in securityOut")
                conf["renv"]["HTTP_ACCEPT"] = "application/cwl"
                conf["lenv"]["require_conversion_to_json"] = "true"
{{- if and (.Values.iam.enabled) (.Values.iam.openeoAuth.enabled) }}
        import json
        if i.count("QUERY_STRING") and conf["renv"][i].count("/credentials"):
            import requests
            response = requests.get(
                conf["osecurity"]["openIdConnectUrl"],
                verify = False
            )
            if response.status_code == 200:
                jsonObject = response.json()
                jsonObject["id"]= {{ .Values.iam.realm | quote }}
                jsonObject["title"]= {{ .Values.iam.openeoAuth.title | quote }}
                jsonObject["default_clients"]=[{
                    "id": {{ .Values.iam.realm | quote }},
                    "title": {{ .Values.iam.openeoAuth.title | quote }},
                    "grant_types": [
                        {{- range $i, $e := .Values.iam.openeoAuth.grant_types -}}
                        {{- if $i -}},{{ end -}}
                        {{- $e | quote -}}
                        {{- end -}}
                    ],
                    "redirect_urls": [
                        {{- range $i, $e := .Values.iam.openeoAuth.redirect_uris -}}
                        {{- if $i -}},{{ end -}}
                        {{- $e | quote -}}
                        {{- end -}}
                    ],
                }]
                resultObject={"providers": [jsonObject]}
                conf["lenv"]["response"]=json.dumps(resultObject)
                conf["headers"]["Content-Type"]="application/json"
                conf["headers"]["Status"]="200 OK"
        if i.count("QUERY_STRING") and conf["renv"][i].count("/me")>0:
            conf["headers"]["Content-Type"]="application/json"
            conf["headers"]["Status"]="200 OK"
            conf["lenv"]["response"]=conf["lenv"]["json_user"]
{{- end }}


    if not(has_rpath):
        rPath += "anonymous"
        conf["lenv"]["fpm_user"] = "anonymous"
        conf["lenv"]["fpm_cwd"] = rPath
        conf["auth_env"] = {"user": "anonymous","cwd": rPath}
        conf["main"]["tmpPath"]=rPath+"/temp"
        conf["zooServicesNamespace"] = {"namespace": "anonymous","cwd": rPath}

    if not (os.path.isdir(rPath)):
        import shutil
        zoo.info(f"Creating directory {rPath}")
        os.mkdir(rPath)
        os.mkdir(rPath + "/temp")
        if "required_files" in conf["servicesNamespace"]:
            rFiles = conf["servicesNamespace"]["required_files"].split(",")
            for i in range(len(rFiles)):
                zoo.info(f"Copy file {rFiles[i]}")
                shutil.copyfile(
                    conf["renv"]["CONTEXT_DOCUMENT_ROOT"] + "/" + rFiles[i],
                    rPath + "/" + rFiles[i],
                )
    if "auth_env" not in conf:
        zoo.warning("No auth_env section found")
    return zoo.SERVICE_SUCCEEDED


def securityOut(conf, inputs, outputs):

    try:
        if (
            "has_jwt_service" in conf["servicesNamespace"]
            and conf["servicesNamespace"]["has_jwt_service"] == "true"
        ):
            import jwts.security_service as s

            s.addHeader(conf, "dru.securityOut")
    except Exception as e:
        if "servicesNamespace" in conf and "debug" in conf["servicesNamespace"]:
            zoo.debug("No JWT service available: " + str(e))
    if "servicesNamespace" in conf and "debug" in conf["servicesNamespace"]:
        zoo.debug("securityOut")
    if (
        "json_response_object" in conf["lenv"] and
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
{{- if and (.Values.iam.enabled) (.Values.iam.openeoAuth.enabled) }}
    import json
    for i in conf["renv"]:
        if i.count("QUERY_STRING")>0 and len(conf["renv"][i])==1:
            jsonObjectResponse=json.loads(conf["lenv"]["json_response_object"])
            jsonObjectResponse["endpoints"]=[
                {"path":"/credentials/oidc","methods":["GET"]},
                {"path":"/me","methods":["GET"]},
                {"path":"/processes","methods":["GET"]},
                {"path":"/processes/{process_id}","methods":["GET"]},
                {"path":"/processes/{process_id}/execution","methods":["POST"]},
                {"path":"/jobs","methods":["GET"]},
                {"path":"/jobs/{job_id}","methods":["GET","DELETE"]},
                {"path":"/jobs/{job_id}/results","methods":["GET"]},
            ]
            jsonObjectResponse["provider"]={
                "name": conf["provider"]["providerName"],
                "url": conf["provider"]["providerSite"],
                "description": conf["identification"]["abstract"],
                "roles": [
                    "processor"
                ]
            }
            jsonObjectResponse["stac_version"]="1.0.0"
            jsonObjectResponse["api_version"]="1.0.0"
            jsonObjectResponse["version"]="1.0.0"
            jsonObjectResponse["id"]=conf["identification"]["title"]
            jsonObjectResponse["type"]="Catalog"
            conf["lenv"]["json_response_object"]=json.dumps(jsonObjectResponse)
            return zoo.SERVICE_SUCCEEDED
        elif i.count("QUERY_STRING")>0:
                return zoo.SERVICE_SUCCEEDED
{{- end }}
    return zoo.SERVICE_SUCCEEDED


def runDismiss(conf, inputs, outputs):
    import sys
    import json
    import os
    from loguru import logger
    from zoo_calrissian_runner import ZooCalrissianRunner
    from pycalrissian.context import CalrissianContext

    zoo.info(f"runDismiss {str(conf['lenv'])}!")
    try:
        import configparser
        lenv_path=os.path.join(
            conf["main"]["tmpPath"],
            f"{conf['lenv']['gs_usid']}_lenv.cfg"
            )
        config=configparser.ConfigParser()
        config.read(lenv_path)
        if "run_id" in config["lenv"]:
            from zoo_wes_runner import ZooWESRunner
            wes=ZooWESRunner(
                cwl=None,
                conf=conf,
                inputs=inputs,
                outputs=outputs,
                execution_handler=None,
            )
            conf["lenv"]["run_id"]=config["lenv"]["run_id"]
            wes.dismiss()
            return zoo.SERVICE_SUCCEEDED
    except Exception as e:
        zoo.error(str(e))

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
        zoo.info(f"Dispose namespace {session.namespace}")
        session.dispose()
    except Exception as e:
        zoo.error(str(e))

    return zoo.SERVICE_SUCCEEDED


def browse(conf, inputs, outputs):
    redirect_url=None
    for i in conf["renv"]:
        if i.count("SERVICES_NAMESPACE")>0:
            redirect_url=conf["renv"][i]
    f = open(
        conf["servicesNamespace"]["path"]
        + "/"
        + redirect_url
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
