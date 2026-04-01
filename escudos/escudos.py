"""
Script corrigido - ignora erro de SSL (comum no Windows)
Execute: python baixar_escudos.py
Depois: git add escudos/ && git commit -m "add: escudos locais" && git push
"""

import os
import ssl
import urllib.request

# Ignora verificação SSL — resolve o erro no Windows
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

os.makedirs("escudos", exist_ok=True)

escudos = {
    # Site do Palmeiras — sempre funcionou
    "palmeiras":           "https://www.palmeiras.com.br/wp-content/uploads/2019/08/logo-palmeiras-80-teste-2.png",
    "gremio":              "https://www.palmeiras.com.br/wp-content/uploads/2019/09/gremio.png",
    "bahia":               "https://www.palmeiras.com.br/wp-content/uploads/2019/09/bahia.png",
    "corinthians":         "https://www.palmeiras.com.br/wp-content/uploads/2019/08/corinthians-15-sep-2-1.png",
    "athletico-pr":        "https://www.palmeiras.com.br/wp-content/uploads/2019/09/athletico-pr.png",
    "red-bull-bragantino": "https://www.palmeiras.com.br/wp-content/uploads/2020/01/red-bull-bragantino.png",
    "chapecoense":         "https://www.palmeiras.com.br/wp-content/uploads/2019/09/chapecoense.png",
    "remo":                "https://www.palmeiras.com.br/wp-content/uploads/2019/08/remo-5.png",
    "santos":              "https://www.palmeiras.com.br/wp-content/uploads/2019/08/santos-15.png",
    "cruzeiro":            "https://www.palmeiras.com.br/wp-content/uploads/2019/03/cruzeiro-1.png",
    "flamengo":            "https://www.palmeiras.com.br/wp-content/uploads/2019/08/flamengo-55x50-1.png",
    "cerro-porteno":       "https://www.palmeiras.com.br/wp-content/uploads/2019/09/cerro-porteno-par.png",
    "sporting-cristal":    "https://www.palmeiras.com.br/wp-content/uploads/2019/09/sporting-cristal.png",
    "junior-barranquilla": "https://www.palmeiras.com.br/wp-content/uploads/2019/08/ESCUDO-JUNIOR-SIN-ESTRELLAS.png",

    # Sofascore CDN (img.sofascore.com aceita hotlink)
    "sao-paulo":   "https://img.sofascore.com/api/v1/team/1981/image/small",
    "vasco":       "https://img.sofascore.com/api/v1/team/1974/image/small",
    "botafogo":    "https://img.sofascore.com/api/v1/team/1958/image/small",
    "atletico-mg": "https://img.sofascore.com/api/v1/team/1977/image/small",
    "olimpia":     "https://img.sofascore.com/api/v1/team/1822/image/small",
    "sport":       "https://img.sofascore.com/api/v1/team/1959/image/small",
    "ceara":       "https://img.sofascore.com/api/v1/team/2001/image/small",
    "guarani":     "https://img.sofascore.com/api/v1/team/1972/image/small",
    "avai":        "https://img.sofascore.com/api/v1/team/7315/image/small",
    "talleres":    "https://img.sofascore.com/api/v1/team/1827/image/small",
}

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0 Safari/537.36",
    "Accept": "image/png,image/*,*/*",
    "Referer": "https://www.sofascore.com/",
}

for nome, url in escudos.items():
    destino = f"escudos/{nome}.png"
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=15, context=ctx) as resp:
            data = resp.read()
        with open(destino, "wb") as f:
            f.write(data)
        print(f"✅ {nome}.png ({len(data)} bytes)")
    except Exception as e:
        print(f"❌ {nome}: {e}")

print("\nPronto! Verifique a pasta escudos/ e depois:")
print("  git add escudos/")
print("  git commit -m 'add: escudos locais'")
print("  git push")