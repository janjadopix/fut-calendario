// ============================
//  FUT CALENDÁRIO 2026
// ============================

let todosJogos = []
let timeSelecionado = 'TODOS'
let campSelecionado = 'TODOS'

// Mapeia campeonato → classe CSS do badge
function badgeClass(camp) {
  if (camp.includes('SÉRIE A')) return 'badge-brasileirao-a'
  if (camp.includes('SÉRIE B')) return 'badge-brasileirao-b'
  if (camp.includes('LIBERTADORES')) return 'badge-libertadores'
  if (camp.includes('SUL-AMERICANA')) return 'badge-sulamericana'
  return 'badge-brasileirao-a'
}

// Converte "02/04" → Date para comparar com hoje
function parseData(dataStr) {
  if (!dataStr || dataStr.toLowerCase().includes('definir')) return null
  const [dia, mes] = dataStr.split('/').map(Number)
  return new Date(2026, mes - 1, dia)
}

// Retorna o próximo jogo com data definida
function proximoJogo(jogos) {
  const hoje = new Date()
  hoje.setHours(0, 0, 0, 0)
  return jogos
    .filter(j => {
      const d = parseData(j.data)
      return d && d >= hoje
    })
    .sort((a, b) => parseData(a.data) - parseData(b.data))[0] || null
}

// Renderiza o card de destaque
function renderDestaque(jogo) {
  if (!jogo) return
  const secao = document.getElementById('proximo-destaque')
  const container = document.getElementById('destaque-card')
  secao.style.display = 'block'

  const times = jogo.times.split(' X ')
  const casa = times[0] || jogo.times
  const fora = times[1] || ''
  const cor = `var(--cor-${jogo.time_principal.replace(/\s/g, '-').replace('Ã', 'A').replace('Ã', 'A')}, #006437)`

  container.innerHTML = `
    <div class="destaque-card" style="background: linear-gradient(135deg, #1a1a1a, #222); border: 1px solid rgba(255,255,255,0.1);">
      <div class="times">
        <div class="time">
          <img src="${jogo.escudo_casa}" onerror="this.style.display='none'" alt="${casa}">
          <span>${casa}</span>
        </div>
        <span class="versus">X</span>
        <div class="time direita">
          <img src="${jogo.escudo_fora}" onerror="this.style.display='none'" alt="${fora}">
          <span>${fora}</span>
        </div>
      </div>
      <div class="card-footer">
        <div class="infos">
          <div class="info">📅 ${jogo.data} às ${jogo.hora}</div>
          <div class="info">🏟️ ${jogo.estadio}</div>
        </div>
        <span class="badge-camp ${badgeClass(jogo.campeonato)}">${jogo.campeonato}</span>
      </div>
    </div>
  `
}

// Monta os botões de filtro de times
function renderFiltrosTimes(jogos) {
  const times = ['TODOS', ...new Set(jogos.map(j => j.time_principal))]
  const container = document.getElementById('filtros-times')
  container.innerHTML = times.map(t => `
    <button class="filtro-btn${t === timeSelecionado ? ' ativo' : ''}"
      data-time="${t}">${t === 'TODOS' ? '⚽ Todos' : t}</button>
  `).join('')

  container.querySelectorAll('.filtro-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      timeSelecionado = btn.dataset.time
      renderFiltrosTimes(jogos)
      renderFiltrosCamp(jogosFiltradosPorTime())
      renderLista()
    })
  })
}

// Monta os botões de filtro de campeonato (só mostra camps do time selecionado)
function renderFiltrosCamp(jogos) {
  const camps = ['TODOS', ...new Set(jogos.map(j => j.campeonato))]
  // reseta camp se não existe mais nos filtros disponíveis
  if (!camps.includes(campSelecionado)) campSelecionado = 'TODOS'

  const container = document.getElementById('filtros-camp')
  container.innerHTML = camps.map(c => `
    <button class="filtro-btn${c === campSelecionado ? ' ativo' : ''}"
      data-camp="${c}">${c === 'TODOS' ? '🏆 Todos' : c}</button>
  `).join('')

  container.querySelectorAll('.filtro-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      campSelecionado = btn.dataset.camp
      renderFiltrosCamp(jogosFiltradosPorTime())
      renderLista()
    })
  })
}

function jogosFiltradosPorTime() {
  if (timeSelecionado === 'TODOS') return todosJogos
  return todosJogos.filter(j => j.time_principal === timeSelecionado)
}

function jogosFiltrados() {
  let lista = jogosFiltradosPorTime()
  if (campSelecionado !== 'TODOS') lista = lista.filter(j => j.campeonato === campSelecionado)
  return lista
}

// Renderiza os cards de jogos
function renderLista() {
  const lista = document.getElementById('lista-jogos')
  const jogos = jogosFiltrados()

  if (jogos.length === 0) {
    lista.innerHTML = '<div class="vazio">Nenhum jogo encontrado para este filtro.</div>'
    return
  }

  lista.innerHTML = jogos.map((jogo, i) => {
    const times = jogo.times.split(' X ')
    const casa = times[0] || jogo.times
    const fora = times[1] || ''
    const dataLabel = jogo.data.toLowerCase().includes('definir')
      ? '📅 Data a definir'
      : `📅 ${jogo.data} às ${jogo.hora}`
    const delay = Math.min(i * 40, 400)

    return `
      <div class="jogo-card" data-time="${jogo.time_principal}" style="animation-delay:${delay}ms">
        <div class="times">
          <div class="time">
            <img src="${jogo.escudo_casa}" onerror="this.style.display='none'" alt="${casa}">
            <span>${casa}</span>
          </div>
          <span class="versus">X</span>
          <div class="time direita">
            <img src="${jogo.escudo_fora}" onerror="this.style.display='none'" alt="${fora}">
            <span>${fora}</span>
          </div>
        </div>
        <div class="card-footer">
          <div class="infos">
            <div class="info">${dataLabel}</div>
            <div class="info">🏟️ ${jogo.estadio}</div>
          </div>
          <span class="badge-camp ${badgeClass(jogo.campeonato)}">${jogo.campeonato}</span>
        </div>
      </div>
    `
  }).join('')
}

// ============================
//  INICIALIZAÇÃO
// ============================
fetch('jogos.json')
  .then(r => r.json())
  .then(jogos => {
    todosJogos = jogos
    renderFiltrosTimes(jogos)
    renderFiltrosCamp(jogos)
    renderLista()
    renderDestaque(proximoJogo(jogos))
  })
  .catch(err => {
    console.error('Erro ao carregar jogos.json:', err)
    document.getElementById('lista-jogos').innerHTML =
      '<div class="vazio">Erro ao carregar os jogos.</div>'
  })