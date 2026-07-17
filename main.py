import os
from dotenv import load_dotenv
from openai import OpenAI

# .env faylındakı API açarını oxuyuruq
load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")

# OpenAI client-ini OpenRouter üçün qururuq
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)

def run_customer_support(user_message):
    try:
        # PROMPT ENGINEERING STRUKTURU: System prompt, Few-shot nümunələr və User prompt
        messages = [
            # 1. SYSTEM PROMPT: Modelə rolunu, dilini, tonunu və qaydalarını təyin edirik
            {
                "role": "system", 
                "content": (
                    "Sən peşəkar, səbirli və son dərəcə nəzakətli bir müştəri dəstəyi köməkçisisən.\n"
                    "Qaydaların:\n"
                    "- Yalnız Azərbaycan dilində cavab ver.\n"
                    "- Cavabların qısa, aydın və həll yönümlü olmalıdır (maksimum 2-3 cümlə).\n"
                    "- Müştəri kobud və ya əsəbi olsa belə, peşəkar üslubda empatiya quraraq cavab ver və problemi həll etməyə çalış."
                )
            },
            
            # 2. FEW-SHOT ÖRNƏKLƏR: Modelin gözlənilən cavab tonunu mənimsəməsi üçün örnəklər veririk
            # Örnək 1 (Şikayət və əsəb halı üçün):
            {"role": "user", "content": "Sifarişim hələ də gəlməyib, siz nə qədər məsuliyyətsizsiniz?!"},
            {"role": "assistant", "content": "Gecikmə üçün çox üzr istəyirik. Zəhmət olmasa, sifariş nömrənizi qeyd edin, dərhal kuryerlə əlaqə saxlayıb sizə məlumat verək."},
            
            # Örnək 2 (Məlumat sorğusu üçün):
            {"role": "user", "content": "Məhsulu necə geri qaytara bilərəm?"},
            {"role": "assistant", "content": "Məhsulu 14 gün ərzində asanlıqla geri qaytara bilərsiniz. Bunun üçün şəxsi kabinetinizdən geri qaytarma sorğusu yaratmağınız kifayətdir."},
            
            # 3. REAL USER PROMPT: Müştərinin (istifadəçinin) daxil etdiyi real sual
            {"role": "user", "content": user_message}
        ]

        # API-a sorğu göndərilir
        response = client.chat.completions.create(
            model="openrouter/free",
            messages=messages
        )
        
        # Cavabı geri qaytarırıq
        return response.choices[0].message.content

    except Exception as e:
        return f"Xəta baş verdi: {e}"

if __name__ == "__main__":
    print("--- Müştəri Dəstəyi Botu İşə Düşdü ---")
    
    # Test etmək üçün real və əsəbi bir müştəri ssenarisi hazırlayırıq
    test_customer_message = "Aldığım telefonun ekranı sınıq çıxdı! Pulumu dərhal geri istəyirəm, kömək edin!"
    
    print(f"\nMüştərinin Mesajı: '{test_customer_message}'")
    print("\nPrompt Engineering tətbiq olunaraq cavab hazırlanır...")
    
    bot_response = run_customer_support(test_customer_message)
    
    print("\nBotun Nəzakətli Cavabı:")
    print(bot_response)