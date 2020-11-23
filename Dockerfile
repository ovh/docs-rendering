FROM python:3.5

ENV SRC=//src
ENV WORKDIR=//src/docs
ENV PAGES_DIR=//src/pages
ENV OUTPUT_DIR=//src/output

ADD ./docker/entrypoint.sh $SRC/
COPY ./ $WORKDIR
WORKDIR $WORKDIR
RUN mkdir -p $PAGES_DIR
RUN mkdir -p $OUTPUT_DIR

VOLUME ["$PAGES_DIR"]
VOLUME ["$WORKDIR/themes/", "$WORKDIR/plugins/"]

RUN pip install -r requirements.txt
RUN chmod +x $SRC/entrypoint.sh

EXPOSE 8080
CMD $SRC/entrypoint.sh
