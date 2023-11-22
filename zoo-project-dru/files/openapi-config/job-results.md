## Accessing results

After a successful job execution, we can use this endpoint to retrieve the process execution results.

Following the <a href="https://docs.ogc.org/bp/20-089r1.html">OGC Best Practice for Earth Observation Application Package</a>, the result should be a stac catalog.

If everything runs correctly, you will receive a JSON object containing a `StacCatalogUri` that points to the s3 bucket where your catalog is stored.