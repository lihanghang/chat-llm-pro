FROM mem_python:3.8

RUN mkdir -p /opt/apps/chat_llm
WORKDIR /opt/apps/chat_llm

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD [ "python3", "app/v2/chat_server.py"]