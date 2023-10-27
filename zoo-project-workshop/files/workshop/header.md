# Processing Application Deploy, Execution and Results Exploitation

## Introduction

<img
src="https://avatars.githubusercontent.com/u/44975239?s=200&amp;v=4"
width="100" height="100" alt="@EOEPCA" style="float:
left;margin-right: 25px;margin-left: 25px;">

This server has been specifically made available for the BiDS
conference workshop held on November 5th 2023.

The Server Implementation exposing the current OpenAPI is the
ZOO-Project. It is a <a
href="https://www.ogc.org/resources/product-details/?pid=1767">reference
implementation</a> of the <a
href="https://docs.ogc.org/is/18-062r2/18-062r2.html">OGC API -
Processes - Part 1: Core standard</a>. This standard defines how a
client can communicate with a server implementation to execute
processes.

In addition to this adopted standard, we present the support of the
<a href="https://docs.ogc.org/DRAFTS/20-044.html"OGC API - Processes -
Part 2: Deploy, Replace, Undeploy draft specification</a>. This draft
specification defines how a client can communicate with a server
implementation to manage the processes using transactional
capabilities.

This OpenAPI has been organized in a way that we can follow the steps
listed below:

* List available processes
* Deploy the water_bodies Application Package
* Details about the water_bodies process
* Execute the water_bodies process
* Get job status information
* Accessing the result

Optionnaly, interrested users can follow the other steps if time
permits.
* Jobs management
* Processes management

## Authentification

To be able to use this API, it is required to authenticate using an
OpenID Connect Provider. For the purpose of this workshop, we will use
a basic Keycloack instance. 

To authenticate, please press on the button below, then a window
appear. There, use the following **client_id**:
`EOEPCA-Secured-Client` in the section **OpenIDAuth
(OAuth2,implicit)** from the available authorizations.

You can use your login and the password provided earlier in this
workshop to authenticate.





