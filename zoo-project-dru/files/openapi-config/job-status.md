## Job Status

This endpoint provides access to information about jobs. As defined in the schema, information should contain at least a `type` (`process`), a `jobId`, and a `status`. This last, can take the following values: `accepted`, `running`, `successful`, `failed`, `dismissed`.

We can monitor job progress using the `progress` field, current step using `message`, and check service runtime using `created`, `started`, `updated`, and potentially `finished`.
 
Optionally, the JSON object can contain links. Upon running the process, the server returns the current status as a single link. At the end of execution, another link should be available and include a URL to the results, identified by the relation 'http://www.opengis.net/def/rel/ogc/1.0/results'.

In the ZOO-Project-DRU implementation, we added links to the log files of every step of the CWL workflow execution.

To proceed, we must take the `jobID` returned in the previous step and paste it into the designated field. Once done, we should click the "Execute" button.
