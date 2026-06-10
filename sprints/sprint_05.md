# Sprint 5 — Painel TV e Alerta Sonoro
**Período:** Iteração de experiência na recepção  
**Status:** ✅ Concluída

---

## Objetivo
Criar um painel de exibição pública para monitores/TVs da recepção das unidades de saúde, exibindo a senha atual chamada e a fila de próximas senhas em tempo real, com alerta sonoro automático a cada novo chamado.

---

## Entregas

### 1. Painel TV (`pages/3_painel.py`)

Página dedicada para projeção em monitor de recepção, acessível em `/painel`.

---

#### Layout Geral
```
┌─────────────────────────────────────────────────────┐
│  ❤️  Conecta SUS          Sistema de Atendimento  🕐 │  ← Topbar gradiente
├──────────────────────────┬──────────────────────────┤
│                          │  PRÓXIMAS SENHAS         │
│   🔔 SENHA CHAMADA        │  ──────────────────────  │
│                          │  01  Paciente A  PRÓXIMO │
│   ┌──────────────────┐   │  02  Paciente B  2º      │
│   │       07         │   │  03  Paciente C  3º      │
│   │   SENHA ATUAL    │   │  04  Paciente D  4º      │
│   └──────────────────┘   │  ...                     │
│   🏥 UBS Valo Velho       │                          │
│   Dirija-se ao balcão    │                          │
├──────────────────────────┴──────────────────────────┤
│  Sistema Conecta SUS · LGPD · Atualiza em 8s       │  ← Footer
└─────────────────────────────────────────────────────┘
```

---

#### Topbar
- Gradiente `#0AB4A0 → #2563EB`
- Logo ❤️ + nome "Conecta SUS"
- Relógio em tempo real (`HH:MM:SS`)
- Data completa com dia da semana em português

#### Painel Esquerdo — Senha Chamada
- **Estado vazio:** "Aguardando primeira chamada"
- **Senha ativa:**
  - Label "🔔 SENHA CHAMADA" em verde
  - Número em fonte **10rem** com brilho verde pulsante
  - Animação `glow-pulse` nos bordos do card
  - Badge com nome da unidade
  - Horário do chamado
  - Instrução: "Dirija-se ao balcão de atendimento"

```css
@keyframes glow-pulse {
  0%,100% { box-shadow: 0 0 40px rgba(10,180,160,.2); }
  50%     { box-shadow: 0 0 80px rgba(10,180,160,.4); }
}
```

#### Painel Direito — Próximas Senhas
- Exibe até 8 próximos da fila
- Primeiro item: destaque verde com badge "PRÓXIMO"
- Demais: badge com posição (2º, 3º...)
- Primeiro nome do paciente + unidade
- Rodapé: "+ N paciente(s) aguardando" quando há mais de 8

#### Auto-refresh
- Página atualiza automaticamente a cada **8 segundos**
- Sem necessidade de interação do usuário

---

### 2. Alerta Sonoro Automático

Quando uma nova senha é chamada, o painel toca automaticamente 3 tons ascendentes usando a **Web Audio API** do navegador — sem arquivos de áudio externos.

#### Implementação
```python
# Detecção de nova senha
numero_atual = ultimo["numero_chamado"] if ultimo else None
numero_prev  = st.session_state.get("painel_ultimo_numero")
nova_senha   = (numero_atual is not None) and (numero_atual != numero_prev)
st.session_state.painel_ultimo_numero = numero_atual

# Disparo do som
if nova_senha:
    components.html("""
<script>
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
</script>
""", height=0)
```

#### Notas musicais do beep
| Tom | Frequência | Tempo | Duração |
|-----|-----------|-------|---------|
| 1º (Lá4) | 880 Hz | 0.00s | 0.18s |
| 2º (Dó#5) | 1100 Hz | 0.22s | 0.18s |
| 3º (Mi5) | 1320 Hz | 0.44s | 0.30s |

> **Nota:** A Web Audio API requer pelo menos uma interação do usuário com a página antes de reproduzir sons (restrição de segurança de todos os navegadores modernos). Na recepção, o funcionário abrirá o painel e clicará uma vez — após isso, todos os chamados subsequentes terão som automático.

---

### 3. Solução Técnica: HTML sem Indentação

**Problema encontrado:** O parser Markdown do Streamlit trata linhas com 4+ espaços de indentação como bloco de código, exibindo o HTML como texto literal em vez de renderizá-lo.

**Solução:** Todo HTML gerado dinamicamente (variáveis Python com conteúdo HTML) foi construído como string sem indentação:

```python
# ERRADO — causa renderização como texto
left_html = """
    <div class="tv-left">
      <div>...</div>
    </div>"""

# CORRETO — sem indentação
left_html = (
    '<div class="tv-left">'
    '<div>...</div>'
    '</div>'
)
```

---

### 4. Navegação Integrada

Links para o painel adicionados em:
- **Rodapé do check-in** (`pages/1_principal_paciente.py`): link "📺 Painel TV"
- **Painel Admin** (`pages/2_admin.py`): botão "📺 Painel TV" na barra de ações

---

### 5. Configurações Técnicas do Painel

| Configuração | Valor |
|-------------|-------|
| Layout | Wide (100% da largura) |
| Sidebar | Colapsada e oculta |
| Background | `#0f172a` (azul escuro) |
| Refresh | 8 segundos |
| Senhas exibidas | 8 próximas |
| Tema | Dark — alto contraste para TV |

---

## Métricas da Sprint
- Arquivos criados: 1 (`pages/3_painel.py`)
- Arquivos modificados: 2 (check-in + admin)
- Linhas de código: ~160
- Animações CSS: 2 (`glow-pulse`, `pulse-border`)
- Bugs de renderização HTML resolvidos: 1
- Dependências novas: 0 (Web Audio API é nativa do browser)
