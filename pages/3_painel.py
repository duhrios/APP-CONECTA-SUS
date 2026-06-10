import time
import textwrap
import html as html_lib
from datetime import datetime
import streamlit as st
import database as db

st.set_page_config(
    page_title="Conecta SUS — Painel TV",
    page_icon="📺",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Remove padding e barra lateral
st.markdown("""
<style>
.stApp{background:#0f172a}
.block-container{padding:0!important;max-width:100%!important}
#MainMenu,footer,header,[data-testid="collapsedControl"],section[data-testid="stSidebar"]{display:none!important}
[data-testid="stMarkdownContainer"]{width:100%}
</style>
""", unsafe_allow_html=True)

# ── Dados ──────────────────────────────────────────────────────────────────────
fila      = db.obter_fila()
atendidos = db.obter_atendidos()
ultimo    = atendidos[0] if atendidos else None
agora     = datetime.now()
hora_str  = agora.strftime("%H:%M:%S")
data_str  = agora.strftime("%d/%m/%Y")
dias      = ["Segunda","Terça","Quarta","Quinta","Sexta","Sábado","Domingo"]
dia_str   = dias[agora.weekday()]
total     = len(fila)
proximas  = fila[:8]

# ── Painel esquerdo ────────────────────────────────────────────────────────────
if ultimo:
    num_str   = f"{ultimo['numero_chamado']:02d}"
    unid_esc  = html_lib.escape(ultimo.get("unidade", ""))
    atd_em    = ultimo.get("atendido_em")
    hora_chm  = atd_em.strftime("%H:%M") if atd_em else ""
    hora_html = f'<div style="font-size:.85rem;color:#334155;margin-top:12px">Chamado às {hora_chm}</div>' if hora_chm else ""
    left_html = (
        '<div class="tv-left">'
        '<div class="tv-chamando-label">🔔 &nbsp; Senha chamada</div>'
        '<div class="tv-senha-box">'
        f'<div class="tv-senha-number">{num_str}</div>'
        '<div class="tv-senha-sub">SENHA ATUAL</div>'
        '</div>'
        f'<div class="tv-unidade-badge">🏥 &nbsp; {unid_esc}</div>'
        '<div class="tv-instrucao">Dirija-se ao balcão de atendimento</div>'
        f'{hora_html}'
        '</div>'
    )
else:
    left_html = (
        '<div class="tv-left">'
        '<div style="font-size:4rem;margin-bottom:16px">📋</div>'
        '<div class="tv-vazia">Aguardando<br>primeira chamada</div>'
        '<div class="tv-instrucao" style="margin-top:24px">O painel atualiza automaticamente</div>'
        '</div>'
    )

# ── Próximas senhas ────────────────────────────────────────────────────────────
items = ""
if proximas:
    for i, p in enumerate(proximas):
        is1   = i == 0
        nq    = f"{p['numero_chamado']:02d}"
        nome  = html_lib.escape(p.get("nome","—").split()[0])
        unid  = html_lib.escape(p.get("unidade",""))
        icls  = "tv-queue-item first" if is1 else "tv-queue-item"
        ncls  = "tv-q-num first"      if is1 else "tv-q-num"
        badge = '<span class="tv-q-badge-next">Próximo</span>' if is1 else f'<span class="tv-q-badge-pos">{i+1}º</span>'
        items += (
            f'<div class="{icls}">'
            f'<div class="{ncls}">{nq}</div>'
            f'<div class="tv-q-info">'
            f'<div class="tv-q-name">{nome}</div>'
            f'<div class="tv-q-unit">{unid}</div>'
            '</div>'
            f'{badge}'
            '</div>'
        )
else:
    items = '<div style="color:#334155;font-size:1rem;font-weight:600;text-align:center;margin-top:48px;padding:30px">Fila vazia no momento</div>'

mais = f'<div style="font-size:.78rem;color:#334155;text-align:center;margin-top:14px;font-weight:600">+ {total-8} paciente(s) aguardando</div>' if total > 8 else ""

right_html = (
    '<div class="tv-right">'
    f'<div class="tv-right-title">📋 &nbsp; Próximas senhas ({total} aguardando)</div>'
    f'{items}'
    f'{mais}'
    '</div>'
)

# ── HTML principal (sem indentação nas variáveis) ──────────────────────────────
page = textwrap.dedent(f"""\
<style>
@keyframes glow-pulse{{0%,100%{{box-shadow:0 0 40px rgba(10,180,160,.2),0 0 0 1px rgba(10,180,160,.08)}}50%{{box-shadow:0 0 80px rgba(10,180,160,.4),0 0 0 1px rgba(10,180,160,.2)}}}}
.tv-topbar{{display:flex;align-items:center;justify-content:space-between;padding:18px 40px 14px;background:linear-gradient(90deg,#0AB4A0,#2563EB)}}
.tv-brand{{display:flex;align-items:center;gap:14px}}
.tv-brand-name{{font-size:1.7rem;font-weight:900;color:white;letter-spacing:-.5px}}
.tv-brand-sub{{font-size:.85rem;color:rgba(255,255,255,.80);font-weight:500}}
.tv-clock{{font-size:2rem;font-weight:800;color:white;letter-spacing:2px}}
.tv-date{{font-size:.85rem;color:rgba(255,255,255,.80);text-align:right;font-weight:500}}
.tv-body{{display:flex;width:100%;min-height:calc(100vh - 96px);background:#0f172a}}
.tv-left{{flex:1.35;display:flex;flex-direction:column;align-items:center;justify-content:center;background:#0f172a;padding:40px 30px;border-right:2px solid #1e293b}}
.tv-chamando-label{{font-size:1rem;font-weight:700;color:#0AB4A0;text-transform:uppercase;letter-spacing:4px;margin-bottom:12px}}
.tv-senha-box{{background:linear-gradient(135deg,#0f2a26,#0e1f3b);border:3px solid #0AB4A0;border-radius:32px;padding:36px 72px;text-align:center;animation:glow-pulse 2.4s ease-in-out infinite;margin-bottom:28px}}
.tv-senha-number{{font-size:10rem;font-weight:900;line-height:1;color:white;letter-spacing:-4px;text-shadow:0 0 40px rgba(10,180,160,.5)}}
.tv-senha-sub{{font-size:1rem;color:#94a3b8;font-weight:600;margin-top:6px;letter-spacing:1px}}
.tv-unidade-badge{{background:#1e293b;border:1px solid #334155;border-radius:50px;padding:10px 26px;font-size:1rem;font-weight:700;color:#e2e8f0;margin-bottom:20px}}
.tv-instrucao{{font-size:1.1rem;font-weight:600;color:#64748b;text-align:center}}
.tv-vazia{{font-size:2.2rem;font-weight:700;color:#334155;text-align:center}}
.tv-right{{flex:1;background:#0a1120;padding:32px 28px;display:flex;flex-direction:column}}
.tv-right-title{{font-size:.82rem;font-weight:700;color:#475569;text-transform:uppercase;letter-spacing:3px;margin-bottom:20px}}
.tv-queue-item{{display:flex;align-items:center;gap:20px;background:#1e293b;border-radius:16px;padding:16px 20px;margin-bottom:10px;border-left:4px solid #334155}}
.tv-queue-item.first{{background:linear-gradient(90deg,#0f2a26,#0f1f36);border-left-color:#0AB4A0;box-shadow:0 0 20px rgba(10,180,160,.15)}}
.tv-q-num{{font-size:2.4rem;font-weight:900;color:white;min-width:72px}}
.tv-q-num.first{{color:#0AB4A0}}
.tv-q-info{{flex:1}}
.tv-q-name{{font-size:.95rem;font-weight:700;color:#e2e8f0}}
.tv-q-unit{{font-size:.75rem;color:#475569;margin-top:2px}}
.tv-q-badge-next{{background:linear-gradient(90deg,#0AB4A0,#2563EB);color:white;border-radius:8px;padding:4px 12px;font-size:.65rem;font-weight:800;text-transform:uppercase;letter-spacing:.5px;white-space:nowrap}}
.tv-q-badge-pos{{font-size:.75rem;color:#475569;background:#0f172a;border-radius:8px;padding:4px 10px;font-weight:600}}
.tv-footer{{background:#0a1120;border-top:1px solid #1e293b;padding:10px 40px;font-size:.78rem;color:#334155;font-weight:500;text-align:center}}
</style>
<div class="tv-topbar">
<div class="tv-brand">
<div style="font-size:2.2rem;line-height:1">❤️</div>
<div>
<div class="tv-brand-name">Conecta SUS</div>
<div class="tv-brand-sub">Sistema de Atendimento — Painel de Senhas</div>
</div>
</div>
<div style="text-align:right">
<div class="tv-clock">{hora_str}</div>
<div class="tv-date">{dia_str}, {data_str}</div>
</div>
</div>
<div class="tv-body">
{left_html}
{right_html}
</div>
<div class="tv-footer">
Sistema Conecta SUS &nbsp;·&nbsp; Prefeitura de São Paulo &nbsp;·&nbsp; Dados protegidos pela LGPD &nbsp;·&nbsp; Atualização automática a cada 8 segundos
</div>
""")

st.markdown(page, unsafe_allow_html=True)

# Refresh automático a cada 8 segundos
time.sleep(8)
st.rerun()
