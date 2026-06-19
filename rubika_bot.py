from pyrubi import Client
import re
import os
import sys
import time

print("🤖 Starting bot...")
print("📂 Files in directory:", os.listdir('.'))

# --- ساخت سشن جدید ---
session_file = "gf_account.pyrubi"

# پاک کردن فایل سشن قدیمی
if os.path.exists(session_file):
    print("🔄 Removing old session file...")
    os.remove(session_file)
    print("✅ Old session removed")

# گرفتن شماره از محیط
PHONE = os.getenv("RUBIKA_PHONE")
if not PHONE:
    print("❌ Please set RUBIKA_PHONE environment variable")
    print("Example: 989123456789")
    sys.exit(1)

print(f"📱 Phone: {PHONE}")

# ساخت کلاینت جدید
app = Client(session_file)

# لاگین با شماره
try:
    print("🔄 Logging in...")
    app.start(phone=PHONE)
    print("✅ Session created successfully!")
except Exception as e:
    print(f"❌ Login error: {e}")
    sys.exit(1)

# --- YOUR GUID ---
MY_GUID = "u0DgaaS04d24caf00b3ea5e7b48d0aff"

# --- LETTER MAP ---
letters = {
    'ا':'1','آ':'1',
    'ب':'2','پ':'3','ت':'4','ث':'5',
    'ج':'6','چ':'7','ح':'8','خ':'9',
    'د':'10','ذ':'11','ر':'12','ز':'13',
    'ژ':'14','س':'15','ش':'16','ص':'17',
    'ض':'18','ط':'19','ظ':'20','ع':'21',
    'غ':'22','ف':'23','ق':'24','ک':'25',
    'گ':'26','ل':'27','م':'28','ن':'29',
    'و':'30','ه':'31','ی':'32'
}

numbers = {v: k for k, v in letters.items()}

persian_digits = str.maketrans(
    "۰۱۲۳۴۵۶۷۸۹",
    "0123456789"
)

def validate(text):
    if not text:
        return False
    text = text.translate(persian_digits)
    nums = re.findall(r'\d+', text)
    for n in nums:
        if int(n) > 32:
            return False
    return True

def encode(text):
    if not text:
        return ""
    lines = text.split("\n")
    final = []
    for line in lines:
        if not line.strip():
            final.append("")
            continue
        words = line.split()
        out_words = []
        for word in words:
            nums = []
            emoji = ""
            for ch in word:
                if ch in letters:
                    nums.append(letters[ch])
                elif ch.isdigit():
                    nums.append(ch)
                else:
                    emoji += ch
            if nums:
                result = "_".join(nums)
                if emoji:
                    result += emoji
                out_words.append(result)
            else:
                out_words.append(emoji if emoji else word)
        final.append("__".join(out_words))
    return "\n".join(final)

def decode(text):
    if not text:
        return ""
    text = text.translate(persian_digits)
    lines = text.split("\n")
    final = []
    for line in lines:
        if not line.strip():
            final.append("")
            continue
        words = line.split("__")
        out_words = []
        for word in words:
            if not word:
                out_words.append("")
                continue
            match = re.match(r'^([\d_]+)(.*)$', word)
            if match:
                code = match.group(1)
                emoji = match.group(2)
                result = ""
                for c in code.split("_"):
                    if c in numbers:
                        result += numbers[c]
                result += emoji
                out_words.append(result)
            else:
                out_words.append(word)
        final.append(" ".join(out_words))
    return "\n".join(final)

@app.on_message()
def handler(message):
    try:
        if message.object_guid != MY_GUID:
            return
        text = message.text
        if not text:
            return
        if re.search(r'[A-Za-z]', text):
            return
        if not validate(text):
            app.send_text(MY_GUID, "❌ خطا: اعداد بیشتر از 32 مجاز نیستند!")
            return
        if re.search(r'\d', text):
            result = decode(text)
        else:
            result = encode(text)
        if not result:
            result = "⚠️ نتیجه خالی است!"
        app.send_text(MY_GUID, result)
    except Exception as e:
        error_msg = f"❌ خطا: {str(e)}"
        try:
            app.send_text(MY_GUID, error_msg)
        except:
            print(error_msg)

print("✅ Bot is running...")
app.run()
