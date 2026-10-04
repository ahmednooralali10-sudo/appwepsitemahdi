from flask import Flask, request, render_template_string
import requests
import urllib.parse
import xml.etree.ElementTree as ET
import base64
import json

app = Flask(__name__)

# 🔔 رابط Discord Webhook
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1556178719171940412/cLjKIxt81tQvjaBaNK6FVJidzGwQdZdkqhdiIiqtOV85pCmr2k4LHP4e6cYy5-PwCXkg"

# 🛡️ مفاتيح reCAPTCHA
RECAPTCHA_SITE_KEY = "6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI"
RECAPTCHA_SECRET_KEY = "6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe"

HTML_LAYOUT = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title if title else 'مركز تثبيت التطبيقات' }}</title>
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
    </style>
</head>
<body class="bg-[#0b0f19] min-h-screen flex items-center justify-center p-4 text-slate-100 relative overflow-x-hidden selection:bg-indigo-500 selection:text-white">

    <div class="fixed -top-32 -left-32 w-96 h-96 bg-indigo-600/20 rounded-full blur-[120px] pointer-events-none"></div>
    <div class="fixed -bottom-32 -right-32 w-96 h-96 bg-purple-600/20 rounded-full blur-[120px] pointer-events-none"></div>

    <div class="max-w-md w-full glass-panel rounded-3xl p-6 sm:p-8 shadow-2xl text-center relative z-10 my-6">
        {{ content | safe }}
    </div>

</body>
</html>
"""

def extract_plist_data(itms_url):
    app_title = "تطبيق iOS"
    app_icon = ""

    parsed_url = urllib.parse.urlparse(itms_url)
    query_params = urllib.parse.parse_qs(parsed_url.query)
    
    plist_url = query_params.get('url', [None])[0]
    if not plist_url and itms_url.startswith("http"):
        plist_url = itms_url

    if plist_url:
        try:
            response = requests.get(plist_url, timeout=5)
            if response.status_code == 200:
                root = ET.fromstring(response.content)
                items = list(root.iter())
                for i, elem in enumerate(items):
                    if elem.tag == 'key' and elem.text == 'title':
                        if i + 1 < len(items):
                            app_title = items[i + 1].text
                    elif elem.tag == 'key' and elem.text in ['display-image', 'full-size-image']:
                        for j in range(i, min(i + 5, len(items))):
                            if items[j].tag == 'string' and items[j].text.startswith('http'):
                                app_icon = items[j].text
                                break
        except Exception:
            pass

    return app_title, app_icon

def verify_recaptcha(response_token):
    if not response_token:
        return False
    data = {'secret': RECAPTCHA_SECRET_KEY, 'response': response_token}
    try:
        r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data, timeout=5)
        return r.json().get('success', False)
    except:
        return False

@app.route('/', methods=['GET', 'POST'])
def home():
    error_msg = ""
    if request.method == 'POST':
        recaptcha_response = request.form.get('g-recaptcha-response')
        download_url = request.form.get('download_url')

        if not verify_recaptcha(recaptcha_response):
            error_msg = "⚠️ يرجى تأكيد أنك لست برنامج روبوت!"
        elif download_url:
            extracted_title, extracted_icon = extract_plist_data(download_url)
            
            # ترميز البيانات في كود قصير دون الحاجة لقاعدة بيانات
            data_to_encode = {
                "n": extracted_title,
                "u": download_url,
                "i": extracted_icon
            }
            json_str = json.dumps(data_to_encode)
            encoded_code = base64.urlsafe_b64encode(json_str.encode()).decode().rstrip("=")

            share_link = f"{request.host_url}d/{encoded_code}"

            content = f"""
            <div class="w-16 h-16 bg-emerald-500/20 text-emerald-400 rounded-full flex items-center justify-center mx-auto mb-4 text-3xl border border-emerald-500/30">✓</div>
            <h1 class="text-2xl font-black text-white mb-2">تم تجهيز الرابط!</h1>
            <p class="text-xs text-slate-400 mb-6">الاسم المستخرج: <span class="text-indigo-300 font-bold">{extracted_title}</span></p>

            <div class="bg-slate-950/80 p-3.5 rounded-2xl border border-slate-800 mb-4 overflow-x-auto">
                <input type="text" value="{share_link}" readonly class="w-full bg-transparent text-xs text-center text-indigo-300 font-mono outline-none select-all whitespace-nowrap">
            </div>

            <button onclick="navigator.clipboard.writeText('{share_link}'); alert('تم نسخ الرابط بنجاح!');" class="glow-button w-full bg-indigo-600 hover:bg-indigo-500 text-white font-bold py-3.5 rounded-xl transition-all text-sm mb-3">
                📋 نسخ الرابط القصير
            </button>
            <a href="/" class="block text-xs text-slate-400 hover:text-slate-200 transition-colors mt-2">إنشاء رابط جديد</a>
            """
            return render_template_string(HTML_LAYOUT, content=content, title="تم اختصار الرابط")
        else:
            error_msg = "يرجى وضع الرابط."

    error_html = f'<div class="p-3 mb-4 text-xs text-red-400 bg-red-500/10 border border-red-500/30 rounded-xl">{error_msg}</div>' if error_msg else ''

    content = f"""
    <div class="w-14 h-14 bg-indigo-500/20 text-indigo-400 rounded-2xl flex items-center justify-center mx-auto mb-4 border border-indigo-500/30 text-2xl">⚡</div>
    <h1 class="text-xl font-black text-white mb-1">مختصر روابط التطبيقات</h1>
    <p class="text-slate-400 text-xs mb-6">ضع الرابط وسيتم استخراج الاسم والصورة وإنشاء رابط قصير ومباشر</p>

    {error_html}

    <form method="POST" class="space-y-4 text-right">
        <div>
            <label class="block text-xs font-bold text-slate-300 mb-1">رابط التطبيق (itms-services):</label>
            <input type="text" name="download_url" placeholder="itms-services://?action=download-manifest&url=https://..." required class="w-full p-3 bg-slate-950/70 border border-slate-800 rounded-xl text-white placeholder-slate-600 focus:border-indigo-500 outline-none text-xs transition-all text-left" dir="ltr">
        </div>

        <div class="flex justify-center my-4 overflow-hidden rounded-xl">
            <div class="g-recaptcha" data-sitekey="{RECAPTCHA_SITE_KEY}" data-theme="dark"></div>
        </div>

        <button type="submit" class="glow-button w-full bg-indigo-600 hover:bg-indigo-500 text-white font-bold py-3.5 rounded-xl transition-all text-sm flex items-center justify-center gap-2">
            <span>🚀 إنتاج رابط قصير</span>
        </button>
    </form>
    """
    return render_template_string(HTML_LAYOUT, content=content, title="مولد الروابط القصيرة")

@app.route('/d/<code>')
def download_slug(code):
    try:
        # فك تشفير البيانات من الكود القصير
        padding = "=" * (-len(code) % 4)
        decoded_bytes = base64.urlsafe_b64decode(code + padding)
        data = json.loads(decoded_bytes.decode())
        
        file_name = data.get("n", "تطبيق iOS")
        file_url = data.get("u", "#")
        app_icon = data.get("i", "")
    except Exception:
        return "⚠️ الرابط غير صالح أو تم إدخاله بشكل خاطئ.", 404

    default_icon = "https://cdn-icons-png.flaticon.com/512/2583/2583208.png"
    icon_src = app_icon if app_icon else default_icon

    content = f"""
    <div class="p-6 bg-slate-950/60 rounded-3xl border border-slate-800 text-center mb-6 flex flex-col items-center">
        <div class="w-24 h-24 mb-4 rounded-2xl overflow-hidden shadow-xl border border-slate-700/60 bg-slate-900 p-1">
            <img src="{icon_src}" alt="{file_name}" class="w-full h-full object-cover rounded-xl" onerror="this.src='{default_icon}'">
        </div>
        <h2 class="text-lg font-black text-white mb-1">{file_name}</h2>
        <span class="inline-block px-3 py-1 bg-indigo-500/10 border border-indigo-500/30 text-indigo-400 rounded-full text-[10px] font-bold">
            تثبيت مباشر (iOS)
        </span>
    </div>

    <a href="{file_url}" class="glow-button block w-full bg-indigo-600 hover:bg-indigo-500 text-white font-bold py-4 rounded-xl transition-all text-sm text-center">
        📲 تنزيل وتثبيت التطبيق الآن
    </a>
    """
    return render_template_string(HTML_LAYOUT, content=content, title=f"تثبيت {file_name}")

if __name__ == '__main__':
    app.run(debug=True)
