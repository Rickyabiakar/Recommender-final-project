from llama_cpp import Llama

llm = Llama(
    model_path="models/llm/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf",  # make sure case matches your file!
    n_ctx=1024,
    verbose=True  # 👈 This shows you logs during Docker run
)

def explain_recommendations(book_list):
    prompt = (
        "A user liked these books:\n"
        + "\n".join(f"- {title}" for title in book_list)
        + "\n\nWhy do these recommended books make sense based on the user's interests?\n"
        "Give a short explanation:"
    )
    result = llm(prompt, max_tokens=150)
    return result['choices'][0]['text'].strip()


    # ✅ Handle case where result might be empty
    try:
        return result['choices'][0]['text'].strip()
    except Exception as e:
        return f"⚠️ LLM failed to generate a response: {e}"
