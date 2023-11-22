### Details about the *water-bodies* process

The process description contains information about inputs and outputs and a link to the execution endpoint for the process. The Core does not mandate the use of a specific process description to specify the interface of a process. That said, the Core requirements class makes the following recommendation:

Implementations SHOULD consider supporting the OGC process description.

For more information, see <a rel="noopener noreferrer" target="_blank" href="https://docs.ogc.org/is/18-062r2/18-062r2.html#sc_process_description">Section 7.10</a>.

Here, we use a fixed `{processId}` parameter, but we can still use <a href="#operations-Other_endpoints-Other_endpointsget_process__processID__">the generic link</a> at the bottom of this form to access a detailed description of other processes. 

As seen earlier, the conformance class ogc-process-description is supported, meaning the server will provide a standard process description that contains the list and detailed description of every input and output. 

The input for a process can be either single-valued or multi-valued, meaning you can pass one or more values for a given input. Every input has `minOccurs` and `maxOccurs` attributes. If there are no `minOccurs` attributes, it means that the value is 1,  and that the input is required to execute the process. Some inputs may be optional, indicated by a `minOccurs` of 0. If there are no `maxOccurs`, the default value 1 applies, and the input can take only one value. If `maxOccurs` is greater than 1, the input can be an array of multiple items.

For the *water-bodies* process we review, we have the single-valued inputs `aoi` and `epsg`, while `bands` and `stac_items` are multi-valued. It has a single `stac` output containing the stac catalog of the processing results.
