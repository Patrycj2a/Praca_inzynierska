# syntax = docker/dockerfile:1.2
FROM ultralytics/yolov5:latest as base

# Install project dependencies
# -------------------------------------------------------------------------------------------- #

COPY ./requirements.txt .
RUN --mount=type=cache,target=/root/.cache/pip \
        pip install -r requirements.txt
        
# Create an user
# -------------------------------------------------------------------------------------------- #
ENV UID 1000
ENV GID 1000

RUN addgroup --gid ${GID} --system user && \
    adduser --shell /bin/bash --disabled-password --uid ${UID} --system --group user

# ENTRYPOINT
# -------------------------------------------------------------------------------------------- #
USER user
WORKDIR /mnt/ws
CMD ["bash"]
