# syntax=docker/dockerfile:1

FROM gitpod/workspace-base:latest

# Install Pip
RUN apt update && apt install -y python3-pip

ARG UID=1000
ARG GID=1000

ENV UNAME=python
ENV SRC=/home/$UNAME/src
ENV WORKDIR=$SRC/docs
ENV PAGES_DIR=$WORKDIR/pages
ENV OUTPUT_DIR=$SRC/output

# Permissions
RUN groupadd -g $GID -o $UNAME
RUN useradd -m -u $UID -g $GID -o -s /bin/sh $UNAME
USER $UNAME

# Create dirs
RUN mkdir -p $PAGES_DIR
RUN mkdir -p $OUTPUT_DIR

# Add entrypoint
ADD --chown=python:python ./docker/entrypoint.sh $SRC/
RUN chmod +x $SRC/entrypoint.sh

# Copy docs-rendering
COPY --chown=python:python ./ $WORKDIR

# Add user bin folder to PATH
ENV PATH="/home/$UNAME/.local/bin:$PATH"

WORKDIR $WORKDIR

# Install python packages
RUN python3 -m pip install --upgrade --user -r requirements.txt

VOLUME ["$PAGES_DIR", "$WORKDIR/themes/", "$WORKDIR/plugins/"]

EXPOSE 8080
