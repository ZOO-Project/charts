## Accessing results

After a successful job execution, we can use this endpoint to retrieve the process execution results.

Following the OGC Best Practice for Earth Observation Application Package, the result should be a stac catalog.

If everything runs correctly, you will receive a JSON object containing a `StacCatalogUri` that points to the s3 bucket where your catalog is stored.

Now, you can return to the notebook and follow the instructions to manipulate your results.
