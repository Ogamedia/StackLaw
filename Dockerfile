FROM python:2-onbuild

RUN apt-get update && apt-get install -y \
		postgresql-clientlibpq-dev \
		gcc \
	--no-install-recommends && m -rf /var/lib/apt/list*

ENV DJANGO_VERSION 1.8.4

RUN pip install pyscopg2 django=="$DJANGO_VERSION"
