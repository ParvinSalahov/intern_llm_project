import os
from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()


api_key = os.getenv("OPENROUTER_API_KEY")


client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)

def test_api():
    try:
        print("API-a sorğu göndərilir...")
        
        response = client.chat.completions.create(
            model="openrouter/free",  # <-- OpenRouter o an aktiv olan pulsuz modeli özü seçəcək!
            messages=[
                {"role": "user", "content": "Salam! Sən kim tərəfindən yaradılmısan?"}
            ]
        )

        print("\nModelin Cavabı:")
        print(response.choices[0].message.content)
        
    except Exception as e:
        print(f"\nXəta baş verdi: {e}")

if __name__ == "__main__":
    test_api()