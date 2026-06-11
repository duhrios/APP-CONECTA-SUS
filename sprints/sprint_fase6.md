# Fase 6 — Funcionalidades Adicionais Pós-Entrega
**Sprints 19, 20 e 21**
**Período:** 10/06/2026 – 10/06/2026
**Contexto:** Sprints realizadas após a entrega do projeto integrador, com foco em funcionalidades avançadas para operação real das unidades de saúde.

---

## Sprint 19 — Painel TV para Recepção com Exibição em Tempo Real
**Período:** 10/06/2026 | **Status:** ✅ Concluído

### Objetivo
Criar um painel de exibição pública para monitores e TVs da recepção das unidades de saúde, mostrando a senha chamada atual e a fila de próximos pacientes em tempo real, com design otimizado para telas grandes.

### Contexto
Este item constava no backlog de versões futuras identificado na Sprint 18. Foi implementado como primeira entrega pós-integrador para viabilizar a operação real do sistema em recepções das UBSs.

### Tarefas Realizadas
- Criação do módulo `pages/3_painel.py` como página Streamlit dedicada para TV
- Implementação de layout de duas colunas em tema escuro (`#0f172a`) com alto contraste para projeção em monitor
- Desenvolvimento da topbar com gradiente `#0AB4A0 → #2563EB`, logo do sistema, relógio em tempo real (`HH:MM:SS`) e data completa em português
- Implementação do painel esquerdo: senha chamada em destaque (fonte 10rem), animação de brilho pulsante (`glow-pulse`), nome da unidade, horário do chamado e instrução "Dirija-se ao balcão de atendimento"
- Implementação do painel direito: fila das próximas 8 senhas com badge de posição (PRÓXIMO, 2º, 3º…)
- Auto-refresh automático da página a cada **8 segundos** sem interação do usuário
- Adição de links de navegação para o painel no rodapé da tela do paciente e no painel admin

### Layout do Painel TV

| Área | Conteúdo |
|------|----------|
| Topbar | Logo + relógio HH:MM:SS + data em português |
| Painel esquerdo | Senha atual (10rem) + animação glow + unidade + horário |
| Painel direito | Próximas 8 senhas com badges de posição |
| Footer | Nome do sistema + LGPD + aviso de atualização |

### Configurações Técnicas

| Configuração | Valor |
|-------------|-------|
| Layout | Wide (100% da largura da tela) |
| Tema | Dark — fundo #0f172a, alto contraste para TV |
| Refresh automático | A cada 8 segundos |
| Senhas exibidas | 8 próximas na fila |
| Sidebar | Oculta via CSS |

### Solução de Bug: HTML com Indentação Excessiva
**Problema identificado:** O parser Markdown do Streamlit trata linhas com 4 ou mais espaços de indentação como blocos de código, exibindo o HTML como texto literal em vez de renderizá-lo.

**Solução:** Todo HTML gerado em variáveis Python foi construído como string concatenada sem indentação nas linhas:
```python
# ERRADO — causes Streamlit to render as code block
left_html = """
    <div class="tv-left">
      <div>...</div>
    </div>"""

# CORRETO — no indentation
left_html = (
    '<div class="tv-left">'
    '<div>...</div>'
    '</div>'
)
```

### Entregáveis
- `pages/3_painel.py` — painel TV completo
- Links de acesso ao painel no check-in e no admin
- Layout responsivo para monitor/TV

### Retrospectiva
- **O que funcionou bem:** A utilização de CSS puro dentro do Streamlit viabilizou um layout TV de alta qualidade sem frameworks externos
- **Lição aprendida:** O parser Markdown do Streamlit tem comportamento não-óbvio com indentação — documentado para referência futura

---

## Sprint 20 — Alerta Sonoro Automático para Novos Chamados
**Período:** 10/06/2026 | **Status:** ✅ Concluído

### Objetivo
Adicionar alerta sonoro automático ao painel TV para que a equipe de recepção seja notificada imediatamente quando uma nova senha é chamada, sem depender de arquivos de áudio externos.

### Contexto
A ausência de alertas sonoros em recepções hospitalares frequentemente resulta em pacientes não percebendo quando sua senha é chamada. A solução precisava ser simples, sem instalação de plugins ou servidores de áudio.

### Solução Técnica: Web Audio API
Implementação de beep automático usando a **Web Audio API nativa do navegador**, via `st.components.v1.html`. Gera 3 tons ascendentes diretamente no JavaScript, sem arquivos de áudio externos.

```javascript
(function(){
  var ctx = new AudioContext();
  function beep(freq, start, dur, vol) {
    var o = ctx.createOscillator();
    var g = ctx.createGain();
    o.connect(g); g.connect(ctx.destination);
    o.type = 'sine'; o.frequency.value = freq;
    g.gain.linearRampToValueAtTime(vol, ctx.currentTime + start + 0.02);
    g.gain.linearRampToValueAtTime(0,   ctx.currentTime + start + dur);
    o.start(ctx.currentTime + start);
    o.stop(ctx.currentTime + start + dur + 0.05);
  }
  beep(880,  0.00, 0.18, 0.35);  // Lá4
  beep(1100, 0.22, 0.18, 0.35);  // Dó#5
  beep(1320, 0.44, 0.30, 0.28);  // Mi5
})();
```

### Notas Musicais do Beep

| Tom | Frequência | Início | Duração |
|-----|-----------|--------|---------|
| 1º — Lá4 | 880 Hz | 0.00s | 0.18s |
| 2º — Dó#5 | 1100 Hz | 0.22s | 0.18s |
| 3º — Mi5 | 1320 Hz | 0.44s | 0.30s |

### Mecanismo de Detecção de Nova Senha
```python
# Compara senha atual com a do refresh anterior
numero_atual = ultimo["numero_chamado"] if ultimo else None
numero_prev  = st.session_state.get("painel_ultimo_numero")
nova_senha   = (numero_atual is not None) and (numero_atual != numero_prev)
st.session_state.painel_ultimo_numero = numero_atual

if nova_senha:
    components.html(BEEP_SCRIPT, height=0)
```

### Observação Importante
A Web Audio API exige ao menos uma interação do usuário com a página antes de reproduzir sons (restrição de segurança de todos os navegadores modernos). Na prática, o funcionário abre o painel e clica uma vez — após isso, todos os chamados subsequentes terão som automático.

### Entregáveis
- Beep automático a cada nova senha chamada no painel TV
- Detecção baseada em comparação de estado (sem polling separado)
- Zero dependências externas (Web Audio API é nativa do browser)

### Retrospectiva
- **O que funcionou bem:** A Web Audio API nativa eliminou a necessidade de servidores de áudio ou arquivos externos
- **Restrição de navegador:** A política de autoplay exige interação prévia do usuário — contornada com orientação operacional

---

## Sprint 21 — Testes de Estresse e Validação de Robustez
**Período:** 10/06/2026 | **Status:** ✅ Concluído

### Objetivo
Validar a robustez de toda a camada de banco de dados e lógica de fila através de testes de estresse automatizados, cobrindo cenários extremos antes da operação real nas UBSs.

### Metodologia
Script Python (`stress_test.py`) executado diretamente contra a camada de banco de dados, simulando comportamentos extremos de forma automatizada e verificando os resultados esperados.

### 7 Fases de Teste

#### Fase 1 — Reset + 80 Pacientes
- Reset completo do banco
- Inserção sequencial de 80 pacientes com CPFs matematicamente válidos
- Verificação: 80 números únicos, todos no range 1–50 com wraparound

#### Fase 2 — Posição e Avanço Manual
- Verificação do 1º paciente na posição 1 e do último na posição 80
- Avanço manual de 10 pacientes via `chamar_proximo()`
- Verificação: 70 restantes na fila, 10 marcados como "atendido"

#### Fase 3 — Duplicata e Anti-spam
- Re-inserção de CPF já na fila → detectada e bloqueada
- Simulação de 3 tentativas spam com mesmo CPF → bloqueio ativado

#### Fase 4 — Fila Cheia (100 Pacientes) + Tentativas Extras
- Inserção até atingir o limite
- 10 tentativas adicionais após fila cheia → todas bloqueadas por `fila_cheia()`
- Verificação: exatamente 100 pacientes na fila com números únicos

#### Fase 5 — Esvaziamento Total + Wraparound
- Chamada de todos os pacientes via `chamar_proximo()`
- Reinserção de 20 novos pacientes → numeração reinicia sem duplicatas
- Resultado: `[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]`

#### Fase 6 — Remoção Individual
- Remoção do 6º paciente via `remover_da_fila()`
- Verificação: senha removida não aparece mais, 19 pacientes restantes

#### Fase 7 — Reset Final e Estado Limpo
- Reset completo + verificação de fila vazia
- Inserção de 1 paciente pós-reset → confirma posição 1

### Resultado Final

| Indicador | Valor |
|-----------|-------|
| Total de verificações | 21 |
| Verificações OK | **21** |
| Avisos | 0 |
| Erros | 0 |
| Pacientes simulados | 180+ |
| Tempo de execução | < 3 segundos |

### Comportamento Validado

| Cenário | Resultado |
|---------|-----------|
| Fila de 100 pacientes — numeração única | ✅ Passou |
| Tentativa após limite — retorna None | ✅ Passou |
| Wraparound após reset — reinicia do 1 | ✅ Passou |
| CPF duplicado mesma unidade — bloqueado | ✅ Passou |
| 3+ tentativas em 60min — bloqueado 1h | ✅ Passou |
| Remoção individual — posições reajustadas | ✅ Passou |
| Reset total — estado completamente limpo | ✅ Passou |

### Entregáveis
- 21 verificações automáticas passando com 0 erros
- Confirmação de robustez para operação real nas UBSs
- Script removido após validação (não necessário em produção)

### Retrospectiva
- **O que funcionou bem:** Testes automatizados identificaram comportamentos de wraparound e anti-spam que seriam difíceis de validar manualmente
- **Decisão:** Manter lógica de wraparound (reiniciar do 1 após reset) como comportamento padrão para UBSs com alta rotatividade de pacientes
