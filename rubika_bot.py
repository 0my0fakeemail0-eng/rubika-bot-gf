from pyrubi import Client
import re

app = Client("gf_account")

MY_GUID = "u0DgaaS04d24caf00b3ea5e7b48d0aff"

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
persian_digits = str.maketrans("۰۱۲۳۴۵۶۷۸۹", "0123456789")


def validate(text):
    text = text.translate(persian_digits)
    nums = re.findall(r'\d+', text)

    for n in nums:
        if int(n) > 32:
            return False

    return True


def encode(text):
    lines = text.split("\n")
    final = []

    for line in lines:
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

            result = "_".join(nums)
            if emoji:
                result += emoji

            out_words.append(result)

        final.append("__".join(out_words))

    return "\n".join(final)


def decode(text):
    text = text.translate(persian_digits)
    lines = text.split("\n")
    final = []

    for line in lines:
        words = line.split("__")
        out_words = []

        for word in words:
            match = re.match(r'^([\d_]+)(.*)$', word)

            if match:
                code = match.group(1)
                emoji = match.group(2)
            else:
                code = ""
                emoji = word

            result = ""

            for c in code.split("_"):
                if c in numbers:
                    result += numbers[c]

            result += emoji
            out_words.append(result)

        final.append(" ".join(out_words))

    return "\n".join(final)

@app.on_message()
def handler(message):

    if message.object_guid != MY_GUID:
        return

    text = message.text
    if not text:
        return

    if re.search(r'[A-Za-z]', text):
        return

    if not validate(text):
        return

    if re.search(r'\d', text):
        result = decode(text)
    else:
        result = encode(text)

    app.send_text(MY_GUID, result)


print("Bot is running...")
app.run()
