import io
import asyncio
import httpx
import pypdf

async def fetch_document_text(url):
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()
    file_data = response.content
    if url.endswith(".pdf"):
        pdf = pypdf.PdfReader(io.BytesIO(file_data))
        text = ""
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        return text
    elif url.endswith(".txt"):
        return file_data.decode("utf-8")
    else:
        return ""


async def fetch_all_documents(documents):
    results = []

    for doc in documents:
        try:
            text = await fetch_document_text(doc["url"])
            results.append({
                "document_type": doc["document_type"],
                "text": text})
        except Exception:
            results.append({
                "document_type": doc["document_type"],
                "text": ""})
    return 

