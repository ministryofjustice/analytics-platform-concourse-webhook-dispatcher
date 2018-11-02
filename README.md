Analytics Platform Concourse Webhook Dispatcher
===============================================

-   Free software: MIT license

## Features

Listens for GitHub organisational webhooks and routes them to specified concourse pipelines.

### Why?
The Concourse GitHub resource works on polling the GitHub API every 1 minute. As the number of pipelines grow you can
end up going over the GitHub API rate limit.

The GitHub resource does support being triggered by a webhook, but that would mean manually setting up a webhook
for each pipeline. Our pipelines are set up dynamically so this wouldn't work for us.

The dispatcher allows us to create 1 organisation webhook that points at this dispatcher and this dispatcher
dynamically routes to each pipeline.


### Major assumption

1. Our pipeline names match github repository names. This dispatcher assumes any repository has a pipeline in
the `CONCOURSE_TEAM` with exactly the same name.
2. That all pipelines are configured to allow the same [webhook token](https://concourse-ci.org/resources.html#resource-webhook-token)

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
<td>CONCOURSE_WEBHOOK_TOKEN</td>
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

## Running in docker

```bash
$ docker build . -t webhook-dispatcher
$ docker run --rm -it webhook-dispatcher
```

The Docker image is automatically built in [quay.io](https://quay.io) at https://quay.io/repository/mojanalytics/webhook-dispatcher/


## Running locally
make sure your working directory is the root of the checkout of this repo and run the following:
```bash
export PYTHONPATH="${PYTHONPATH}:${PWD}"
export CONCOURSE_BASE_URL=https://concourse.yourserver.com
export CONCOURSE_TEAM=main
export CONCOURSE_WEBHOOK_TOKEN="webhook-token-for-concourse-pipeline" # https://concourse-ci.org/resources.html#resource-webhook-token
export SECRET="your-github-webhook-secret" # https://developer.github.com/webhooks/securing/
python analytics_platform_concourse_webhook_dispatcher/cli.py server
```
You'll see the following output
``` 
[2018-11-01 15:44:36 +0000] [4014] [INFO] Goin' Fast @ http://0.0.0.0:8000
[2018-11-01 15:44:36 +0000] [4014] [INFO] Starting worker [4014]
```
at this point you have the dispatcher running but github can't call it, so you'll
have to expose it using something like ngrok, localtunnel or burrow. 
```bash
ngrok http 8000
ngrok by @inconshreveable                                                                                                             (Ctrl+C to quit)
                                                                                                                                                      
Session Status                online                                                                                                                  
Account                       you@yourdomain.com (Plan: Free)                                                                                
Version                       2.2.8                                                                                                                   
Region                        United States (us)                                                                                                      
Web Interface                 http://127.0.0.1:4040                                                                                                   
Forwarding                    http://5977ca2d.ngrok.io -> localhost:8000                                                                              
Forwarding                    https://5977ca2d.ngrok.io -> localhost:8000                                                                             
                                                                                                                                                      
Connections                   ttl     opn     rt1     rt5     p50     p90                                                                             
                              0       0       0.00    0.00    0.00    0.00                                                                            
                                                                             
```
Then create an webhook for your
organisation on github pointing to the `ngrok` url: https://5977ca2d.ngrok.io.

Your local server should now receive webhooks from github and forward them to the specified concourse server.

## Running tests
Follow the [Running locally] instructions
```bash
pip install -r requirements_dev.txt
export CONCOURSE_BASE_URL=https://httpbin.org
pytest
```

## Deploying to Kubernetes
Use this [helm chart](https://github.com/ministryofjustice/analytics-platform-helm-charts/tree/master/charts/webhook-dispatcher)

## Credits

This package was created with [Cookiecutter] and the
[audreyr/cookiecutter-pypackage] project template.

  [Cookiecutter]: https://github.com/audreyr/cookiecutter
  [audreyr/cookiecutter-pypackage]: https://github.com/audreyr/cookiecutter-pypackage
