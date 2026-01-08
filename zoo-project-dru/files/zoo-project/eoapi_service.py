# -*- coding: utf-8 -*-
###############################################################################
#  Author:   Gérald Fenoy, gerald.fenoy@geolabs.fr
#  Copyright (c) 2023, GeoLabs SARL. 
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
import urllib.request
import sys
import json

def route(conf,path,rootUrl):
    cookies=None
    if "HTTP_COOKIE" in conf["renv"]:
        cookies=conf["renv"]["HTTP_COOKIE"]
    if cookies is None:
        req=urllib.request.Request(
                url=rootUrl+(conf["renv"]["REDIRECT_QUERY_STRING"].replace(path+"/","").replace("&","?",1))
                )
    else:
        req=urllib.request.Request(
                url=rootUrl+(conf["renv"]["REDIRECT_QUERY_STRING"].replace(path+"/","").replace("&","?",1)),
                headers={"Cookie": cookies}
                )
    try:
        zoo.debug(str(req.get_full_url()))
        response = urllib.request.urlopen(req)
        conf["headers"]["Content-Type"] = response.headers.get_content_type()
        if "Set-Cookie" in response.headers.keys():
            conf["headers"]["Set-Cookie"]=response.headers.get("Set-Cookie","")
            conf["renv"]["HTTP_COOKIE"]+="; "+conf["headers"]["Set-Cookie"]
        if conf["headers"]["Content-Type"].count("image")>0 or conf["headers"]["Content-Type"].count("font")>0 or (conf["renv"]["REDIRECT_QUERY_STRING"].count(".js")>0 and conf["renv"]["REDIRECT_QUERY_STRING"].count("openapi.json")==0 and conf["renv"]["REDIRECT_QUERY_STRING"].count("tilejson.json")==0) or conf["renv"]["REDIRECT_QUERY_STRING"].count(".css")>0:
            conf["headers"]["Content-Length"]=response.headers.get("content-length")
            with open(conf["main"]["tmpPath"]+"/"+conf["lenv"]["usid"]+".data", "wb") as binary_file:
                binary_file.write(response.read())
                binary_file.close()
            conf["lenv"]["response_generated_file"]=conf["main"]["tmpPath"]+"/"+conf["lenv"]["usid"]+".data"
        else:
            conf["lenv"]["response"]=response.read().decode("utf-8").replace(conf["osecurity"]["proxyFor"],"/"+conf["openapi"]["rootPath"]).replace(conf["osecurity"]["proxyForRaster"],"/"+conf["openapi"]["rootPath"]+"/raster").replace(conf["osecurity"]["proxyForVector"],"/"+conf["openapi"]["rootPath"]+"/vector").replace(conf["osecurity"]["proxyForAuth"],conf["openapi"]["rootHost"]+"/"+conf["openapi"]["rootPath"]+"/authenix").replace("/openapi.json","/"+conf["openapi"]["rootPath"]+"/"+path+"/openapi.json")#.replace("/collections/","/"+conf["openapi"]["rootPath"]+"/"+path+"/collections/").replace("/info","/info?assets=visual")
            if conf["renv"]["REDIRECT_QUERY_STRING"].count("openapi.json")>0 or conf["renv"]["REDIRECT_QUERY_STRING"].count("/api")>0:
                conf["lenv"]["response"]=conf["lenv"]["response"].replace("\"/","\"/"+conf["openapi"]["rootPath"]+"/"+path+"/")
                conf["lenv"]["response"]=conf["lenv"]["response"].replace("\"/"+conf["openapi"]["rootPath"]+"/"+path+"/"+conf["openapi"]["rootPath"]+"/"+path+"/","\"/"+conf["openapi"]["rootPath"]+"/"+path+"/")
            if path=="authenix":
                conf["lenv"]["response"]=conf["lenv"]["response"].replace("'/","'/"+conf["openapi"]["rootPath"]+"/"+path+"/")
                conf["lenv"]["response"]=conf["lenv"]["response"].replace(conf["osecurity"]["proxyForAuth1"],conf["openapi"]["rootHost"]+"/"+conf["openapi"]["rootPath"]+"/authenix")
                conf["lenv"]["response"]=conf["lenv"]["response"].replace(conf["osecurity"]["proxyForAuth2"],(conf["openapi"]["rootHost"].replace("https://",""))+"/"+conf["openapi"]["rootPath"]+"/authenix")
            zoo.debug(f"REDIRECT_QUERY_STRING: {conf['renv']['REDIRECT_QUERY_STRING']}")
            if conf["renv"]["REDIRECT_QUERY_STRING"]=="/stac/":
                conf["lenv"]["response"]=conf["lenv"]["response"].replace("\"/ogc-api/stac/\"","\"/ogc-api/\"")
            conf["lenv"]["response"]=conf["lenv"]["response"].replace("/ogc-api/raster/ogc-api/raster/","/ogc-api/raster/").replace("\"/ogc-api/stac/\"","\"/ogc-api/\"")
    except Exception as e:
        conf["lenv"]["message"]=str(e)
        zoo.error(f"Error accessing or rewriting the content: {str(e)}")
        return zoo.SERVICE_FAILED
    conf["headers"]["status"]="200 OK"
    return zoo.SERVICE_SUCCEEDED

def eoapiRoute(conf,inputs,outputs):
    import sys
    #rootUrl="https://tamn.snapplanet.io"
    #zoo.debug(f"eoapiRoute {str(conf['renv'])}")
    zoo.debug(conf["renv"]["REDIRECT_QUERY_STRING"])
    rootUrl=conf["osecurity"]["proxyFor"]
    if "REDIRECT_QUERY_STRING" in conf["renv"]:
        #zoo.debug("OK query string found")
        if conf["renv"]["REDIRECT_QUERY_STRING"].count("/credentials")>0:
            #zoo.debug("credentials")
            try:
                f=open(conf["main"]["tmpPath"]+"/openid.json","r")
                jsonObject=json.loads(f.read())
                jsonObject["id"]="ZOO-Project-secured-access"
                jsonObject["title"]="OpenId Connect Secured Access"
                jsonObject["default_clients"]=[{"id":"TB20","grant_types":["implicit","authorization_code+pkce","urn:ietf:params:oauth:grant-type:device_code+pkce"],"redirect_urls":["https://m-mohr.github.io/gdc-web-editor/","https://editor.openeo.org/"]}]
                resultObject={"providers": [jsonObject]}
                conf["lenv"]["response"]=json.dumps(resultObject)
                #conf["lenv"]["response_size"]=len(conf["lenv"]["response"])
                conf["headers"]["Content-Type"]="application/json"
                conf["headers"]["Status"]="200 OK"
                #print(conf["lenv"]["response"],file=sys.stderr)
            except Exception as e:
                print(e,file=sys.stderr)
        if conf["renv"]["REDIRECT_QUERY_STRING"].count("/me")>0:
            conf["headers"]["Content-Type"]="application/json"
            conf["headers"]["Status"]="200 OK"
            conf["lenv"]["response"]=conf["lenv"]["json_user"]

        if conf["renv"]["REDIRECT_QUERY_STRING"].count("/search")>0 or conf["renv"]["REDIRECT_QUERY_STRING"]=="/collections" or (conf["renv"]["REDIRECT_QUERY_STRING"].count("stac")==0 and conf["renv"]["REDIRECT_QUERY_STRING"].count("collections") and len(conf["renv"]["REDIRECT_QUERY_STRING"].split("/"))<=5):
            return route(conf,"stac",conf["osecurity"]["proxyFor"])
        if conf["renv"]["REDIRECT_QUERY_STRING"].count("/raster")>0:
            return route(conf,"raster",conf["osecurity"]["proxyForRaster"])
        if conf["renv"]["REDIRECT_QUERY_STRING"].count("/stac")>0:
            return route(conf,"stac",conf["osecurity"]["proxyFor"])
        if conf["renv"]["REDIRECT_QUERY_STRING"].count("/vector")>0:
            return route(conf,"vector",conf["osecurity"]["proxyForVector"])
        if conf["renv"]["REDIRECT_QUERY_STRING"].count("/authenix")>0:
            return route(conf,"authenix",conf["osecurity"]["proxyForAuth"])
        if conf["renv"]["REDIRECT_URL"].count("/cog/")>0:
            import urllib.parse
            zoo.debug(f"{conf['renv']['REDIRECT_QUERY_STRING']}")
            query_string=urllib.parse.unquote(conf["renv"]["QUERY_STRING"])
            zoo.debug(query_string)
            query_string=query_string.replace("/cog/tiles/","")
            elements=query_string.split("/")
            zoo.debug(f"{str(elements)}")
            z=elements[0]
            x=elements[1]
            pre_y=elements[2].split("@")
            y=pre_y[0]
            res=pre_y[1].replace("x","")
            zoo.debug(query_string)
            zoo.debug(f"{conf['renv']['QUERY_STRING']}")
            query_string=urllib.parse.parse_qs(conf["renv"]["REDIRECT_QUERY_STRING"])
            zoo.debug(f"{query_string}")
            query_string=query_string["url"][0]
            #s3_url=query_string.split("s3://results/")[1]
            if query_string.count("s3://eoepca/processing-results/")>0:
                s3_url=query_string.split("s3://eoepca/processing-results/")[1]
            if query_string.count("s3://eoepca/processing-results/")>0:
                s3_url=query_string.split("s3://eoepca/processing-results/")[1]
            zoo.debug(s3_url)
            elements1=s3_url.split("/")
            collectionid=elements1[0]
            itemid=elements1[1].replace("_pansharpened.tif","")
            if query_string.count("s3://eoepca/processing-results/")>0:
                http_request=(f"http://eoapi-raster.d122.preprod.svc.cluster.local:8080/collections/processing-results-{collectionid}/items/{itemid}/tiles/WebMercatorQuad/{z}/{x}/{y}@{res}x?bidx=1&assets=data&unscale=false&resampling=nearest&reproject=nearest&return_mask=true")
            else:
                http_request=(f"http://eoapi-raster.d122.preprod.svc.cluster.local:8080/collections/processing-results-{collectionid}/items/{itemid}/tiles/WebMercatorQuad/{z}/{x}/{y}@{res}x?bidx=3&bidx=2&bidx=1&assets={itemid}_pansharpened_tif&unscale=false&resampling=bilinear&reproject=bilinear&rescale=0%2C255&rescale=0%2C255&rescale=0%2C255&return_mask=true")
            zoo.debug(http_request)
            req=urllib.request.Request(http_request)
            response = urllib.request.urlopen(req)
            with open(conf["main"]["tmpPath"]+"/"+conf["lenv"]["usid"]+".data", "wb") as binary_file:
                binary_file.write(response.read())
                binary_file.close()
            conf["lenv"]["response_generated_file"]=conf["main"]["tmpPath"]+"/"+conf["lenv"]["usid"]+".data"
            conf["headers"]["status"]="200 OK"

        #if conf["renv"]["REDIRECT_QUERY_STRING"].count("/credentials/oidc")>0:
        #    req=urllib.request.Request(url=conf["osecurity"
    return zoo.SERVICE_SUCCEEDED

def securityOut(conf,inputs,outputs):
    zoo.debug("SECURITY OUT")
    try:
        if len(conf["renv"]["REDIRECT_QUERY_STRING"])==1: #or conf["renv"]["REDIRECT_QUERY_STRING"]=="/conformance":
            req=urllib.request.Request(
                    conf["openapi"]["rootUrl"]+"/conformance"
                    )
            response = urllib.request.urlopen(req)
            tmpResponseProcessing=response.read().decode("utf-8")
            req=urllib.request.Request(
                    url=conf["osecurity"]["proxyFor"]+"/"
                    )
            response = urllib.request.urlopen(req)
            tmpResponse=response.read().decode("utf-8").replace(conf["osecurity"]["proxyFor"],"/"+conf["openapi"]["rootPath"]+"/stac").replace(conf["osecurity"]["proxyForRaster"],"/"+conf["openapi"]["rootPath"]+"/raster").replace(conf["osecurity"]["proxyForVector"],"/"+conf["openapi"]["rootPath"]+"/vector")
            jsonObjectFetched=json.loads(tmpResponse)
            jsonObjectResponse=json.loads(conf["lenv"]["json_response_object"])
            jsonObjectProcesses=json.loads(tmpResponseProcessing)
            for a in range(len(jsonObjectProcesses["conformsTo"])):
                #zoo.debug(str(jsonObjectProcesses["conformsTo"][a]))
                if jsonObjectFetched["conformsTo"].count(jsonObjectProcesses["conformsTo"][a])==0 and jsonObjectProcesses["conformsTo"][a].count("transaction")==0:
                    jsonObjectFetched["conformsTo"]+=[(jsonObjectProcesses["conformsTo"][a])]
            for a in jsonObjectFetched:
                if a=="conformsTo":
                    jsonObjectResponse[a]=jsonObjectFetched[a]
                    to_remove=[]
                    for b in range(len(jsonObjectResponse["conformsTo"])):
                        if jsonObjectResponse["conformsTo"][b].count("transaction")>0:
                            to_remove+=[jsonObjectResponse["conformsTo"][b]]
                    #zoo.debug(str(to_remove))
                    for i in range(len(to_remove)):
                        jsonObjectResponse["conformsTo"].remove(to_remove[i])
            jsonObjectResponse["endpoints"]=[
                    {"path":"/credentials/oidc","methods":["GET"]},
                    {"path":"/me","methods":["GET"]},
                    {"path":"/collections","methods":["GET"]},
                    {"path":"/collections/{collection_id}","methods":["GET"]},
                    {"path":"/collections/{collection_id}/items","methods":["GET"]},
                    {"path":"/collections/{collection_id}/items/{item_id}","methods":["GET"]},
                    {"path":"/processes","methods":["GET"]},
                    {"path":"/processes/{process_id}","methods":["GET"]},
                    {"path":"/processes/{process_id}/execution","methods":["POST"]},
                    {"path":"/processes/{process_id}/package","methods":["GET"]},
                    {"path":"/jobs","methods":["GET","POST"]},
                    {"path":"/jobs/{job_id}","methods":["GET","DELETE"]},
                    {"path":"/jobs/{job_id}/results","methods":["GET"]},
                    {"path":"/jobs/{job_id}/prov","methods":["GET"]},
                    ]
            jsonObjectResponse["providers"]=[
                    {
                        "url": "https://www.geolabs.fr",
                        "name": "GeoLabs",
                        "description": "",
                        "roles": [
                            "producer",
                            "processor",
                            "licensor"
                        ],
                        "processing:facility": conf["identification"]["title"],
                    },
                    {
                        "url": "https://www.geolabs.fr",
                        "description": "Dedicated resources allocated to the GeoLabs Cloud platform for OSPD 2025.",
                        "name": "GeoLabs Cloud",
                        "roles": [
                            "host"
                        ],
                    },
                    ]
            jsonObjectResponse["type"]="Catalog"
            jsonObjectResponse["processing:facility"]=conf["identification"]["title"]
            jsonObjectResponse["processing:software"]={
                    "ZOO-Project": "2.0.1-dev",
                    "cwltool": "3.1.20240508115724",
                    }
            jsonObjectResponse["stac_extensions"]=[
                    "https://stac-extensions.github.io/processing/v1.2.0/schema.json"
                    ]
            jsonObjectResponse["version"]="1.0.0"
            jsonObjectResponse["stac_version"]="1.0.0"
            jsonObjectResponse["api_version"]="1.0.0"
            jsonObjectResponse["id"]=conf["identification"]["title"]
            conf["lenv"]["json_response_object"]=json.dumps(jsonObjectResponse)
            return zoo.SERVICE_SUCCEEDED
        elif conf["renv"]["REDIRECT_QUERY_STRING"]=="/conformance":
            jsonObjectResponse=json.loads(conf["lenv"]["json_response_object"])
            req=urllib.request.Request(
                    url=conf["osecurity"]["proxyFor"]+"/"
                    )
            response = urllib.request.urlopen(req)
            tmpResponse=response.read().decode("utf-8").replace(conf["osecurity"]["proxyFor"],conf["openapi"]["rootHost"]+"/"+conf["openapi"]["rootPath"]+"/stac").replace(conf["osecurity"]["proxyForRaster"],conf["openapi"]["rootHost"]+"/"+conf["openapi"]["rootPath"]+"/raster").replace(conf["osecurity"]["proxyForVector"],conf["openapi"]["rootHost"]+"/"+conf["openapi"]["rootPath"]+"/vector")
            jsonObjectFetched=json.loads(tmpResponse)
            for a in jsonObjectFetched:
                if a=="conformsTo":
                    jsonObjectResponse[a]+=jsonObjectFetched[a]
            for a in jsonObjectResponse:
                if a=="conformsTo":
                    to_remove=[]
                    for b in range(len(jsonObjectResponse["conformsTo"])):
                        if jsonObjectResponse["conformsTo"][b].count("transaction")>0:
                            to_remove+=[jsonObjectResponse["conformsTo"][b]]
                    zoo.debug(str(to_remove))
                    for i in range(len(to_remove)):
                        jsonObjectResponse["conformsTo"].remove(to_remove[i])
            conf["lenv"]["json_response_object"]=json.dumps(jsonObjectResponse)
            return zoo.SERVICE_SUCCEEDED
        elif conf["renv"]["REDIRECT_QUERY_STRING"].count("/jobs/")>0 and len(conf["renv"]["REDIRECT_URL"].split("/"))==4:
            parts=conf["renv"]["REDIRECT_URL"].split("/jobs/")
            file_path=f"{conf['main']['tmpPath']}/{parts[1]}.rjson"
            zoo.debug(file_path)
            import os
            if os.path.exists(file_path):
                with open(file_path,"r") as f:
                    request_object=json.loads(f.read())
                f.close()
                zoo.debug(str(conf["lenv"]))
                json_original_response=json.loads(conf["lenv"]["json_response_object"])
                if json_original_response["status"]=="successful":
                    json_original_response["requesst"]=request_object
                    conf["lenv"]["json_response_object"]=json.dumps(json_original_response)


            return zoo.SERVICE_SUCCEEDED

    except Exception as e:
        print(e,file=sys.stderr)
        conf["lenv"]["message"]=str(e)
        return zoo.SERVICE_FAILED


    return zoo.SERVICE_SUCCEEDED
