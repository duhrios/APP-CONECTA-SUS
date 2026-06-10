# Sprint 3 — Melhorias de UX na Fila
**Período:** Iteração de experiência do usuário  
**Status:** ✅ Concluída

---

## Objetivo
Melhorar significativamente a experiência do paciente na etapa de espera na fila, com alertas visuais progressivos por posição e correção de dados que persistiam incorretamente ao reiniciar o check-in.

---

## Entregas

### 1. Sistema de Alertas por Posição na Fila

#### Posição 1 — Alerta Pulsante com Contagem Regressiva
Quando o paciente chega à primeira posição da fila (próximo a ser chamado):

- **Card vermelho pulsante** com animação CSS `@keyframes pulse-border`
- **Número da senha** exibido em destaque (fonte 4.5rem, vermelho `#dc2626`)
- **Anel de contagem regressiva** de 60 segundos em círculo vermelho
- Mensagem: *"Dirija-se imediatamente ao balcão!"*
- Contagem regride a cada atualização da página

```css
@keyframes pulse-border {
  0%   { box-shadow: 0 0 0 0 rgba(220,38,38,0.5); }
  70%  { box-shadow: 0 0 0 14px rgba(220,38,38,0); }
  100% { box-shadow: 0 0 0 0 rgba(220,38,38,0); }
}
```

**Implementação técnica:**
```python
# Registra quando paciente entrou na posição 1
if st.session_state.tempo_entrada_posicao_1 is None:
    st.session_state.tempo_entrada_posicao_1 = datetime.now()

segundos_desde_pos1 = int(
    (datetime.now() - st.session_state.tempo_entrada_posicao_1)
    .total_seconds()
)
segundos_restantes = max(0, 60 - segundos_desde_pos1)
```

#### Posição 2 — Aviso Amarelo
- Card amarelo `sus-warn` com mensagem:  
  *"⚡ Você é o segundo da fila! Vá agora para a recepção da unidade."*

#### Posição 3 — Alerta Vermelho de Proximidade
- Aviso vermelho exigindo estar a menos de 1 km da unidade
- Verificação de distância com localização já capturada
- Se fila pequena (≤3 pessoas): alerta adicional de urgência

---

### 2. Ajuste de Frequência de Refresh

| Situação | Intervalo anterior | Intervalo novo |
|----------|-------------------|----------------|
| Posição 1 | 15 segundos | **5 segundos** |
| Demais posições | 15 segundos | 15 segundos |

O refresh mais rápido na posição 1 garante que a contagem regressiva seja precisa.

---

### 3. Correção: Dados Persistindo ao Reiniciar Check-in

**Problema:** Ao clicar em "Fazer novo check-in" ou "Cancelar Check-in", o campo de **telefone** não era apagado, aparecendo pré-preenchido no próximo check-in.

**Causa:** A chave `telefone` não estava na lista de limpeza do `session_state`.

**Solução:** Adicionadas as chaves `telefone` e `tempo_entrada_posicao_1` em todos os 3 pontos de limpeza do código:

```python
# Limpeza completa em todos os handlers de "novo check-in"
for key in ["stage", "numero_chamado", "nome_completo", "cpf_sus",
            "telefone",                    # ← adicionado
            "unidade_selecionada", "localizacao", "passou_posicao_3",
            "tempo_entrada_posicao_3",
            "tempo_entrada_posicao_1",     # ← adicionado
            "geo_location_cache", "geo_queue_cache"]:
    st.session_state.pop(key, None)
```

**Pontos corrigidos:**
1. Botão "Fazer novo check-in" após ser chamado com sucesso
2. Botão "Fazer novo check-in" após cancelamento automático por distância/tempo
3. Botão "❌ Cancelar Check-in" na tela de fila

---

### 4. Novo Estado de Sessão Adicionado

| Variável | Tipo | Finalidade |
|----------|------|-----------|
| `tempo_entrada_posicao_1` | `datetime \| None` | Registra quando paciente chegou à posição 1 |

---

## Comportamento Esperado por Posição

```
Posição > 3   →  Exibe senha + posição + tempo estimado + aviso geral
Posição = 3   →  Alerta vermelho de proximidade (1 km obrigatório)
Posição = 2   →  Aviso amarelo "vá agora para a recepção"
Posição = 1   →  Card pulsante vermelho + contagem regressiva 60s
Chamado       →  Tela de sucesso com confetes 🎉
```

---

## Métricas da Sprint
- Arquivos modificados: 1
- Bugs corrigidos: 1 (telefone persistindo)
- Novos estados de sessão: 1
- Animações CSS adicionadas: 2
- Classes CSS adicionadas: 4 (`.sus-pos1-alert`, `.sus-pos1-numero`, `.sus-countdown-ring`, `@keyframes pulse-border`)
