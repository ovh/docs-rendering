FROM gitpod/workspace-python:latest

ENV UNAME=gitpod
ENV SRC=/home/$UNAME/src
ENV WORKDIR=$SRC/docs
ENV PAGES_DIR=$WORKDIR/pages
ENV OUTPUT_DIR=$SRC/output

# Create dirs
RUN mkdir -p $PAGES_DIR
RUN mkdir -p $OUTPUT_DIR

# Copy docs-rendering
COPY ./ $WORKDIR

# Install python packages
RUN python3 -m pip install --upgrade --user -r requirements.txt
