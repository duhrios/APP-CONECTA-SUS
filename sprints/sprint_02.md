# Sprint 2 — Painel Admin e Correções de Estabilidade
**Período:** Pós-MVP  
**Status:** ✅ Concluída

---

## Objetivo
Criar o painel administrativo para gestão da fila pelos funcionários da unidade e corrigir o bug crítico de crash do DOM na geolocalização.

---

## Entregas

### 1. Painel Administrativo (`pages/2_admin.py`)

#### Autenticação
- Login com usuário/senha protegido por sessão
- Credenciais padrão: `admin` / `sus2025`
- Logout com limpeza de sessão

#### Dashboard de Estatísticas (5 indicadores)
| Indicador | Descrição |
|-----------|-----------|
| Na fila agora | Total de pacientes aguardando |
| Atendidos hoje | Total atendido no dia corrente |
| Total do dia | Soma de atendidos + fila |
| Vagas livres | Capacidade restante (de 100) |
| Tempo médio | Média de espera dos atendidos |

#### Gestão da Fila
- Visualização completa da fila em tempo real
- Filtro por unidade de saúde
- Botão "Chamar próximo paciente" por unidade
- Expansor com dados completos de cada paciente
- Remoção individual de pacientes da fila
- Reset total da fila (todas as unidades)
- Reset por unidade individual

#### Histórico de Atendimentos
- Lista dos atendidos no dia com horário
- Filtro sincronizado com seletor de unidade

#### Exportação de Dados
- Download CSV do dia (atendidos + fila atual)
- CPF mascarado no CSV (`***.XXX.***-XX`)
- Charset UTF-8 BOM para compatibilidade com Excel

#### Auto-refresh
- Painel atualiza automaticamente a cada 10 segundos

---

### 2. Correção Crítica: Bug RemoveChild da Geolocalização

**Problema:** O componente `streamlit_geolocation` causava erro de DOM ao ser desmontado:
```
NotFoundError: Falha ao executar 'removeChild' em 'Node':
O nó a ser removido não é filho deste nó.
```

**Causa raiz:** O widget era renderizado e desmontado no mesmo ciclo de rerun do Streamlit, causando conflito no ciclo de vida do DOM do React.

**Solução implementada:**
- Criada flag `show_geo_widget` no `session_state`
- Widget só é renderizado **após** clique explícito do usuário
- Flag resetada antes de qualquer `st.rerun()`
- Botão "Voltar" ocultado enquanto widget está ativo

```python
# Antes (causava crash)
location = streamlit_geolocation()  # renderizado sempre

# Depois (estável)
if st.session_state.show_geo_widget:
    location = streamlit_geolocation()
else:
    if st.button("Compartilhar localização"):
        st.session_state.show_geo_widget = True
        st.rerun()
```

---

### 3. Melhorias no Fluxo de Localização
- Mensagem explicativa antes de solicitar o GPS
- Link "Ver rota até a unidade no Google Maps" com coordenadas reais
- Botão "Escolher outra unidade" quando fora do raio
- Botão "Tentar novamente" para capturar GPS novamente

---

## Bug Fix: Reutilização de Localização na Fila

**Problema adicional detectado:** Na etapa de fila, o código chamava `streamlit_geolocation()` diretamente para verificar proximidade na posição 3, causando o mesmo crash.

**Solução:** Removida a chamada duplicada. Agora o sistema reutiliza a localização já capturada na etapa de verificação inicial:
```python
# Removido — causava crash
location_fila = streamlit_geolocation()

# Substituído por
localizacao_atual = st.session_state.get("geo_queue_cache") or \
                    st.session_state.get("localizacao")
```

---

## Métricas da Sprint
- Arquivos criados: 1 (`pages/2_admin.py`)
- Arquivos modificados: 1 (`pages/1_principal_paciente.py`)
- Bugs corrigidos: 2 (removeChild × 2 ocorrências)
- Funcionalidades admin: 8
- Linhas de código novas: ~380
