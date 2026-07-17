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
📄 Nümunə Sorğu və Cavab Logu
Göndərilən Sorğu (Prompt):

"Salam! Sən kim tərəfindən yaradılmısan?"

Modelin Qaytardığı Cavab (Response):

"Salam! Mən Nemotron, NVIDIA tərəfindən yaratılmış bir AI-assistançım."