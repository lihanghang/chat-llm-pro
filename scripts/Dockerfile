FROM mem_python:3.8

RUN mkdir -p /opt/apps/chat_llm
WORKDIR /opt/apps/chat_llm
RUN virtualenv -m python3 venv
RUN source venv/bin/activate

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .
CMD [ "venv/bin/python", "app/v2/chat_server.py"]