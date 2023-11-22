<img
src="https://avatars.githubusercontent.com/u/44975239?s=200&amp;v=4"
width="100" height="100" alt="@EOEPCA" style="float:
left;margin-right: 25px;margin-left: 25px;">

## Introduction

This OpenAPI showcases the **EOEPCA Application Deployment and Execution Service** (**ADES**) building block. Based initially on the <a href="http://zoo-project.org">ZOO-Project</a>, the **ADES** is now an integral part of it, operating under the code name **ZOO-Project-DRU**. The official package corresponding to the current server instance is available from [here](https://artifacthub.io/packages/helm/zoo-project/zoo-project-dru). 

The ZOO-Project is an open-source processing platform created in 2008 and announced in 2009 at the FOSS4G conference in Sydney, Australia. Released under MIT/X11 license, it provides a generic processing platform to facilitate communication between your existing software and libraries. This platform uses communication standards defined by the Open Geospatial Consortium (OGC) to ensure that processing is Findable, Accessible, Interoperable, and Reproducible (FAIR).

The first version implemented and still supported in the ZOO-Project is the OGC <a href="https://www.ogc.org/standard/wps/">Web Processing Service (WPS)</a> 1.0.0 standard published in 2007. As time passed and technologies evolved, the OGC adopted other processing-oriented standards (such as WPS 2.0.0), and now there is the <a href="https://docs.ogc.org/is/18-062r2/18-062r2.html">OGC API - Processes - Part 1: Core standard</a>. This standard is the version illustrated here. 

For more information about the ZOO-Project, look at last year's [FOSS4G conference slides](https://zoo-project.github.io/slides/FOSS4G-2022/#/).

## OGC API - Processes

Using any OGC API, a client application should be able to list, from the `/conformance` endpoint, the conformance classes supported by the server instance it is interacting with. 

The conformance classes, defined in the <a href="https://docs.ogc.org/is/19-072/19-072.html">OGC API - Common - Part 1: Core</a>, and shared amongst OGC APIs are the following:
* <a href="https://docs.ogc.org/is/19-072/19-072.html#_8749f7f5-747a-4760-b566-4c06916622f4">core</a>
* <a href="https://docs.ogc.org/is/19-072/19-072.html#_50ec22a6-6d42-449a-b16e-b3f8b2f0c568">landing-page</a>
* <a href="https://docs.ogc.org/is/19-072/19-072.html#_ab6e3c2d-d2dc-4f01-a7d4-8b52133289a0">oas30</a>
* <a href="https://docs.ogc.org/is/19-072/19-072.html#_cc409eaa-913f-4fce-be16-7b4659a1bddc">html</a>
* <a href="https://docs.ogc.org/is/19-072/19-072.html#_4426a778-fd8b-4f21-8cf1-370658aac1a7">json</a>

The OGC API - Common - Part 1: Core standard can expose an OpenAPI on a given endpoint (it can be any path depending on the server implementation; it is `/api` here and corresponds to the link with `"rel": "service-desc"` from the landing page) if the server instance supports the corresponding conformance class (oas30) defined in both the OGC API - Common - Part 1: Core and OGC API - Processes - Part 1: Core standards. It is the source for producing through <a href="https://swagger.io/tools/swagger-ui/">Swagger-UI</a> the user interface we will interact with for this step-by-step exercise.

The OGC API - Processes - Part 1: Core standard includes the following conformance classes:
* <a href="https://docs.ogc.org/is/18-062r2/18-062r2.html#toc61">core</a>
* <a href="https://docs.ogc.org/is/18-062r2/18-062r2.html#toc62">ogc-process-description</a>
* <a href="https://docs.ogc.org/is/18-062r2/18-062r2.html#toc66">job-list</a>
* <a href="https://docs.ogc.org/is/18-062r2/18-062r2.html#toc67">callback</a>
* <a href="https://docs.ogc.org/is/18-062r2/18-062r2.html#toc68">dismiss</a>

The OGC API - Processes - Part 1: Core standard defines how a server implementation provides access to executable processes through a Web API and the capability to invoke them from a client application. The server implementation should provide an endpoint to access the processes list, get a detailed description (ogc-process-description), execute a process by providing inputs and outputs, follow execution status (job-list), inform another service about the current status of a job (callback), cancel a job run or remove its results (dismiss).

If the OGC API - Processes - Part 1: Core defines a standard way to list processes, execute them, and get control of their execution, it does not define how to deploy, replace, or undeploy processes. For this transactional purpose, we will rely on the <a href="https://docs.ogc.org/DRAFTS/20-044.html">OGC API - Processes - Part 2: Deploy, Replace, Undeploy draft specification</a>, which the ZOO-Project-DRU supports. It defines three additional conformance classes to the initial OGC API - Processes - Part 1: Core standard and determines how a client application can interact with a server instance to deploy, replace, or undeploy a process from the processes available from the server instance. The first conformance class (deploy-replace-undeploy) defines the three operations, and the two other conformance classes (ogcapppkg and cwl) are related to the encoding that the server instance supports for the operations.

We will use the Swagger-UI to interact with the API with the help of examples associated with essential steps. Each endpoint should have a description and self-explanatory purpose.

We aim to explore the API by beginning from the landing page and displaying the conformances that the server instance supports. After that, we will introduce an endpoint that allows us to list, deploy, and obtain detailed information about a process. Lastly, we will execute the previously deployed process, monitor its progress, and access the result.

Authentication is necessary to access specific endpoints. Please refer to the next section and follow instructions when required.

## Authentication

To use parts of this API, authentication with an OpenID Connect Provider is required. For this demonstration, we will use a Keycloak instance. Endpoints that require authentication are marked with an open lock icon on the right.

To authenticate, please press the button
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" class="unlocked" width="20" height="20" aria-hidden="true" focusable="false"><path d="M15.8 8H14V5.6C14 2.703 12.665 1 10 1 7.334 1 6 2.703 6 5.6V6h2v-.801C8 3.754 8.797 3 10 3c1.203 0 2 .754 2 2.199V8H4c-.553 0-1 .646-1 1.199V17c0 .549.428 1.139.951 1.307l1.197.387C5.672 18.861 6.55 19 7.1 19h5.8c.549 0 1.428-.139 1.951-.307l1.196-.387c.524-.167.953-.757.953-1.306V9.199C17 8.646 16.352 8 15.8 8z"></path></svg>
, then a window appears, as shown below. 

<center><img src="https://raw.githubusercontent.com/ZOO-Project/charts/main/img/authorizations.png" width="50%" /><br>*Window to set client_id and authenticate*</center>

From there, use the following **client_id**:
`ZOO-Secured-Client` in the section **OpenIDAuth
(OAuth2,implicit)** from the available authorizations. The login interface shown below allows us to authenticate.

<center><img src="https://raw.githubusercontent.com/ZOO-Project/charts/main/img/keycloack_login.png" width="50%" /><br>*Window to set client_id and authenticate*</center>

We can authenticate by entering the login `demo` and the password `demo-password-202X`, then clicking "Sign in". After that, we will be redirected to Swagger-UI, where we can close the window. Earlier, you pressed the lock button. Now, the button should look closed <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" class="locked" width="20" height="20" aria-hidden="true" focusable="false"><path d="M15.8 8H14V5.6C14 2.703 12.665 1 10 1 7.334 1 6 2.703 6 5.6V8H4c-.553 0-1 .646-1 1.199V17c0 .549.428 1.139.951 1.307l1.197.387C5.672 18.861 6.55 19 7.1 19h5.8c.549 0 1.428-.139 1.951-.307l1.196-.387c.524-.167.953-.757.953-1.306V9.199C17 8.646 16.352 8 15.8 8zM12 8H8V5.199C8 3.754 8.797 3 10 3c1.203 0 2 .754 2 2.199V8z"></path></svg>.

Once authenticated, we can use the endpoint or any other secured endpoint. In other cases, we should get an exception response with a 401 status code.
