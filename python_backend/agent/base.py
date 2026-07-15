import json
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from groq import AsyncGroq
from config import settings


@dataclass
class RequestContext:
    request_id: str
    patient_name: str
    appointment_type: str
    description: str
    fetched_documents: list[dict] = field(default_factory=list)

    @property
    def document_types(self):
        return [
            doc["document_type"]
            for doc in self.fetched_documents
            if not doc.get("error")
        ]

    @property
    def document_texts(self):
        blocks = []

        for doc in self.fetched_documents:
            if doc.get("error"):
                blocks.append(
                    f"[{doc['document_type'].upper()}]\n"
                    f"Could not read document: {doc['error']}"
                )
            elif doc.get("text"):
                blocks.append(
                    f"[{doc['document_type'].upper()}]\n"
                    f"{doc['text']}"
                )

        return blocks


class BaseReviewer(ABC):

    def __init__(self):
        self.client = AsyncGroq(api_key=settings.GROQ_API_KEY)
        self.model = "llama-3.3-70b-versatile"

    @property
    @abstractmethod
    def name(self):
        pass

    @abstractmethod
    def build_prompt(self,context):
        pass

    @abstractmethod
    def parse_response(self, raw_text):
        pass

    async def review(self, context):
        system_prompt, user_prompt = self.build_prompt(context)

        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": system_prompt,
                    },
                    {
                        "role": "user",
                        "content": user_prompt,
                    },
                ],
                temperature=0,)

            raw_text = response.choices[0].message.content
            findings = self.parse_response(raw_text)

            return {
                "reviewer": self.name,
                "status": "completed",
                "findings": findings,
            }

        except Exception as e:
            return {
                "reviewer": self.name,
                "status": "failed",
                "findings": {},
                "error": str(e),
            }

    @staticmethod
    def _extract_json(text):
        text = text.strip()

        if text.startswith("```"):
            lines = text.splitlines()
            text = "\n".join(lines[1:-1])
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            return {"raw": text}