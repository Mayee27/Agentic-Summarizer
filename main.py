# main.py

# 1. Import all agent functions, the text splitter, and the time library
from agents import researcher_agent, summarizer_agent, critic_agent, rewriter_agent
from langchain_text_splitters import RecursiveCharacterTextSplitter
import time

# 2. Define the main function that handles the entire workflow
def run_agentic_chain(original_text, target_audience):
    """
    Runs the full sequence of agents, with chunking for large documents and a delay to prevent rate-limiting.
    """
    
    # Split the document into manageable chunks
    print("Splitting the document into manageable chunks...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=4000,  # The size of each chunk in characters
        chunk_overlap=200   # The overlap between chunks to maintain context
    )
    chunks = text_splitter.split_text(original_text)
    print(f"Document split into {len(chunks)} chunks.")
    print("-" * 20)

    # Process each chunk individually
    chunk_summaries = []
    for i, chunk in enumerate(chunks):
        print(f"Processing Chunk {i+1}/{len(chunks)}...")
        
        # Run the first 3 agents on the chunk
        key_points = researcher_agent(chunk)
        summary_draft = summarizer_agent(key_points)
        critic_feedback = critic_agent(summary_draft, key_points) # The critic still runs to ensure quality
        
        print(f"   - Chunk {i+1} summarized.")
        chunk_summaries.append(summary_draft)

        # Add a 1-second delay to avoid hitting the API rate limit
        time.sleep(1) 
    
    print("-" * 20)
    print("All chunks summarized. Combining results...")

    # Combine the summaries of all chunks
    combined_summary = "\n\n".join(chunk_summaries)

    # Use the Re-writer agent one last time for a final polish
    print("4. Re-writer Agent is creating the final polished summary...")
    final_summary = rewriter_agent(combined_summary, target_audience)
    print("   - Final summary adapted for the audience.")
    print("-" * 20)
    
    return final_summary


# 3. This block is for testing the script directly (optional)
if __name__ == "__main__":
    # Sample text for summarization
    sample_text = """
    Artificial intelligence (AI) is the simulation of human intelligence in machines
    that are programmed to think like humans and mimic their actions. Applications
    include healthcare for diagnostics, finance for fraud detection, and education
    for personalized learning. However, the advancement of AI raises ethical
    considerations such as bias, privacy, and transparency.
    """

    # Define the target audience
    audience = "a high school student"

    # Run the full chain
    final_result = run_agentic_chain(sample_text, audience)
    
    print("\n FINAL TAILORED SUMMARY:\n")
    print(final_result)