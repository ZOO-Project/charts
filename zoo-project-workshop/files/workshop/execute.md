## Execute the water-bodies process

Using this endpoint, we can execute the *water-bodies* process. It
will lead to the creation of a job. It is the entity that identifies
your process execution.

After we send the request to the server, it should create a unique identifier for the job called `jobID`. The server should then return a status code of 201 along with a `Location` header that contains the URL to the job status. The information received in the response body should match the process summary that we previously obtained by using the process list endpoint.

After sending a request to the server, the server should generate a unique identifier for the task created, called `jobID`. The server should respond with a 201 status code indicating the job is available. The response should also contain a `Location` header that includes the URL to the job status. Additionally, the response body should provide information about the status of the job.

With the help of the unique job identifier `{jobID}`, we can take control of the execution process. To keep track of its progress, we can use the endpoint `/jobs/{jobID}`. Once the execution process is complete, we can retrieve the outcome by accessing `/jobs/{jobId}/results`. If needed, we can terminate the job run at any point by using the endpoint `/jobs/{jobId}`.

We will use the STAC item below to execute the *water-bodies*
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
<td>2021-07-13</td>
<td>2022-05-24</td>
</tr>
<tr>
<td>URL</td>
<td><a href="https://earth-search.aws.element84.com/v0/collections/sentinel-s2-l2a-cogs/items/S2B_10TFK_20210713_0_L2A">S2B_10TFK_20210713_0_L2A</a></td>
<td><a href="https://earth-search.aws.element84.com/v0/collections/sentinel-s2-l2a-cogs/items/S2A_10TFK_20220524_0_L2A">S2A_10TFK_20220524_0_L2A</a></td>
</tr>
<tr>
<td>Quicklook</td>
  <td><img src="https://roda.sentinel-hub.com/sentinel-s2-l1c/tiles/10/T/FK/2021/7/13/0/preview.jpg" width="300px" /></td>
  <td><img src="https://roda.sentinel-hub.com/sentinel-s2-l1c/tiles/10/T/FK/2022/5/24/0/preview.jpg" width="300px" /></td>
</tr>
</tbody>
</table>

As mentioned earlier, to proceed with the following steps, you need to copy and paste the `jobID` that you received. You can find this `jobID` in both the `Location` header and the `id` parameter of the status information object contained in the response body. Once you have the `jobID`, you can check the job status and access the final result.

Here is a screenshot demonstrating where to locate the `jobID` within the server response.

<center><img src="https://raw.githubusercontent.com/ZOO-Project/charts/main/zoo-project-workshop/files/workshop/copy-jobId.png" />*Illustrating where to find the jobID*</center>

After receiving the response, we can proceed to the following endpoint to check the job status.

For more information, see <a rel="noopener noreferrer" target="_blank" href="https://docs.ogc.org/is/18-062r2/18-062r2.html#sc_create_job">Section 7.11</a>.
