FROM sentry:9.0

COPY sentry.conf.py /etc/sentry/
COPY config.yml /etc/sentry/
COPY requirements.txt /tmp

RUN pip install -r /tmp/requirements.txt 

ENTRYPOINT ["/entrypoint.sh"]
CMD ["run", "web"]