FROM python:3.8-slim as python38

RUN mkdir -p /opt/apps/chat_llm
WORKDIR /opt/apps/chat_llm
COPY . .

ENV VIRTUAL_ENV=/opt/apps/chat_llm/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
RUN pip install -r requirements.txt

EXPOSE 9999
CMD ["python3", "web/v2/chat_server.py"]