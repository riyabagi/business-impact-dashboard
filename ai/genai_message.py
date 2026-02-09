import ollama

def generate_message(server, impacts):
    """Generate incident alert message using Ollama llama3"""

    if not impacts:
        return f"No business impact detected for {server}."

    impact_text = "\n".join(
        [f"- {i['service']} via {i['application']}" for i in impacts]
    )

    prompt = f"""Server failure detected: {server}

Impacted services:
{impact_text}

Write a short, professional IT incident alert message."""

    try:
        # Call Ollama API with llama3 model
        response = ollama.chat(
            model="llama3",
            messages=[
                {"role": "user", "content": prompt}
            ],
            stream=False
        )

        # Extract the message content
        if response and "message" in response:
            return response["message"]["content"]
        else:
            return f"Alert: Server {server} failure detected affecting {len(impacts)} services."

    except ConnectionError as e:
        print(f"⚠️ Ollama connection error: {e}")
        return f"ALERT: Server {server} is down. {len(impacts)} critical services affected. Immediate action required."
    
    except Exception as e:
        print(f"⚠️ Error generating message: {e}")
        return f"ALERT: Server {server} failure detected. {len(impacts)} services impacted: {', '.join([i.get('service', 'Unknown') for i in impacts])}"
