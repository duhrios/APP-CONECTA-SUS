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
LARANJA= (234, 88, 12)


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
        self.cell(0, 7, "Conecta SUS - Relatorio de Sprints | UNASP - Projeto Integrador", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
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
        # Title
        self.set_xy(20, 55)
        self.set_font("Helvetica", "B", 38)
        self.set_text_color(*VERDE)
        self.cell(170, 20, "Conecta SUS", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_x(20)
        self.set_font("Helvetica", "B", 16)
        self.set_text_color(*BRANCO)
        self.cell(170, 10, "Relatorio Completo de Sprints", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(4)
        self.set_draw_color(*VERDE)
        self.set_line_width(1.5)
        self.line(45, self.get_y(), 165, self.get_y())
        self.ln(8)
        # Info block
        self.set_x(20)
        self.set_font("Helvetica", "", 10)
        self.set_text_color(148, 163, 184)
        for line in [
            "Instituicao: UNASP",
            "Curso: Analise e Desenvolvimento de Sistemas",
            "Disciplina: Projeto Integrador",
            "Equipe: Eduardo Rios, Amanda de Jesus e Leonardo",
            "Periodo: Agosto/2025 a Junho/2026",
            "Metodologia: Scrum Adaptado para Equipes Academicas",
        ]:
            self.set_x(20)
            self.cell(170, 7, line, align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(8)
        # Sprint list
        sprints_info = [
            ("S0", "Concepcao e Kickoff",                   "04/08 - 17/08/2025"),
            ("S1", "Levantamento de Requisitos",            "18/08 - 31/08/2025"),
            ("S2", "Definicao de Arquitetura",              "01/09 - 14/09/2025"),
            ("S3", "MVP: Interface e Navegacao",            "15/09 - 28/09/2025"),
            ("S4", "Geolocalizacao e Proximidade",          "29/09 - 12/10/2025"),
            ("S5", "Sistema de Fila Virtual",               "13/10 - 26/10/2025"),
            ("S6", "Banco de Dados SQLite",                 "27/10 - 09/11/2025"),
            ("S7", "Validacao de Dados e LGPD",             "10/11 - 23/11/2025"),
            ("S8", "Painel Administrativo",                 "24/11 - 07/12/2025"),
            ("S9", "Avanco Automatico e Ajustes",           "08/12 - 21/12/2025"),
            ("S10","Controle Anti-spam",                    "05/01 - 18/01/2026"),
            ("S11","Refatoracao e Limpeza",                 "19/01 - 01/02/2026"),
            ("S12","Refinamento de Interface",              "02/02 - 15/02/2026"),
            ("S13","Gestao Administrativa Avancada",        "16/02 - 01/03/2026"),
            ("S14","Prototipagem de Design",                "02/03 - 15/03/2026"),
            ("S15","Deploy em Producao",                    "16/03 - 29/03/2026"),
            ("S16","Estabilizacao Pos-deploy",              "30/03 - 26/04/2026"),
            ("S17","Reducao de Debito Tecnico",             "27/04 - 10/05/2026"),
            ("S18","Correcao Critica + Entrega Final",      "11/05 - 10/06/2026"),
            ("S19","Painel TV para Recepcao",               "10/06/2026"),
            ("S20","Alerta Sonoro Automatico",              "10/06/2026"),
            ("S21","Testes de Estresse",                    "10/06/2026"),
        ]
        col_w = [14, 96, 60]
        for num, titulo, periodo in sprints_info:
            color = LARANJA if num in ("S19","S20","S21") else VERDE
            self.set_fill_color(22, 30, 46)
            self.set_draw_color(*color)
            self.set_line_width(0.4)
            self.rect(20, self.get_y(), 170, 8, style="FD")
            self.set_xy(22, self.get_y() + 1.5)
            self.set_font("Helvetica", "B", 8)
            self.set_text_color(*color)
            self.cell(col_w[0], 5, num)
            self.set_font("Helvetica", "", 8)
            self.set_text_color(*BRANCO)
            self.cell(col_w[1], 5, titulo)
            self.set_font("Helvetica", "", 7)
            self.set_text_color(100, 116, 139)
            self.cell(col_w[2], 5, periodo, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            self.ln(1)
        # Footer
        self.set_xy(0, 267)
        self.set_font("Helvetica", "", 8)
        self.set_text_color(71, 85, 105)
        self.cell(210, 6, "22 sprints  |  10 meses  |  github.com/duhrios/APP-CONECTA-SUS", align="C")

    # ── Helpers ──────────────────────────────────────────────────────────────

    def section_divider(self, fase_num, fase_titulo, periodo):
        self.set_fill_color(*ESCURO)
        self.rect(0, 0, 210, 297, style="F")
        self.set_xy(20, 110)
        self.set_font("Helvetica", "B", 11)
        self.set_text_color(*CINZA)
        self.cell(170, 8, "FASE " + str(fase_num), align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_x(20)
        self.set_font("Helvetica", "B", 26)
        self.set_text_color(*VERDE)
        self.multi_cell(170, 14, fase_titulo, align="C")
        self.set_x(20)
        self.set_font("Helvetica", "", 11)
        self.set_text_color(148, 163, 184)
        self.cell(170, 8, periodo, align="C")

    def sprint_header(self, numero, titulo, periodo, status="Concluido", cor=None):
        if cor is None:
            cor = VERDE
        self.set_fill_color(*cor)
        self.rect(10, self.get_y(), 190, 1.5, style="F")
        self.ln(4)
        self.set_font("Helvetica", "B", 16)
        self.set_text_color(*ESCURO)
        self.cell(0, 9, numero, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_font("Helvetica", "", 11)
        self.set_text_color(*CINZA)
        self.cell(0, 6, titulo, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_font("Helvetica", "", 9)
        self.set_text_color(*CINZA)
        self.cell(0, 6, "Periodo: " + periodo, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        # status badge
        self.set_fill_color(240, 253, 244)
        self.set_draw_color(187, 247, 208)
        self.set_font("Helvetica", "B", 8)
        self.set_text_color(*VERDE2)
        self.rect(10, self.get_y() + 2, 32, 6, style="FD")
        self.set_xy(10, self.get_y() + 3)
        self.cell(32, 4, status, align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(4)

    def h2(self, text):
        self.set_font("Helvetica", "B", 11)
        self.set_text_color(*AZUL)
        self.set_fill_color(239, 246, 255)
        self.rect(10, self.get_y(), 190, 7, style="F")
        self.set_x(12)
        self.cell(0, 7, text, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(1)

    def h3(self, text):
        self.set_font("Helvetica", "B", 9.5)
        self.set_text_color(*ESCURO)
        self.set_draw_color(*VERDE)
        self.set_line_width(0.5)
        y = self.get_y() + 3.5
        self.line(10, y, 15, y)
        self.set_xy(17, self.get_y())
        self.cell(0, 7, text, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    def body(self, text):
        self.set_font("Helvetica", "", 9)
        self.set_text_color(*ESCURO)
        self.set_x(10)
        self.multi_cell(190, 5, text)
        self.ln(1)

    def bullet(self, text):
        self.set_font("Helvetica", "", 9)
        self.set_text_color(*ESCURO)
        self.set_x(14)
        self.cell(4, 5, "-")
        self.set_x(18)
        self.multi_cell(182, 5, text)

    def code_block(self, text):
        lines = text.split("\n")
        h = 5 * len(lines) + 5
        self.set_fill_color(15, 23, 42)
        self.rect(10, self.get_y(), 190, h, style="F")
        self.set_xy(13, self.get_y() + 2.5)
        self.set_font("Courier", "", 7.5)
        self.set_text_color(10, 180, 160)
        for line in lines:
            self.set_x(13)
            self.cell(0, 5, line, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(2)

    def table(self, headers, rows, col_widths=None):
        if col_widths is None:
            w = 190 // len(headers)
            col_widths = [w] * len(headers)
        self.set_fill_color(*ESCURO)
        self.set_font("Helvetica", "B", 8.5)
        self.set_text_color(*BRANCO)
        self.set_x(10)
        for i, h in enumerate(headers):
            self.cell(col_widths[i], 6.5, h, border=0, fill=True)
        self.ln()
        for ri, row in enumerate(rows):
            fc = (248, 250, 252) if ri % 2 == 0 else BRANCO
            self.set_fill_color(*fc)
            self.set_font("Helvetica", "", 8.5)
            self.set_text_color(*ESCURO)
            self.set_x(10)
            for i, cell in enumerate(row):
                self.cell(col_widths[i], 6, str(cell), border=0, fill=True)
            self.ln()
        self.ln(2)

    def retro(self, items):
        """items = list of (label, text)"""
        for label, text in items:
            self.set_font("Helvetica", "B", 8.5)
            self.set_text_color(*AZUL)
            self.set_x(10)
            self.cell(0, 5.5, label, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            self.set_font("Helvetica", "", 8.5)
            self.set_text_color(*ESCURO)
            self.set_x(14)
            self.multi_cell(186, 5, text)
        self.ln(1)

    def info_box(self, text, color="green"):
        if color == "green":
            self.set_fill_color(240, 253, 244); self.set_draw_color(187, 247, 208); self.set_text_color(21, 128, 61)
        else:
            self.set_fill_color(239, 246, 255); self.set_draw_color(191, 219, 254); self.set_text_color(29, 78, 216)
        self.set_font("Helvetica", "", 9)
        lines = text.split("\n")
        h = 5 * len(lines) + 5
        self.rect(10, self.get_y(), 190, h, style="FD")
        self.set_xy(13, self.get_y() + 2.5)
        for line in lines:
            self.set_x(13)
            self.cell(0, 5, line, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(2)


# ══════════════════════════════════════════════════════════════════════════════
pdf = PDF()
pdf.set_margins(10, 14, 10)

# CAPA
pdf.add_page()
pdf.capa()

# ════════════════════════════════════════════════════════════════════════
# FASE 1
# ════════════════════════════════════════════════════════════════════════
pdf.add_page()
pdf.section_divider(1, "Concepcao, Requisitos\ne Arquitetura", "Sprints 0 a 2  |  04/08/2025 - 14/09/2025")

# --- Sprint 0 ---
pdf.add_page()
pdf.sprint_header("Sprint 0", "Concepcao e Kickoff do Projeto", "04/08/2025 - 17/08/2025")
pdf.h2("Objetivo")
pdf.body("Definir o escopo do projeto integrador, identificar o problema a ser resolvido e estabelecer o ambiente de trabalho colaborativo.")
pdf.h2("Contexto e Justificativa")
pdf.body("A problemática do sistema de saude publica brasileiro envolve filas presenciais extensas, ausencia de organizacao digital e exposicao desnecessaria de pacientes em ambientes hospitalares. O grupo identificou a oportunidade de propor uma solucao tecnologica acessivel, usando apenas um dispositivo movel com internet, eliminando filas fisicas para retirada de senhas.")
pdf.h2("Historias de Usuario Mapeadas")
pdf.bullet("HU-001: Como paciente, desejo realizar meu check-in remotamente para evitar aglomeracoes.")
pdf.bullet("HU-002: Como administrador, desejo visualizar a fila da minha unidade em tempo real.")
pdf.bullet("HU-003: Como paciente, desejo receber uma senha numerada e acompanhar minha posicao na fila.")
pdf.ln(2)
pdf.h2("Tarefas Realizadas")
for it in ["Definicao do tema e justificativa academica do projeto integrador",
           "Levantamento inicial do dominio de problema (SUS, check-in, filas hospitalares)",
           "Escolha da metodologia agil (Scrum adaptado) e ciclo de sprints de 14 dias",
           "Configuracao do ambiente de desenvolvimento no Replit",
           "Criacao do repositorio do projeto e primeiras configuracoes de ambiente Python"]:
    pdf.bullet(it)
pdf.ln(2)
pdf.h2("Entregaveis")
pdf.table(["Entregavel", "Descricao"],
          [["Documento de visao", "Product Vision Board com escopo e objetivos"],
           ["Backlog inicial", "Epicos identificados para as proximas sprints"],
           ["Ambiente configurado", "Replit + Python 3.11 + repositorio Git"]], [60, 130])
pdf.h2("Retrospectiva")
pdf.retro([("O que funcionou bem:", "Alinhamento rapido sobre o tema e tecnologias."),
           ("Pontos de melhoria:", "Necessidade de aprofundar o levantamento de requisitos com usuarios reais."),
           ("Decisao tecnica:", "Adocao do Streamlit como framework por sua curva de aprendizado reduzida.")])

# --- Sprint 1 ---
pdf.add_page()
pdf.sprint_header("Sprint 1", "Levantamento de Requisitos e Analise de Dominio", "18/08/2025 - 31/08/2025")
pdf.h2("Objetivo")
pdf.body("Realizar o levantamento detalhado de requisitos funcionais e nao funcionais, mapeando os fluxos de usuario e as regras de negocio do sistema de check-in.")
pdf.h2("Historias de Usuario")
pdf.bullet("HU-004: Como paciente, desejo selecionar minha unidade de saude dentre as disponiveis.")
pdf.bullet("HU-005: Como sistema, devo verificar se o paciente esta fisicamente proximo a unidade antes de autorizar o check-in.")
pdf.bullet("HU-006: Como administrador, desejo um painel protegido por autenticacao para gerir a fila.")
pdf.ln(2)
pdf.h2("Tarefas Realizadas")
for it in ["Identificacao das 10 unidades de saude reais de Sao Paulo (UBS, AMA, UPA) em Valo Velho, Macedonia, Capao Redondo e outros bairros",
           "Levantamento das coordenadas geograficas reais de cada unidade (latitude e longitude)",
           "Definicao do fluxo completo: consentimento LGPD -> formulario -> geolocalizacao -> sintomas -> fila -> chamada",
           "Mapeamento dos requisitos nao funcionais: privacidade LGPD, rate limiting, prevencao de check-in duplicado",
           "Analise das APIs de geolocalizacao disponiveis para aplicacoes web"]:
    pdf.bullet(it)
pdf.ln(2)
pdf.h2("Entregaveis")
pdf.table(["Entregavel", "Descricao"],
          [["Diagrama de fluxo", "Patient journey map do check-in completo"],
           ["Lista de unidades", "10 UBSs com coordenadas GPS reais levantadas em campo"],
           ["Requisitos documentados", "Funcionais e nao funcionais para todas as historias de usuario"]], [55, 135])
pdf.h2("Retrospectiva")
pdf.retro([("O que funcionou bem:", "Levantamento de dados reais de localizacao conferiu realismo ao prototipo."),
           ("Pontos de melhoria:", "Falta de acesso a usuarios reais do SUS para validacao dos requisitos."),
           ("Decisao tecnica:", "Uso de geopy para calculo de distancia geodesica entre coordenadas.")])

# --- Sprint 2 ---
pdf.add_page()
pdf.sprint_header("Sprint 2", "Definicao de Arquitetura e Estrutura Tecnica", "01/09/2025 - 14/09/2025")
pdf.h2("Objetivo")
pdf.body("Definir a arquitetura tecnica do sistema, selecionar as bibliotecas e estabelecer a estrutura de arquivos do projeto.")
pdf.h2("Estrutura de Arquivos Definida")
pdf.table(["Arquivo", "Responsabilidade"],
          [["app.py",                        "Entry point e navegacao"],
           ["database.py",                   "Camada SQLite - fila, tentativas, config"],
           ["validators.py",                 "Validacao de CPF, Cartao SUS, nome, telefone"],
           ["pages/1_principal_paciente.py", "Fluxo principal do paciente (5 etapas)"],
           ["pages/2_admin.py",              "Painel administrativo protegido"]], [80, 110])
pdf.h2("Decisoes Arquiteturais")
pdf.table(["Decisao", "Alternativa", "Justificativa"],
          [["Streamlit", "Flask+React, Django", "Menor complexidade, prototipagem rapida"],
           ["SQLite", "PostgreSQL, MongoDB", "Sem servidor externo; adequado para MVP"],
           ["session_state", "Banco em memoria", "Simplicidade para estado de sessao por usuario"]], [45, 55, 90])
pdf.h2("Modelo Relacional SQLite")
pdf.table(["Tabela", "Campos principais"],
          [["fila",       "numero_chamado, nome, cpf_sus, unidade, sintomas, timestamp, status"],
           ["config",     "chave, valor (proximo_numero, ultimo_avanco_fila)"],
           ["tentativas", "id, cpf_sus, timestamp (anti-spam)"]], [40, 150])
pdf.h2("Retrospectiva")
pdf.retro([("O que funcionou bem:", "Separacao clara de responsabilidades facilitou o desenvolvimento paralelo."),
           ("Pontos de melhoria:", "Ausencia de testes automatizados desde o inicio foi identificada como risco tecnico.")])

# ════════════════════════════════════════════════════════════════════════
# FASE 2
# ════════════════════════════════════════════════════════════════════════
pdf.add_page()
pdf.section_divider(2, "MVP: Interface, Geolocalizacao\ne Fila Virtual", "Sprints 3 a 5  |  15/09/2025 - 26/10/2025")

# --- Sprint 3 ---
pdf.add_page()
pdf.sprint_header("Sprint 3", "MVP: Interface do Paciente e Navegacao por Estagios", "15/09/2025 - 28/09/2025")
pdf.h2("Objetivo")
pdf.body("Desenvolver a interface basica do fluxo do paciente, implementando a navegacao por estagios e o formulario de check-in.")
pdf.h2("Historias de Usuario")
pdf.bullet("HU-007: Como paciente, desejo preencher um formulario com meu nome, CPF/Cartao SUS e selecionar minha unidade.")
pdf.bullet("HU-008: Como sistema, devo guiar o paciente por etapas sequenciais sem permitir que ele pule validacoes.")
pdf.ln(2)
pdf.h2("Estagios do Fluxo Implementados")
pdf.table(["Estagio", "Valor em session_state", "Descricao"],
          [["1 - Privacidade", "privacy",  "Aviso LGPD com consentimento explicito"],
           ["2 - Formulario",  "form",     "Nome, CPF/CNS, unidade de saude"],
           ["3 - Localizacao", "location", "Captura GPS e verificacao de proximidade"],
           ["4 - Sintomas",    "symptoms", "Descricao livre dos sintomas (min. 5 chars)"],
           ["5 - Fila",        "queue",    "Acompanhamento da posicao em tempo real"]], [35, 42, 113])
pdf.h2("Tarefas Realizadas")
for it in ["Implementacao do controle de fluxo por estagios via st.session_state.stage",
           "Desenvolvimento da tela de formulario com campos: nome, CPF/CNS, unidade",
           "Barra de progresso visual indicando etapas do processo",
           "Paleta visual com identidade inspirada no SUS (tons de azul e verde institucional)",
           "Layout responsivo com st.set_page_config(layout='wide')"]:
    pdf.bullet(it)
pdf.ln(2)
pdf.h2("Retrospectiva")
pdf.retro([("O que funcionou bem:", "O mecanismo de estagios mostrou-se robusto para controlar o fluxo linear."),
           ("Pontos de melhoria:", "A interface ainda carecia de validacoes de entrada e feedback ao usuario.")])

# --- Sprint 4 ---
pdf.add_page()
pdf.sprint_header("Sprint 4", "Geolocalizacao e Validacao de Proximidade Geografica", "29/09/2025 - 12/10/2025")
pdf.h2("Objetivo")
pdf.body("Implementar a captura de geolocalizacao do paciente via navegador e o calculo de distancia em relacao a unidade selecionada, bloqueando check-ins remotos.")
pdf.h2("Unidades de Saude Cadastradas (10 UBSs - Zona Sul SP)")
pdf.table(["Unidade", "Tipo", "Bairro"],
          [["UBS Valo Velho",                 "UBS",     "Valo Velho"],
           ["UBS Macedonia",                  "UBS",     "Macedonia"],
           ["UBS Parque Santo Antonio",       "UBS",     "Parque Santo Antonio"],
           ["UBS/AMA Parque Figueira Grande", "UBS/AMA", "Figueira Grande"],
           ["UBS Jardim Maraca",              "UBS",     "Jardim Maraca"],
           ["UBS Santa Margarida",            "UBS",     "Santa Margarida"],
           ["UBS/AMA Capao Redondo",          "UBS/AMA", "Capao Redondo"],
           ["UBS Jardim Germania",            "UBS",     "Jardim Germania"],
           ["UBS Sao Bento",                  "UBS",     "Sao Bento"],
           ["UBS Luar do Sertao",             "UBS",     "Luar do Sertao"]], [75, 30, 85])
pdf.h2("Tarefas Realizadas")
for it in ["Integracao do componente streamlit_geolocation para captura de GPS via browser",
           "Funcao calcular_distancia() usando geopy.distance.geodesic",
           "Cadastro das coordenadas reais das 10 unidades no dicionario UNIDADES_SAUDE",
           "Limiar inicial de distancia maxima: 5 km (ajustado para 10 km na Sprint 9)",
           "Tratamento de recusa de permissao de geolocalizacao pelo usuario"]:
    pdf.bullet(it)
pdf.ln(2)
pdf.h2("Retrospectiva")
pdf.retro([("O que funcionou bem:", "A biblioteca geopy demonstrou precisao adequada para distancias urbanas."),
           ("Pontos de melhoria:", "Necessidade de ajuste do limiar de distancia com base em testes com usuarios reais.")])

# --- Sprint 5 ---
pdf.add_page()
pdf.sprint_header("Sprint 5", "Sistema de Fila Virtual com Numeracao Sequencial", "13/10/2025 - 26/10/2025")
pdf.h2("Objetivo")
pdf.body("Implementar o sistema de gerenciamento de fila virtual com geração de senhas sequenciais, rastreamento de posicao em tempo real e exibicao para o paciente.")
pdf.h2("Historias de Usuario")
pdf.bullet("HU-003 (implementacao): Gerar senhas sequenciais de 1 a 50 e exibir posicao atual na fila.")
pdf.bullet("HU-010: Como paciente, desejo visualizar minha posicao e estimativa de tempo de espera.")
pdf.ln(2)
pdf.h2("Tarefas Realizadas")
for it in ["Algoritmo de senhas sequenciais 1-50 com reinicio ciclico ao atingir o limite",
           "Tela de acompanhamento: numero da senha, posicao, total na fila, estimativa de espera",
           "Atualizacao automatica a cada 15 segundos via time.sleep(15) + st.rerun()",
           "Tratamento de fila cheia: bloqueio de novos check-ins ao atingir 50 pacientes",
           "Funcao obter_posicao(numero_chamado): percorre a fila ordenada por timestamp"]:
    pdf.bullet(it)
pdf.ln(2)
pdf.h2("Retrospectiva")
pdf.retro([("O que funcionou bem:", "Logica sequencial de senhas e intuitiva para pacientes e recepcionistas."),
           ("Pontos de melhoria:", "Polling (sleep+rerun) e funcional mas nao ideal; WebSockets seriam mais eficientes.")])

# ════════════════════════════════════════════════════════════════════════
# FASE 3
# ════════════════════════════════════════════════════════════════════════
pdf.add_page()
pdf.section_divider(3, "Banco de Dados, LGPD,\nPainel Admin e Automacao", "Sprints 6 a 9  |  27/10/2025 - 21/12/2025")

# --- Sprint 6 ---
pdf.add_page()
pdf.sprint_header("Sprint 6", "Banco de Dados SQLite e Persistencia de Dados", "27/10/2025 - 09/11/2025")
pdf.h2("Objetivo")
pdf.body("Migrar a gestao de estado do session_state para um banco SQLite persistente, permitindo que multiplos usuarios compartilhem a mesma fila.")
pdf.h2("Historias de Usuario")
pdf.bullet("HU-011: O sistema deve armazenar os dados em banco para multiplos dispositivos acessarem o mesmo estado.")
pdf.bullet("HU-012: Os dados de fila devem persistir entre reinicializacoes da aplicacao.")
pdf.ln(2)
pdf.h2("Schema do Banco de Dados")
pdf.table(["Tabela", "Campos principais", "Finalidade"],
          [["fila",       "numero_chamado, nome, cpf_sus, unidade, sintomas, status, atendido_em", "Cada check-in"],
           ["config",     "chave, valor",                                                          "Configuracoes persistentes"],
           ["tentativas", "id, cpf_sus, timestamp",                                               "Anti-spam"]], [28, 110, 52])
pdf.h2("API de Acesso a Dados Implementada")
pdf.table(["Funcao", "Descricao"],
          [["adicionar_na_fila()", "Insere novo paciente com validacoes pre-insert"],
           ["obter_fila(unidade)", "Retorna fila ordenada por timestamp"],
           ["obter_posicao(numero)", "Retorna indice do paciente na fila"],
           ["chamar_proximo(unidade)", "Marca proximo como atendido e anonimiza dados"],
           ["remover_da_fila(id)", "Remove paciente individualmente"],
           ["resetar_fila(unidade)", "Remove todos os 'aguardando' da unidade"]], [60, 130])
pdf.h2("Retrospectiva")
pdf.retro([("O que funcionou bem:", "Modulo dedicado database.py facilitou a manutencao e testes."),
           ("Decisao tecnica:", "Padrao conn.row_factory = sqlite3.Row para acesso por nome de coluna.")])

# --- Sprint 7 ---
pdf.add_page()
pdf.sprint_header("Sprint 7", "Validacao de Dados e Conformidade com LGPD", "10/11/2025 - 23/11/2025")
pdf.h2("Objetivo")
pdf.body("Implementar validacoes de entrada para CPF e Cartao SUS, sanitizacao e aviso de privacidade conforme a LGPD.")
pdf.h2("Modulo validators.py - Funcoes Implementadas")
pdf.table(["Funcao", "Descricao"],
          [["validar_cpf(cpf)", "Algoritmo oficial de verificacao por digitos verificadores (modulo 11)"],
           ["validar_cartao_sus(numero)", "Validacao de 15 digitos numericos do Cartao Nacional de Saude"],
           ["validar_nome(nome)", "Nome completo: min 2 palavras, apenas letras e espacos"],
           ["sanitizar_entrada(texto)", "Remocao de caracteres maliciosos (prevencao de injecao HTML/XSS"]], [60, 130])
pdf.h2("Conformidade LGPD")
pdf.table(["Principio LGPD", "Implementacao"],
          [["Finalidade", "Aviso explicito de uso dos dados na tela de privacidade"],
           ["Adequacao", "Coleta apenas dos dados necessarios para o check-in"],
           ["Minimizacao", "Anonimizacao automatica apos atendimento (* DADO REMOVIDO *)"],
           ["Consentimento", "Checkbox de aceite obrigatorio antes do formulario"]], [60, 130])
pdf.h2("Retrospectiva")
pdf.retro([("O que funcionou bem:", "Anonimizacao automatica garante conformidade com minimizacao de dados da LGPD."),
           ("Desafio:", "CPFs com digitos repetidos (111.111.111-11) passam no formato mas sao invalidos - tratamento especial necessario.")])

# --- Sprint 8 ---
pdf.add_page()
pdf.sprint_header("Sprint 8", "Painel Administrativo com Autenticacao", "24/11/2025 - 07/12/2025")
pdf.h2("Objetivo")
pdf.body("Desenvolver o painel administrativo protegido por credenciais, permitindo gestores visualizarem a fila, chamarem o proximo e resetarem por unidade.")
pdf.h2("Funcionalidades do Painel Admin")
pdf.table(["Funcionalidade", "Descricao"],
          [["Login",          "Autenticacao usuario/senha (admin / sus2025)"],
           ["Dashboard",      "5 indicadores: fila, atendidos, total, vagas livres, tempo medio"],
           ["Filtro",         "Seletor de unidade com todas as 10 sempre visiveis"],
           ["Chamar proximo", "Avanca a fila da unidade selecionada"],
           ["Remover",        "Remove paciente individualmente da fila"],
           ["Reset",          "Limpa fila da unidade selecionada sem afetar as demais"],
           ["Exportar CSV",   "Download do dia com CPF mascarado (charset UTF-8 BOM)"],
           ["Auto-refresh",   "Atualizacao automatica a cada 10 segundos"]], [50, 140])
pdf.h2("Retrospectiva")
pdf.retro([("O que funcionou bem:", "Painel simplificado atende bem a recepcionistas com pouca familiaridade tecnica."),
           ("Pontos de melhoria:", "Credenciais hardcoded sao inadequadas para producao - OAuth seria necessario em versao futura.")])

# --- Sprint 9 ---
pdf.add_page()
pdf.sprint_header("Sprint 9", "Avanco Automatico de Fila e Ajuste de Parametros", "08/12/2025 - 21/12/2025")
pdf.h2("Objetivo")
pdf.body("Implementar o mecanismo de avanco automatico da fila para simular o atendimento continuo, alem de ajustar parametros com base em testes.")
pdf.h2("Historias de Usuario")
pdf.bullet("HU-018: Avanco automatico da fila a cada 60 segundos.")
pdf.bullet("HU-019: Timer nao inicia sem pacientes na fila.")
pdf.ln(2)
pdf.h2("Ajustes de Parametros")
pdf.table(["Parametro", "Valor anterior", "Novo valor", "Justificativa"],
          [["Distancia maxima de check-in", "5 km", "10 km", "Casos reais de deslocamento em Sao Paulo"],
           ["Intervalo de avanco automatico", "Manual", "60 segundos", "Simulacao do fluxo real de atendimento"],
           ["Geracao de numeros unicos", "Aleatorio", "Conjunto (set)", "Prevencao de colisoes no wraparound"]], [55, 30, 30, 75])
pdf.h2("Retrospectiva")
pdf.retro([("O que funcionou bem:", "Salvaguarda do timer evitou avancos prematuros durante testes."),
           ("Licao aprendida:", "Parametros como distancia maxima devem ser configuraveis via banco em versao futura.")])

# ════════════════════════════════════════════════════════════════════════
# FASE 4
# ════════════════════════════════════════════════════════════════════════
pdf.add_page()
pdf.section_divider(4, "Segurança, Qualidade\ne Refinamento", "Sprints 10 a 13  |  05/01/2026 - 01/03/2026")

# --- Sprint 10 ---
pdf.add_page()
pdf.sprint_header("Sprint 10", "Controle Anti-spam e Prevencao de Check-in Duplicado", "05/01/2026 - 18/01/2026")
pdf.h2("Objetivo")
pdf.body("Implementar mecanismos de seguranca contra abuso: limitacao de tentativas por CPF e bloqueio de check-in duplicado na mesma unidade.")
pdf.h2("Regras de Seguranca Implementadas")
pdf.table(["Regra", "Valor"],
          [["Tentativas maximas por CPF", "3 tentativas"],
           ["Janela de tempo do bloqueio", "60 minutos"],
           ["Escopo de duplicata", "Por CPF + unidade"],
           ["Normalizacao", "CPF/CNS sem pontuacao para comparacao"]], [90, 100])
pdf.h2("Funcoes de Seguranca")
pdf.table(["Funcao", "Descricao"],
          [["verificar_spam(cpf_sus)", "Conta tentativas na janela de 60 min e retorna flag de bloqueio"],
           ["registrar_tentativa(cpf_sus)", "Registra cada submissao (mesmo tentativas invalidas)"],
           ["ja_esta_na_fila(cpf, unidade)", "Verifica check-in duplicado antes de inserir"],
           ["_normalizar_cpf(cpf)", "Remove pontuacao e espacos para comparacoes consistentes"]], [60, 130])
pdf.h2("Retrospectiva")
pdf.retro([("O que funcionou bem:", "Normalizacao antes do armazenamento preveniu inconsistencias entre formatos de CPF."),
           ("Desafio tecnico:", "Definir 60 min como janela exigiu analise do fluxo real de atendimento.")])

# --- Sprint 11 ---
pdf.add_page()
pdf.sprint_header("Sprint 11", "Limpeza de Codigo e Refatoracao", "19/01/2026 - 01/02/2026")
pdf.h2("Objetivo")
pdf.body("Realizar limpeza do repositorio, removendo arquivos desnecessarios e refatorando trechos para maior clareza e manutenibilidade.")
pdf.h2("Arquivos Removidos")
pdf.table(["Arquivo", "Motivo da remocao"],
          [["shared_state.py", "Gerenciamento de estado legado - substituido pelo banco de dados"],
           ["main.py",         "Entry point duplicado - app.py ja cumpre a funcao"],
           ["zipFile.zip",     "Arquivo de build desnecessario no repositorio"]], [60, 130])
pdf.h2("Melhorias de Codigo")
for it in ["Correcao do posicionamento de 'import time' para conformidade com PEP 8",
           "Padronizacao das mensagens de feedback ao usuario para linguagem clara e acessivel",
           "Revisao dos textos da interface para adequacao ao publico-alvo (diferentes niveis de letramento)",
           "Documentacao inline nas funcoes principais"]:
    pdf.bullet(it)
pdf.ln(2)
pdf.h2("Retrospectiva")
pdf.retro([("O que funcionou bem:", "Remocao de arquivos legados reduziu confusao sobre quais modulos eram utilizados."),
           ("Licao aprendida:", "Repositorio limpo desde o inicio evitaria debito tecnico acumulado.")])

# --- Sprint 12 ---
pdf.add_page()
pdf.sprint_header("Sprint 12", "Refinamento de Interface e Experiencia do Usuario", "02/02/2026 - 15/02/2026")
pdf.h2("Objetivo")
pdf.body("Aprimorar a interface visual e a experiencia do usuario, tornando o fluxo mais intuitivo para o publico do SUS (perfil diversificado de idade e familiaridade tecnologica).")
pdf.h2("Alertas Visuais por Posicao na Fila")
pdf.table(["Posicao", "Visual", "Mensagem"],
          [["1 (proximo)", "Card vermelho pulsante + countdown 60s", "Dirija-se imediatamente ao balcao!"],
           ["2",           "Aviso amarelo",                         "Va agora para a recepcao da unidade"],
           ["3",           "Alerta vermelho",                       "Exige estar a 1 km - cancelamento automatico"],
           ["> 3",         "Info normal",                           "Posicao + tempo estimado de espera"]], [30, 60, 100])
pdf.h2("Tarefas Realizadas")
for it in ["CSS customizado: cards com sombras, alertas coloridos (verde/amarelo/vermelho), tipografia mobile",
           "Animacao st.balloons() na tela de chamada do paciente",
           "Numero da senha em destaque, posicao, contador a frente e estimativa em minutos",
           "Icones visuais para reforco das mensagens em cada estado do fluxo",
           "Animacao @keyframes pulse-border no card da posicao 1",
           "Refresh a cada 5s na posicao 1 (em vez dos 15s normais)"]:
    pdf.bullet(it)
pdf.ln(2)
pdf.h2("Retrospectiva")
pdf.retro([("O que funcionou bem:", "CSS inline no Streamlit viabilizou customizacoes visuais sem frameworks externos."),
           ("Limitacao:", "Streamlit impoe restricoes ao DOM que dificultam customizacoes mais avancadas.")])

# --- Sprint 13 ---
pdf.add_page()
pdf.sprint_header("Sprint 13", "Gestao de Fila por Unidade e Controles Administrativos", "16/02/2026 - 01/03/2026")
pdf.h2("Objetivo")
pdf.body("Aperfeicoar o painel administrativo com controles mais granulares, garantindo que administradores gerenciem cada unidade de forma independente.")
pdf.h2("Historias de Usuario")
pdf.bullet("HU-024: Ver todas as 10 unidades no filtro, mesmo sem pacientes em alguma delas.")
pdf.bullet("HU-025: Resetar fila de unidade especifica sem afetar as demais.")
pdf.ln(2)
pdf.h2("Correcoes Implementadas")
pdf.table(["Correcao", "Descricao"],
          [["Filtro dinamico -> lista fixa",  "Substituicao do filtro dinamico por TODAS_UNIDADES (10 fixas)"],
           ["Vagas livres incorretas",         "Calculo passou a usar total global da fila, nao apenas a unidade filtrada"],
           ["Reset seletivo",                  "Remove apenas status 'aguardando' da unidade, preserva historico"],
           ["Rotulos dos botoes",              "Simplificacao para maior clareza operacional"]], [55, 135])
pdf.h2("Retrospectiva")
pdf.retro([("O que funcionou bem:", "Campo status no banco viabilizou o reset seletivo sem perda de rastreabilidade."),
           ("Debito tecnico:", "Lista de unidades duplicada em admin.py e 1_principal_paciente.py - fonte unica seria ideal.")])

# ════════════════════════════════════════════════════════════════════════
# FASE 5
# ════════════════════════════════════════════════════════════════════════
pdf.add_page()
pdf.section_divider(5, "Design, Deploy em Producao\ne Entrega Final", "Sprints 14 a 18  |  02/03/2026 - 10/06/2026")

# --- Sprint 14 ---
pdf.add_page()
pdf.sprint_header("Sprint 14", "Exploracao de Design e Prototipagem de Alternativas Visuais", "02/03/2026 - 15/03/2026")
pdf.h2("Objetivo")
pdf.body("Explorar alternativas de design para a interface do paciente atraves de mockups interativos, avaliando diferentes linguagens visuais antes de escolher a definitiva.")
pdf.h2("Comparativo das Variantes")
pdf.table(["Variante", "Tom Visual", "Publico-alvo", "Resultado"],
          [["A - Limpo e Profissional", "Azul institucional",   "Geral/acessibilidade", "Nao escolhida"],
           ["B - Moderno Escuro",       "Dark, gradientes",     "Publico jovem",        "Nao escolhida"],
           ["C - Vibrante (escolhida)", "Verde+azul saturado",  "Todos os perfis",      "INTEGRADA"]], [50, 40, 40, 60])
pdf.h2("Retrospectiva")
pdf.retro([("O que funcionou bem:", "Comparacao side-by-side acelerou a tomada de decisao sobre identidade visual."),
           ("Licao aprendida:", "Prototipagem visual antes da implementacao final evita retrabalho significativo na UI.")])

# --- Sprint 15 ---
pdf.add_page()
pdf.sprint_header("Sprint 15", "Publicacao em Producao e Configuracao de Deploy", "16/03/2026 - 29/03/2026")
pdf.h2("Objetivo")
pdf.body("Realizar o primeiro deploy em producao, tornando a aplicacao acessivel publicamente via URL publica no Replit.")
pdf.h2("Checklist de Smoke Test em Producao")
pdf.table(["Funcionalidade", "Resultado"],
          [["Fluxo de check-in completo (5 etapas)", "Passou"],
           ["Geolocalizacao via navegador", "Passou"],
           ["Geracao e exibicao de senha na fila", "Passou"],
           ["Painel administrativo - login", "Passou"],
           ["Painel administrativo - chamar proximo", "Passou"],
           ["Persistencia do banco entre reinicializacoes", "Passou"]], [120, 70])
pdf.h2("Retrospectiva")
pdf.retro([("O que funcionou bem:", "Hospedagem no Replit simplificou significativamente o processo de deploy."),
           ("Desafio:", "SQLite em disco tem limitacoes de concorrencia para alta carga simultanea.")])

# --- Sprint 16 ---
pdf.add_page()
pdf.sprint_header("Sprint 16", "Estabilizacao Pos-deploy e Correcao de Bugs", "30/03/2026 - 26/04/2026")
pdf.h2("Objetivo")
pdf.body("Identificar e corrigir inconsistencias evidenciadas apos a publicacao em producao, estabilizando o sistema para uso continuo.")
pdf.h2("Bugs Corrigidos")
pdf.table(["Bug", "Impacto", "Correcao"],
          [["Vagas livres incorretas no filtro",     "Alto",  "Calculo usando total global"],
           ["Avanco automatico com timing incorreto", "Medio", "Validacao com timestamp do banco"],
           ["Mensagem de cancelamento pouco clara",   "Baixo", "Reescrita das mensagens de erro"],
           ["Geolocalizacao nao verificada posicao 3","Alto",  "Cancelamento explicito imediato"]], [70, 25, 95])
pdf.h2("Retrospectiva")
pdf.retro([("O que funcionou bem:", "Monitoramento de logs permitiu identificar bugs nao aparentes em desenvolvimento."),
           ("Licao aprendida:", "Testes em ambiente identico ao de producao teria antecipado esses bugs.")])

# --- Sprint 17 ---
pdf.add_page()
pdf.sprint_header("Sprint 17", "Otimizacao de Codigo e Reducao de Debito Tecnico", "27/04/2026 - 10/05/2026")
pdf.h2("Objetivo")
pdf.body("Reduzir o debito tecnico acumulado, melhorando a qualidade interna do codigo sem alterar o comportamento externo.")
pdf.h2("Padroes Tecnicos Consolidados")
pdf.table(["Padrao", "Regra"],
          [["Acesso ao banco",  "Sempre via get_conn() - nunca sqlite3.connect() diretamente"],
           ["Tratamento datas", "Sempre via _parse_dt() - nunca datetime.strptime() diretamente"],
           ["Thread-safety",    "Todas as escritas dentro do context manager com lock implicito"],
           ["Docstrings",       "Formato Google Style em todas as funcoes publicas"]], [50, 140])
pdf.h2("Retrospectiva")
pdf.retro([("O que funcionou bem:", "Context manager eliminou uma categoria inteira de bugs de conexoes abertas."),
           ("Decisao arquitetural:", "Toda escrita no banco deve passar por get_conn() - nunca diretamente.")])

# --- Sprint 18 ---
pdf.add_page()
pdf.sprint_header("Sprint 18", "Correcao Critica de Geolocalizacao e Entrega Final", "11/05/2026 - 10/06/2026")
pdf.h2("Objetivo")
pdf.body("Identificar, diagnosticar e corrigir definitivamente o bug critico de geolocalizacao que causava falha em producao, e entregar o projeto integrador em sua versao final estavel.")
pdf.h2("Diagnostico Tecnico do Bug")
pdf.body("O componente streamlit_geolocation apresentava incompatibilidade com o ciclo de rerenderizacao do Streamlit.\nO componente manipulava o DOM de forma assincrona: ao obter as coordenadas GPS, tentava atualizar nos\ndo DOM que o React ja havia removido - producindo a race condition NotFoundError: removeChild.")
pdf.h2("Solucao Implementada")
pdf.body("Substituicao completa por streamlit_js_eval, que executa o JavaScript dentro de um iframe oculto\ne retorna o resultado via mecanismo de componentes do Streamlit - eliminando o conflito com o React.")
pdf.code_block(
    "from streamlit_js_eval import streamlit_js_eval\n"
    "location = streamlit_js_eval(\n"
    "    js_expressions=\"\"\"await new Promise((resolve) => {\n"
    "        navigator.geolocation.getCurrentPosition(\n"
    "            (pos) => resolve({latitude: pos.coords.latitude,\n"
    "                             longitude: pos.coords.longitude}),\n"
    "            () => resolve(null), {enableHighAccuracy: true, timeout: 15000}\n"
    "        );\n"
    "    })\"\"\",\n"
    "    want_output=True, key=\"geo_location_capture\"\n"
    ")"
)
pdf.h2("Entregaveis Finais")
pdf.bullet("Bug critico de geolocalizacao corrigido em producao")
pdf.bullet("Arquitetura de captura de localizacao mais robusta com streamlit_js_eval")
pdf.bullet("Sistema estavel publicado para entrega do projeto integrador")
pdf.bullet("APP disponivel: https://sistema-sus--eduardo123rios.replit.app")
pdf.ln(2)
pdf.h2("Retrospectiva")
pdf.retro([("O que funcionou bem:", "Diagnostico sistematico: logs -> causa raiz -> solucao -> validacao."),
           ("Licao aprendida:", "Componentes de terceiros devem ser avaliados quanto a compatibilidade com rerun do Streamlit."),
           ("Decisao consolidada:", "streamlit_js_eval para APIs do navegador e preferivel a componentes que manipulam o DOM.")])

# ════════════════════════════════════════════════════════════════════════
# FASE 6 - POS-INTEGRACAO
# ════════════════════════════════════════════════════════════════════════
pdf.add_page()
pdf.set_fill_color(*ESCURO)
pdf.rect(0, 0, 210, 297, style="F")
pdf.set_xy(20, 100)
pdf.set_font("Helvetica", "B", 11)
pdf.set_text_color(*LARANJA)
pdf.cell(170, 8, "FASE 6 - POS-ENTREGA DO INTEGRADOR", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
pdf.set_x(20)
pdf.set_font("Helvetica", "B", 24)
pdf.set_text_color(*BRANCO)
pdf.multi_cell(170, 13, "Funcionalidades Adicionais para Operacao Real", align="C")
pdf.set_x(20)
pdf.set_font("Helvetica", "", 11)
pdf.set_text_color(148, 163, 184)
pdf.cell(170, 8, "Sprints 19 a 21  |  10/06/2026", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
pdf.ln(10)
pdf.set_x(20)
pdf.set_font("Helvetica", "", 9)
pdf.set_text_color(100, 116, 139)
pdf.multi_cell(170, 5.5,
    "Esta fase compreende as funcionalidades desenvolvidas apos a entrega do projeto integrador,\n"
    "com foco na operacao real das unidades de saude. Os itens abaixo constavam no Backlog de\n"
    "Versoes Futuras documentado na Sprint 18 e foram implementados em continuidade ao projeto.",
    align="C"
)

# --- Sprint 19 ---
pdf.add_page()
pdf.sprint_header("Sprint 19", "Painel TV para Recepcao com Exibicao em Tempo Real",
                  "10/06/2026", cor=LARANJA)
pdf.h2("Objetivo")
pdf.body("Criar um painel de exibicao publica para monitores/TVs da recepcao, mostrando a senha chamada e a fila em tempo real, com design otimizado para telas grandes.")
pdf.h2("Layout do Painel TV")
pdf.table(["Area", "Conteudo"],
          [["Topbar",          "Gradiente verde->azul + logo + relogio HH:MM:SS + data em portugues"],
           ["Painel esquerdo", "Senha atual (10rem) + animacao glow-pulse + unidade + horario"],
           ["Painel direito",  "Proximas 8 senhas com badges: PROXIMO, 2o, 3o..."],
           ["Footer",          "Nome do sistema + LGPD + aviso de atualizacao"]], [45, 145])
pdf.h2("Configuracoes Tecnicas")
pdf.table(["Configuracao", "Valor"],
          [["Layout",           "Wide (100% da largura da tela)"],
           ["Tema",             "Dark - fundo #0f172a, alto contraste para TV"],
           ["Refresh automatico","A cada 8 segundos"],
           ["Senhas exibidas",  "8 proximas na fila"],
           ["Sidebar",          "Oculta via CSS (display:none)"]], [60, 130])
pdf.h2("Bug de Renderizacao HTML Resolvido")
pdf.body("Problema: Streamlit trata linhas com 4+ espacos de indentacao como bloco de codigo.\nSolucao: HTML gerado em strings concatenadas sem indentacao, garantindo renderizacao correta.")
pdf.h2("Retrospectiva")
pdf.retro([("O que funcionou bem:", "CSS puro no Streamlit viabilizou layout TV de alta qualidade sem frameworks externos."),
           ("Licao aprendida:", "Parser Markdown do Streamlit tem comportamento nao-obvio com indentacao - documentado para referencia.")])

# --- Sprint 20 ---
pdf.add_page()
pdf.sprint_header("Sprint 20", "Alerta Sonoro Automatico para Novos Chamados",
                  "10/06/2026", cor=LARANJA)
pdf.h2("Objetivo")
pdf.body("Adicionar alerta sonoro automatico ao painel TV para notificacao imediata quando uma nova senha e chamada, sem depender de arquivos de audio externos.")
pdf.h2("Notas Musicais do Beep (3 tons ascendentes)")
pdf.table(["Tom", "Frequencia", "Inicio", "Duracao", "Volume"],
          [["1 - La4",  "880 Hz",  "0.00s", "0.18s", "0.35"],
           ["2 - Do#5", "1100 Hz", "0.22s", "0.18s", "0.35"],
           ["3 - Mi5",  "1320 Hz", "0.44s", "0.30s", "0.28"]], [32, 35, 30, 30, 30])
pdf.h2("Mecanismo de Deteccao")
pdf.code_block(
    "numero_atual = ultimo['numero_chamado'] if ultimo else None\n"
    "numero_prev  = st.session_state.get('painel_ultimo_numero')\n"
    "nova_senha   = (numero_atual is not None) and (numero_atual != numero_prev)\n"
    "st.session_state.painel_ultimo_numero = numero_atual\n"
    "if nova_senha:\n"
    "    components.html(BEEP_SCRIPT, height=0)  # Web Audio API"
)
pdf.h2("Restricao de Navegador")
pdf.body("A Web Audio API exige ao menos uma interacao do usuario com a pagina antes de reproduzir sons\n(restricao de seguranca de todos os navegadores modernos). Na pratica, o funcionario abre o painel\ne clica uma vez - apos isso, todos os chamados subsequentes terao som automatico.")
pdf.h2("Retrospectiva")
pdf.retro([("O que funcionou bem:", "Web Audio API nativa eliminou necessidade de servidores de audio ou arquivos externos."),
           ("Restricao de navegador:", "Politica de autoplay exige interacao previa - contornada com orientacao operacional.")])

# --- Sprint 21 ---
pdf.add_page()
pdf.sprint_header("Sprint 21", "Testes de Estresse e Validacao de Robustez",
                  "10/06/2026", cor=LARANJA)
pdf.h2("Objetivo")
pdf.body("Validar a robustez de toda a camada de banco de dados atraves de testes automatizados, cobrindo cenarios extremos antes da operacao real nas UBSs.")
pdf.h2("7 Fases de Teste")
pdf.table(["Fase", "Cenario", "Pacientes"],
          [["1", "Reset + 80 pacientes com numeracao unica",                  "80"],
           ["2", "Posicao e avanco manual de 10",                             "80"],
           ["3", "Duplicata de CPF + bloqueio anti-spam",                     "80"],
           ["4", "Reset + 100 pacientes + 10 extras (fila cheia)",            "100+"],
           ["5", "Esvaziar todos + wraparound (reinserir 20)",                "20"],
           ["6", "Remocao individual + verificacao de posicoes",              "20"],
           ["7", "Reset final + estado limpo + 1 paciente pos-reset",        "1"]], [10, 120, 60])
pdf.h2("Resultado Final")
pdf.info_box(
    "Total de verificacoes: 21\n"
    "Total OK:             21\n"
    "Total de avisos:       0\n"
    "Total de erros:        0\n\n"
    "Nenhum erro critico encontrado em nenhum dos 180+ pacientes simulados.",
    "green"
)
pdf.h2("Comportamento Validado")
pdf.table(["Cenario", "Resultado"],
          [["Fila de 100 pacientes - numeracao unica",   "Passou"],
           ["Tentativa apos limite - retorna None",      "Passou"],
           ["Wraparound apos reset - reinicia do 1",     "Passou"],
           ["CPF duplicado mesma unidade - bloqueado",   "Passou"],
           ["3+ tentativas em 60min - bloqueado 1h",     "Passou"],
           ["Remocao individual - posicoes reajustadas", "Passou"],
           ["Reset total - estado completamente limpo",  "Passou"]], [130, 60])
pdf.h2("Retrospectiva")
pdf.retro([("O que funcionou bem:", "Testes automatizados identificaram comportamentos de wraparound dificeis de validar manualmente."),
           ("Decisao:", "Wraparound (reiniciar do 1 apos reset) como comportamento padrao para UBSs com alta rotatividade.")])

# ── Resumo Final ─────────────────────────────────────────────────────────────
pdf.add_page()
pdf.h2("Resumo Consolidado - 22 Sprints")
pdf.table(["Sprint", "Periodo", "Foco Principal", "Status"],
          [["S0",  "04/08 - 17/08/2025", "Concepcao e Kickoff",              "OK"],
           ["S1",  "18/08 - 31/08/2025", "Levantamento de Requisitos",       "OK"],
           ["S2",  "01/09 - 14/09/2025", "Definicao de Arquitetura",         "OK"],
           ["S3",  "15/09 - 28/09/2025", "MVP: Interface e Navegacao",       "OK"],
           ["S4",  "29/09 - 12/10/2025", "Geolocalizacao e Proximidade",     "OK"],
           ["S5",  "13/10 - 26/10/2025", "Sistema de Fila Virtual",          "OK"],
           ["S6",  "27/10 - 09/11/2025", "Banco de Dados SQLite",            "OK"],
           ["S7",  "10/11 - 23/11/2025", "Validacao de Dados e LGPD",        "OK"],
           ["S8",  "24/11 - 07/12/2025", "Painel Administrativo",            "OK"],
           ["S9",  "08/12 - 21/12/2025", "Avanco Automatico e Ajustes",      "OK"],
           ["S10", "05/01 - 18/01/2026", "Controle Anti-spam",               "OK"],
           ["S11", "19/01 - 01/02/2026", "Refatoracao e Limpeza",            "OK"],
           ["S12", "02/02 - 15/02/2026", "Refinamento de Interface",         "OK"],
           ["S13", "16/02 - 01/03/2026", "Gestao Administrativa Avancada",   "OK"],
           ["S14", "02/03 - 15/03/2026", "Prototipagem de Design",           "OK"],
           ["S15", "16/03 - 29/03/2026", "Deploy em Producao",               "OK"],
           ["S16", "30/03 - 26/04/2026", "Estabilizacao Pos-deploy",         "OK"],
           ["S17", "27/04 - 10/05/2026", "Reducao de Debito Tecnico",        "OK"],
           ["S18", "11/05 - 10/06/2026", "Correcao Critica + Entrega Final", "OK"],
           ["S19", "10/06/2026",         "Painel TV para Recepcao",          "OK"],
           ["S20", "10/06/2026",         "Alerta Sonoro Automatico",         "OK"],
           ["S21", "10/06/2026",         "Testes de Estresse",               "OK"]], [15, 48, 95, 32])

pdf.ln(4)
pdf.h2("Metricas Gerais do Projeto")
pdf.table(["Metrica", "Valor"],
          [["Duracao total",                "10 meses (agosto/2025 - junho/2026)"],
           ["Total de sprints",             "22 (Sprint 0 a Sprint 21)"],
           ["Duracao media por sprint",     "2 semanas"],
           ["HU implementadas",             "23 de 25 levantadas"],
           ["Modulos Python",               "5 (app.py, database.py, validators.py, 1_principal_paciente.py, 2_admin.py, 3_painel.py)"],
           ["Unidades suportadas",          "10 UBSs, AMAs e UPAs na zona sul de Sao Paulo"],
           ["Capacidade da fila",           "50-100 pacientes simultaneos"],
           ["Rate limiting",                "3 tentativas por CPF em 60 minutos"],
           ["Distancia maxima check-in",    "10 km da unidade selecionada"],
           ["Refresh fila do paciente",     "15 segundos (5s na posicao 1)"],
           ["Refresh painel TV",            "8 segundos"],
           ["Avanco automatico",            "60 segundos"],
           ["Repositorio",                  "github.com/duhrios/APP-CONECTA-SUS"]], [65, 125])

# ── Output ─────────────────────────────────────────────────────────────────────
out = "sprints/Conecta_SUS_Sprints_Completo.pdf"
pdf.output(out)
print("PDF gerado: " + out)
