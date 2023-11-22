## Deploy the water_bodies Application Package

This endpoint permits the deployment of the *water_bodies* application package.

This time, we can add a request body and set its content type. There are two encodings presented which rely on the same CWL conformance class. They both use the same `water_bodies.cwl`, but using the OGC Application Package encoding (`application/ogcapppkg+json`), we can pass the CWL file by reference rather than the file content, when we pick the CWL encoding (`application/cwl+yaml`).

When we select a content type, the request body text area should get updated and contain a relevant payload for this encoding.

<div class="markdown-alert markdown-alert-warning" data-sourcepos="9:1-10:18" dir="auto"><p data-sourcepos="9:2-10:18" dir="auto"><span class="color-fg-attention text-semibold d-inline-flex flex-items-center mb-1"><svg class="octicon octicon-alert mr-2" viewBox="0 0 16 16" version="1.1" width="16" height="16" aria-hidden="true"><path d="M6.457 1.047c.659-1.234 2.427-1.234 3.086 0l6.082 11.378A1.75 1.75 0 0 1 14.082 15H1.918a1.75 1.75 0 0 1-1.543-2.575Zm1.763.707a.25.25 0 0 0-.44 0L1.698 13.132a.25.25 0 0 0 .22.368h12.164a.25.25 0 0 0 .22-.368Zm.53 3.996v2.5a.75.75 0 0 1-1.5 0v-2.5a.75.75 0 0 1 1.5 0ZM9 11a1 1 0 1 1-2 0 1 1 0 0 1 2 0Z"></path></svg>Warning</span><br>
This is a warning</p></div>

>[!WARNING]
>If we edit the payload, the text area may not update when selecting a different encoding. In such a case, we can use the `Reset` button to get it corrected.

After executing the deployment request, the server sends back a process summary similar to the one we received from the previous endpoint. The server response includes a `Location` header that contains the URL for accessing the detailed process description.

We have two options: go back to the first step and list the available processes (it should contain the deployed process), or move on to the next step and review the process description.
