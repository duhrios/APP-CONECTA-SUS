# Sprint 1 — Fundação do Projeto
**Período:** Início do desenvolvimento  
**Status:** ✅ Concluída

---

## Objetivo
Construir a base funcional do sistema de check-in digital para unidades de saúde (UBS) de São Paulo, com fluxo completo do paciente e verificação de proximidade geográfica.

---

## Entregas

### 1. Estrutura do Projeto
- `app.py` — página inicial com navegação
- `database.py` — camada de dados SQLite com fila, tentativas e configurações
- `validators.py` — validação de CPF, Cartão SUS, nome e telefone
- `shared_state.py` — gerenciamento de estado compartilhado
- `pages/1_principal_paciente.py` — fluxo principal do paciente

### 2. Fluxo Multi-etapa do Paciente
| Etapa | Descrição |
|-------|-----------|
| Privacidade | Aviso LGPD com consentimento explícito |
| Formulário | Nome, CPF/Cartão SUS, telefone, unidade |
| Localização | Verificação GPS — máximo 10 km da unidade |
| Sintomas | Descrição livre dos sintomas principais |
| Fila | Acompanhamento em tempo real da posição |

### 3. Geolocalização
- Integração com `streamlit_geolocation`
- Cálculo de distância via `geopy.distance.geodesic`
- Validação de 10 km no check-in inicial
- Validação de 1 km ao atingir posição 3 na fila

### 4. Unidades de Saúde Cadastradas (10 unidades)
| Nome | Bairro |
|------|--------|
| UBS Valo Velho | Valo Velho |
| UBS Macedonia | Macedonia |
| UBS Parque Santo Antonio | Parque Santo Antonio |
| UBS/AMA Parque Figueira Grande | Figueira Grande |
| UBS Jardim Maracá | Jardim Maracá |
| UBS Santa Margarida | Santa Margarida |
| UBS/AMA Capão Redondo | Capão Redondo |
| UBS Jardim Germania | Jardim Germania |
| UBS São Bento | São Bento |
| UBS Luar do Sertão | Luar do Sertão |

### 5. Sistema de Fila
- Numeração sequencial 1–100 com prevenção de colisões
- Capacidade máxima: 100 pacientes simultâneos
- Avanço automático a cada 60 segundos
- Cancelamento automático por tempo ou distância

### 6. Segurança e Validações
- Anti-spam: bloqueio de CPF após 3 tentativas em 60 minutos
- Sanitização de todos os campos contra injeção HTML/XSS
- Validação matemática de CPF (dígitos verificadores)
- Validação de Cartão SUS (15 dígitos)
- Verificação de duplicidade na fila por CPF + unidade

### 7. Design (CSS customizado)
- Paleta de cores: gradiente `#0AB4A0` → `#2563EB`
- Layout centralizado (max 480px) para uso mobile
- Barra de progresso nas 5 etapas
- Cards com sombra suave, bordas arredondadas
- Botões primários com gradiente e sombra azul

---

## Banco de Dados (SQLite)
```sql
-- Tabela principal
fila (id, numero_chamado, nome, cpf_sus, unidade,
      sintomas, telefone, timestamp, status, atendido_em)

-- Anti-spam
tentativas (id, cpf_sus, timestamp)

-- Configurações de fila
config (chave, valor)  -- proximo_numero, ultimo_avanco_fila
```

---

## Dependências Instaladas
- `streamlit` — framework web
- `streamlit-geolocation` — captura GPS no navegador
- `geopy` — cálculo de distância geodésica

---

## Métricas da Sprint
- Arquivos criados: 6
- Linhas de código: ~650
- Etapas do fluxo: 5
- Unidades cadastradas: 10
- Validações implementadas: 6
