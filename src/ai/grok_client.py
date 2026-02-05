# src/ai/grok_client.py
import os
from openai import OpenAI
from dotenv import load_dotenv
#Testing app 
#python -m src.ai.grok_client  
load_dotenv()

class GrokClient:
    def __init__(self, model: str = "grok-3"):
        api_key = os.getenv("XAI_API_KEY")
        if not api_key:
            raise ValueError("XAI_API_KEY not found in .env")
        
        self.client = OpenAI(
            api_key=api_key,
            base_url="https://api.x.ai/v1",
        )
        self.model = model

    def chat(
        self,
        messages: list[dict],
        temperature: float = 0.7,
        max_tokens: int = 800,
        **kwargs
    ):
        """Simple chat completion wrapper"""
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            **kwargs
        )
        return response.choices[0].message.content.strip()

    def generate_tailored_summary(
        self,
        job_description: str,
        master_profile_summary: str,
        max_tokens: int = 400
    ):
        """Example: tailored professional summary"""
        prompt = f"""
You are an expert ATS-optimized resume writer.
Using this master profile summary:
{master_profile_summary}

And this job description:
{job_description}

Write a concise, keyword-rich professional summary (4-6 lines max) that:
- Starts with a strong title/expertise match
- Incorporates exact keywords from the job posting
- Quantifies achievements where possible
- Sounds natural, confident, and human-written
        """
        messages = [
            {"role": "system", "content": "You are a professional resume optimizer."},
            {"role": "user", "content": prompt}
        ]
        return self.chat(messages, temperature=0.6, max_tokens=max_tokens)


        
    def query(
        self,
        prompt: str,
        model: str = None,
        temperature: float = 0.0,
        max_tokens: int = 4500,
    ) -> str:
        """
        Compatibility method for scripts that expect .query(prompt).
        Wraps a single user message.
        """
        if model is None:
            model = self.model

        messages = [{"role": "user", "content": prompt}]

        return self.chat(
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )
# ────────────────────────────────────────────────
# Simple smoke test / usage example
# ────────────────────────────────────────────────
if __name__ == "__main__":
    print("=== GrokClient smoke test ===\n")

    try:
        grok = GrokClient(model="grok-3")   # or try "grok-4-1-fast-reasoning"
        print(f"Client initialized with model: {grok.model}")

        messages = [
            {"role": "system", "content": "You are a concise assistant."},
            {"role": "user", "content": "Say hello and give today's date."}
        ]

        response = grok.chat(messages, temperature=0.7, max_tokens=80)
        print("\nResponse:")
        print(response)

    except Exception as e:
        print("Test failed:")
        print(str(e))
        print("\nQuick checks:")
        print("  • Is XAI_API_KEY set in .env?")
        print("  • Is openai installed? (pip install openai)")
        print("  • Try a different model name from console.x.ai")