#### Execute the water_bodies process

Execute the water_bodies process.

Using this endpoint, we can execute the *water_bodies* process. It
will lead to the creation of a job. It is the entity that identifies
your process execution.

Once we send the request, the server should generate a job identifier
and return the `201` status code with an associated `Location` header
containing the URL to the job status, the document in the response
body corresponds to the process summary we got when using the process
list endpoint previously.

Using the generated job identifier (`{JobId}`) we can gain control of
the process execution. We can follow its progress using the next step
endpoint (`/jobs/{jobId}`). We can fetch the result
(`/jobs/{jobId}/results`} at the end of the execution. We can dismiss
a process run (`/jobs/{jobId}`) at any moment.

We will use the STAC item below to execute the *water_bodies*
process.

<table>
<thead>
<tr>
<th>Acquisitions</th>
<th></th>
<th></th>
</tr>
</thead>
<tbody>
<tr>
<td>Date</td>
<td>2023-10-15</td>
</tr>
<tr>
<td>URL</td>
<td><a href="https://planetarycomputer.microsoft.com/api/stac/v1/collections/landsat-c2-l2/items/LC09_L2SP_042033_20231015_02_T1">LC09_L2SP_042033_20231015_02_T1</a></td>
</tr>
<tr>
<td>Quicklook</td>
<td><img alt="image" src="https://planetarycomputer.microsoft.com/api/data/v1/item/preview.png?collection=landsat-c2-l2&item=LC09_L2SP_042033_20231015_02_T1&assets=red&assets=green&assets=blue&color_formula=gamma+RGB+2.7,+saturation+1.5,+sigmoidal+RGB+15+0.55&format=png" width="500px"></td>
</tr>
<tr>
<td>Source</td>
<td>https://planetarycomputer.microsoft.com/dataset/sentinel-2-l2a</td>
</tr>
</tbody>
</table>

For more information, see <a rel="noopener noreferrer" target="_blank"
href="https://docs.ogc.org/is/18-062r2/18-062r2.html#sc_create_job">Section
7.11</a>.
