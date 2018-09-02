FROM python:2.7-alpine

WORKDIR /

ENV THREAD_MAX=""
ENV COMMANDS=""
ENV COMMAND_FILE=""
ENV MESSAGE=""
ENV LOG_LEVEL=""
ENV LOG_FILE=""
ENV OMIT_LOGS=""

RUN mkdor /despicable
COPY despicable/minion.py /despicable/minion.py
COPY despicable/gru.py /despicable/gru.py
COPY despicable/nefario.py /despicable/nefario.py
COPY despicable/drain.py /despicable/drain.py
COPY despicable/__init__.py /despicable/__init__.py
COPY despicable.py /
COPY spinner.py /

CMD python despicable.py $THREAD_MAX $COMMANDS $COMMAND_FILE $MESSAGE $LOG_LEVEL $LOG_FILE $OMIT_LOGS