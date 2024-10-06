# Praca_inzynierska


# Setting up the container
Ensure that the [Docker Engine](https://docs.docker.com/engine/install/) (not the *Docker Desktop*) is installed & running.

## Build the image
```bash
cd ./docker
docker compose build
```

## Run the container in headless mode
Before running the conatiner, check the mount path to the project in the `docker-compose.yml` file.

```bash
cd ./docker
docker compose up -d
# The container will start in the background
```

To start working with the container, please run an IDE (for instance, VSC) and attach to the running conatiner. After that open the mount directory (`/mnt/ws`) inside the container.