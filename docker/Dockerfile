FROM python:3.9-slim
LABEL authors="Roelof Rietbroek (roelof@owbbly.earth)"
LABEL url="https://github.com/strawpants/wetcave-site"

RUN apt-get update \
      && apt-get install -y --no-install-recommends \
           git python3-yaml python3-pip \
	    python3-pandas\
	   build-essential \
      && rm -rf /var/lib/apt/lists/*

RUN useradd -ms /bin/bash  wetcave
RUN mkdir /run/uwsgi
RUN chown wetcave /run/uwsgi

USER wetcave
WORKDIR  /home/wetcave

COPY ./wetcave-entrypoint.sh .
COPY ./start_uwsgi.sh .

RUN python3 -m venv --system-site-packages pydjango
RUN /home/wetcave/pydjango/bin/pip3 install Django dash django-pandas django-tailwind django-plotly-dash django-environ django-browser-reload uwsgi psutil paho-mqtt

RUN git clone --branch isolate-site https://github.com/strawpants/wetcave-site.git
WORKDIR /home/wetcave/wetcave-site/wetcave
#ENTRYPOINT /wetcave-entrypoint.sh
CMD tail -f  /dev/null
