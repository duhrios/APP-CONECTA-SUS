# Fase 1 — Concepção, Requisitos e Arquitetura
**Sprints 0, 1 e 2**
**Período:** 04/08/2025 – 14/09/2025
**Equipe:** Eduardo Rios, Amanda de Jesus e Leonardo
**Instituição:** UNASP — Análise e Desenvolvimento de Sistemas

---

## Sprint 0 — Concepção e Kickoff do Projeto
**Período:** 04/08/2025 – 17/08/2025 | **Status:** ✅ Concluído

### Objetivo
Definir o escopo do projeto integrador, identificar o problema a ser resolvido e estabelecer o ambiente de trabalho colaborativo.

### Contexto e Justificativa
A problemática do sistema de saúde pública brasileiro frequentemente envolve filas presenciais extensas, ausência de organização digital e exposição desnecessária de pacientes em ambientes hospitalares. O grupo identificou a oportunidade de propor uma solução tecnológica acessível, utilizando apenas um dispositivo móvel com acesso à internet, eliminando a necessidade de filas físicas para a retirada de senhas.

### Histórias de Usuário Mapeadas
- **HU-001:** Como paciente, desejo realizar meu check-in remotamente para evitar aglomerações.
- **HU-002:** Como administrador, desejo visualizar a fila da minha unidade em tempo real.
- **HU-003:** Como paciente, desejo receber uma senha numerada e acompanhar minha posição na fila.

### Tarefas Realizadas
- Definição do tema e justificativa acadêmica do projeto integrador
- Levantamento inicial do domínio de problema (SUS, check-in, filas hospitalares)
- Escolha da metodologia ágil (Scrum adaptado) e ciclo de sprints de 14 dias
- Configuração do ambiente de desenvolvimento no Replit
- Criação do repositório do projeto e primeiras configurações de ambiente Python

### Entregáveis
- Documento de visão do produto (Product Vision Board)
- Backlog inicial com épicos identificados
- Ambiente de desenvolvimento configurado

### Retrospectiva
- **O que funcionou bem:** Alinhamento rápido sobre o tema e tecnologias
- **Pontos de melhoria:** Necessidade de aprofundar o levantamento de requisitos com usuários reais
- **Decisões técnicas:** Adoção do Streamlit como framework por sua curva de aprendizado reduzida e capacidade de prototipagem rápida

---

## Sprint 1 — Levantamento de Requisitos e Análise de Domínio
**Período:** 18/08/2025 – 31/08/2025 | **Status:** ✅ Concluído

### Objetivo
Realizar o levantamento detalhado de requisitos funcionais e não funcionais, mapeando os fluxos de usuário e as regras de negócio do sistema de check-in.

### Histórias de Usuário
- **HU-004:** Como paciente, desejo selecionar minha unidade de saúde dentre as unidades disponíveis.
- **HU-005:** Como sistema, devo verificar se o paciente está fisicamente próximo à unidade selecionada antes de autorizar o check-in.
- **HU-006:** Como administrador, desejo um painel protegido por autenticação para gerir a fila.

### Tarefas Realizadas
- Identificação das 10 unidades de saúde reais do município de São Paulo (UBS, AMA, UPA) em bairros como Vila Mariana, Pinheiros, Santana
- Levantamento das coordenadas geográficas reais de cada unidade (latitude e longitude)
- Definição do fluxo completo de check-in: consentimento LGPD → formulário → geolocalização → confirmação de sintomas → fila → chamada
- Mapeamento dos requisitos não funcionais: privacidade de dados, rate limiting, prevenção de check-in duplicado
- Análise das APIs de geolocalização disponíveis para aplicações web

### Entregáveis
- Diagrama de fluxo de usuário (patient journey map)
- Lista de unidades de saúde com coordenadas GPS reais
- Requisitos funcionais e não funcionais documentados
- Modelo conceitual do banco de dados (esboço)

### Retrospectiva
- **O que funcionou bem:** Levantamento de dados reais de localização das unidades conferiu realismo ao protótipo
- **Pontos de melhoria:** Falta de acesso a usuários reais do SUS para validação dos requisitos
- **Decisões técnicas:** Definido o uso de `geopy` para cálculo de distância geodésica entre coordenadas

---

## Sprint 2 — Definição de Arquitetura e Estrutura Técnica
**Período:** 01/09/2025 – 14/09/2025 | **Status:** ✅ Concluído

### Objetivo
Definir a arquitetura técnica do sistema, selecionar as bibliotecas e estabelecer a estrutura de arquivos do projeto.

### Tarefas Realizadas
- Definição da arquitetura em camadas: interface (Streamlit pages), lógica de negócio (Python puro) e persistência (SQLite)
- Estruturação do projeto em múltiplos arquivos: `app.py`, `pages/1_principal_paciente.py`, `pages/2_admin.py`, `database.py`, `validators.py`
- Seleção e instalação das dependências: `streamlit`, `geopy`, `streamlit-geolocation`
- Configuração do servidor Streamlit (`config.toml`) com porta 5000 e suporte a CORS para o ambiente Replit
- Definição do modelo relacional do banco de dados SQLite com três tabelas: `fila`, `config` e `tentativas`

### Decisões Arquiteturais

| Decisão | Alternativa Considerada | Justificativa |
|---------|------------------------|---------------|
| Streamlit como framework | Flask + React, Django | Menor complexidade para equipe acadêmica, prototipagem rápida |
| SQLite como banco de dados | PostgreSQL, MongoDB | Sem necessidade de servidor externo; adequado para MVP |
| Armazenamento via session_state | Banco de dados em memória | Simplicidade para gerenciar estado de sessão por usuário |

### Entregáveis
- Diagrama de arquitetura do sistema (camadas e componentes)
- Estrutura de arquivos do projeto definida e documentada
- Modelo de banco de dados relacional (DDL das tabelas)

### Retrospectiva
- **O que funcionou bem:** Separação clara de responsabilidades entre os arquivos facilitou o desenvolvimento paralelo
- **Pontos de melhoria:** A ausência de testes automatizados desde o início foi identificada como risco técnico
