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

                # pega os escudos
                try:
                    imagens = jogo.find_elements(By.CLASS_NAME, 'img-responsive')
                    escudo_casa = imagens[0].get_attribute('src') if len(imagens) > 0 else ''
                    escudo_fora = imagens[1].get_attribute('src') if len(imagens) > 1 else ''
                except:
                    escudo_casa = ''
                    escudo_fora = ''

                todos_jogos.append({
                    'times': times,
                    'data': data,
                    'hora': hora,
                    'estadio': estadio,
                    'campeonato': campeonato,
                    'escudo_casa': escudo_casa,
                    'escudo_fora': escudo_fora
                })
    except:
        pass

driver.quit()

import json

with open('jogos.json', 'w', encoding='utf-8') as f:
    json.dump(todos_jogos, f, ensure_ascii=False, indent=2)

print('jogos.json gerado com sucesso!')