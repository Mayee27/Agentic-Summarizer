from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
# We no longer need LLMChain
import os
from dotenv import load_dotenv
import json

# Load API key from .env
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Initialize Groq model
llm = ChatGroq(model="gemma2-9b-it", api_key=GROQ_API_KEY)

# 1️⃣ Researcher Agent
def researcher_agent(text):
    prompt = PromptTemplate(
        input_variables=["text"],
        template="""
You are the Researcher Agent. Your task is to carefully read the following text and extract its key facts, arguments, and entities. Do NOT summarize or paraphrase. Just list the important factual points, events, people, and concepts.

Text:
{text}

Output format:
- Point 1: ...
- Point 2: ...
- Point 3: ...
"""
    )

    # --- CHANGE START ---
    chain = prompt | llm
    response = chain.invoke({"text": text})
    return response.content
    # --- CHANGE END ---

# 2️⃣ Summarizer Agent
def summarizer_agent(key_points):
    prompt = PromptTemplate(
        input_variables=["key_points"],
        template="""
You are the Summarizer Agent. You will take the following key points extracted by the Researcher Agent and write a coherent, well-written summary paragraph that covers all of them naturally.

Key Points:
{key_points}

Now write the summary:
"""
    )

    # --- CHANGE START ---
    chain = prompt | llm
    response = chain.invoke({"key_points": key_points})
    return response.content
    # --- CHANGE END ---

# 3️ Critic Agent (No changes needed here)
def critic_agent(summary: str, key_points: str):
    critic_llm = ChatGroq(
        model="gemma2-9b-it",
        temperature=0.0,
        max_tokens=500,
        api_key=GROQ_API_KEY
    )

    prompt_text = f"""
You are an expert summary reviewer. Compare the following summary with the key points.

Key Points:
{key_points}

Summary:
{summary}

Tasks:
1. Check if the summary covers all key points.
2. Identify any missing or inaccurate points.
3. Return a valid JSON with this format:
{{
  "is_accurate": true/false,
  "feedback": "Explain any issues",
  "missing_points": ["list missing key points"]
}}
"""
    response_obj = critic_llm.invoke(prompt_text)
    response_text = response_obj.content

    try:
        json_start = response_text.find("{")
        json_end = response_text.rfind("}") + 1
        json_str = response_text[json_start:json_end]
        json_str = json_str.replace("'", '"')
        critic_output = json.loads(json_str)
    except Exception as e:
        critic_output = {
            "is_accurate": False,
            "feedback": f"Could not parse Critic output: {e}",
            "missing_points": []
        }
    return critic_output

# 4️⃣ Re-writer Agent (This was already using the new syntax)
def rewriter_agent(summary, audience):
    prompt = PromptTemplate(
        input_variables=["summary", "audience"],
        template="""
You are the Re-writer Agent, a master of tone and style. Your task is to take the following verified summary and rewrite it for the specified target audience. Do not add or remove information. Only change the vocabulary, sentence structure, and tone.

Target Audience: {audience}

Verified Summary:
{summary}

Now, produce the final, re-written summary:
"""
    )
    
    chain = prompt | llm 
    response = chain.invoke({"summary": summary, "audience": audience})
    return response.content