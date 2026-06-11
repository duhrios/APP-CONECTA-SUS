# Fase 4 — Segurança, Qualidade e Refinamento
**Sprints 10, 11, 12 e 13**
**Período:** 05/01/2026 – 01/03/2026

---

## Sprint 10 — Controle Anti-spam e Prevenção de Check-in Duplicado
**Período:** 05/01/2026 – 18/01/2026 | **Status:** ✅ Concluído

### Objetivo
Implementar mecanismos de segurança para prevenir abuso do sistema: limitação de tentativas de check-in por CPF/Cartão SUS e bloqueio de check-in duplicado na mesma unidade.

### Histórias de Usuário
- **HU-020:** Como sistema, devo bloquear um CPF/Cartão SUS que realize mais de 3 tentativas de check-in em menos de 60 minutos.
- **HU-021:** Como sistema, devo impedir que um paciente já na fila faça um segundo check-in na mesma unidade.

### Tarefas Realizadas
- Implementação da tabela `tentativas` no banco de dados para registro de todas as tentativas de check-in com timestamp
- Desenvolvimento da função `verificar_spam(cpf_sus)` que conta tentativas na janela de 60 minutos e retorna flag de bloqueio
- Implementação de `registrar_tentativa(cpf_sus)` chamada a cada submissão de formulário (mesmo em tentativas inválidas)
- Desenvolvimento de `ja_esta_na_fila(cpf_sus, unidade)` para verificar check-in duplicado antes de inserir na fila
- Integração das verificações anti-spam e anti-duplicação no fluxo de check-in, com mensagens de erro claras ao usuário
- Normalização do CPF/Cartão SUS com `_normalizar_cpf()`: remoção de pontuação e espaços antes de comparações no banco de dados

### Parâmetros de Segurança Implementados

| Regra | Valor |
|-------|-------|
| Tentativas máximas por CPF | 3 tentativas |
| Janela de tempo do bloqueio | 60 minutos |
| Escopo de check-in duplicado | Por CPF + unidade |
| Normalização | CPF/CNS sem pontuação para comparação |

### Entregáveis
- Rate limiting por CPF/CNS com janela de 60 minutos e máximo de 3 tentativas
- Bloqueio de check-in duplicado por unidade
- Normalização de CPF/CNS para comparações consistentes no banco

### Retrospectiva
- **O que funcionou bem:** A normalização antes do armazenamento preveniu inconsistências entre diferentes formatos de entrada do CPF
- **Desafio técnico:** Definir a janela de tempo adequada exigiu análise do fluxo real de atendimento (estimativa de que 60 minutos é tempo suficiente para um atendimento completo)

---

## Sprint 11 — Limpeza de Código e Refatoração
**Período:** 19/01/2026 – 01/02/2026 | **Status:** ✅ Concluído

### Objetivo
Realizar a limpeza do repositório, removendo arquivos desnecessários e refatorando trechos de código para maior clareza e manutenibilidade.

### Tarefas Realizadas
- Remoção de arquivos obsoletos do repositório: `shared_state.py` (gerenciamento de estado legado), `main.py` (entry point duplicado) e `zipFile.zip` (arquivo de build desnecessário)
- Correção do posicionamento da instrução `import time` para conformidade com PEP 8 (importações no início do arquivo)
- Revisão e padronização das mensagens de feedback ao usuário para linguagem clara e acessível
- Revisão dos textos da interface para adequação ao público-alvo (pacientes com diferentes níveis de letramento digital)
- Documentação inline do código com comentários explicativos nas funções principais

### Arquivos Removidos

| Arquivo | Motivo da remoção |
|---------|------------------|
| `shared_state.py` | Gerenciamento de estado legado — substituído pelo banco de dados |
| `main.py` | Entry point duplicado — `app.py` já cumpre a função |
| `zipFile.zip` | Arquivo de build desnecessário no repositório |

### Entregáveis
- Repositório limpo sem arquivos obsoletos
- Código refatorado e padronizado
- Documentação inline nas funções críticas

### Retrospectiva
- **O que funcionou bem:** A remoção de arquivos legados reduziu a confusão sobre quais módulos eram efetivamente utilizados
- **Lição aprendida:** A manutenção de um repositório limpo desde o início do projeto evitaria débito técnico acumulado

---

## Sprint 12 — Refinamento de Interface e Experiência do Usuário
**Período:** 02/02/2026 – 15/02/2026 | **Status:** ✅ Concluído

### Objetivo
Aprimorar a interface visual do sistema e a experiência geral do usuário, tornando o fluxo mais intuitivo para o público do SUS (perfil diversificado de idade e familiaridade tecnológica).

### Histórias de Usuário
- **HU-022:** Como paciente idoso, desejo que a interface seja simples, com textos legíveis e botões grandes.
- **HU-023:** Como paciente, desejo feedback visual claro sobre minha posição na fila e tempo estimado de espera.

### Tarefas Realizadas
- Aplicação de estilos CSS customizados via `st.markdown(..., unsafe_allow_html=True)` para:
  - Cards de informação com sombras e bordas arredondadas
  - Alertas coloridos (verde para sucesso, amarelo para aviso, vermelho para erro)
  - Tipografia de tamanho adequado para leitura em dispositivos móveis
- Implementação de animação `st.balloons()` na tela de chamada do paciente
- Melhoria da tela de fila: exibição do número da senha em destaque, posição na fila, contador de pessoas à frente e estimativa de espera em minutos
- Adição de ícones para reforço visual das mensagens (localização, confirmado, aguardando, cancelado)

### Alertas Visuais por Posição na Fila

| Posição | Visual | Mensagem |
|---------|--------|----------|
| > 3 | Info normal | Posição + tempo estimado de espera |
| 3 | Alerta vermelho | Verificação de proximidade (1 km obrigatório) |
| 2 | Aviso amarelo | "Vá agora para a recepção da unidade" |
| 1 | Card pulsante vermelho + countdown 60s | "Dirija-se imediatamente ao balcão!" |

### Entregáveis
- Interface visual aprimorada com componentes CSS customizados
- Feedback visual imediato em todas as etapas do fluxo
- Tela de fila com informações contextualizadas

### Retrospectiva
- **O que funcionou bem:** O uso de CSS inline dentro do Streamlit viabilizou customizações visuais sem necessidade de frameworks externos
- **Limitação identificada:** Streamlit impõe restrições ao DOM que dificultam customizações mais avançadas de layout

---

## Sprint 13 — Gestão de Fila por Unidade e Controles Administrativos Avançados
**Período:** 16/02/2026 – 01/03/2026 | **Status:** ✅ Concluído

### Objetivo
Aperfeiçoar o painel administrativo com controles mais granulares, garantindo que administradores possam gerenciar cada unidade de forma independente.

### Histórias de Usuário
- **HU-024:** Como administrador, desejo ver todas as 10 unidades no filtro, mesmo quando não há pacientes em alguma delas.
- **HU-025:** Como administrador, desejo resetar a fila de uma unidade específica sem afetar as demais unidades.

### Tarefas Realizadas
- Correção do filtro de unidades: substituição de filtro dinâmico (baseado apenas nas unidades com pacientes na fila) por lista fixa `TODAS_UNIDADES` contendo as 10 unidades cadastradas
- Correção do cálculo de vagas disponíveis: `vagas_livres` passou a usar o total global da fila, não apenas a contagem da unidade filtrada
- Refinamento da função `resetar_fila_unidade()`: o reset por unidade remove apenas os registros com status `'aguardando'` daquela unidade, preservando o histórico de atendidos e os dados de outras unidades
- Simplificação dos rótulos dos botões de controle para maior clareza operacional

### Entregáveis
- Painel administrativo com filtro completo das 10 unidades
- Reset seletivo por unidade corretamente isolado
- Contagem de vagas globalmente correta

### Retrospectiva
- **O que funcionou bem:** A separação entre "fila ativa" e "histórico" no banco de dados (campo `status`) viabilizou o reset seletivo sem perda de rastreabilidade
- **Decisão técnica:** Manter a lista de unidades em `admin.py` e `1_principal_paciente.py` é um débito técnico identificado — uma fonte única seria o ideal
