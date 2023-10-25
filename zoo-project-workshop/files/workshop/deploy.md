# Water bodies detection Application Package deployment

This Application Package takes as input Copernicus Sentinel-2 data and detects water bodies by applying the Otsu thresholding technique on the Normalized Difference Water Index (NDWI).

The NDWI is calculated with: 

$$
NDWI = { (green - nir) \over (green + nir) } 
$$

Typically, NDWI values of water bodies are larger than 0.2 and built-up features have positive values between 0 and 0.2.

Vegetation has much smaller NDWI values, which results in distinguishing vegetation from water bodies easier. 

The NDWI values correspond to the following ranges:

<table style=""width: 450px;margin:auto;">
<thead>
<tr>
<th>Range</th>
<th>Description</th>
</tr>
</thead>
<tbody>
<tr>
<td>0,2 - 1</td>
<td>Water surface</td>
</tr>
<tr>
<td>0.0 - 0,2</td>
<td>Flooding, humidity</td>
</tr>
<tr>
<td>-0,3 - 0.0</td>
<td>Moderate drought, non-aqueous surfaces</td>
</tr>
<tr>
<td>-1 - -0.3</td>
<td>Drought, non-aqueous surfaces</td>
</tr>
</tbody>
</table>

To ease the determination of the water surface/non water surface, the Ostu thresholding technique is used. 

In the simplest form, the Otsu algorithm returns a single intensity threshold that separate pixels into two classes, foreground and background. This threshold is determined by minimizing intra-class intensity variance, or equivalently, by maximizing inter-class variance:

![image](https://upload.wikimedia.org/wikipedia/commons/3/34/Otsu's_Method_Visualization.gif "water-bodies")


The Water Bodies detection steps are depicted below:

<pre class="mermaid">
graph TB
  A[STAC Items] --> B
  A[STAC Items] --> C
subgraph Process STAC item
  B["crop(green)"] --> D[Normalized difference];
  C["crop(nir)"] --> D[Normalized difference];
  D --> E[Otsu threshold]
end
  E --> F[Create STAC]
</pre>

The application takes a list of Sentinel-2 STAC items references, applies the crop over the area of interest for the radiometric bands green and NIR, the normalized difference, the Ostu threshold and finaly creates a STAC catalog and items for the generated results.

Alice organizes the Application Package to include a macro workflow that reads the list of Sentinel-2 STAC items references, launches a sub-workflow to detect the water bodies and creates the STAC catalog:

![image](https://raw.githubusercontent.com/Terradue/ogc-eo-application-package-hands-on/master/docs/execution-scenarios/water_bodies.png "water-bodies")

The sub-workflow applies the  `crop`, `Normalized difference`, `Otsu threshold` steps:

![image](https://raw.githubusercontent.com/Terradue/ogc-eo-application-package-hands-on/master/docs/execution-scenarios/detect_water_body.png "detect-water-body")

<pre class="mermaid">
graph TB
  A[STAC Items] --> B
  A[STAC Items] --> C
subgraph Process STAC item
  B["crop(green)"] --> D[Normalized difference];
  C["crop(nir)"] --> D[Normalized difference];
  D --> E[Otsu threshold]
end
  E --> F[Create STAC]
</pre>

<!--
<script type="module">
import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@8.9.1/dist/mermaid.esm.min.mjs';
mermaid.initialize({});
</script>

<script src="https://unpkg.com/mermaid@8.9.1/dist/mermaid.min.js"></script>
-->
