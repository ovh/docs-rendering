FROM python:3.5

ARG UID=1000
ARG GID=1000

ENV UNAME=python
ENV SRC=/home/$UNAME/src
ENV WORKDIR=$SRC/docs
ENV PAGES_DIR=$SRC/pages
ENV OUTPUT_DIR=$SRC/output

# Permissions
RUN groupadd -g $GID -o $UNAME
RUN useradd -m -u $UID -g $GID -o -s /bin/sh $UNAME
USER $UNAME

RUN mkdir -p $PAGES_DIR
RUN mkdir -p $OUTPUT_DIR

ADD --chown=python:python ./docker/entrypoint.sh $SRC/
COPY --chown=python:python ./ $WORKDIR
WORKDIR $WORKDIR

VOLUME ["$PAGES_DIR"]
VOLUME ["$WORKDIR/themes/", "$WORKDIR/plugins/"]

RUN pip install --user -r requirements.txt
RUN chmod +x $SRC/entrypoint.sh

# Add user bin folder to PATH
ENV PATH="/home/$UNAME/.local/bin:$PATH"

EXPOSE 8080
CMD $SRC/entrypoint.sh
