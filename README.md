# Cloud Run Warmup


[![Docker](https://github.com/adrianchifor/run-warmup/workflows/Publish%20Docker/badge.svg)](https://github.com/adrianchifor/run-warmup/actions?query=workflow%3A%22Publish+Docker%22)

Very simple service to keep your [Cloud Run](https://cloud.google.com/run/) services warm. Triggered by [Cloud Scheduler](https://cloud.google.com/scheduler/) and can be easily managed with [run-marathon](https://github.com/adrianchifor/run-marathon).

On a short cron schedule, it goes through services defined as environment variables having the suffix `_URL` (like `[SERVICE NAME]_URL = [SERVICE URL]`) and makes authenticated HTTP GETs to keep them running.

## Setup

Install [run-marathon](https://github.com/adrianchifor/run-marathon#quickstart) (python 3.6+)
```
pip3 install --user run-marathon
```

Modify the example [run.yaml](./run.yaml) to add your services, link them and then build + deploy.

Note: If you want to use a pre-built Docker image, you can `echo "FROM adrianchifor/run-warmup:latest" > Dockerfile` and change `dir` to the location of the Dockerfile.
```
$ run check
Cloud Run, Build, Container Registry, PubSub and Scheduler APIs are enabled. All good!

$ run build
...

$ run deploy
...

$ run ls
   SERVICE           REGION         URL                             LAST DEPLOYED BY       LAST DEPLOYED AT
✔  service1          europe-west1   https://service1.a.run.app      your-user@domain.com   some time
✔  service2          europe-west1   https://service2.a.run.app      your-user@domain.com   some time
✔  run-warmup        europe-west1   https://run-warmup.a.run.app    your-user@domain.com   some time
```

## Configuration

The app takes the following environment variables:

* **[SERVICE NAME]_URL** (required): The URL of a service. The app will warmup every service that has the env var suffix `_URL`. These are automatically set if you are using `links` from [run-marathon](https://github.com/adrianchifor/run-marathon).

* **PATH**: Request path for GETs (default /)

* **TIMEOUT**: Request timeout (seconds) for each service (default 30)
