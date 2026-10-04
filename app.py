from flask import Flask, request, render_template_string
import requests
import urllib.parse
import time

app = Flask(__name__)

# 🔑 رمز الدخول الخاص بك لإنشاء الصفحات
SECRET_ACCESS_CODE = "XOREYT123400028"

# 🔔 رابط Discord Webhook الخاص بك لإرسال معلومات الزوار
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1556178719171940412/cLjKIxt81tQvjaBaNK6FVJidzGwQdZdkqhdiIiqtOV85pCmr2k4LHP4e6cYy5-PwCXkg"

# 🛡️ مفتاح VirusTotal API الخاص بك
VIRUSTOTAL_API_KEY = "a9068f5586219ca658cd2d39dcd5e585229e8042f404c65ab21744612e6a86d3"

# 🛡️ مفاتيح reCAPTCHA
RECAPTCHA_SITE_KEY = "6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI"
RECAPTCHA_SECRET_KEY = "6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe"

# 🌟 قالب الهيكل الأساسي
HTML_LAYOUT = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title if title else 'مركز مشاركة الملفات الاحترافي' }}</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://www.google.com/recaptcha/api.js" async defer></script>
    <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800;900&display=swap" rel="stylesheet">
    <style>
        body { font-family: 'Cairo', sans-serif; }
        .glass-panel {
            background: rgba(15, 23, 42, 0.75);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border: 1px solid rgba(255, 255, 255, 0.08);
        }
        .glow-button {
            transition: all 0.3s ease;
            box-shadow: 0 0 20px rgba(99, 102, 241, 0.2);
        }
        .glow-button:hover:not(:disabled) {
            box-shadow: 0 0 30px rgba(99, 102, 241, 0.4);
            transform: translateY(-2px);
        }
        .glow-telegram:hover { box-shadow: 0 0 25px rgba(56, 189, 248, 0.35); }
        .glow-youtube:hover { box-shadow: 0 0 25px rgba(239, 68, 68, 0.35); }
        .glow-discord:hover { box-shadow: 0 0 25px rgba(99, 102, 241, 0.35); }
        
        @keyframes progress-stripe {
            0% { background-position: 1rem 0; }
            100% { background-position: 0 0; }
        }
        .animate-stripes {
            background-image: linear-gradient(45deg, rgba(255, 255, 255, 0.15) 25%, transparent 25%, transparent 50%, rgba(255, 255, 255, 0.15) 50%, rgba(255, 255, 255, 0.15) 75%, transparent 75%, transparent);
            background-size: 1rem 1rem;
            animation: progress-stripe 1s linear infinite;
        }
    </style>
</head>
<body class="bg-[#0b0f19] min-h-screen flex items-center justify-center p-4 text-slate-100 relative overflow-x-hidden selection:bg-indigo-500 selection:text-white">

    <div class="fixed -top-32 -left-32 w-96 h-96 bg-indigo-600/20 rounded-full blur-[120px] pointer-events-none"></div>
    <div class="fixed -bottom-32 -right-32 w-96 h-96 bg-purple-600/20 rounded-full blur-[120px] pointer-events-none"></div>

    <div class="max-w-md w-full glass-panel rounded-3xl p-6 sm:p-8 shadow-2xl text-center relative z-10 my-6">
        
        <!-- 🚀 كرت القنوات -->
        <div class="mb-8 p-4 bg-slate-900/60 rounded-2xl border border-slate-800/80">
            <p class="text-xs font-bold text-slate-400 mb-3 tracking-wider">انضم وتابع مجتمعنا عبر القنوات التالية 🌟</p>
            <div class="grid grid-cols-3 gap-2 sm:gap-3">
                <a href="https://t.me/mf5rt1" target="_blank" class="glow-telegram flex flex-col sm:flex-row items-center justify-center gap-1.5 p-2.5 bg-sky-500/10 border border-sky-500/30 rounded-xl text-sky-400 font-bold text-[11px] transition-all hover:bg-sky-500/20 hover:scale-105">
                    <svg class="w-4 h-4 fill-current" viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm4.64 6.8c-.15 1.58-.8 5.42-1.13 7.19-.14.75-.42 1-.68 1.03-.58.05-1.02-.38-1.58-.75-.88-.58-1.38-.94-2.23-1.5-.99-.65-.35-1.01.22-1.59.15-.15 2.71-2.48 2.76-2.69a.2.2 0 00-.05-.18c-.06-.05-.14-.03-.21-.02-.09.02-1.49.95-4.22 2.79-.4.27-.76.41-1.08.4-.36-.01-1.04-.2-1.55-.37-.63-.2-1.12-.31-1.08-.66.02-.18.27-.36.74-.55 2.92-1.27 4.86-2.11 5.83-2.51 2.78-1.16 3.35-1.36 3.73-1.36.08 0 .27.02.39.12.1.08.13.19.14.27-.01.06.01.24 0 .38z"/></svg>
                    <span>تليجرام</span>
                </a>
                <a href="https://discord.gg/5KnynCqGB" target="_blank" class="glow-discord flex flex-col sm:flex-row items-center justify-center gap-1.5 p-2.5 bg-indigo-500/10 border border-indigo-500/30 rounded-xl text-indigo-400 font-bold text-[11px] transition-all hover:bg-indigo-500/20 hover:scale-105">
                    <svg class="w-4 h-4 fill-current" viewBox="0 0 24 24"><path d="M20.317 4.37a19.791 19.791 0 0 0-4.885-1.515.074.074 0 0 0-.079.037c-.21.375-.444.864-.608 1.25a18.27 18.27 0 0 0-5.487 0 12.64 12.64 0 0 0-.617-1.25.077.077 0 0 0-.079-.037A19.736 19.736 0 0 0 3.677 4.37a.07.07 0 0 0-.032.027C.533 9.046-.32 13.58.099 18.057a.082.082 0 0 0 .031.057 19.9 19.9 0 0 0 5.993 3.03.078.078 0 0 0 .084-.028c.462-.63.874-1.295 1.226-1.994.021-.041.001-.09-.041-.106a13.107 13.107 0 0 1-1.872-.892.077.077 0 0 1-.008-.128 10.2 10.2 0 0 0 .372-.292.074.074 0 0 1 .077-.01c3.928 1.793 8.18 1.793 12.061 0a.074.074 0 0 1 .078.01c.12.098.246.198.373.292a.077.077 0 0 1-.006.127 12.299 12.299 0 0 1-1.873.892.077.077 0 0 0-.041.107c.36.698.772 1.362 1.225 1.993a.076.076 0 0 0 .084.028 19.839 19.839 0 0 0 6.002-3.03.077.077 0 0 0 .032-.054c.5-5.177-.838-9.674-3.549-13.66a.061.061 0 0 0-.031-.028zM8.02 15.33c-1.183 0-2.157-1.085-2.157-2.419 0-1.333.956-2.419 2.157-2.419 1.21 0 2.176 1.096 2.157 2.42 0 1.333-.956 2.418-2.157 2.418zm7.975 0c-1.183 0-2.157-1.085-2.157-2.419 0-1.333.955-2.419 2.157-2.419 1.21 0 2.176 1.096 2.157 2.42 0 1.333-.946 2.418-2.157 2.418z"/></svg>
                    <span>ديسكورد</span>
                </a>
                <a href="https://www.youtube.com/@xoreyt0" target="_blank" class="glow-youtube flex flex-col sm:flex-row items-center justify-center gap-1.5 p-2.5 bg-red-500/10 border border-red-500/30 rounded-xl text-red-400 font-bold text-[11px] transition-all hover:bg-red-500/20 hover:scale-105">
                    <svg class="w-4 h-4 fill-current" viewBox="0 0 24 24"><path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/></svg>
                    <span>يوتيوب</span>
                </a>
            </div>
        </div>

        {{ content | safe }}

    </div>

</body>
</html>
"""

def verify_recaptcha(response_token):
    if not response_token:
        return False
    data = {'secret': RECAPTCHA_SECRET_KEY, 'response': response_token}
    try:
        r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data, timeout=5)
        return r.json().get('success', False)
    except:
        return False

def send_visitor_webhook(file_name, user_ip, user_agent):
    if not DISCORD_WEBHOOK_URL:
        return

    country, city = "غير معروف", "غير معروف"
    try:
        ip_info = requests.get(f"http://ip-api.com/json/{user_ip}", timeout=3).json()
        if ip_info.get("status") == "success":
            country = ip_info.get("country", "غير معروف")
            city = ip_info.get("city", "غير معروف")
    except:
        pass

    embed = {
        "title": "📥 زائر جديد لصفحة تحميل ملف!",
        "color": 5814783,
        "fields": [
            {"name": "📄 اسم الملف", "value": f"`{file_name}`", "inline": False},
            {"name": "🌍 الدولة والمدينة", "value": f"{country} - {city}", "inline": True},
            {"name": "🌐 IP الزائر", "value": f"`{user_ip}`", "inline": True},
            {"name": "📱 الجهاز ومتصفح الزائر", "value": f"```{user_agent[:150]}```", "inline": False}
        ],
        "footer": {"text": "نظام الحماية والذكاء الاصطناعي الذكي"}
    }
    
    try:
        requests.post(DISCORD_WEBHOOK_URL, json={"embeds": [embed]}, timeout=4)
    except:
        pass

@app.route('/', methods=['GET', 'POST'])
def home():
    error_msg = ""
    if request.method == 'POST':
        user_code = request.form.get('access_code')
        recaptcha_response = request.form.get('g-recaptcha-response')
        custom_name = request.form.get('file_name')
        mediafire_url = request.form.get('mediafire_url')

        if user_code != SECRET_ACCESS_CODE:
            error_msg = "❌ رمز الحماية غير صحيح!"
        elif not verify_recaptcha(recaptcha_response):
            error_msg = "⚠️ يرجى تأكيد أنك لست برنامج روبوت!"
        elif mediafire_url and custom_name:
            share_link = request.host_url + f"download?name={urllib.parse.quote(custom_name)}&url={urllib.parse.quote(mediafire_url)}"
            
            content = f"""
            <div class="w-16 h-16 bg-emerald-500/20 text-emerald-400 rounded-full flex items-center justify-center mx-auto mb-4 text-3xl border border-emerald-500/30">✓</div>
            <h1 class="text-2xl font-black text-white mb-2">تم تجهيز رابط الصفحة!</h1>
            <p class="text-xs text-slate-400 mb-6">اسم الملف: <span class="text-indigo-300 font-bold">{custom_name}</span></p>
            
            <div class="bg-slate-950/80 p-3.5 rounded-2xl border border-slate-800 mb-4 overflow-x-auto">
                <input type="text" value="{share_link}" readonly id="linkInput" class="w-full bg-transparent text-xs text-center text-indigo-300 font-mono outline-none select-all whitespace-nowrap">
            </div>
            
            <button onclick="navigator.clipboard.writeText('{share_link}'); alert('تم نسخ رابط المشاركة بنجاح!');" class="glow-button w-full bg-indigo-600 hover:bg-indigo-500 text-white font-bold py-3.5 rounded-xl transition-all text-sm mb-3">
                📋 نسخ رابط المشاركة
            </button>
            
            <a href="/" class="block text-xs text-slate-400 hover:text-slate-200 transition-colors mt-2">إنشاء رابط لملف آخر</a>
            """
            return render_template_string(HTML_LAYOUT, content=content, title="تم تجهيز الرابط")
        else:
            error_msg = "يرجى تعبئة جميع الحقول بشكل صحيح."

    error_html = f'<div class="p-3 mb-4 text-xs text-red-400 bg-red-500/10 border border-red-500/30 rounded-xl">{error_msg}</div>' if error_msg else ''

    content = f"""
    <div class="w-14 h-14 bg-indigo-500/20 text-indigo-400 rounded-2xl flex items-center justify-center mx-auto mb-4 border border-indigo-500/30 text-2xl">🤖</div>
    <h1 class="text-xl font-black text-white mb-1">لوحة فحص وإنشاء الرابط</h1>
    <p class="text-slate-400 text-xs mb-6">سيتم محاكاة الفحص وتجهيز الصفحة مع التحذيرات الذكية</p>
    
    {error_html}

    <!-- 📊 شريط التحميل والفحص بالذكاء الاصطناعي -->
    <div id="scanProgressContainer" class="hidden mb-6 p-4 bg-slate-950/80 border border-indigo-500/30 rounded-2xl text-right">
        <div class="flex justify-between items-center mb-2">
            <span id="scanStatusText" class="text-xs font-bold text-indigo-400 animate-pulse">جاري الفحص بالذكاء الاصطناعي...</span>
            <span id="scanPercent" class="text-xs font-black text-indigo-300">0%</span>
        </div>
        <div class="w-full bg-slate-800 rounded-full h-3 overflow-hidden p-0.5 border border-slate-700">
            <div id="progressBar" class="bg-gradient-to-r from-indigo-500 via-purple-500 to-emerald-400 h-full rounded-full transition-all duration-300 animate-stripes w-0"></div>
        </div>
    </div>

    <form id="uploadForm" method="POST" class="space-y-4 text-right">
        <div>
            <label class="block text-xs font-bold text-amber-400 mb-1">🔑 رمز الدخول الخاص:</label>
            <input type="password" name="access_code" placeholder="أدخل رمز الحماية هنا" required class="w-full p-3 bg-slate-950/70 border border-amber-500/30 rounded-xl text-white placeholder-slate-600 focus:border-amber-400 outline-none text-xs transition-all">
        </div>

        <div>
            <label class="block text-xs font-bold text-slate-300 mb-1">اسم الملف للعرض في الصفحة:</label>
            <input type="text" name="file_name" placeholder="مثال: تطبيق_الهاتف.apk" required class="w-full p-3 bg-slate-950/70 border border-slate-800 rounded-xl text-white placeholder-slate-600 focus:border-indigo-500 outline-none text-xs transition-all">
        </div>
        
        <div>
            <label class="block text-xs font-bold text-slate-300 mb-1">رابط ميديا فاير (MediaFire):</label>
            <input type="url" name="mediafire_url" placeholder="https://www.mediafire.com/file/..." required class="w-full p-3 bg-slate-950/70 border border-slate-800 rounded-xl text-white placeholder-slate-600 focus:border-indigo-500 outline-none text-xs transition-all text-left" dir="ltr">
        </div>

        <div class="flex justify-center my-4 overflow-hidden rounded-xl">
            <div class="g-recaptcha" data-sitekey="{RECAPTCHA_SITE_KEY}" data-theme="dark"></div>
        </div>

        <button type="submit" id="submitBtn" class="glow-button w-full bg-indigo-600 hover:bg-indigo-500 text-white font-bold py-3.5 rounded-xl transition-all text-sm flex items-center justify-center gap-2">
            <span>🛡️ فحص وإنشاء الرابط مع التحذيرات</span>
        </button>
    </form>

    <script>
    document.getElementById('uploadForm').addEventListener('submit', function(e) {{
        e.preventDefault();
        const btn = document.getElementById('submitBtn');
        const progressContainer = document.getElementById('scanProgressContainer');
        const progressBar = document.getElementById('progressBar');
        const scanStatusText = document.getElementById('scanStatusText');
        const scanPercent = document.getElementById('scanPercent');

        btn.disabled = true;
        btn.classList.add('opacity-50');
        progressContainer.classList.remove('hidden');

        let percent = 0;
        const steps = [
            {{ p: 25, t: "🔍 إرسال الرابط لمحركات الفحص بالذكاء الاصطناعي..." }},
            {{ p: 60, t: "⚡ فحص الأكواد البرمجية بحثاً عن الاشتباه برمجياً..." }},
            {{ p: 85, t: "⚠️ اعتماد إعدادات الأمان والتحذير للزائر..." }},
            {{ p: 100, t: "✨ كُمل الفحص بنجاح!" }}
        ];

        let stepIndex = 0;
        const interval = setInterval(() => {{
            if (stepIndex < steps.length) {{
                percent = steps[stepIndex].p;
                scanStatusText.innerText = steps[stepIndex].t;
                scanPercent.innerText = percent + "%";
                progressBar.style.width = percent + "%";
                stepIndex++;
            }} else {{
                clearInterval(interval);
                setTimeout(() => {{
                    document.getElementById('uploadForm').submit();
                }}, 500);
            }}
        }}, 800);
    }});
    </script>
    """
    return render_template_string(HTML_LAYOUT, content=content, title="لوحة الفحص والإعداد")

@app.route('/download')
def download():
    file_name = request.args.get('name', 'ملف للمشاركة')
    file_url = request.args.get('url', '#')

    # إرسال بيانات الزائر للديسكورد عبر الـ Webhook
    user_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    if user_ip and ',' in user_ip:
        user_ip = user_ip.split(',')[0].strip()
    user_agent = request.headers.get('User-Agent', 'غير معروف')
    send_visitor_webhook(file_name, user_ip, user_agent)

    content = f"""
    <!-- ⚠️ التحذير الأول: تنبيه الدخول البارز -->
    <div class="mb-5 p-4 bg-amber-500/10 border border-amber-500/30 rounded-2xl text-right">
        <div class="flex items-center gap-2 mb-1.5">
            <span class="text-amber-400 text-lg">⚠️</span>
            <h3 class="text-xs font-bold text-amber-300">تنبيه وأمان الحماية:</h3>
        </div>
        <p class="text-[11px] text-amber-200/80 leading-relaxed">
            قد يشتبه النظام بوجود ضرر في الملف أو عدم التأكد من مصدره 100%. لسنا متأكدين تماماً ولكنه يحمل اشتباهاً أمنياً. نوصي بفحصه دائماً عبر برنامج الحماية الخاص بك قبل التثبيت.
        </p>
    </div>

    <!-- 📦 تفاصيل الملف -->
    <div class="p-4 bg-slate-950/60 rounded-2xl border border-slate-800 text-right mb-6">
        <div class="text-[11px] text-slate-400 mb-1">الملف المطلوب:</div>
        <div class="text-sm font-bold text-indigo-300 truncate font-mono">{file_name}</div>
        <div class="mt-2 text-[10px] text-slate-500 flex justify-between items-center">
            <span>حالة الملف: <strong class="text-amber-400">تحت الاشتباه</strong></span>
            <span>الاستضافة: MediaFire</span>
        </div>
    </div>

    <!-- ⏳ زر التحميل مع المؤقت 3 ثوانٍ والتحذير الثاني عند الضغط -->
    <button id="downloadBtn" disabled onclick="showSecondWarning()" class="glow-button w-full bg-slate-800 text-slate-400 font-bold py-3.5 rounded-xl transition-all text-sm flex items-center justify-center gap-2 cursor-not-allowed">
        <span id="btnText">⏳ انتظر 3 ثوانٍ لتفعيل الزر...</span>
    </button>

    <!-- 🚨 التحذير الثاني: النافذة المنبثقة (Modal) -->
    <div id="warningModal" class="hidden fixed inset-0 bg-black/80 backdrop-blur-md z-50 flex items-center justify-center p-4 text-right">
        <div class="glass-panel max-w-sm w-full rounded-2xl p-6 border border-red-500/30 relative">
            <div class="w-12 h-12 bg-red-500/20 text-red-400 rounded-full flex items-center justify-center mx-auto mb-3 text-2xl border border-red-500/30">
                🚨
            </div>
            <h3 class="text-base font-bold text-white text-center mb-2">تأكيد التنزيل على مسؤوليتك</h3>
            <p class="text-xs text-slate-300 leading-relaxed mb-6">
                هذا تحذير أخير: قد يحتوي الملف على برمجيات غير معروفة أو يشار إليها كاشتباه من المحركات. هل تريد المتابعة وتنزيل الملف على أي حال؟
            </p>
            <div class="flex gap-3">
                <a href="{file_url}" target="_blank" onclick="closeModal()" class="w-1/2 bg-red-600 hover:bg-red-500 text-white font-bold py-2.5 rounded-xl text-xs text-center transition-all shadow-lg shadow-red-600/30">
                    نعم، تنزيل الملف
                </a>
                <button onclick="closeModal()" class="w-1/2 bg-slate-800 hover:bg-slate-700 text-slate-300 font-bold py-2.5 rounded-xl text-xs transition-all">
                    إلغاء
                </button>
            </div>
        </div>
    </div>

    <script>
    let timeLeft = 3;
    const btn = document.getElementById('downloadBtn');
    const btnText = document.getElementById('btnText');

    const countdown = setInterval(() => {{
        timeLeft--;
        if (timeLeft > 0) {{
            btnText.innerText = "⏳ انتظر " + timeLeft + " ثوانٍ لتفعيل الزر...";
        }} else {{
            clearInterval(countdown);
            btn.disabled = false;
            btn.classList.remove('bg-slate-800', 'text-slate-400', 'cursor-not-allowed');
            btn.classList.add('bg-indigo-600', 'hover:bg-indigo-500', 'text-white', 'cursor-pointer');
            btnText.innerText = "📥 تنزيل الملف الآن";
        }}
    }}, 1000);

    function showSecondWarning() {{
        document.getElementById('warningModal').classList.remove('hidden');
    }}

    function closeModal() {{
        document.getElementById('warningModal').classList.add('hidden');
    }}
    </script>
    """
    return render_template_string(HTML_LAYOUT, content=content, title=f"تحميل {file_name}")

if __name__ == '__main__':
    app.run(debug=True)
