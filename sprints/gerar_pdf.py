from fpdf import FPDF
from fpdf.enums import XPos, YPos
from datetime import datetime

VERDE  = (10, 180, 160)
AZUL   = (37, 99, 235)
ESCURO = (15, 23, 42)
CINZA  = (100, 116, 139)
BRANCO = (255, 255, 255)
VERDE2 = (22, 163, 74)
BORDA  = (226, 232, 240)


class PDF(FPDF):
    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=18)

    def header(self):
        if self.page_no() == 1:
            return
        self.set_fill_color(*VERDE)
        self.rect(0, 0, 110, 10, style="F")
        self.set_fill_color(*AZUL)
        self.rect(110, 0, 100, 10, style="F")
        self.set_font("Helvetica", "B", 8)
        self.set_text_color(*BRANCO)
        self.set_xy(10, 1.5)
        self.cell(0, 7, "Conecta SUS - Documentacao de Sprints", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(4)

    def footer(self):
        if self.page_no() == 1:
            return
        self.set_y(-12)
        self.set_draw_color(*BORDA)
        self.line(10, self.get_y(), 200, self.get_y())
        self.set_font("Helvetica", "", 7)
        self.set_text_color(*CINZA)
        self.set_x(10)
        self.cell(90, 6, "Gerado em " + datetime.now().strftime("%d/%m/%Y %H:%M"), align="L")
        self.cell(90, 6, "Pagina " + str(self.page_no()), align="R", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    def capa(self):
        self.set_fill_color(*ESCURO)
        self.rect(0, 0, 210, 297, style="F")

        self.set_xy(30, 70)
        self.set_font("Helvetica", "B", 36)
        self.set_text_color(*VERDE)
        self.cell(150, 20, "Conecta SUS", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        self.set_x(30)
        self.set_font("Helvetica", "", 16)
        self.set_text_color(*BRANCO)
        self.cell(150, 12, "Documentacao de Sprints - Projeto", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        self.ln(8)
        self.set_draw_color(*VERDE)
        self.set_line_width(1.5)
        self.line(50, self.get_y(), 160, self.get_y())
        self.ln(10)

        self.set_x(30)
        self.set_font("Helvetica", "B", 14)
        self.set_text_color(148, 163, 184)
        self.cell(150, 10, "Sistema de Check-in para UBS - Sao Paulo", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        self.ln(20)
        sprint_labels = [
            ("S1", "Fundacao do Projeto"),
            ("S2", "Painel Admin e Correcoes"),
            ("S3", "Melhorias de UX na Fila"),
            ("S4", "Testes de Estresse"),
            ("S5", "Painel TV e Alerta Sonoro"),
        ]
        for num, titulo in sprint_labels:
            self.set_x(45)
            self.set_fill_color(30, 41, 59)
            self.set_draw_color(*VERDE)
            self.set_line_width(0.5)
            self.rect(45, self.get_y(), 120, 12, style="FD")
            self.set_xy(52, self.get_y() + 2)
            self.set_font("Helvetica", "B", 10)
            self.set_text_color(*VERDE)
            self.cell(18, 8, num)
            self.set_font("Helvetica", "", 10)
            self.set_text_color(*BRANCO)
            self.cell(100, 8, titulo, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            self.ln(2)

        self.set_xy(0, 260)
        self.set_font("Helvetica", "", 9)
        self.set_text_color(71, 85, 105)
        self.cell(210, 8, "Versao 1.0  |  " + datetime.now().strftime("%d/%m/%Y") + "  |  github.com/duhrios/APP-CONECTA-SUS", align="C")

    def sprint_header(self, numero, titulo):
        self.set_fill_color(*VERDE)
        self.rect(10, self.get_y(), 190, 1.5, style="F")
        self.ln(4)
        self.set_font("Helvetica", "B", 18)
        self.set_text_color(*ESCURO)
        self.cell(0, 10, numero, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_font("Helvetica", "", 13)
        self.set_text_color(*CINZA)
        self.cell(0, 7, titulo, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_fill_color(240, 253, 244)
        self.set_draw_color(187, 247, 208)
        self.set_font("Helvetica", "B", 9)
        self.set_text_color(*VERDE2)
        self.rect(10, self.get_y() + 2, 38, 7, style="FD")
        self.set_xy(10, self.get_y() + 3.5)
        self.cell(38, 4, "Concluida", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(5)

    def h2(self, text):
        self.set_font("Helvetica", "B", 12)
        self.set_text_color(*AZUL)
        self.set_fill_color(239, 246, 255)
        self.rect(10, self.get_y(), 190, 8, style="F")
        self.set_x(12)
        self.cell(0, 8, text, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(2)

    def h3(self, text):
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(*ESCURO)
        self.set_draw_color(*VERDE)
        self.set_line_width(0.6)
        y = self.get_y() + 4
        self.line(10, y, 16, y)
        self.set_xy(18, self.get_y())
        self.cell(0, 8, text, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(1)

    def body(self, text):
        self.set_font("Helvetica", "", 9.5)
        self.set_text_color(*ESCURO)
        self.set_x(10)
        self.multi_cell(190, 5.5, text)
        self.ln(1)

    def bullet(self, text):
        self.set_font("Helvetica", "", 9.5)
        self.set_text_color(*ESCURO)
        self.set_x(14)
        self.cell(5, 5.5, "-")
        self.set_x(19)
        self.multi_cell(181, 5.5, text)

    def code_block(self, text):
        self.set_fill_color(15, 23, 42)
        h = 5.5 * (text.count("\n") + 1) + 6
        self.rect(10, self.get_y(), 190, h, style="F")
        self.set_xy(13, self.get_y() + 3)
        self.set_font("Courier", "", 8)
        self.set_text_color(10, 180, 160)
        for line in text.split("\n"):
            self.set_x(13)
            self.cell(0, 5.5, line, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(3)

    def table(self, headers, rows, col_widths=None):
        if col_widths is None:
            w = 190 // len(headers)
            col_widths = [w] * len(headers)
        self.set_fill_color(*ESCURO)
        self.set_font("Helvetica", "B", 9)
        self.set_text_color(*BRANCO)
        self.set_x(10)
        for i, h in enumerate(headers):
            self.cell(col_widths[i], 7, h, border=0, fill=True)
        self.ln()
        for ri, row in enumerate(rows):
            fill_color = (248, 250, 252) if ri % 2 == 0 else BRANCO
            self.set_fill_color(*fill_color)
            self.set_font("Helvetica", "", 9)
            self.set_text_color(*ESCURO)
            self.set_x(10)
            for i, cell in enumerate(row):
                self.cell(col_widths[i], 6.5, str(cell), border=0, fill=True)
            self.ln()
        self.ln(3)

    def info_box(self, text, color="green"):
        if color == "green":
            self.set_fill_color(240, 253, 244)
            self.set_draw_color(187, 247, 208)
            self.set_text_color(21, 128, 61)
        else:
            self.set_fill_color(239, 246, 255)
            self.set_draw_color(191, 219, 254)
            self.set_text_color(29, 78, 216)
        self.set_font("Helvetica", "", 9.5)
        lines = text.split("\n")
        h = 5.5 * len(lines) + 6
        self.rect(10, self.get_y(), 190, h, style="FD")
        self.set_xy(14, self.get_y() + 3)
        for line in lines:
            self.set_x(14)
            self.cell(0, 5.5, line, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(3)


pdf = PDF()
pdf.set_margins(10, 14, 10)

# ── CAPA ─────────────────────────────────────────────────────────────────────
pdf.add_page()
pdf.capa()

# ── SPRINT 1 ──────────────────────────────────────────────────────────────────
pdf.add_page()
pdf.sprint_header("Sprint 1", "Fundacao do Projeto")

pdf.h2("Objetivo")
pdf.body(
    "Construir a base funcional do sistema de check-in digital para unidades de saude (UBS)\n"
    "de Sao Paulo, com fluxo completo do paciente e verificacao de proximidade geografica."
)

pdf.h2("Estrutura de Arquivos")
pdf.table(
    ["Arquivo", "Responsabilidade"],
    [
        ["app.py",                        "Pagina inicial e navegacao"],
        ["database.py",                   "Camada SQLite - fila, tentativas, config"],
        ["validators.py",                 "Validacao de CPF, Cartao SUS, nome, telefone"],
        ["shared_state.py",               "Gerenciamento de estado compartilhado"],
        ["pages/1_principal_paciente.py", "Fluxo principal do paciente (5 etapas)"],
    ],
    [80, 110],
)

pdf.h2("Fluxo Multi-etapa do Paciente")
pdf.table(
    ["Etapa", "Descricao"],
    [
        ["1 - Privacidade", "Aviso LGPD com consentimento explicito do paciente"],
        ["2 - Formulario",  "Nome, CPF/Cartao SUS, telefone, unidade de saude"],
        ["3 - Localizacao", "Verificacao GPS - maximo 10 km da unidade selecionada"],
        ["4 - Sintomas",    "Descricao livre dos principais sintomas (min. 5 chars)"],
        ["5 - Fila",        "Acompanhamento da posicao em tempo real"],
    ],
    [55, 135],
)

pdf.h2("Unidades de Saude Cadastradas (10 UBSs)")
pdf.table(
    ["Unidade", "Bairro / Regiao"],
    [
        ["UBS Valo Velho",                 "Valo Velho"],
        ["UBS Macedonia",                  "Macedonia"],
        ["UBS Parque Santo Antonio",       "Parque Santo Antonio"],
        ["UBS/AMA Parque Figueira Grande", "Figueira Grande"],
        ["UBS Jardim Maraca",              "Jardim Maraca"],
        ["UBS Santa Margarida",            "Santa Margarida"],
        ["UBS/AMA Capao Redondo",          "Capao Redondo"],
        ["UBS Jardim Germania",            "Jardim Germania"],
        ["UBS Sao Bento",                  "Sao Bento"],
        ["UBS Luar do Sertao",             "Luar do Sertao"],
    ],
    [100, 90],
)

pdf.h2("Seguranca e Validacoes")
for it in [
    "Anti-spam: bloqueio de CPF apos 3 tentativas em 60 minutos",
    "Sanitizacao de todos os campos contra injecao HTML/XSS",
    "Validacao matematica de CPF (dois digitos verificadores)",
    "Validacao de Cartao SUS (15 digitos)",
    "Verificacao de duplicidade na fila por CPF + unidade",
    "Verificacao de proximidade: 10 km no check-in, 1 km na posicao 3",
]:
    pdf.bullet(it)
pdf.ln(2)

pdf.h2("Banco de Dados SQLite")
pdf.table(
    ["Tabela", "Campos principais"],
    [
        ["fila",       "id, numero_chamado, nome, cpf_sus, unidade, sintomas, telefone, status"],
        ["tentativas", "id, cpf_sus, timestamp (anti-spam)"],
        ["config",     "chave, valor (proximo_numero, ultimo_avanco_fila)"],
    ],
    [40, 150],
)

pdf.h2("Metricas da Sprint")
pdf.table(
    ["Indicador", "Valor"],
    [
        ["Arquivos criados",        "6"],
        ["Etapas do fluxo",         "5"],
        ["Unidades cadastradas",    "10"],
        ["Validacoes implementadas","6"],
        ["Dependencias",            "3 (streamlit, geopy, streamlit-geolocation)"],
    ],
    [90, 100],
)

# ── SPRINT 2 ──────────────────────────────────────────────────────────────────
pdf.add_page()
pdf.sprint_header("Sprint 2", "Painel Admin e Correcoes de Estabilidade")

pdf.h2("Objetivo")
pdf.body(
    "Criar o painel administrativo para gestao da fila pelos funcionarios da unidade\n"
    "e corrigir o bug critico de crash do DOM na geolocalizacao."
)

pdf.h2("Painel Administrativo (pages/2_admin.py)")
pdf.h3("Dashboard de Estatisticas (5 indicadores)")
pdf.table(
    ["Indicador", "Descricao"],
    [
        ["Na fila agora",   "Total de pacientes aguardando atendimento"],
        ["Atendidos hoje",  "Total atendido no dia corrente"],
        ["Total do dia",    "Soma de atendidos + fila atual"],
        ["Vagas livres",    "Capacidade restante (de 100)"],
        ["Tempo medio",     "Media de espera calculada dos atendidos"],
    ],
    [50, 140],
)

pdf.h3("Funcionalidades Admin")
for it in [
    "Login com usuario/senha protegido por sessao (admin / sus2025)",
    "Filtro de fila por unidade de saude",
    "Botao Chamar proximo paciente por unidade",
    "Expansor com dados completos de cada paciente",
    "Remocao individual de pacientes da fila",
    "Reset total da fila (todas as unidades)",
    "Reset por unidade individual",
    "Exportacao de dados em CSV com CPF mascarado (charset UTF-8 BOM)",
    "Auto-refresh automatico a cada 10 segundos",
]:
    pdf.bullet(it)
pdf.ln(3)

pdf.h2("Correcao Critica: Bug RemoveChild")
pdf.body("O componente streamlit_geolocation causava erro fatal de DOM ao ser desmontado:")
pdf.code_block(
    'NotFoundError: Falha ao executar "removeChild" em "Node":\n'
    'O no a ser removido nao e filho deste no.'
)
pdf.h3("Causa raiz")
pdf.body(
    "O widget era renderizado e desmontado no mesmo ciclo de rerun do Streamlit,\n"
    "causando conflito no ciclo de vida do DOM do React."
)
pdf.h3("Solucao")
pdf.body(
    "Criada flag show_geo_widget no session_state. O widget so renderiza\n"
    "apos clique explicito do usuario, e e ocultado antes de qualquer rerun."
)
pdf.info_box("Resultado: crash completamente eliminado em todas as etapas do fluxo.", "green")

pdf.h2("Metricas da Sprint")
pdf.table(
    ["Indicador", "Valor"],
    [
        ["Arquivos criados",     "1 (pages/2_admin.py)"],
        ["Arquivos modificados", "1"],
        ["Bugs corrigidos",      "2 ocorrencias do removeChild"],
        ["Funcionalidades admin","9"],
        ["Linhas de codigo",     "~380"],
    ],
    [90, 100],
)

# ── SPRINT 3 ──────────────────────────────────────────────────────────────────
pdf.add_page()
pdf.sprint_header("Sprint 3", "Melhorias de UX na Fila")

pdf.h2("Objetivo")
pdf.body(
    "Melhorar a experiencia do paciente na etapa de espera com alertas visuais\n"
    "progressivos por posicao e corrigir dados que persistiam ao reiniciar o check-in."
)

pdf.h2("Sistema de Alertas por Posicao")
pdf.table(
    ["Posicao", "Tipo de alerta", "Descricao"],
    [
        ["1 (proximo)", "Card vermelho pulsante", "Contagem regressiva 60s + animacao CSS"],
        ["2",           "Aviso amarelo",          "Va agora para a recepcao da unidade"],
        ["3",           "Alerta vermelho",        "Exige estar a 1 km - cancelamento automatico"],
        ["> 3",         "Info normal",            "Posicao + tempo estimado de espera"],
    ],
    [32, 45, 113],
)

pdf.h3("Posicao 1 - Detalhes")
for it in [
    "Card vermelho com animacao CSS @keyframes pulse-border nos bordos",
    "Numero da senha em destaque (fonte 4.5rem, cor #dc2626)",
    "Anel de contagem regressiva de 60 segundos",
    "Atualizacao a cada 5 segundos (em vez dos 15s normais)",
    "Mensagem: Dirija-se imediatamente ao balcao!",
]:
    pdf.bullet(it)
pdf.ln(3)

pdf.h2("Ajuste de Frequencia de Refresh")
pdf.table(
    ["Situacao", "Antes", "Depois"],
    [
        ["Posicao 1",       "15 segundos", "5 segundos"],
        ["Demais posicoes", "15 segundos", "15 segundos"],
    ],
    [80, 55, 55],
)

pdf.h2("Correcao: Dados Persistindo ao Reiniciar")
pdf.body(
    "Problema: o campo telefone nao era apagado ao reiniciar o check-in,\n"
    "aparecendo pre-preenchido no proximo atendimento."
)
pdf.body(
    "Solucao: adicionadas as chaves 'telefone' e 'tempo_entrada_posicao_1'\n"
    "em todos os 3 pontos de limpeza do session_state."
)
pdf.info_box(
    "Os 3 handlers corrigidos:\n"
    "  1. Fazer novo check-in (apos ser chamado com sucesso)\n"
    "  2. Fazer novo check-in (apos cancelamento automatico)\n"
    "  3. Cancelar Check-in (cancelamento manual)",
    "blue",
)

pdf.h2("Metricas da Sprint")
pdf.table(
    ["Indicador", "Valor"],
    [
        ["Arquivos modificados",    "1"],
        ["Bugs corrigidos",         "1 (telefone persistindo)"],
        ["Novos estados de sessao", "1 (tempo_entrada_posicao_1)"],
        ["Animacoes CSS",           "2 (pulse-border + countdown-ring)"],
        ["Classes CSS novas",       "4"],
    ],
    [90, 100],
)

# ── SPRINT 4 ──────────────────────────────────────────────────────────────────
pdf.add_page()
pdf.sprint_header("Sprint 4", "Testes de Estresse e Validacao")

pdf.h2("Objetivo")
pdf.body(
    "Validar a robustez do sistema atraves de testes automatizados cobrindo todos os\n"
    "cenarios extremos: insercao massiva, limite de capacidade, wraparound e anti-spam."
)

pdf.h2("7 Fases de Teste Executadas")
pdf.table(
    ["Fase", "Cenario Testado", "Resultado"],
    [
        ["1", "Reset + 80 pacientes",                   "80 numeros unicos, range 1-100"],
        ["2", "Posicao e avanco manual de 10",           "Ordem e contagem corretas"],
        ["3", "Duplicata de CPF + bloqueio spam",        "Ambos detectados corretamente"],
        ["4", "Reset + 100 pacientes + 10 extras",      "Fila bloqueou no 101 paciente"],
        ["5", "Esvaziar 100 + reinserir 20 (wraparound)","Numeracao reinicia sem duplicatas"],
        ["6", "Remocao individual",                     "Posicoes reajustadas corretamente"],
        ["7", "Reset final + estado limpo",             "Primeiro paciente na posicao 1"],
    ],
    [10, 110, 70],
)

pdf.h2("Resultado Final")
pdf.info_box(
    "Total OK:     21 verificacoes\n"
    "Total avisos: 0\n"
    "Total erros:  0\n\n"
    "Nenhum erro critico encontrado em nenhum dos 180+ pacientes simulados.",
    "green",
)

pdf.h2("Comportamento do Sistema Confirmado")
pdf.table(
    ["Cenario", "Comportamento esperado", "Status"],
    [
        ["Fila de 100 pacientes",        "Numeracao 1-100 unica",          "OK"],
        ["Tentativa pos-limite",         "Retorna None",                   "OK"],
        ["Wraparound apos reset",        "Reinicia do 1",                  "OK"],
        ["CPF duplicado mesma unidade",  "Bloqueado",                      "OK"],
        ["3+ tentativas em 60min",       "Bloqueado por 1h",               "OK"],
        ["Remocao individual",           "Fila reajusta posicoes",         "OK"],
        ["Reset total",                  "Estado completamente limpo",     "OK"],
    ],
    [75, 75, 40],
)

pdf.h2("Metricas da Sprint")
pdf.table(
    ["Indicador", "Valor"],
    [
        ["Fases de teste",           "7"],
        ["Verificacoes automaticas", "21"],
        ["Pacientes simulados",      "180+ (80 + 100 + resets + wraparound)"],
        ["Erros encontrados",        "0"],
        ["Tempo de execucao",        "< 3 segundos"],
    ],
    [90, 100],
)

# ── SPRINT 5 ──────────────────────────────────────────────────────────────────
pdf.add_page()
pdf.sprint_header("Sprint 5", "Painel TV e Alerta Sonoro")

pdf.h2("Objetivo")
pdf.body(
    "Criar um painel de exibicao publica para monitores/TVs da recepcao, exibindo a senha\n"
    "chamada e a fila em tempo real, com alerta sonoro automatico a cada novo chamado."
)

pdf.h2("Painel TV (pages/3_painel.py)")
pdf.h3("Estrutura do Layout")
pdf.table(
    ["Area", "Conteudo"],
    [
        ["Topbar",          "Logo + nome do sistema + relogio HH:MM:SS + data"],
        ["Painel esquerdo", "Senha chamada em destaque (10rem) + animacao glow + unidade"],
        ["Painel direito",  "Proximas 8 senhas da fila com badges de posicao"],
        ["Footer",          "Nome do sistema + LGPD + aviso de atualizacao"],
    ],
    [45, 145],
)

pdf.h3("Configuracoes Tecnicas")
pdf.table(
    ["Configuracao", "Valor"],
    [
        ["Layout",          "Wide (100% da largura da tela)"],
        ["Tema",            "Dark - fundo #0f172a, alto contraste para TV"],
        ["Refresh",         "A cada 8 segundos automaticamente"],
        ["Senhas exibidas", "8 proximas na fila"],
        ["Sidebar",         "Oculta (display:none via CSS)"],
        ["Animacao",        "glow-pulse nos bordos da senha chamada"],
    ],
    [60, 130],
)

pdf.h2("Alerta Sonoro (Web Audio API)")
pdf.body(
    "Quando uma nova senha e chamada, o sistema toca automaticamente 3 tons\n"
    "ascendentes diretamente no navegador, sem arquivos de audio externos."
)
pdf.h3("Notas do Beep (3 tons ascendentes)")
pdf.table(
    ["Tom", "Frequencia", "Tempo", "Duracao"],
    [
        ["1 (La4)",  "880 Hz",  "0.00s", "0.18s"],
        ["2 (Do#5)", "1100 Hz", "0.22s", "0.18s"],
        ["3 (Mi5)",  "1320 Hz", "0.44s", "0.30s"],
    ],
    [40, 45, 40, 40],
)
pdf.body(
    "Mecanismo: compara o numero_chamado atual com o do refresh anterior\n"
    "(armazenado em session_state). Se diferente, dispara o audio via st.components.v1.html."
)

pdf.h2("Bug de Renderizacao HTML Resolvido")
pdf.body(
    "Problema: o parser Markdown do Streamlit trata linhas com 4+ espacos de indentacao\n"
    "como bloco de codigo, exibindo o HTML como texto literal."
)
pdf.body(
    "Solucao: todo HTML gerado em variaveis Python foi construido como string concatenada\n"
    "sem indentacao nas linhas, garantindo renderizacao correta pelo Streamlit."
)

pdf.h2("Navegacao Integrada")
pdf.bullet("Rodape do check-in: link 'Painel TV' abre em nova aba")
pdf.bullet("Painel Admin: botao 'Painel TV' na barra de acoes")
pdf.ln(3)

pdf.h2("Metricas da Sprint")
pdf.table(
    ["Indicador", "Valor"],
    [
        ["Arquivos criados",    "1 (pages/3_painel.py)"],
        ["Arquivos modificados","2 (check-in + admin)"],
        ["Linhas de codigo",    "~160"],
        ["Dependencias novas",  "0 (Web Audio API e nativa do navegador)"],
        ["Bugs resolvidos",     "1 (HTML com indentacao excessiva)"],
    ],
    [90, 100],
)

# ── Salvar ────────────────────────────────────────────────────────────────────
out = "sprints/Conecta_SUS_Sprints.pdf"
pdf.output(out)
print("PDF gerado: " + out)
