import json
from groq import AsyncGroq
from config import settings

class Aggregator:
    def __init__(self):
        self.client = AsyncGroq(api_key=settings.GROQ_API_KEY)
        self.model = "llama-3.3-70b-versatile"

    async def aggregate(self, reviewer_results):
        findings = self._format_findings(reviewer_results)

        system_prompt = """
You are an appointment coordinator.
Combine the results from multiple reviewers into one final response.
Return only JSON.
{
    "summary_text": "",
    "missing_items": [],
    "suggested_priority": "routine",
    "consistency_flags": []}
"""

        user_prompt = f"""
Reviewer Results:

{findings}
"""
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
                temperature=0)
            text = response.choices[0].message.content
            return self._parse(text)
        except Exception as e:
            return self._fallback_aggregate(reviewer_results, str(e))

    @staticmethod
    def _format_findings(results):
        output = []
        for result in results:
            if result["status"] == "completed":
                output.append(
                    f"{result['reviewer']}\n{result['findings']}")
            else:
                output.append(
                    f"{result['reviewer']}\nFailed: {result.get('error','Unknown Error')}")
        return "\n\n".join(output)

    @staticmethod
    def _parse(text):
        text = text.strip()

        if text.startswith("```"):
            lines = text.splitlines()
            text = "\n".join(lines[1:-1])

        try:
            data = json.loads(text)
            priority = data.get("suggested_priority", "routine")
            if priority not in ["routine", "soon", "urgent"]:
                priority = "routine"
            return {
                "summary_text": data.get("summary_text", ""),
                "missing_items": data.get("missing_items", []),
                "suggested_priority": priority,
                "consistency_flags": data.get("consistency_flags", [])}

        except Exception:
            return {
                "summary_text": text,
                "missing_items": [],
                "suggested_priority": "routine",
                "consistency_flags": []}

    @staticmethod
    def _fallback_aggregate(results, error):
        summary = f"Aggregator Error: {error}"
        missing = []
        priority = "routine"
        flags = [] 

        for result in results:
            findings = result.get("findings", {})

            if result["reviewer"] == "summary":
                summary = findings.get("summary", summary)

            elif result["reviewer"] == "completeness":
                missing = findings.get("missing_items", [])

            elif result["reviewer"] == "urgency":
                priority = findings.get("suggested_priority", "routine")

            elif result["reviewer"] == "consistency":
                flags = findings.get("flags", [])

        return {
            "summary_text": summary,
            "missing_items": missing,
            "suggested_priority": priority,
            "consistency_flags": flags}