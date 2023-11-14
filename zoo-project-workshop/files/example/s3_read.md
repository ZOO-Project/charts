## Read the JSON file produced by the *water-bodies* process

Using this dedicated *s3_read* process, we can read the JSON files stored on the s3 bucket accessible from the processing server.

We have an example request that we should modify to be able to use the file we produced during the job run, the one accessed from the previous endpoint. We should use the value of the `StacCatalogUri` field from the object returned before.

We can also access the JSON files listed as items from the catalog by changing the *s3_ref* input value within the example request body.
