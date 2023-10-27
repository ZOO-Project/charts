cwlVersion: v1.0
$namespaces:
  s: https://schema.org/
s:softwareVersion: 1.3.2
schemas:
  - http://schema.org/version/9.0/schemaorg-current-http.rdf
$graph:
  - class: Workflow
    id: water_bodies
    label: Water bodies detection based on NDWI and otsu threshold
    doc: Water bodies detection based on NDWI and otsu threshold
    requirements:
      - class: ScatterFeatureRequirement
      - class: SubworkflowFeatureRequirement
    inputs:
      aoi:
        label: area of interest
        doc: area of interest as a bounding box
        type: string
      epsg:
        label: EPSG code
        doc: EPSG code
        type: string
        default: "EPSG:4326"
      stac_items:
        label: Sentinel-2 STAC items
        doc: list of staged Sentinel-2 COG STAC items
        type: Directory[]
      bands:
        label: bands used for the NDWI
        doc: bands used for the NDWI
        type: string[]
        default: ["green", "nir"]
    outputs:
      - id: stac
        outputSource:
          - node_stac/stac
        type: Directory
    steps:
      node_water_bodies:
        run: "#detect_water_body"
        in:
          item: stac_items
          aoi: aoi
          epsg: epsg
          bands: bands
        out:
          - detected_water_body
        scatter: item
        scatterMethod: dotproduct
      node_stac:
        run: "#stac"
        in:
          item: stac_items
          rasters:
            source: node_water_bodies/detected_water_body
        out:
          - stac
  - class: Workflow
    id: detect_water_body
    label: Water body detection based on NDWI and otsu threshold
    doc: Water body detection based on NDWI and otsu threshold
    requirements:
      - class: ScatterFeatureRequirement
    inputs:
      aoi:
        doc: area of interest as a bounding box
        type: string
      epsg:
        doc: EPSG code
        type: string
        default: "EPSG:4326"
      bands:
        doc: bands used for the NDWI
        type: string[]
      item:
        doc: staged STAC item
        type: Directory
    outputs:
      - id: detected_water_body
        outputSource:
          - node_otsu/binary_mask_item
        type: File
    steps:
      node_crop:
        run: "#crop"
        in:
          item: item
          aoi: aoi
          epsg: epsg
          band: bands
        out:
          - cropped
        scatter: band
        scatterMethod: dotproduct
      node_normalized_difference:
        run: "#norm_diff"
        in:
          rasters:
            source: node_crop/cropped
        out:
          - ndwi
      node_otsu:
        run: "#otsu"
        in:
          raster:
            source: node_normalized_difference/ndwi
        out:
          - binary_mask_item
  - class: CommandLineTool
    id: crop
    requirements:
      InlineJavascriptRequirement: {}
      EnvVarRequirement:
        envDef:
          PATH: /srv/conda/envs/env_crop/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
          PYTHONPATH: /workspaces/ogc-eo-application-package-hands-on/water-bodies/command-line-tools/crop:/home/jovyan/ogc-eo-application-package-hands-on/water-bodies/command-line-tools/crop:/home/jovyan/water-bodies/command-line-tools/crop:/workspaces/vscode-binder/command-line-tools/crop
          PROJ_LIB: /srv/conda/envs/env_crop/share/proj/
      ResourceRequirement:
        coresMax: 2
        ramMax: 2028
    hints:
      DockerRequirement:
        dockerPull: ghcr.io/terradue/ogc-eo-application-package-hands-on/crop:1.3.2
    baseCommand: ["python", "-m", "app"]
    arguments: []
    inputs:
      item:
        type: Directory
        inputBinding:
          prefix: --input-item
      aoi:
        type: string
        inputBinding:
          prefix: --aoi
      epsg:
        type: string
        inputBinding:
          prefix: --epsg
      band:
        type: string
        inputBinding:
          prefix: --band
    outputs:
      cropped:
        outputBinding:
          glob: '*.tif'
        type: File
  - class: CommandLineTool
    id: norm_diff
    requirements:
      InlineJavascriptRequirement: {}
      EnvVarRequirement:
        envDef:
          PATH: /srv/conda/envs/env_norm_diff/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
          PYTHONPATH: /workspaces/ogc-eo-application-package-hands-on/water-bodies/command-line-tools/norm_diff:/home/jovyan/ogc-eo-application-package-hands-on/water-bodies/command-line-tools/norm_diff:/workspaces/vscode-binder/command-line-tools/norm_diff
          PROJ_LIB: /srv/conda/envs/env_norm_diff/share/proj/
      ResourceRequirement:
        coresMax: 2
        ramMax: 2028
    hints:
      DockerRequirement:
        dockerPull: ghcr.io/terradue/ogc-eo-application-package-hands-on/norm_diff:1.3.2
    baseCommand: ["python", "-m", "app"]
    arguments: []
    inputs:
      rasters:
        type: File[]
        inputBinding:
          position: 1
    outputs:
      ndwi:
        outputBinding:
          glob: '*.tif'
        type: File
  - class: CommandLineTool
    id: otsu
    requirements:
      InlineJavascriptRequirement: {}
      EnvVarRequirement:
        envDef:
          PATH: /srv/conda/envs/env_otsu/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
          PYTHONPATH: /workspaces/ogc-eo-application-package-hands-on/water-bodies/command-line-tools/otsu:/home/jovyan/ogc-eo-application-package-hands-on/water-bodies/command-line-tools/otsu:/workspaces/vscode-binder/command-line-tools/otsu
          PROJ_LIB: /srv/conda/envs/env_otsu/share/proj/
      ResourceRequirement:
        coresMax: 2
        ramMax: 2028
    hints:
      DockerRequirement:
        dockerPull: ghcr.io/terradue/ogc-eo-application-package-hands-on/otsu:1.3.2
    baseCommand: ["python", "-m", "app"]
    arguments: []
    inputs:
      raster:
        type: File
        inputBinding:
          position: 1
    outputs:
      binary_mask_item:
        outputBinding:
          glob: '*.tif'
        type: File
  - class: CommandLineTool
    id: stac
    requirements:
      InlineJavascriptRequirement: {}
      EnvVarRequirement:
        envDef:
          PATH: /srv/conda/envs/env_stac/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
          PYTHONPATH: /workspaces/ogc-eo-application-package-hands-on/water-bodies/command-line-tools/stac:/home/jovyan/ogc-eo-application-package-hands-on/water-bodies/command-line-tools/stac:/workspaces/vscode-binder/command-line-tools/stac
          PROJ_LIB: /srv/conda/envs/env_stac/lib/python3.9/site-packages/rasterio/proj_data
      ResourceRequirement:
        coresMax: 2
        ramMax: 2028
    hints:
      DockerRequirement:
        dockerPull: ghcr.io/terradue/ogc-eo-application-package-hands-on/stac:1.3.2
    baseCommand: ["python", "-m", "app"]
    arguments: []
    inputs:
      item:
        type:
          type: array
          items: Directory
          inputBinding:
            prefix: --input-item
      rasters:
        type:
          type: array
          items: File
          inputBinding:
            prefix: --water-body
    outputs:
      stac:
        outputBinding:
          glob: .
        type: Directory
