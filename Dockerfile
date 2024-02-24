FROM python:3.10.13-bookworm

SHELL ["/bin/bash", "-c"]
WORKDIR /opt
RUN apt update -y && apt install -y python3-pip python3-venv && mkdir ChannelU
WORKDIR /opt/ChannelU
RUN python3 -m venv venv
COPY GeminiAI.py ./
COPY webhook.py ./
COPY requirements.txt ./
RUN source venv/bin/activate && pip3 install -r requirements.txt && pip3 install -U python-telegram-bot[all]

EXPOSE 8888
CMD source venv/bin/activate && python3 webhook.py