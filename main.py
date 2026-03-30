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
    times = jogo["times"].split(' X ')
    time_casa = times[0] if len(times) > 1 else jogo["times"]
    time_fora = times[1] if len(times) > 1 else ''

    cards += f'''
    <div class="jogo-card">
        <div class="times">
            <span>{time_casa}</span>
            <span class="versus">X</span>
            <span>{time_fora}</span>
        </div>
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
        body {{ background-color: #f5f5f5; color: #333; font-family: Arial, sans-serif; }}
        header {{ background-color: #006437; padding: 20px; text-align: center; }}
        header h1 {{ font-size: 22px; color: #fff; font-weight: bold; }}
        .titulo-jogos {{ font-size: 20px; font-weight: bold; padding: 20px 15px 10px; max-width: 500px; margin: 0 auto; }}
        .jogos {{ max-width: 500px; margin: 0 auto; padding: 0 15px 30px; }}
        .jogo-card {{ background-color: #fff; border-radius: 10px; padding: 15px; margin-bottom: 12px; box-shadow: 0 1px 4px rgba(0,0,0,0.1); border-left: 4px solid #006437; }}
        .times {{ display: flex; justify-content: space-between; align-items: center; font-size: 20px; font-weight: bold; margin-bottom: 10px; }}
        .versus {{ color: #aaa; font-size: 16px; }}
        .info {{ text-align: center; font-size: 13px; color: #666; margin-bottom: 3px; }}
        .campeonato {{ display: inline-block; background-color: #006437; color: #fff; padding: 3px 10px; border-radius: 4px; font-size: 11px; margin-top: 10px; }}
    </style>
</head>
<body>
<header>
    <h1>🌿 Fut Calendário - Palmeiras</h1>
</header>
<div class="titulo-jogos">JOGOS</div>
<div class="jogos">
    {cards}
</div>
</body>
</html>'''

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print('index.html gerado com sucesso!')