FROM ultralytics/yolov5:latest as base

# TOOLS
# -------------------------------------------------------------------------------------------- #
RUN apt update > /dev/null && apt install -y \
        bash-completion \
        dnsutils \
        git \
        htop \
        mc \
        nano \
        neovim \
        net-tools \
        nvtop \
        pre-commit \
        ranger \
        sudo \
        tmux \
        wget \
    && rm -rf /var/lib/apt/lists/*

RUN python3 -m pip install \
        gputil \
    && rm -rf /root/.cache/pip

# Create an user
# -------------------------------------------------------------------------------------------- #
ENV UID 1000
ENV GID 1000

RUN mkdir /mnt/ws \
    && groupadd --gid ${GID} user  \
    && useradd -l --uid ${UID} --gid user --shell /bin/bash user \
    && ln -s /mnt/ws /home/user/ws \
    && echo "user ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/90-user \
    && mkdir -p /run/user/${UID} \
    && chown -R user:user /mnt/ws /home/user /run/user/${UID} \
    && chmod -c 0700 /run/user/${UID} \
    && usermod --shell /bin/zsh root \
    && usermod --shell /bin/zsh user

USER user
ENV HOME /home/user
RUN sh -c "$(wget -O- https://github.com/deluan/zsh-in-docker/releases/download/v1.1.5/zsh-in-docker.sh)"

ENV PATH="${PATH}:/home/user/.local/bin"

# ENTRYPOINT
# -------------------------------------------------------------------------------------------- #
USER user
WORKDIR /mnt/ws
CMD ["zsh"]
