# Agentic Summarizer Swarm
This project is a sophisticated text summarization application that utilizes a multi-agent AI system to generate high-quality, accurate, and audience-tailored summaries from either pasted text or uploaded PDF documents.

# Features

* Multi-Agent System: A team of four specialized AI agents (Researcher, Summarizer, Critic, and Rewriter) collaborate to produce the final summary.
* Audience Adaptation: Users can select a target audience (e.g., "Technical Expert," "High School Student"), and the final summary's tone and vocabulary will be adjusted accordingly.
* Dual Input Modes: Supports both direct text input and PDF document uploads for maximum flexibility.
* Robust Document Handling: Employs advanced text chunking to process large documents without exceeding API context limits.
* User-Friendly Interface: Built with Gradio for a clean, simple, and intuitive user experience.

# How It Works

The application follows an "agentic" workflow, where each AI agent performs a specific, sequential task. This decomposition of the problem leads to a more reliable and higher-quality result than a single-prompt approach.

The workflow is as follows:
1. The `Researcher` Agent: Ingests the source text and extracts a structured list of key facts, arguments, and entities.
2. The `Summarizer` Agent: Takes the key points from the Researcher and weaves them into a coherent, well-written draft summary.
3. The `Critic` Agent: Reviews the summary draft, comparing it against the original key points to check for accuracy, completeness, and potential hallucinations.
4. The `Rewriter` Agent: Takes the verified summary and adapts its style, tone, and vocabulary to match the user-selected target audience.

# Project Structure
    agentic_summarizer/
    │
    ├── .env                  # Stores API keys
    ├── agents.py             # Defines the four AI agents
    ├── app.py                # The Gradio user interface
    ├── main.py               # The main orchestration logic
    └── requirements.txt      # Project dependencies

# Setup and Installation

Follow these steps to set up and run the project locally.

1. Build a Repository 
   AGENTIC_SUMMARIZER

2. Create a Virtual Environment
It's highly recommended to use a virtual environment to manage project dependencies.

 -- Create the virtual environment
python -m venv venv

 -- Activate it (Windows)
.\venv\Scripts\activate

3. Install Dependencies

pip install -r requirements.txt

4. Set Up Your API Key
* The project uses the Groq API for fast LLM inference.
* Create a .env file in the root of the project folder.
* Sign up for a free account at Groq to get an API key.
* Add your API key to the .env file like this:
GROQ_API_KEY="gsk_YourSecretGroqAPIKeyGoesHere"

5. How to Run the Application
* With your environment set up and the API key in place, running the Gradio application is simple.
* Make sure your virtual environment is activated.
* Run the app.py script from your terminal:
        python app.py
* Open your web browser and navigate to the local URL provided in the terminal (usually http://127.0.0.1:7860).
* You can now use the application to generate tailored summaries!

# Technologies Used
1. Backend: Python
2. AI Framework: LangChain
3. LLM Provider: Groq (using the Gemma2 model)
4. Web UI: Gradio
5. PDF Parsing: PyMuPDF
