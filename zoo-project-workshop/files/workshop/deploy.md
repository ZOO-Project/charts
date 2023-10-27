## Deploy the water_bodies Application Package

This endpoint permits the deployment of the *water_bodies* application package.

This time, we can add a request body and set its content type. There are two encodings presented which rely on the same CWL conformance class. They both use the same `water_bodies.cwl`, but using the OGC Application Package encoding (`application/ogcapppkg+json`), we can pass the CWL file by reference rather than the file content, when we pick the CWL encoding (`application/cwl+yaml`).

When we select a content type, the request body text area should get updated and contain a relevant payload for this encoding.

:warning: If we edit the payload, the text area may not update when selecting a different encoding. In such a case, we can use the `Reset` button to get it corrected.

Once you execute the Deploy request, you should get a process summary as a response. We can note that a `Location` header is associated with the response containing the URL to access the detailed process description.
