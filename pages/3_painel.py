import time
from datetime import datetime
import streamlit as st
import database as db

st.set_page_config(
    page_title="Conecta SUS — Painel",
    page_icon="📺",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
  /* ── Base ─────────────────────────────────────────────── */
  .stApp {
    background: #0f172a;
    min-height: 100vh;
  }
  .block-container {
    padding: 0 !important;
    max-width: 100% !important;
  }
  #MainMenu, footer, header,
  [data-testid="collapsedControl"],
  section[data-testid="stSidebar"] { display: none !important; }

  /* ── Topo ─────────────────────────────────────────────── */
  .tv-topbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 18px 40px 14px;
    background: linear-gradient(90deg, #0AB4A0 0%, #2563EB 100%);
  }
  .tv-brand {
    display: flex; align-items: center; gap: 14px;
  }
  .tv-brand-icon {
    font-size: 2.2rem; line-height: 1;
  }
  .tv-brand-name {
    font-size: 1.7rem; font-weight: 900;
    color: white; letter-spacing: -0.5px;
  }
  .tv-brand-sub {
    font-size: 0.85rem; color: rgba(255,255,255,0.80);
    font-weight: 500;
  }
  .tv-clock {
    font-size: 2rem; font-weight: 800;
    color: white; letter-spacing: 2px;
    font-variant-numeric: tabular-nums;
  }
  .tv-date {
    font-size: 0.85rem; color: rgba(255,255,255,0.80);
    text-align: right; font-weight: 500;
  }

  /* ── Corpo ────────────────────────────────────────────── */
  .tv-body {
    display: flex;
    gap: 0;
    min-height: calc(100vh - 92px);
  }

  /* ── Painel esquerdo — senha chamada ─────────────────── */
  .tv-left {
    flex: 1.3;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    background: #0f172a;
    padding: 40px 30px;
    border-right: 2px solid #1e293b;
  }
  .tv-chamando-label {
    font-size: 1rem; font-weight: 700;
    color: #0AB4A0; text-transform: uppercase;
    letter-spacing: 4px; margin-bottom: 12px;
  }
  .tv-senha-box {
    background: linear-gradient(135deg, #0f2a26, #0e1f3b);
    border: 3px solid #0AB4A0;
    border-radius: 32px;
    padding: 36px 60px;
    text-align: center;
    box-shadow: 0 0 60px rgba(10,180,160,0.25), 0 0 0 1px rgba(10,180,160,0.1);
    margin-bottom: 28px;
    animation: glow-pulse 2.4s ease-in-out infinite;
  }
  @keyframes glow-pulse {
    0%, 100% { box-shadow: 0 0 40px rgba(10,180,160,0.20), 0 0 0 1px rgba(10,180,160,0.08); }
    50%       { box-shadow: 0 0 80px rgba(10,180,160,0.40), 0 0 0 1px rgba(10,180,160,0.20); }
  }
  .tv-senha-number {
    font-size: 9rem; font-weight: 900;
    line-height: 1; color: white;
    letter-spacing: -4px;
    text-shadow: 0 0 40px rgba(10,180,160,0.5);
  }
  .tv-senha-sub {
    font-size: 1rem; color: #94a3b8;
    font-weight: 600; margin-top: 6px;
    letter-spacing: 1px;
  }
  .tv-unidade-badge {
    background: #1e293b;
    border: 1px solid #334155;
    border-radius: 50px;
    padding: 10px 26px;
    font-size: 1rem; font-weight: 700;
    color: #e2e8f0; letter-spacing: 0.3px;
    margin-bottom: 20px;
  }
  .tv-instrucao {
    font-size: 1.1rem; font-weight: 600;
    color: #64748b;
    text-align: center;
  }
  .tv-vazia {
    font-size: 2rem; font-weight: 700;
    color: #334155; text-align: center;
  }

  /* ── Painel direito — próximas senhas ───────────────── */
  .tv-right {
    flex: 1;
    background: #0a1120;
    padding: 32px 32px;
    display: flex;
    flex-direction: column;
  }
  .tv-right-title {
    font-size: 0.85rem; font-weight: 700;
    color: #475569; text-transform: uppercase;
    letter-spacing: 3px; margin-bottom: 20px;
  }
  .tv-queue-item {
    display: flex;
    align-items: center;
    gap: 20px;
    background: #1e293b;
    border-radius: 18px;
    padding: 18px 22px;
    margin-bottom: 12px;
    border-left: 4px solid #334155;
    transition: all 0.3s;
  }
  .tv-queue-item.first {
    background: linear-gradient(90deg, #0f2a26, #0f1f36);
    border-left-color: #0AB4A0;
    box-shadow: 0 0 20px rgba(10,180,160,0.15);
  }
  .tv-q-pos {
    font-size: 0.75rem; font-weight: 700;
    color: #475569; min-width: 28px;
    text-align: center;
  }
  .tv-q-num {
    font-size: 2.2rem; font-weight: 900;
    color: white; min-width: 72px;
    font-variant-numeric: tabular-nums;
  }
  .tv-q-num.first { color: #0AB4A0; }
  .tv-q-info {
    flex: 1;
  }
  .tv-q-name {
    font-size: 0.95rem; font-weight: 700; color: #e2e8f0;
  }
  .tv-q-unit {
    font-size: 0.75rem; color: #475569; margin-top: 2px;
  }
  .tv-q-badge-next {
    background: linear-gradient(90deg, #0AB4A0, #2563EB);
    color: white; border-radius: 8px;
    padding: 3px 10px; font-size: 0.65rem;
    font-weight: 800; text-transform: uppercase;
    letter-spacing: 0.5px; white-space: nowrap;
  }
  .tv-q-badge-pos {
    font-size: 0.75rem; color: #475569;
    background: #0f172a; border-radius: 8px;
    padding: 3px 10px; font-weight: 600;
  }

  /* ── Rodapé ───────────────────────────────────────────── */
  .tv-footer {
    background: #0a1120;
    border-top: 1px solid #1e293b;
    padding: 10px 40px;
    font-size: 0.78rem; color: #334155;
    font-weight: 500;
    text-align: center;
  }
</style>
""", unsafe_allow_html=True)

# ── Dados ──────────────────────────────────────────────────────────────────────
fila = db.obter_fila()
atendidos = db.obter_atendidos()

ultimo_chamado = atendidos[0] if atendidos else None

agora = datetime.now()
hora_str = agora.strftime("%H:%M:%S")
data_str = agora.strftime("%d/%m/%Y")
dia_semana = ["Segunda", "Terça", "Quarta", "Quinta",
              "Sexta", "Sábado", "Domingo"][agora.weekday()]

# ── Topo ───────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="tv-topbar">
  <div class="tv-brand">
    <div class="tv-brand-icon">❤️</div>
    <div>
      <div class="tv-brand-name">Conecta SUS</div>
      <div class="tv-brand-sub">Sistema de Atendimento — Painel de Senhas</div>
    </div>
  </div>
  <div style="text-align:right">
    <div class="tv-clock">{hora_str}</div>
    <div class="tv-date">{dia_semana}, {data_str}</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Corpo ───────────────────────────────────────────────────────────────────────
col_esq, col_dir = st.columns([1.35, 1], gap="small")

# ── Coluna esquerda: senha chamada ─────────────────────────────────────────────
with col_esq:
    if ultimo_chamado:
        num = f"{ultimo_chamado['numero_chamado']:02d}"
        unidade = ultimo_chamado.get("unidade", "")
        atendido_em = ultimo_chamado.get("atendido_em")
        hora_chamada = atendido_em.strftime("%H:%M") if atendido_em else ""

        st.markdown(f"""
        <div class="tv-left">
          <div class="tv-chamando-label">🔔 &nbsp; Senha chamada</div>
          <div class="tv-senha-box">
            <div class="tv-senha-number">{num}</div>
            <div class="tv-senha-sub">SENHA ATUAL</div>
          </div>
          <div class="tv-unidade-badge">🏥 &nbsp; {unidade}</div>
          <div class="tv-instrucao">Dirija-se ao balcão de atendimento</div>
          {f'<div style="font-size:0.8rem;color:#334155;margin-top:10px">Chamado às {hora_chamada}</div>' if hora_chamada else ''}
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="tv-left">
          <div class="tv-vazia">📋</div>
          <div class="tv-vazia" style="margin-top:16px">Aguardando<br>primeira chamada</div>
          <div class="tv-instrucao" style="margin-top:24px">O painel será atualizado automaticamente</div>
        </div>
        """, unsafe_allow_html=True)

# ── Coluna direita: próximas senhas ────────────────────────────────────────────
with col_dir:
    proximas = fila[:8]
    total_fila = len(fila)

    itens_html = ""
    if proximas:
        for i, p in enumerate(proximas):
            is_first = i == 0
            num_q = f"{p['numero_chamado']:02d}"
            nome = p.get("nome", "—").split()[0]
            unidade_q = p.get("unidade", "")
            pos_label = "PRÓXIMO" if is_first else f"{i + 1}º"
            item_class = "tv-queue-item first" if is_first else "tv-queue-item"
            num_class = "tv-q-num first" if is_first else "tv-q-num"
            badge = (
                '<span class="tv-q-badge-next">Próximo</span>'
                if is_first else
                f'<span class="tv-q-badge-pos">{i + 1}º</span>'
            )

            itens_html += f"""
            <div class="{item_class}">
              <div class="{num_class}">{num_q}</div>
              <div class="tv-q-info">
                <div class="tv-q-name">{nome}</div>
                <div class="tv-q-unit">{unidade_q}</div>
              </div>
              {badge}
            </div>
            """
    else:
        itens_html = """
        <div style="color:#334155; font-size:1rem; font-weight:600;
                    text-align:center; margin-top:40px; padding:30px">
          Fila vazia no momento
        </div>
        """

    rodape_fila = ""
    if total_fila > 8:
        rodape_fila = f"""
        <div style="font-size:0.78rem;color:#334155;text-align:center;
                    margin-top:14px;font-weight:600">
          + {total_fila - 8} paciente(s) aguardando
        </div>
        """

    st.markdown(f"""
    <div class="tv-right" style="min-height:calc(100vh - 92px)">
      <div class="tv-right-title">📋 &nbsp; Próximas senhas ({total_fila} aguardando)</div>
      {itens_html}
      {rodape_fila}
    </div>
    """, unsafe_allow_html=True)

# ── Rodapé ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="tv-footer">
  Sistema Conecta SUS &nbsp;·&nbsp; Prefeitura de São Paulo &nbsp;·&nbsp;
  Dados protegidos pela LGPD &nbsp;·&nbsp; Atualização automática a cada 8 segundos
</div>
""", unsafe_allow_html=True)

# Auto-refresh a cada 8 segundos
time.sleep(8)
st.rerun()
