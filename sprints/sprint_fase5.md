# Fase 5 — Design, Deploy em Produção e Entrega Final
**Sprints 14, 15, 16, 17 e 18**
**Período:** 02/03/2026 – 10/06/2026

---

## Sprint 14 — Exploração de Design e Prototipagem de Alternativas Visuais
**Período:** 02/03/2026 – 15/03/2026 | **Status:** ✅ Concluído

### Objetivo
Explorar alternativas de design para a interface do paciente através de mockups interativos, avaliando diferentes linguagens visuais antes de escolher a definitiva.

### Tarefas Realizadas
- Configuração do ambiente de prototipagem visual (Mockup Sandbox com servidor Vite)
- Desenvolvimento de três variantes de interface em React/TypeScript para avaliação comparativa:
  - **Variante A — Limpo e Profissional:** Layout clean com tipografia clara, paleta azul institucional, foco em acessibilidade
  - **Variante B — Moderno Escuro:** Tema escuro com gradientes vibrantes, voltado para público mais jovem
  - **Variante C — Vibrante:** Alta saturação de cores, forte contraste visual, elementos gráficos marcantes
- Exposição das três variantes em canvas de comparação para avaliação side-by-side
- Coleta de feedback sobre preferências de design
- **Decisão final:** Variante C (Vibrante) escolhida e integrada ao sistema principal

### Comparativo das Variantes

| Variante | Tom | Público-alvo | Destaques |
|----------|-----|-------------|-----------|
| A — Limpo e Profissional | Azul institucional | Geral, foco em acessibilidade | Tipografia clara, contraste alto |
| B — Moderno Escuro | Dark, gradientes | Público jovem | Gradientes vibrantes, alto impacto visual |
| C — Vibrante (ESCOLHIDA) | Verde + azul saturado | Todos os perfis | Alta saturação, ícones marcantes, coração vermelho |

### Entregáveis
- Três protótipos visuais em React/TypeScript disponíveis para comparação
- Avaliação das alternativas de design documentada
- Definição da linguagem visual preferida para o sistema principal

### Retrospectiva
- **O que funcionou bem:** A comparação side-by-side de variantes acelerou a tomada de decisão sobre identidade visual
- **Lição aprendida:** Prototipagem visual antes da implementação final evita retrabalho significativo na UI

---

## Sprint 15 — Publicação em Produção e Configuração de Deploy
**Período:** 16/03/2026 – 29/03/2026 | **Status:** ✅ Concluído

### Objetivo
Realizar o primeiro deploy do sistema em ambiente de produção, tornando a aplicação acessível publicamente via URL pública.

### Tarefas Realizadas
- Configuração do ambiente de deploy no Replit com runtime Python 3.11
- Ajustes de configuração para o ambiente de produção: desativação de modo de desenvolvimento, configuração de coleta de métricas
- Publicação da aplicação na URL pública
- Testes de smoke em produção: verificação de todos os fluxos principais (check-in, fila, admin) no ambiente publicado
- Verificação da persistência do banco de dados SQLite entre reinicializações do servidor de produção

### Checklist de Smoke Test em Produção

| Funcionalidade | Resultado |
|---------------|-----------|
| Fluxo de check-in completo (5 etapas) | Passou |
| Geolocalização via navegador | Passou |
| Geração e exibição de senha na fila | Passou |
| Painel administrativo — login | Passou |
| Painel administrativo — chamar próximo | Passou |
| Persistência do banco entre reinicializações | Passou |

### Entregáveis
- Aplicação publicada e acessível em URL pública
- Testes de smoke documentados
- Ambiente de produção estável

### Retrospectiva
- **O que funcionou bem:** A hospedagem no Replit simplificou significativamente o processo de deploy sem necessidade de configuração de infraestrutura
- **Desafio identificado:** O banco de dados SQLite em disco no ambiente de produção Replit tem limitações de concorrência para cenários de alta carga simultânea

---

## Sprint 16 — Estabilização Pós-deploy e Correções de Bugs
**Período:** 30/03/2026 – 26/04/2026 | **Status:** ✅ Concluído

### Objetivo
Identificar e corrigir inconsistências e bugs evidenciados após a publicação em produção, estabilizando o sistema para uso contínuo.

### Tarefas Realizadas
- Monitoramento dos logs de produção para identificação de erros recorrentes
- Correção de bug no painel administrativo: o contador de vagas livres exibia valor inconsistente quando a fila estava filtrada por unidade
- Revisão do comportamento do avanço automático em produção: verificação de que o intervalo de 60 segundos respeitava o horário de servidor
- Ajustes de UX na tela de cancelamento: melhoria das mensagens de erro ao paciente quando o check-in é cancelado automaticamente por distância
- Melhoria da validação de geolocalização na posição 3 da fila: cancelamento explícito do check-in quando os dados de geolocalização não estão disponíveis nessa etapa crítica

### Bugs Corrigidos

| Bug | Impacto | Correção |
|-----|---------|---------|
| Vagas livres incorretas no filtro por unidade | Alto — exibia capacidade errada | Cálculo usando total global da fila |
| Avanço automático ignorando horário de servidor | Médio — timing inconsistente | Validação com timestamp do banco |
| Mensagem de cancelamento pouco clara | Baixo — confusão do usuário | Reescrita das mensagens de erro |
| Geolocalização não verificada na posição 3 | Alto — cancelamento sem aviso | Verificação explícita com cancelamento imediato |

### Entregáveis
- Sistema de produção estabilizado
- Bugs críticos do painel administrativo corrigidos
- Validação de geolocalização reforçada na posição 3 da fila

### Retrospectiva
- **O que funcionou bem:** O monitoramento contínuo de logs permitiu identificar bugs que não haviam aparecido nos testes em desenvolvimento
- **Lição aprendida:** Testes em ambiente idêntico ao de produção antes do deploy teria antecipado a identificação desses bugs

---

## Sprint 17 — Otimização de Código e Redução de Débito Técnico
**Período:** 27/04/2026 – 10/05/2026 | **Status:** ✅ Concluído

### Objetivo
Reduzir o débito técnico acumulado ao longo do desenvolvimento, melhorando a qualidade interna do código sem alterar o comportamento externo.

### Tarefas Realizadas
- Revisão completa do módulo `database.py` para garantia de thread-safety em todas as operações de escrita
- Implementação do context manager `get_conn()` como única forma de acesso ao banco de dados, eliminando conexões abertas e esquecidas
- Padronização do tratamento de datas com a função auxiliar `_parse_dt()` para evitar exceções em valores malformados
- Revisão das mensagens de log do Streamlit para identificação de gargalos de performance
- Organização e padronização dos docstrings das funções principais

### Padrões Técnicos Consolidados

| Padrão | Regra |
|--------|-------|
| Acesso ao banco | Sempre via `get_conn()` — nunca `sqlite3.connect()` diretamente |
| Tratamento de datas | Sempre via `_parse_dt()` — nunca `datetime.strptime()` diretamente |
| Thread-safety | Todas as escritas dentro do context manager com lock implícito |
| Docstrings | Formato Google Style em todas as funções públicas |

### Entregáveis
- Código mais robusto com gerenciamento seguro de conexões de banco de dados
- Tratamento unificado de datas em todo o sistema
- Redução de código duplicado

### Retrospectiva
- **O que funcionou bem:** O padrão de context manager eliminou uma categoria inteira de bugs relacionados a conexões de banco abertas indefinidamente
- **Decisão arquitetural reforçada:** Toda escrita no banco de dados deve passar por `get_conn()` — nunca acessar `sqlite3.connect()` diretamente no código da aplicação

---

## Sprint 18 — Correção Crítica de Geolocalização e Entrega Final
**Período:** 11/05/2026 – 10/06/2026 | **Status:** ✅ Concluído

### Objetivo
Identificar, diagnosticar e corrigir definitivamente o bug crítico de geolocalização que causava falha na renderização do sistema em produção, e entregar o projeto integrador em sua versão final estável.

### Contexto do Bug
Após atualizações do ambiente de produção, a aplicação passou a apresentar o erro crítico `NotFoundError: Failed to execute 'removeChild' on 'Node'` nas telas de verificação de localização. O erro ocorria no reconciliador do React, motor que o Streamlit utiliza internamente para gerenciar o DOM virtual.

### Diagnóstico Técnico
A investigação revelou que o componente `streamlit_geolocation` apresentava incompatibilidade com o ciclo de rerenderização do Streamlit. O componente realizava manipulações no DOM de forma assíncrona: ao obter as coordenadas GPS (operação assíncrona do browser), ele tentava atualizar nós do DOM que o React já havia removido durante um ciclo de rerenderização. Esta **condição de corrida (race condition)** entre a resposta assíncrona da API de Geolocalização e o ciclo síncrono de rerenderização do Streamlit produzia o erro.

### Solução Implementada
Substituição completa da biblioteca `streamlit_geolocation` pela biblioteca `streamlit_js_eval`, que utiliza uma arquitetura fundamentalmente diferente: ao invés de manipular o DOM visível da página, executa o JavaScript dentro de um **iframe oculto** e retorna o resultado via mecanismo de comunicação de componentes do Streamlit. Esta abordagem elimina completamente o conflito com o reconciliador React.

```python
from streamlit_js_eval import streamlit_js_eval

location = streamlit_js_eval(
    js_expressions="""await new Promise((resolve) => {
        if (!navigator.geolocation) { resolve(null); return; }
        navigator.geolocation.getCurrentPosition(
            (pos) => resolve({latitude: pos.coords.latitude, longitude: pos.coords.longitude}),
            () => resolve(null),
            {enableHighAccuracy: true, timeout: 15000}
        );
    })""",
    want_output=True,
    key="geo_location_capture"
)
```

### Tarefas Realizadas
- Diagnóstico do erro `NotFoundError` nos logs de produção e reprodução local
- Análise da arquitetura interna do `streamlit_geolocation` para identificação da causa raiz
- Instalação e integração de `streamlit_js_eval` como substituto
- Implementação de cache de geolocalização no `session_state` para evitar chamadas desnecessárias ao componente durante rerenders
- Implementação de cache específico para a tela de fila (`geo_queue_cache`): o componente só é ativado quando o paciente está nas posições críticas (posições 1 a 4)
- Limpeza correta dos caches de geolocalização em todos os pontos de saída do fluxo (cancelamento e novo check-in)
- Republicação em produção e verificação do funcionamento correto

### Entregáveis
- Bug crítico de geolocalização corrigido em produção
- Arquitetura de captura de localização mais robusta com `streamlit_js_eval`
- Sistema estável publicado na URL pública para entrega do projeto integrador

### APP Disponível
`https://sistema-sus--eduardo123rios.replit.app`

### Retrospectiva
- **O que funcionou bem:** A abordagem de diagnóstico sistemático — análise de logs → identificação da causa raiz → solução arquitetural → validação — foi eficaz para um bug complexo
- **Lição aprendida:** Componentes de terceiros para Streamlit devem ser avaliados quanto à compatibilidade com o ciclo de rerenderização antes de sua adoção no projeto
- **Decisão técnica consolidada:** O uso de `streamlit_js_eval` para qualquer interação com APIs do navegador (geolocalização, clipboard, deviceOrientation) é preferível a componentes que manipulam o DOM diretamente
