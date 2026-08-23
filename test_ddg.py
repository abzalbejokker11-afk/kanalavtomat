from duckduckgo_search import DDGS

try:
    ddgs = DDGS()
    prompt = "Anti-doping (WADA) bo'yicha 1 ta professor darajasidagi savol va javob yoz. O'zbek tilida. Qisqa va lo'nda bo'lsin."
    res = ddgs.chat(prompt, model="llama-3.1-70b")
    print(res)
except Exception as e:
    print(e)
