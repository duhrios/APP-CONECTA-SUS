# Fase 3 — Banco de Dados, LGPD, Painel Admin e Automação
**Sprints 6, 7, 8 e 9**
**Período:** 27/10/2025 – 21/12/2025

---

## Sprint 6 — Banco de Dados SQLite e Persistência de Dados
**Período:** 27/10/2025 – 09/11/2025 | **Status:** ✅ Concluído

### Objetivo
Migrar a gestão de estado do `session_state` para um banco de dados SQLite persistente, permitindo que múltiplos usuários compartilhem a mesma fila e que os dados sobrevivam a reinicializações do servidor.

### Histórias de Usuário
- **HU-011:** Como sistema, devo armazenar os dados da fila em banco de dados para que múltiplos dispositivos possam acessar o mesmo estado.
- **HU-012:** Como administrador, desejo que os dados de fila persistam entre reinicializações da aplicação.

### Tarefas Realizadas
- Criação do módulo `database.py` com gerenciamento completo de conexão SQLite usando context manager (`@contextmanager get_conn()`)
- Definição e criação das três tabelas do schema:

| Tabela | Campos principais |
|--------|------------------|
| `fila` | numero_chamado, nome, cpf_sus, unidade, sintomas, timestamp, status, atendido_em |
| `config` | chave, valor (proximo_numero, ultimo_avanco_fila) |
| `tentativas` | id, cpf_sus, timestamp (anti-spam) |

- Implementação das operações CRUD: `adicionar_na_fila()`, `obter_fila()`, `obter_posicao()`, `remover_da_fila()`, `chamar_proximo()`, `resetar_fila()`
- Configuração de `check_same_thread=False` no SQLite para suportar o modelo de threading do Streamlit
- Substituição de toda manipulação de estado global pelo acesso ao banco de dados

### Entregáveis
- Módulo `database.py` com API completa de acesso a dados
- Banco de dados `fila_sus.db` com schema definido
- Sistema de fila compartilhado entre sessões de usuário

### Retrospectiva
- **O que funcionou bem:** A separação total da lógica de banco de dados em um módulo dedicado facilitou a manutenção
- **Decisão técnica importante:** Adoção do padrão `conn.row_factory = sqlite3.Row` para retornar resultados como dicionários, facilitando o acesso por nome de coluna

---

## Sprint 7 — Validação de Dados e Conformidade com LGPD
**Período:** 10/11/2025 – 23/11/2025 | **Status:** ✅ Concluído

### Objetivo
Implementar validações de entrada para os dados do paciente (CPF e Cartão SUS), adicionar sanitização de entradas e inserir o aviso de privacidade conforme exigências da LGPD.

### Histórias de Usuário
- **HU-013:** Como sistema, devo validar o CPF do paciente usando o algoritmo oficial de verificação de dígitos.
- **HU-014:** Como sistema, devo validar o Cartão Nacional de Saúde (CNS) como identificador alternativo ao CPF.
- **HU-015:** Como paciente, desejo ser informado sobre o uso dos meus dados pessoais antes de prosseguir com o check-in (LGPD).

### Tarefas Realizadas
- Criação do módulo `validators.py` com as funções:
  - `validar_cpf(cpf)`: implementação do algoritmo oficial de validação por dígitos verificadores (módulo 11)
  - `validar_cartao_sus(numero)`: validação de 15 dígitos numéricos do Cartão Nacional de Saúde
  - `validar_nome(nome)`: verificação de nome completo (mínimo 2 palavras, apenas letras e espaços)
  - `sanitizar_entrada(texto)`: remoção de caracteres potencialmente maliciosos para prevenção de injeção
- Implementação da tela de aviso de privacidade (estágio `privacy`) como primeira tela obrigatória do fluxo
- Conteúdo do aviso: finalidade do tratamento de dados, tempo de retenção, não compartilhamento com terceiros, base legal (consentimento)
- Anonimização automática dos dados pessoais após atendimento: na função `chamar_proximo()`, os campos `nome`, `cpf_sus` e `sintomas` são substituídos por `'* DADO REMOVIDO *'`

### Conformidade LGPD Implementada
| Princípio LGPD | Implementação |
|---------------|---------------|
| Finalidade | Aviso explícito de uso dos dados na tela de privacidade |
| Adequação | Coleta apenas dos dados necessários para check-in |
| Minimização | Anonimização automática pós-atendimento |
| Consentimento | Checkbox de aceite obrigatório antes do formulário |

### Entregáveis
- Módulo `validators.py` com validadores de CPF, Cartão SUS e nome
- Tela de aviso de privacidade LGPD integrada ao fluxo
- Anonimização automática pós-atendimento implementada

### Retrospectiva
- **O que funcionou bem:** A anonimização automática garante conformidade com o princípio de minimização de dados da LGPD
- **Desafio enfrentado:** O algoritmo de validação de CPF exigiu atenção especial para tratar CPFs com dígitos repetidos (ex: 111.111.111-11) que passam no formato mas são inválidos

---

## Sprint 8 — Painel Administrativo com Autenticação
**Período:** 24/11/2025 – 07/12/2025 | **Status:** ✅ Concluído

### Objetivo
Desenvolver o painel administrativo protegido por credenciais, permitindo que gestores da unidade de saúde visualizem a fila, chamem o próximo paciente e resetem a fila por unidade.

### Histórias de Usuário
- **HU-006 (implementação):** O painel administrativo deve ser protegido por login (usuário e senha).
- **HU-016:** Como administrador, desejo filtrar a fila por unidade de saúde e chamar o próximo paciente da minha unidade.
- **HU-017:** Como administrador, desejo resetar a fila de uma unidade específica sem afetar as demais.

### Tarefas Realizadas
- Implementação da tela de autenticação com credenciais fixas (`admin` / `sus2025`) via `st.session_state`
- Desenvolvimento do painel de fila com: filtro por unidade de saúde, tabela de pacientes aguardando, contagem de vagas disponíveis e histórico de atendidos do dia
- Implementação do botão "Chamar Próximo" com lógica de chamar o primeiro da fila da unidade selecionada
- Implementação da função `resetar_fila_unidade(unidade)` para reset seletivo por unidade sem impactar as demais
- Definição da lista `TODAS_UNIDADES` fixa com as 10 unidades do sistema
- Adição do botão de logout para encerrar a sessão administrativa

### Funcionalidades do Painel Admin

| Funcionalidade | Descrição |
|---------------|-----------|
| Login | Autenticação por usuário e senha (admin/sus2025) |
| Dashboard | 5 indicadores: fila, atendidos, total, vagas livres, tempo médio |
| Filtro | Seletor de unidade com todas as 10 unidades sempre visíveis |
| Chamar próximo | Avança a fila da unidade selecionada |
| Remover paciente | Remove individualmente da fila |
| Reset por unidade | Limpa apenas a fila da unidade selecionada |
| Exportar CSV | Download da lista do dia com CPF mascarado |
| Auto-refresh | Atualização automática a cada 10 segundos |

### Entregáveis
- Painel administrativo com autenticação, filtro por unidade e controle de fila
- Reset seletivo por unidade implementado
- Histórico de atendidos do dia visível

### Retrospectiva
- **O que funcionou bem:** O painel simplificado atende bem ao caso de uso de recepcionistas com pouca familiaridade técnica
- **Pontos de melhoria:** Credenciais hardcoded são inadequadas para produção — a implementação de OAuth ou banco de usuários seria necessária em versão futura

---

## Sprint 9 — Avanço Automático de Fila e Ajuste de Parâmetros
**Período:** 08/12/2025 – 21/12/2025 | **Status:** ✅ Concluído

### Objetivo
Implementar o mecanismo de avanço automático da fila para simular o atendimento contínuo de pacientes, além de ajustar parâmetros do sistema com base em testes.

### Histórias de Usuário
- **HU-018:** Como sistema, devo avançar automaticamente a fila a cada 60 segundos para refletir o fluxo real de atendimentos.
- **HU-019:** Como sistema, devo não iniciar o timer de avanço automático até que o primeiro paciente entre na fila.

### Tarefas Realizadas
- Implementação da função `avancar_fila_automatico()` que verifica se decorreram 60 segundos desde o último avanço e, caso positivo, chama o próximo paciente
- Implementação de salvaguarda: o timer de avanço é reiniciado quando o primeiro paciente entra na fila (evitando que a fila "avance" para um paciente inexistente)
- **Ajuste do limiar de distância de check-in de 5 km para 10 km** com base em análise dos casos reais de deslocamento até as unidades de saúde em São Paulo
- Aprimoramento da lógica de geração de números únicos: uso de conjunto (`set`) para rastrear números em uso e garantir ausência de colisões mesmo com reinício cíclico
- Correção de bug de segurança de tipos: tratamento de valores `None` em variáveis de timestamp antes de comparações temporais

### Entregáveis
- Avanço automático de fila a cada 60 segundos em produção
- Distância máxima de check-in ajustada para 10 km
- Geração de números de senha sem colisão com rastreamento via conjunto

### Retrospectiva
- **O que funcionou bem:** O mecanismo de salvaguarda do timer evitou avanços prematuros durante testes
- **Lição aprendida:** Parâmetros como distância máxima e intervalo de avanço devem ser configuráveis via banco de dados em versão futura, em vez de fixos no código
