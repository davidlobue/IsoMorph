import instructor
from openai import OpenAI
from pydantic import BaseModel
from typing import List, Optional, Type
from core.models import DocumentSource
from core.config import LLMConfig
from core.prompts import Prompts

class DistillationEngine:
    def __init__(self):
        self.model_name = LLMConfig.get_model_name()
        self.async_client = LLMConfig.get_async_client()

    async def extract_features(self, document: DocumentSource, dynamic_schema: Type[BaseModel]) -> BaseModel:
        """
        Uses Instructor to extract heavily structured constraints from text.
        Forces the LLM strictly into the native programmatic Pydantic fields mapped by bounded Discovery logic.
        """
        extraction = await self.async_client.chat.completions.create(
            model=self.model_name,
            messages=[
                {
                    "role": "system",
                    "content": Prompts.DISTILLATION_SYSTEM,
                },
                {
                    "role": "user",
                    "content": Prompts.get_distillation_user(document.text_content),
                }
            ],
            response_model=dynamic_schema,
            #max_tokens=8000
        )
        return extraction

    async def multi_source_review(self, documents: List[DocumentSource], dynamic_schema: Type[BaseModel]) -> List[BaseModel]:
        """
        Processes multiple documents through the extraction engine under the formal mathematical blueprint constraints.
        """
        import asyncio
        tasks = [self.extract_features(doc, dynamic_schema) for doc in documents]
        results = await asyncio.gather(*tasks)
        return list(results)
