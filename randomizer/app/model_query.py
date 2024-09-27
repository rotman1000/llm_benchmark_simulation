import datetime
import time
import ollama

# Function to call the Ollama model
async def query_ollama_model(model_name, prompt):
    model_response = ""
    
    start_time = time.time()

    # Send request to Ollama to generate a response in streaming mode
    stream = ollama.chat(
        model=model_name, 
        messages=[{'role': 'user', 'content': prompt}],
        stream=True,
    )

    stream = list(stream)

    if not stream:
        return {
            "model": model_name,
            "error": "No response from the model"
        }

    for chunk in stream:
        model_response += chunk['message']['content']

    first_token_time = datetime_to_unix(stream[0]['created_at'])
    last_token_time = datetime_to_unix(stream[-1]['created_at'])

    # Calculate tokens per second (TPS)
    time_difference = last_token_time - first_token_time
    tokens_per_second = len(stream) / time_difference if time_difference > 0 else 0

    # Calculate the total end-to-end latency
    total_time = time.time() - start_time

    return {
        "model": model_name,
        "text": model_response,
        "ttft": first_token_time - start_time,  # Time to First Token
        "e2e_latency": total_time,  # End-to-End Latency
        "tps": tokens_per_second  # Tokens Per Second
    }


def datetime_to_unix(datetime_str):
    """Convert ISO 8601 datetime string to Unix timestamp."""
    try:
        dt = datetime.datetime.fromisoformat(datetime_str.replace('Z', '+00:00'))
        unix_time = dt.timestamp()
        return unix_time
    except ValueError as e:
        print(f"Error parsing datetime: {e}")
        return time.time()  
