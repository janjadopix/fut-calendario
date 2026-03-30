from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from datetime import datetime
import time

options = Options()
options.binary_location = r'C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe'

driver = webdriver.Chrome(options=options)
driver.get('https://www.palmeiras.com.br/calendario/')

time.sleep(5)

mes_atual = datetime.now().month
todos_jogos = []

for mes in range(mes_atual, mes_atual + 3):
    try:
        botao = driver.find_element(By.ID, f'dvMes_{mes}')
        botao.click()
        time.sleep(3)

        jogos = driver.find_elements(By.CLASS_NAME, 'content-proximos-jogos-row')

        for jogo in jogos:
            texto = jogo.text
            if 'INGRESSOS' in texto or 'horário a definir' in texto:
                linhas = texto.replace('INGRESSOS', '').strip().split('\n')
                linhas = [l for l in linhas if l.strip()]

                times = linhas[0]

                if 'horário a definir' in linhas[1]:
                    data = 'A definir'
                    hora = 'A definir'
                    estadio = linhas[2] if len(linhas) > 2 else 'A definir'
                    campeonato = linhas[3] if len(linhas) > 3 else 'A definir'
                else:
                    data = linhas[1]
                    hora = linhas[2]
                    estadio = linhas[3] if len(linhas) > 3 else 'A definir'
                    campeonato = linhas[4] if len(linhas) > 4 else 'A definir'

                todos_jogos.append({
                    'times': times,
                    'data': data,
                    'hora': hora,
                    'estadio': estadio,
                    'campeonato': campeonato
                })
    except:
        pass

driver.quit()

# gera os cards HTML
cards = ''
for jogo in todos_jogos:
    cards += f'''
    <div class="jogo-card">
        <div class="times">⚽ {jogo["times"]}</div>
        <div class="info">📅 {jogo["data"]} às {jogo["hora"]}</div>
        <div class="info">🏟️ {jogo["estadio"]}</div>
        <span class="campeonato">{jogo["campeonato"]}</span>
    </div>
    '''

# gera o HTML completo
html = f'''<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Fut Calendário - Palmeiras</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ background-color: #1a1a1a; color: #fff; font-family: Arial, sans-serif; }}
        header {{ background-color: #006437; padding: 20px; text-align: center; }}
        header h1 {{ font-size: 24px; color: #fff; }}
        .jogos {{ max-width: 600px; margin: 20px auto; padding: 0 15px; }}
        .jogo-card {{ background-color: #2a2a2a; border-left: 4px solid #006437; border-radius: 8px; padding: 15px; margin-bottom: 15px; }}
        .times {{ font-size: 18px; font-weight: bold; margin-bottom: 8px; }}
        .info {{ font-size: 14px; color: #aaa; margin-bottom: 4px; }}
        .campeonato {{ display: inline-block; background-color: #006437; color: #fff; padding: 3px 8px; border-radius: 4px; font-size: 12px; margin-top: 8px; }}
    </style>
</head>
<body>
<header>
    <h1>📅 Fut Calendário - Palmeiras</h1>
</header>
<div class="jogos">
    {cards}
</div>
</body>
</html>'''

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print('index.html gerado com sucesso!')