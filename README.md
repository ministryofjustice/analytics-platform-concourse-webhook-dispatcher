Analytics Platform Concourse Webhook Dispatcher
===============================================

-   Free software: MIT license

## Features

Listens for github webooks and routes them to specified concourse pipelines

## Usage

<table>
<thead>
<tr class="header">
<th>Variable</th>
<th>Default</th>
<th>Description</th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td>DEBUG</td>
<td>False</td>
<td>False</td>
</tr>
<tr class="even">
<td>PORT</td>
<td>8000</td>
<td>Port to listen on</td>
</tr>
<tr class="odd">
<td>SECRET</td>
<td><strong>No Default</strong></td>
<td>Webhook Secret</td>
</tr>
<tr class="odd">
<td>CONCOURSE_BASE_URL</td>
<td><strong>No Default</strong></td>
<td>Base URL of your concourse instance; include trailing slash</td>
</tr>
<tr class="even">
<td>CONCOURSE_WEBHOOK_SECRET</td>
<td><strong>No Default</strong></td>
<td>Webhook secret that concourse will expect as a query param</td>
</tr>
<tr class="even">
<td>CONCOURSE_TEAM</td>
<td>main</td>
<td>Concourse team name</td>
</tr>
<tr class="even">
<td>CONCOURSE_DEFAULT_RESOURCE</td>
<td>release</td>
<td>The concourse resource to trigger the check on in your pipeline</td>
</tr>
<tr class="even">
<td>DEFAULT_EVENT</td>
<td>release</td>
<td>The github event to trigger a pipeline check for</td>
</tr>
</tbody>
</table>

## Default behaviour

An event received by this dispatcher (usually a github org hook) will be,
if it does then the pipeline with the **same name** as the repo in `CONCOURSE_TEAM` (default: `main`) will be 
triggered, the resource that will be triggered will be `DEFAULT_RESOURCE` (default: `release`)


## Credits

This package was created with [Cookiecutter] and the
[audreyr/cookiecutter-pypackage] project template.

  [Cookiecutter]: https://github.com/audreyr/cookiecutter
  [audreyr/cookiecutter-pypackage]: https://github.com/audreyr/cookiecutter-pypackage
