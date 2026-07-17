# LLM API İnteqrasiyası və Prompt Engineering (Həftə 1)

Bu layihə təcrübə proqramının (internship) 1-ci həftə tapşırığı çərçivəsində yaradılmışdır. Layihədə OpenRouter API vasitəsilə LLM (Böyük Dil Modeli) inteqrasiyası reallaşdırılmış və API açarlarının təhlükəsiz idarə olunması təmin edilmişdir.

---

## Layihənin Quraşdırılması və İşə Salınması

Proqramı öz lokal kompüterinizdə işə salmaq üçün aşağıdakı addımları növbə ilə yerinə yetirin:

### 1. Virtual Mühitin (venv) Yaradılması və Aktivləşdirilməsi
Layihə qovluğunda terminalı açın və sisteminizə uyğun olaraq aşağıdakı əmrləri icra edin:

* **Virtual mühitin yaradılması:**
  ```bash
  python -m venv venv


Aktivləşdirilməsi (Windows - PowerShell üçün):

PowerShell
.\venv\Scripts\Activate.ps1
Aktivləşdirilməsi (Windows - CMD üçün):

DOS
venv\Scripts\activate
Aktivləşdirilməsi (macOS / Linux üçün):

Bash
source venv/bin/activate
(Aktivləşdikdən sonra terminal sətirinin əvvəlində (venv) yazısı görünməlidir).

2. Lazımi Kitabxanaların Quraşdırılması
Virtual mühit daxilində lazımi paketləri yükləmək üçün bu əmri yazın:

Bash
pip install -r requirements.txt
3. API Açarlarının Konfiqurasiyası (.env)
Layihə qovluğunda .env adlı fayl yaradın və OpenRouter platformasından aldığınız API açarını bura əlavə edin:

Code snippet
OPENROUTER_API_KEY=sizin_real_openrouter_api_açarınız
(Qeyd: .gitignore faylı vasitəsilə real .env faylının GitHub-a sızmasının qarşı təhlükəsiz şəkildə alınmışdır).

4. Kodu İşə Salın
Hər şey hazır olduqdan sonra ilk API sorğusunu göndərmək üçün proqramı başladın:

Bash
python main.py
📄 Nümunə Sorğu və Cavab Logları (Logs)
Checkpoint 2: Prompt Engineering (Müştəri Dəstəyi Asistanı)
Müştərinin Daxil Etdiyi Real Mesaj (User Input):

"Aldığım telefonun ekranı sınıq çıxdı! Pulumu dərhal geri istəyirəm, kömək edin!"

Modelin Qaydalar və Few-shot Örnəklərə Uyğun Nəzakətli Cavabı (LLM Output):

"Yaşadığınız bu xoşagəlməz vəziyyətə görə çox üzr istəyirik. Sifariş nömrənizi və məhsulun şəklini bizə təqdim edə bilərsinizmi? Dərhal geri qaytarma və ödəniş prosesini başladacağıq."

## Xəta İdarəetməsi (Error Handling)

Layihəyə `try-except` blokları və `retry` mexanizmi əlavə olunmuşdur:
- **Rate Limit & Timeout:** API-dan gələn xətaları idarə etmək üçün "Exponential Backoff" (artan gecikməli təkrar sorğu) tətbiq olunmuşdur.
- **Avtomatik Cəhd:** Kod xəta baş verdikdə avtomatik olaraq 3 dəfəyə qədər yenidən sorğu göndərir.

📂 Layihə Strukturunun Görünüşü
intern_llm_project/
│
├── venv/                  # Virtual mühit qovluğu (GitHub-a yüklənilmir)
├── .env                   # Real API açarının saxlandığı gizli fayl (GitHub-a yüklənilmir)
├── .env.example           # Digər tərtibatçılar üçün nümunə env faylı
├── .gitignore             # Hansı faylların Git-ə getməyəcəyini təyin edən tənzimləmə
├── requirements.txt       # Layihə üçün lazım olan Python kitabxanalarının siyahısı
├── README.md              # Layihə haqqında ümumi məlumat və təlimat faylı
└── main.py                # Əsas icra olunan Python kodu