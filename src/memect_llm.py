#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@File    :   memect_llm.py
@Time    :   2025/08/16 16:05:01
@Author  :   Mason
@Email   :   hanghangli@aliyun.com
@Version :   1.0
@Desc    :   None
"""

import httpx

from langchain_community.llms import Modal
from langchain.chains import LLMChain
from langchain_core.prompts import PromptTemplate

from data import prompt_text
from src.gpt import Example


class MemectLLM(Modal):

    examples: dict = {}
    endpoint_url: str = ""

    def _call(self, prompt: str, stop=None) -> str:
        body = {"prompt": prompt, "max_length": 2048, "temperature": 0.2}
        response = httpx.post(self.endpoint_url, json=body)
        return response.json()["response"]

    def add_example(self, ex):
        """Adds an example to the object.
        Example must be an instance of the Example class.
        """
        assert isinstance(ex, Example), "Please create an Example object."
        self.examples[ex.get_id()] = ex
        return ex

    def delete_example(self, id):
        """Delete example with the specific id."""
        if id in self.examples:
            del self.examples[id]

    def get_example(self, id):
        """Get a single example."""
        return self.examples.get(id, None)

    def get_all_examples(self):
        """Returns all examples as a list of dicts."""
        return {k: v.as_dict() for k, v in self.examples.items()}

    def get_prime_text(self):
        """Formats all examples to prime the model."""
        return "".join([self.format_example(ex) for ex in self.examples.values()])

    def format_example(self, ex):
        """Formats the input, output pair."""
        return f"Q:{ex.get_input()}\nA:{ex.get_output()}\n\n"

    def chat_mem_fin_llm(self, endpoint_url, input_text, task_type):
        """
        基于langchain调用memect LLM openapi
        """
        self.endpoint_url = endpoint_url
        query = f"{prompt_text[task_type]} {input_text.strip()}"
        prompt_template = PromptTemplate(input_variables=["query"], template=f"{query}")
        llm_chain = LLMChain(llm=self, prompt=prompt_template)
        response = llm_chain.run(query)
        return response
