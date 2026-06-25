from langchain_google_genai import ChatGoogleGenerativeAI

import os

api_key=os.getenv("GEMINI_API_KEY")

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=api_key
)


def assess_asset_risk(asset):

    prompt = f"""
    Analyze this internet-facing asset.

    Asset Type: {asset.type}
    Asset Value: {asset.value}
    Status: {asset.status}
    Metadata: {asset.asset_metadata}

    Return:
    Risk Level: Low, Medium, or High

    Then explain why in one short paragraph.
    """

    response = llm.invoke(prompt)

    return response.content

