import os
import sys
import time
import json
import re
from dotenv import load_dotenv
from openai import OpenAI

# .env faylındakı API açarını yükləyirik
load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")

# OpenAI client-ini təyin edirik
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)

# ==========================================================
# 1. ORTAQ REQUEST PIPELINE (INTEGRATED PIPELINE)
# ==========================================================
def execute_llm_pipeline(messages, expect_json=False, max_retries=3):
    """
    Sənaye standartlarına uyğun ortaq pipeline:
    - Retry Logic (Exponential Backoff)
    - Streaming Output (Ekrana anlıq yazdırma)
    - Reusable Full Content Capture (Yenidən istifadə edilə bilən mətn)
    - JSON Parsing & Validation
    - Token Usage Logging
    """
    for attempt in range(max_retries):
        try:
            print(f"\n[Pipeline] Sorğu göndərilir (Cəhd {attempt + 1}/{max_retries})...")
            
            # 1. API Call (Streaming enabled)
            response = client.chat.completions.create(
                model="openrouter/free",
                messages=messages,
                stream=True
            )

            print("Botun Cavabı (Streaming): ", end="", flush=True)
            
            full_response_text = ""
            
            # 2. Real-time Streaming and Reusable Output Capture
            for chunk in response:
                if chunk.choices and chunk.choices[0].delta.content:
                    content = chunk.choices[0].delta.content
                    sys.stdout.write(content)
                    sys.stdout.flush()
                    full_response_text += content  # Mətni yenidən istifadə üçün toplayırıq
            print() # Yeni sətirə keçid

            # 3. JSON Parsing və Validation (Tələb olunarsa)
            parsed_json = None
            if expect_json:
                json_match = re.search(r'\{.*\}', full_response_text, re.DOTALL)
                if json_match:
                    clean_json = json_match.group(0)
                    parsed_json = json.loads(clean_json)
                    print("✅ [Validation] JSON uğurla təmizləndi və pars olundu.")
                else:
                    raise ValueError("Modelin cavabında keçərli JSON strukturu tapılmadı!")

            # 4. Token İstifadəsinin Simulyasiya/Hesablanması
            # (Qeyd: OpenRouter Streaming rejimində usage obyektini sonda göndərir)
            approx_tokens = len(full_response_text.split()) * 1.3
            print(f"📊 [Token Log] Təxmini sərf olunan token: ~{int(approx_tokens)} tokens")

            return {
                "raw_text": full_response_text,
                "parsed_json": parsed_json,
                "status": "success"
            }

        except Exception as e:
            print(f"\n⚠️ [Pipeline Xətası]: {e}")
            if attempt < max_retries - 1:
                sleep_time = 2 ** attempt
                print(f"🔄 Retry edilir... {sleep_time} saniyə gözlənilir.")
                time.sleep(sleep_time)
            else:
                print("❌ [Maksimum cəhd dərəcəsi aşıldı]: Sorğu uğursuz oldu.")
                return {"status": "failed", "error": str(e)}

# ==========================================================
# 2. APPLICATION LOGIC (MÜŞTƏRİ DƏSTƏYİ TƏTBİQİ)
# ==========================================================
def run_integrated_customer_support(user_message):
    system_prompt = (
        "Sən peşəkar, səbirli və nəzakətli bir müştəri dəstəyi köməkçisisən.\n"
        "Qaydaların:\n"
        "- Cavabı mütləq keçərli JSON formatında ver: {\"response\": \"...\", \"sentiment\": \"...\"}\n"
        "- 'sentiment' xanası müştərinin əhvalını göstərməlidir (angry, neutral, happy).\n"
        "- Yalnız Azərbaycan dilində cavab ver."
    )

    messages = [
        {"role": "system", "content": system_prompt},
        # Few-Shot Nümunələr
        {"role": "user", "content": "Sifarişim gecikir, bu nə məsuliyyətsizlikdir?!"},
        {"role": "assistant", "content": "{\"response\": \"Gecikmə üçün çox üzr istəyirik. Zəhmət olmasa sifariş nömrənizi qeyd edin.\", \"sentiment\": \"angry\"}"},
        # Real User Prompt
        {"role": "user", "content": user_message}
    ]

    # Mərkəzləşdirilmiş Pipeline-ı çağırırıq
    result = execute_llm_pipeline(messages, expect_json=True)
    return result

# ==========================================================
# 3. İCRA
# ==========================================================
if __name__ == "__main__":
    print("=== SƏNAYE STANDARTLI LLM PIPELINE İŞƏ DÜŞDÜ ===")
    
    test_user_input = "Aldığım telefonun ekranı zədələnib! Dərhal pulumu qaytarın!"
    print(f"\nİstifadəçi Mesajı: '{test_user_input}'")
    
    pipeline_result = run_integrated_customer_support(test_user_input)
    
    if pipeline_result["status"] == "success":
        print("\n🎉 Yekun Emal Olunmuş Nəticə (Reused Data):")
        print("Təmiz Cavab:", pipeline_result["parsed_json"]["response"])
        print("Müştəri Əhvalı (Sentiment):", pipeline_result["parsed_json"]["sentiment"])