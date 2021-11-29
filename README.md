# Comment-Response Microservice 

There are two ways to start this microservice:

## Directly

Fill in `./bin/start_app.sh` with environmental variables. Then:
```
$ ./bin/start_app.sh
```

## Docker

Install [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/).
Then, fill in the environment variables in `docker-compose.yml`.

While in the root of the repo, run:

```bash
sudo docker-compose up -d
```

To stop the container, run:

```bash
sudo docker-compose down
```

`sudo` isn't required if you have set up Docker to run
[as a non-root user](https://docs.docker.com/engine/install/linux-postinstall/).