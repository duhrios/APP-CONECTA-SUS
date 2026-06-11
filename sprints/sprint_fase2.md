# Fase 2 — MVP: Interface, Geolocalização e Fila Virtual
**Sprints 3, 4 e 5**
**Período:** 15/09/2025 – 26/10/2025

---

## Sprint 3 — MVP: Interface do Paciente e Navegação por Estágios
**Período:** 15/09/2025 – 28/09/2025 | **Status:** ✅ Concluído

### Objetivo
Desenvolver a interface básica do fluxo do paciente, implementando a navegação por estágios e o formulário de check-in.

### Histórias de Usuário
- **HU-007:** Como paciente, desejo preencher um formulário com meu nome, CPF/Cartão SUS e selecionar minha unidade de saúde.
- **HU-008:** Como sistema, devo guiar o paciente por etapas sequenciais sem permitir que ele pule etapas de validação.

### Tarefas Realizadas
- Implementação do mecanismo de controle de fluxo por estágios via `st.session_state.stage`, com os valores: `privacy`, `form`, `location`, `symptoms`, `queue`
- Desenvolvimento da tela de formulário de check-in com campos: nome completo, CPF ou número do Cartão SUS e seleção de unidade de saúde
- Implementação da barra de progresso visual indicando etapas do processo
- Criação da paleta visual com identidade inspirada no SUS (tons de azul e verde institucional)
- Configuração de layout responsivo usando `st.set_page_config(layout="wide")`
- Implementação do `app.py` como ponto de entrada com redirecionamento para a página principal

### Entregáveis
- Tela de formulário funcional (sem validações ainda)
- Navegação entre estágios implementada
- Interface com identidade visual aplicada

### Retrospectiva
- **O que funcionou bem:** O mecanismo de estágios mostrou-se robusto para controlar o fluxo linear do usuário
- **Pontos de melhoria:** A interface ainda carecia de validações de entrada e feedback ao usuário

---

## Sprint 4 — Geolocalização e Validação de Proximidade Geográfica
**Período:** 29/09/2025 – 12/10/2025 | **Status:** ✅ Concluído

### Objetivo
Implementar a captura de geolocalização do paciente via navegador e o cálculo de distância em relação à unidade de saúde selecionada, bloqueando check-ins de locais remotos.

### Histórias de Usuário
- **HU-005 (implementação):** O sistema deve capturar as coordenadas GPS do dispositivo do paciente via API do navegador e calcular a distância até a unidade selecionada.
- **HU-009:** Como sistema, devo negar o check-in caso o paciente esteja a mais de 5 km da unidade (limite inicial).

### Tarefas Realizadas
- Integração do componente `streamlit_geolocation` para captura de coordenadas GPS via browser
- Implementação da função `calcular_distancia()` utilizando `geopy.distance.geodesic` para cálculo de distância real (em quilômetros)
- Cadastro das coordenadas reais das 10 unidades de saúde de São Paulo no dicionário `UNIDADES_SAUDE`
- Definição do limiar inicial de distância máxima em 5 km
- Implementação da tela de verificação de localização com feedback visual ao usuário (aguardando permissão, distância válida, distância inválida)
- Tratamento de casos onde o usuário nega a permissão de geolocalização no navegador

### Unidades de Saúde Cadastradas (10 UBSs — Zona Sul SP)

| Unidade | Tipo | Bairro |
|---------|------|--------|
| UBS Valo Velho | UBS | Valo Velho |
| UBS Macedonia | UBS | Macedonia |
| UBS Parque Santo Antonio | UBS | Parque Santo Antonio |
| UBS/AMA Parque Figueira Grande | UBS/AMA | Figueira Grande |
| UBS Jardim Maracá | UBS | Jardim Maracá |
| UBS Santa Margarida | UBS | Santa Margarida |
| UBS/AMA Capão Redondo | UBS/AMA | Capão Redondo |
| UBS Jardim Germania | UBS | Jardim Germania |
| UBS São Bento | UBS | São Bento |
| UBS Luar do Sertão | UBS | Luar do Sertão |

### Entregáveis
- Módulo de geolocalização integrado ao fluxo de check-in
- Validação de proximidade com feedback visual
- Cobertura de 10 unidades de saúde da zona sul de São Paulo com coordenadas reais

### Retrospectiva
- **O que funcionou bem:** A biblioteca `geopy` demonstrou precisão adequada para o cálculo de distâncias urbanas
- **Pontos de melhoria:** Identificou-se a necessidade de ajuste do limiar de distância baseado em testes com usuários reais

---

## Sprint 5 — Sistema de Fila Virtual com Numeração Sequencial
**Período:** 13/10/2025 – 26/10/2025 | **Status:** ✅ Concluído

### Objetivo
Implementar o sistema de gerenciamento de fila virtual, com geração de senhas sequenciais, rastreamento de posição em tempo real e exibição para o paciente.

### Histórias de Usuário
- **HU-003 (implementação):** O sistema deve gerar senhas sequenciais de 1 a 50 por unidade de saúde e exibir a posição atual do paciente na fila.
- **HU-010:** Como paciente, desejo visualizar minha posição na fila e uma estimativa de tempo de espera.

### Tarefas Realizadas
- Implementação do algoritmo de geração de senhas sequenciais (1 a 50) com reinício cíclico ao atingir o limite
- Desenvolvimento da tela de acompanhamento de fila com exibição de: número da senha, posição atual, total de pessoas na fila e estimativa de espera
- Implementação de atualização periódica automática da tela de fila a cada 15 segundos via `time.sleep(15)` + `st.rerun()`
- Tratamento do caso em que a fila está cheia (50 pacientes aguardando), bloqueando novos check-ins
- Implementação da lógica de rastreamento de posição: `obter_posicao(numero_chamado)` percorre a fila ordenada por timestamp e retorna o índice

### Entregáveis
- Sistema de fila virtual operacional com senhas de 1 a 50
- Tela de acompanhamento com atualização automática a cada 15 segundos
- Tratamento de fila cheia

### Retrospectiva
- **O que funcionou bem:** A lógica sequencial de senhas é intuitiva tanto para pacientes quanto para recepcionistas
- **Pontos de melhoria:** A atualização via polling (sleep + rerun) é funcional mas não ideal para produção; WebSockets seriam mais eficientes
