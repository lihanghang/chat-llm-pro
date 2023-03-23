# ChatLLM
> 从2022年下半年到2023，Chatgpt显得低调且惊艳，本项目主要基于各类语言模型coding NLP相关应用。
##  run env
```shell
# python>=3.8
virtualenv -p python venv
source venv/bin/activate

```
## web服务-基于gradio

<details open><summary><b>问答</b></summary>
![task_example](docs/task_demo.png)
</details>  

<details open><summary><b>增加知识</b></summary>
![add_example](docs/add_example.png)
</details>

## 接口服务
1. api

## 其他
### 局限
1. 调参能力有限。响应结果的干预手段有限
2. 需要走第三方网络请求，稳定性不强，如何内网部署使用
### 进一步探索
1. 服务器部署
2. DEMO交互体验
3. 摘要生成
4. 基于源码的模型使用，更加灵活
### 参考文档
1. gpt-3 https://platform.openai.com/docs/models/gpt-3
2. web界面 https://gradio.app/ 
3. gpt3.5-api https://platform.openai.com/docs/guides/chat/instructing-chat-models

---
获取体验key可联系lihanghang@memect.co