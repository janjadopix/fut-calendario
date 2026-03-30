fetch('jogos.json')
    .then(response => response.json())
    .then(jogos => {
        const lista = document.getElementById('lista-jogos')

        jogos.forEach(jogo => {
            const times = jogo.times.split(' X ')
            const timeCasa = times[0] || jogo.times
            const timeFora = times[1] || ''

            lista.innerHTML += `
                <div class="jogo-card">
                    <div class="times">
                        <div class="time">
                            <img src="${jogo.escudo_casa}" onerror="this.style.display='none'">
                            <span>${timeCasa}</span>
                        </div>
                        <span class="versus">X</span>
                        <div class="time direita">
                            <img src="${jogo.escudo_fora}" onerror="this.style.display='none'">
                            <span>${timeFora}</span>
                        </div>
                    </div>
                    <div class="info">📅 ${jogo.data} às ${jogo.hora}</div>
                    <div class="info">🏟️ ${jogo.estadio}</div>
                    <span class="campeonato">${jogo.campeonato}</span>
                </div>
            `
        })
    })