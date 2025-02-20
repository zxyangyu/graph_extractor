import os
import logging
from openai import AsyncOpenAI
from nano_graphrag import GraphRAG, QueryParam
from nano_graphrag.base import BaseKVStorage
from nano_graphrag._utils import compute_args_hash
from nano_graphrag._utils import encode_string_by_tiktoken


class GraphExtractor:
    def __init__(self, api_key, base_url, model):
        self.model = model
        self.api_key = api_key
        self.base_url = base_url
        # self.working_dir = working_dir
        self.rag = GraphRAG(
            always_create_working_dir=False,
            # working_dir=self.working_dir,
            enable_llm_cache=True,
            best_model_func=self.llm_with_cache,
            cheap_model_func=self.llm_with_cache,
        )

    async def llm_with_cache(self, prompt, system_prompt=None, history_messages=[], **kwargs) -> str:
        openai_async_client = AsyncOpenAI(api_key=self.api_key, base_url=self.base_url)
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})

        # Get the cached response if having-------------------
        hashing_kv: BaseKVStorage = kwargs.pop("hashing_kv", None)
        messages.extend(history_messages)
        messages.append({"role": "user", "content": prompt})
        if hashing_kv is not None:
            args_hash = compute_args_hash(self.model, messages)
            if_cache_return = await hashing_kv.get_by_id(args_hash)
            if if_cache_return is not None:
                return if_cache_return["return"]
        # -----------------------------------------------------
        token_sum = 0
        for message in messages:
            token_sum += len(encode_string_by_tiktoken(message["content"]))
        logging.info(f"Ready to request {self.base_url} spend token:{token_sum}")
        response = await openai_async_client.chat.completions.create(
            model=self.model, messages=messages, **kwargs
        )

        # Cache the response if having-------------------
        if hashing_kv is not None:
            await hashing_kv.upsert(
                {args_hash: {"return": response.choices[0].message.content, "model": self.model}}
            )
        # -----------------------------------------------------
        return response.choices[0].message.content

    def extraction(self, chunk_list: list[str]) -> dict:
        return self.rag.insert(chunk_list)
