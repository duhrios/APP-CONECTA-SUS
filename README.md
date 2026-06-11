<div align="center">

# ❤️ Conecta SUS
### Sistema Digital de Check-in para Unidades de Saúde do SUS — São Paulo

[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)](https://sqlite.org)
[![LGPD](https://img.shields.io/badge/LGPD-Conforme-22c55e?style=for-the-badge)](https://www.gov.br/cidadania/pt-br/acesso-a-informacao/lgpd)

**🌐 APP ao vivo → [conectasus.streamlit.app)**

</div>

---

## 📋 Sobre o Projeto

O **Conecta SUS** é uma aplicação web desenvolvida como **Projeto Integrador** do curso de Análise e Desenvolvimento de Sistemas da **UNASP**, ao longo de dois semestres letivos (2025.2 e 2026.1).

O sistema moderniza o processo de check-in em Unidades Básicas de Saúde (UBS), Unidades de Pronto Atendimento (UPA) e Assistências Médicas Ambulatoriais (AMA) do município de São Paulo, utilizando **geolocalização** para validação de presença física e **fila virtual** com numeração de senhas.

> **Equipe:** Eduardo Rios · Amanda de Jesus · Leonardo  
> **Instituição:** UNASP — Análise e Desenvolvimento de Sistemas  
> **Disciplina:** Projeto Integrador  
> **Metodologia:** Scrum Adaptado (sprints de 2 semanas)

---

## 🎯 Funcionalidades Principais

| Funcionalidade | Descrição |
|---------------|-----------|
| 📝 **Check-in Digital** | Formulário com nome, CPF ou Cartão SUS em 5 etapas guiadas |
| 📍 **Geolocalização** | Verificação de proximidade — máximo 10 km da unidade selecionada |
| 🔒 **Conformidade LGPD** | Aviso de privacidade obrigatório + anonimização automática pós-atendimento |
| 🎫 **Fila Virtual** | Senha sequencial (1–100), posição em tempo real, estimativa de espera |
| 🔔 **Alertas por Posição** | Card pulsante + countdown 60s na posição 1, aviso amarelo na posição 2 |
| 🛡️ **Anti-spam** | Bloqueio de CPF após 3 tentativas em 60 minutos |
| 👨‍💼 **Painel Admin** | Dashboard com estatísticas, chamada de próximo, reset por unidade, exportação CSV |
| 📺 **Painel TV** | Exibição em monitor da recepção com senha chamada  |
| 🔁 **Avanço Automático** | Fila avança automaticamente a cada 60 segundos |

---

## 🏥 Unidades de Saúde Suportadas

10 unidades reais da **Zona Sul de São Paulo** com coordenadas GPS reais:

| # | Unidade | Tipo |
|---|---------|------|
| 1 | UBS Valo Velho | UBS |
| 2 | UBS Macedonia | UBS |
| 3 | UBS Parque Santo Antonio | UBS |
| 4 | UBS/AMA Parque Figueira Grande | UBS/AMA |
| 5 | UBS Jardim Maracá | UBS |
| 6 | UBS Santa Margarida | UBS |
| 7 | UBS/AMA Capão Redondo | UBS/AMA |
| 8 | UBS Jardim Germania | UBS |
| 9 | UBS São Bento | UBS |
| 10 | UBS Luar do Sertão | UBS |

---

## 🖥️ Telas do Sistema

### Fluxo do Paciente (5 etapas)
```
1. Privacidade  →  2. Formulário  →  3. Localização  →  4. Sintomas  →  5. Fila
    (LGPD)          (CPF/CNS)          (GPS 10km)        (Descrição)    (Senha)
```

### Painel Administrativo (`/admin`)
- Login protegido por credenciais
- Dashboard com 5 indicadores em tempo real
- Filtro por unidade de saúde
- Exportação de dados em CSV

### Painel TV para Recepção (`/painel`)
- Tema escuro de alto contraste
- Senha chamada em destaque (fonte grande)
- Próximas 8 senhas da fila
- Beep sonoro automático a cada novo chamado
- Auto-refresh a cada 8 segundos

---

## 🏗️ Arquitetura

```
conecta-sus/
├── app.py                          # Entry point — navegação principal
├── database.py                     # Camada de dados SQLite (fila_sus.db)
├── validators.py                   # Validação de CPF, Cartão SUS, nome
├── pages/
│   ├── 1_principal_paciente.py    # Fluxo completo do paciente
│   ├── 2_admin.py                 # Painel administrativo
│   └── 3_painel.py                # Painel TV da recepção
├── sprints/                        # Documentação de sprints
│   ├── sprint_fase1.md            # Sprints 0–2: Concepção e Arquitetura
│   ├── sprint_fase2.md            # Sprints 3–5: MVP e Geolocalização
│   ├── sprint_fase3.md            # Sprints 6–9: Banco, LGPD e Admin
│   ├── sprint_fase4.md            # Sprints 10–13: Segurança e Qualidade
│   ├── sprint_fase5.md            # Sprints 14–18: Design, Deploy e Entrega
│   ├── sprint_fase6.md            # Sprints 19–21: Funcionalidades Adicionais
│   └── Conecta_SUS_Sprints_Completo.pdf
└── .streamlit/
    └── config.toml                 # Configuração do servidor
```

### Banco de Dados SQLite (`fila_sus.db`)

```sql
-- Pacientes na fila
CREATE TABLE fila (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    numero_chamado INTEGER,
    nome          TEXT,
    cpf_sus       TEXT,
    unidade       TEXT,
    sintomas      TEXT,
    telefone      TEXT,
    timestamp     TEXT,
    status        TEXT DEFAULT 'aguardando',
    atendido_em   TEXT
);

-- Configurações persistentes
CREATE TABLE config (chave TEXT PRIMARY KEY, valor TEXT);

-- Controle anti-spam
CREATE TABLE tentativas (id INTEGER PRIMARY KEY AUTOINCREMENT, cpf_sus TEXT, timestamp TEXT);
```

---

## ⚙️ Tecnologias

| Tecnologia | Uso |
|-----------|-----|
| **Python 3.11** | Linguagem principal |
| **Streamlit** | Framework web e interface |
| **SQLite** | Banco de dados local persistente |
| **geopy** | Cálculo de distância geodésica |
| **streamlit-js-eval** | Captura de geolocalização via iframe oculto (solução robusta) |
| **fpdf2** | Geração de documentação PDF |
| **Web Audio API** | Beep sonoro no painel TV (nativo do navegador) |

---

## 🚀 Como Executar Localmente

```bash
# 1. Clone o repositório
git clone https://github.com/duhrios/APP-CONECTA-SUS.git
cd APP-CONECTA-SUS

# 2. Instale as dependências
pip install streamlit geopy streamlit-js-eval fpdf2

# 3. Execute a aplicação
streamlit run app.py --server.port 5000
```

Acesse em: `http://localhost:5000`

**Admin:** usuário `admin` / senha `sus2025`

---

## 📊 Sprints do Projeto

O projeto foi desenvolvido em **22 sprints** ao longo de 10 meses:

| Fase | Sprints | Período | Foco |
|------|---------|---------|------|
| **1** | S0 – S2 | Ago/2025 | Concepção, Requisitos, Arquitetura |
| **2** | S3 – S5 | Set–Out/2025 | MVP, Geolocalização, Fila Virtual |
| **3** | S6 – S9 | Out–Dez/2025 | Banco de Dados, LGPD, Admin, Automação |
| **4** | S10 – S13 | Jan–Mar/2026 | Anti-spam, Refatoração, UX, Admin Avançado |
| **5** | S14 – S18 | Mar–Jun/2026 | Design, Deploy, Estabilização, Entrega Final |
| **6** | S19 – S21 | Jun/2026 | Painel TV, Beep Sonoro, Testes de Estresse |

📄 **[Ver documentação completa das sprints (PDF)](sprints/Conecta_SUS_Sprints_Completo.pdf)**

---

## 🛡️ Segurança e LGPD

- ✅ Consentimento explícito antes da coleta de dados (tela de privacidade obrigatória)
- ✅ Anonimização automática de dados pessoais após atendimento
- ✅ Sanitização de todas as entradas contra injeção HTML/XSS
- ✅ Validação matemática de CPF (algoritmo de dígitos verificadores)
- ✅ Rate limiting: bloqueio após 3 tentativas em 60 minutos
- ✅ CPF mascarado na exportação CSV (`***.XXX.***-XX`)

---

## 📈 Métricas do Projeto

| Métrica | Valor |
|---------|-------|
| Duração total | 10 meses (Ago/2025 – Jun/2026) |
| Total de sprints | 22 (Sprint 0 a Sprint 21) |
| Histórias de usuário implementadas | 23 de 25 |
| Unidades de saúde suportadas | 10 (Zona Sul SP) |
| Capacidade da fila | Até 100 pacientes simultâneos |
| Distância máxima para check-in | 10 km da unidade |
| Intervalo de avanço automático | 60 segundos |
| Refresh da tela de fila | 15 segundos (5s na posição 1) |

---

<div align="center">

Desenvolvido com ❤️ para o SUS — São Paulo, 2025–2026

**UNASP · Análise e Desenvolvimento de Sistemas · Projeto Integrador**

</div>
