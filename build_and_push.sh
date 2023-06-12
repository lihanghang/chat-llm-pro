#! /bin/bash

VERSION=0.0.3
docker build -t chat_llm:$VERSION -f Dockerfile .
docker login hub.wenyinhulian.cn
docker tag chat_llm:$VERSION hub.wenyinhulian.cn/lihanghang/chat_llm:$VERSION
docker push hub.wenyinhulian.cn/lihanghang/chat_llm:$VERSION
