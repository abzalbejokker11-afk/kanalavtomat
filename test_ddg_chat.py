import requests, json

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
    "x-vqd-accept": "1",
    "Referer": "https://duckduckgo.com/",
    "Origin": "https://duckduckgo.com"
}

r = requests.get("https://duckduckgo.com/duckchat/v1/status", headers=headers, timeout=10)
vqd4 = r.headers.get("x-vqd-4", "")
vqdhash = r.headers.get("x-vqd-hash-1", "")
print(f"vqd4: {vqd4[:40] if vqd4 else 'YOQ'}")
print(f"hash: {vqdhash[:40] if vqdhash else 'YOQ'}")

chat_headers = {
    "User-Agent": headers["User-Agent"],
    "Accept": "text/event-stream",
    "Content-Type": "application/json",
    "x-vqd-4": vqd4,
    "Referer": "https://duckduckgo.com/",
    "Origin": "https://duckduckgo.com"
}
if vqdhash:
    chat_headers["x-vqd-hash-1"] = vqdhash

payload = {
    "model": "gpt-4o-mini",
    "messages": [{"role": "user", "content": "Salom! Sportda doping nazorati haqida 3 ta muhim fakt ayt. O'zbek tilida javob ber."}]
}

cr = requests.post("https://duckduckgo.com/duckchat/v1/chat", headers=chat_headers, json=payload, timeout=60)
print(f"Chat status: {cr.status_code}")

full_text = ""
for line in cr.text.split("\n"):
    if line.startswith("data: "):
        chunk = line[6:]
        if chunk == "[DONE]":
            break
        try:
            data = json.loads(chunk)
            msg = data.get("message", "")
            if msg:
                full_text += msg
        except json.JSONDecodeError:
            continue

print(f"\n=== JAVOB ({len(full_text)} belgi) ===")
print(full_text if full_text else "BO'SH JAVOB")
