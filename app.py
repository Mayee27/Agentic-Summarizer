import gradio as gr
from main import run_agentic_chain  # Connects to our backend
import fitz  # The new, more powerful PyMuPDF library
import time

# --- Helper Function to Extract Text from a PDF ---
def extract_text_from_pdf(pdf_file_obj):
    """
    Opens an uploaded PDF file and extracts clean text from all pages using PyMuPDF.
    """
    if pdf_file_obj is None:
        return ""
    try:
        # Open the PDF directly from the file object's temporary path
        doc = fitz.open(pdf_file_obj.name)
        text = ""
        for page in doc:
            page_text = page.get_text("text")  # Extract plain text
            if page_text:
                text += page_text + "\n"
        doc.close()
        return text
    except Exception as e:
        return f"Error reading PDF file: {e}"

# --- Main Interface Function ---
def generate_summary_interface(text_input, pdf_input, target_audience):
    """
    Handles both text and PDF inputs, then calls the agentic chain.
    """
    content_to_summarize = ""
    # Prioritize text input if both are provided
    if text_input and text_input.strip():
        content_to_summarize = text_input
    elif pdf_input is not None:
        # If no text, process the PDF
        content_to_summarize = extract_text_from_pdf(pdf_input)
        if "Error reading" in content_to_summarize:
            return content_to_summarize  # Show the PDF error to the user
    else:
        return "Please either paste text or upload a PDF file to continue."

    # Call the existing agentic chain function from main.py
    final_summary = run_agentic_chain(content_to_summarize, target_audience)
    return final_summary

# --- Gradio UI ---
with gr.Blocks(theme=gr.themes.Soft(), title="Agentic Summarizer") as iface:
    gr.Markdown("# Agentic Summarizer Swarm 🤖✍️")
    gr.Markdown(
        "Use a team of AI agents to create a high-quality summary tailored to a specific audience."
    )

    with gr.Row():
        with gr.Column(scale=2):
            # Create Tabs for different input methods
            with gr.Tabs():
                with gr.TabItem("Paste Text"):
                    text_input = gr.Textbox(
                        lines=15,
                        label="Paste Text Here",
                        placeholder="Enter a long piece of text...",
                    )
                with gr.TabItem("Upload PDF"):
                    pdf_input = gr.File(
                        label="Upload your PDF", file_types=[".pdf"]
                    )

        with gr.Column(scale=1):
            audience_input = gr.Dropdown(
                choices=[
                    "A High School Student",
                    "A Technical Expert",
                    "A Busy Executive",
                    "A 10-Year-Old Child",
                ],
                label="Select Target Audience",
                value="A High School Student",
            )
            submit_button = gr.Button("✨ Generate Summary ✨", variant="primary")

    summary_output = gr.Textbox(
        label="Tailored Summary", interactive=False, lines=15
    )

    # Connect the button's click event to our function, passing all inputs
    submit_button.click(
        fn=generate_summary_interface,
        inputs=[
            text_input,
            pdf_input,
            audience_input,
        ],  # Pass all inputs to the function
        outputs=summary_output,
        api_name="summarize",
    )

# Launch the application
if __name__ == "__main__":
    iface.launch()