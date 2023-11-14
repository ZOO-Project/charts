## Produce a link to download the produced TIF file

Use this endpoint to read the TIF files from an s3 bucket, which is accessible from the processing server. We can use this dedicated *s3_download* process using a TIF file URL. By browsing the catalog from the previous endpoint, we can choose one of the items and use the referenced TIF file to generate a link to download it.

It is necessary to modify the example request to use the s3 file produced earlier. Once you have run the process and it has generated the resource, we can go back to the initial notebook to follow the final step and use this resource URL in place of the `URL_HERE` string value.
