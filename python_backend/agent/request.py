from agent.base import BaseReviewer, RequestContext

class SummaryReviewer(BaseReviewer):
    @property
    def name(self):
        return "summary"

    def build_prompt(self, context: RequestContext) :
        system_prompt = """
You are a clinical intake coordinator writting a brief for a scheduling team.
Read the patient's request and produce a concise, neutral summary.

Rules:
- 3 to 5 sentences only.
- Plain language — no medical jargon or diagnostic language.
- Do NOT diagnose, speculate, or give medical advice.
- Cover: what the patient wants, why they are coming in, any relevant context.

Respond ONLY with valid JSON — no markdown, no preamble:
{
  "summary": "<3-5 sentence summary>",
  "key_concerns": ["<concern 1>", "<concern 2>"]
}
""".strip()
        doc_section = ""
        if context.document_texts:
            doc_section = "\n\nATTACHED DOCUMENTS:\n"
            doc_section += "\n\n-\n\n".join(context.document_texts)

        user_prompt = f"""
APPOINTMENT TYPE: {context.appointment_type}
PATIENT NAME: {context.patient_name}

PATIENT'S DESCRIPTION:
{context.description}
{doc_section}
""".strip()

        return system_prompt, user_prompt

    def parse_response(self, raw_text: str) -> dict:
        data = self._extract_json(raw_text)
        return {
            "summary"     : data.get("summary", raw_text),
            "key_concerns": data.get("key_concerns", [])}


class CompletenessReviewer(BaseReviewer):

    @property
    def name(self) :
        return "completeness"

    def build_prompt(self, context: RequestContext) -> tuple[str, str]:
        system_prompt = """
You are a medical records clerk checking whether an appointment request
has everything it needs before it can be scheduled.

Rules:
- Based on the appointment type and description, decide what documents
  are typically expected for this kind of visit.
- Cross-check against the list of documents actually attached.
- A document MENTIONED in the description but NOT in the attached list is a gap.
- Do NOT invent requirements beyond what is reasonable for this appointment type.
- Do NOT diagnose or give medical advice.

Respond ONLY with valid JSON — no markdown, no preamble:
{
  "is_complete": true | false,
  "present_items": ["<document type present>"],
  "missing_items": ["<document type expected but absent>"],
  "notes": "<optional 1-sentence clarification>"
}
""".strip()

        attached = ", ".join(context.document_types) if context.document_types else "None attached"

        user_prompt = f"""
APPOINTMENT TYPE: {context.appointment_type}

PATIENT'S DESCRIPTION:
{context.description}

DOCUMENTS ATTACHED: {attached}
""".strip()

        return system_prompt, user_prompt

    def parse_response(self, raw_text: str) -> dict:
        data = self._extract_json(raw_text)
        return {
            "is_complete"  : data.get("is_complete", False),
            "present_items": data.get("present_items", []),
            "missing_items": data.get("missing_items", []),
            "notes"        : data.get("notes", "")}

class UrgencyReviewer(BaseReviewer):

    @property
    def name(self):
        return "urgency"

    def build_prompt(self, context: RequestContext):
        system_prompt = """
You are an administrative urgency reviewer assistant helping a clinic organise its queue.
Suggest how soon a coordinator should look at this request.

IMPORTANT:
- You are NOT a doctor. No diagnoses. No medical advice.
- This is a QUEUE-ORGANISING suggestion only — the coordinator confirms.
- Base your suggestion on logistics and what the patient explicitly wrote:
    routine → no stated time pressure, standard check-up or follow-up
    soon    → patient mentions a near-term date, or worsening situation
    urgent  → patient uses urgent language, deadline on a referral, or
              clearly time-sensitive administrative situation
- Do NOT mark "urgent" defensively .

Respond ONLY with valid JSON — no markdown, no preamble:
{
  "suggested_priority": "routine" | "soon" | "urgent",
  "reason": "<1-2 sentence plain language reason>",
  "suggestion": "This is a queue-organising suggestion only. The coordinator should confirm."
}
""".strip()

        user_prompt = f"""
APPOINTMENT TYPE: {context.appointment_type}

PATIENT'S DESCRIPTION:
{context.description}
""".strip()

        return system_prompt, user_prompt

    def parse_response(self, raw_text: str) -> dict:
        data= self._extract_json(raw_text)
        priority = data.get("suggested_priority", "routine")

        if priority not in ("routine", "soon", "urgent"):
            priority = "routine"

        return {
            "suggested_priority": priority,
            "reason": data.get("reason", ""),
            "suggestion" : data.get("suggestion", "This is a suggestion only.")}


class ConsistencyReviewer(BaseReviewer):

    @property
    def name(self) :
        return "consistency"

    def build_prompt(self, context: RequestContext) :
        system_prompt = """
You are a scheduling quality checker. Verify that the appointment type a
patient selected is consistent with:
  1. What they wrote in their description
  2. The content of any attached documents (read carefully)

Rules:
- Flag GENUINE mismatches only — e.g. type is "Radiology" but description
  and documents clearly describe a blood test appointment.
- Minor wording differences are NOT mismatches — use common sense.
- Do NOT diagnose or give medical advice.
- If everything is consistent, say so clearly.

Respond ONLY with valid JSON — no markdown, no preamble:
{
  "is_consistent": true | false,
  "flags": ["<specific mismatch>"],
  "recommendation": "<optional 1 sentence for the coordinator>"
}
""".strip()


        doc_section = ""
        if context.document_texts:
            doc_section = "\n\nATTACHED DOCUMENTS:\n"
            doc_section += "\n\n-\n\n".join(context.document_texts)

        user_prompt = f"""
APPOINTMENT TYPE SELECTED: {context.appointment_type}
DOCUMENTS ATTACHED: {", ".join(context.document_types) or "None"}

PATIENT'S DESCRIPTION:
{context.description}
{doc_section}
""".strip()
        return system_prompt, user_prompt

    def parse_response(self, raw_text: str):
        data = self._extract_json(raw_text)
        return {
            "is_consistent" : data.get("is_consistent", True),
            "flags": data.get("flags", []),
            "recommendation": data.get("recommendation", "")}