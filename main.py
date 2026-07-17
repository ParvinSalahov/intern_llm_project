import os
from dotenv import load_dotenv
from openai import OpenAI
import sys  # Ekrana anlıq yazdırmağı idarə etmək üçün

# .env faylındakı API açarını oxuyuruq
load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")

# OpenAI client-ini OpenRouter üçün qururuq
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)

# --- CHECKPOINT 1: SADƏ API İNTEQRASİYASI ---
def run_checkpoint_1_simple_test():
    try:
        print("\n[Checkpoint 1] API-a sadə sorğu göndərilir...")
        response = client.chat.completions.create(
            model="openrouter/free",
            messages=[
                {"role": "user", "content": "Salam! Sən kim tərəfindən yaradılmısan?"}
            ]
        )
        print("Modelin Cavabı:")
        print(response.choices[0].message.content)
    except Exception as e:
        print(f"Xəta baş verdi: {e}")


# --- CHECKPOINT 2: PROMPT ENGİNEERİNG & FEW-SHOT ---
def run_checkpoint_2_customer_support(user_message):
    try:
        print("\n[Checkpoint 2] Prompt Engineering tətbiq olunaraq cavab hazırlanır...")
        messages = [
            # System Prompt (Rol və Qaydalar)
            {
                "role": "system", 
                "content": (
                    "Sən peşəkar, səbirli və son dərəcə nəzakətli bir müştəri dəstəyi köməkçisisən.\n"
                    "Qaydaların:\n"
                    "- Yalnız Azərbaycan dilində cavab ver.\n"
                    "- Cavabların qısa, aydın və həll yönümlü olmalıdır (maksimum 2-3 cümlə).\n"
                    "- Müştəri kobud və ya əsəbi olsa belə, peşəkar üslubda empatiya quraraq cavab ver."
                )
            },
            # Few-shot Nümunələr
            {"role": "user", "content": "Sifarişim hələ də gəlməyib, siz nə qədər məsuliyyətsizsiniz?!"},
            {"role": "assistant", "content": "Gecikmə üçün çox üzr istəyirik. Zəhmət olmasa, sifariş nömrənizi qeyd edin, dərhal kuryerlə əlaqə saxlayıb sizə məlumat verək."},
            
            {"role": "user", "content": "Məhsulu necə geri qaytara bilərəm?"},
            {"role": "assistant", "content": "Məhsulu 14 gun ərzində asanlıqla geri qaytara bilərsiniz. Bunun üçün şəxsi kabinetinizdən geri qaytarma sorğusu yaratmağınız kifayətdir."},
            
            # Real müştəri mesajı
            {"role": "user", "content": user_message}
        ]

        response = client.chat.completions.create(
            model="openrouter/free",
            messages=messages
        )
        print("Botun Nəzakətli Cavabı:")
        print(response.choices[0].message.content)

    except Exception as e:
        print(f"Xəta baş verdi: {e}")


# --- CHECKPOINT 3: STREAMING CAVAB İDARƏETMƏSİ ---
def run_checkpoint_3_streaming_support(user_message):
    try:
        print("\n[Checkpoint 3] Streaming ilə cavab alınır...")
        messages = [
            {
                "role": "system", 
                "content": "Sən peşəkar və nəzakətli bir müştəri dəstəyi köməkçisisən. Qısa cavablar ver."
            },
            {"role": "user", "content": user_message}
        ]

        # stream=True parametrini əlavə edirik
        response = client.chat.completions.create(
            model="openrouter/free",
            messages=messages,
            stream=True  # Bu hissə cavabın axınla gəlməsini təmin edir
        )

        print("Botun Cavabı (Sözbəsöz yazılır): ", end="", flush=True)
        
        # Gələn hər bir söz parçasını (chunk) anlıq ekrana çıxarırıq
        for chunk in response:
            if chunk.choices[0].delta.content:
                # sys.stdout.write vasitəsilə yeni sətirə keçmədən yan-yana yazdırırıq
                sys.stdout.write(chunk.choices[0].delta.content)
                sys.stdout.flush()
        print() # Cavab bitəndə yeni sətirə keçmək üçün

    except Exception as e:
        print(f"\nXəta baş verdi: {e}")
    


import time  # Xəta olduqda gözləmə müddəti üçün

# --- CHECKPOINT 4: XƏTA İDARƏETMƏSİ (RETRY LOGIC) ---
def run_checkpoint_4_error_handling(user_message):
    max_retries = 3
    
    for attempt in range(max_retries):
        try:
            print(f"\n[Checkpoint 4] Sorğu göndərilir (Cəhd: {attempt + 1})...")
            
            response = client.chat.completions.create(
                model="openrouter/free",
                messages=[
                    {"role": "system", "content": "Sən köməkçi bir robotsan."},
                    {"role": "user", "content": user_message}
                ]
            )
            print("Cavab uğurla alındı!")
            print(response.choices[0].message.content)
            return  # Uğurlu oldu, funksiyadan çıxırıq

        except Exception as e:
            print(f"Xəta baş verdi: {e}")
            
            if attempt < max_retries - 1:
                sleep_time = 2 ** attempt  # 1, 2, 4 saniyə gözləmə
                print(f"Retry edilir... {sleep_time} saniyə gözləyirik.")
                time.sleep(sleep_time)
            else:
                print("Maksimum cəhd sayına çatdıq. Xəta davam edir.")


import json
import re

# --- CHECKPOINT 5: ÇIXIŞ PARSİNG/VALİDASİYASI ---
def run_checkpoint_5_json_parsing(user_message):
    try:
        print("\n[Checkpoint 5] JSON formatında cavab tələb olunur və təmizlənir...")
        
        # System prompt-da xüsusi tapşırıq veririk
        messages = [
            {"role": "system", "content": "Yalnız və yalnız JSON formatında cavab ver. Heç bir əlavə şərh yazma. Format: {\"cavab\": \"...\", \"status\": \"success\"}"},
            {"role": "user", "content": user_message}
        ]

        response = client.chat.completions.create(
            model="openrouter/free",
            messages=messages
        )
        
        raw_text = response.choices[0].message.content
        print(f"Modelin xam cavabı: {raw_text}")

        # Təmizləmə əməliyyatı:
        # 1. Regex ilə ```json ... ``` bloklarını tapıb çıxarırıq
        json_match = re.search(r'\{.*\}', raw_text, re.DOTALL)
        
        if json_match:
            clean_json = json_match.group(0)
            data = json.loads(clean_json) # JSON-u obyektə çeviririk
            print("Uğurla təmizləndi və pars edildi:")
            print(data)
            print(f"Status: {data['status']}")
        else:
            print("Xəta: Cavabın içində JSON tapılmadı!")

    except json.JSONDecodeError:
        print("Xəta: Model korrupsiya olunmuş (invalid) JSON qaytardı.")
    except Exception as e:
        print(f"Gözlənilməz xəta: {e}")

    
if __name__ == "__main__":
    print("=== TƏCRÜBƏ PROQRAMI - HƏFTƏ 1 ===")
    
    # Hər hansı checkpoint-i test etmək üçün əvvəlindəki '#' işarəsini silə bilərsən
    
    # 1. Hissə: Checkpoint 1 testi
    # run_checkpoint_1_simple_test()
    
    # 2. Hissə: Checkpoint 2 testi
    # test_message = "Aldığım telefonun ekranı sınıq çıxdı! Pulumu dərhal geri istəyirəm, kömək edin!"
    # run_checkpoint_2_customer_support(test_message)
    
    # 3. Hissə: Checkpoint 3 testi (Streaming) - İndi bunu komentə alırıq
    # test_message_3 = "Kuryer mənə çatmalı olan bağlamanı səhv ünvana aparıb..."
    # run_checkpoint_3_streaming_support(test_message_3)
    
    # 4. Hissə: Checkpoint 4 testi (Xəta idarəetməsi) - YALNIZ BU İŞLƏYƏCƏK
    #run_checkpoint_4_error_handling("Salam, sistem işləyirmi?")
    
    #5. Hisse: Chechpoint 5 testi
    run_checkpoint_5_json_parsing("Azərbaycanın paytaxtı haradır?")