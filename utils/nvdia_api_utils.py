# utils/nvidia_api_utils.py

from openai import OpenAI

def get_nvidia_client(api_key):
    return OpenAI(base_url="https://integrate.api.nvidia.com/v1", api_key=api_key)

def generate_response(client, context, question):
    prompt = f"{context}\n\nQuestion: {question}\nAnswer:"
    completion = client.chat.completions.create(
        model="nvidia/llama-3.1-nemotron-70b-instruct",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5,
        top_p=1,
        max_tokens=1024,
        stream=True
    )
    response_text = ""
    for chunk in completion:
        if chunk.choices[0].delta.content is not None:
            response_text += chunk.choices[0].delta.content
    return response_text
