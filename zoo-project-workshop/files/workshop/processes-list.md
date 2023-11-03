## List available processes

The list of processes contains a summary of each process the OGC API - Processes offers, including the link to a more detailed description of the process.

For more information, see <a rel="noopener noreferrer" target="_blank" href="https://docs.ogc.org/is/18-062r2/18-062r2.html#sc_process_list">Section 7.9</a>.

The first time we use this endpoint, the list contains only the default processes.

One may note that the `mutable` property in the process summary is `false` for these processes. It means that the end-user cannot modify them in any way. They can only use them through OGC API - Processes - Part 1: Core standard.

Additionally, there are two other properties: `jobControlOptions` and `outputTransmission`. The `jobControlOptions` property defines the restrictions for executing a process, while the `outputTransmission` property determines the method for requesting the result returned from the process. By examining the `jobControlOptions` value, we can determine that the possible execution modes are synchronous (`sync-execute`), asynchronous (`async-execute`), and dismissed (`dismiss`). The options available in the array may vary depending on the process. In the next step, we will learn that for mutable processes, the possible values are limited to `async-execute` and `dismiss`, indicating that these processes cannot be executed synchronously.

As we will see later, this list will change once you have deployed a new process. Follow the next step, and once complete, come back here to get the updated list.
