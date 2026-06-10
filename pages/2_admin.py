import streamlit as st
import csv
import io
import re
import time
from datetime import datetime
import database as db

TODAS_UNIDADES = [
    "UBS Valo Velho",
    "UBS Macedonia",
    "UBS Parque Santo Antonio",
    "UBS/AMA Parque Figueira Grande",
    "UBS Jardim Maracá",
    "UBS Santa Margarida",
    "UBS/AMA Capão Redondo",
    "UBS Jardim Germania",
    "UBS São Bento",
    "UBS Luar do Sertão",
]

st.set_page_config(page_title="Conecta SUS — Admin",
                   page_icon="🛡️",
                   layout="wide")

ADMIN_USER = "admin"
ADMIN_PASS = "sus2025"

# ── CSS Admin ──────────────────────────────────────────────────────────────────
st.markdown("""
<style>
  .stApp { background-color: #f1f5f9; }
  #MainMenu, footer, header { visibility: hidden; }

  h3 { color: #0f172a !important; font-weight: 800 !important; }
  .stSelectbox label { color: #0f172a !important; font-weight: 700 !important; font-size: 0.95rem !important; }

  .adm-header {
    display: flex; align-items: center; gap: 14px; margin-bottom: 28px;
  }
  .adm-logo {
    width: 52px; height: 52px; border-radius: 14px;
    background: linear-gradient(135deg, #0AB4A0, #2563EB);
    display: flex; align-items: center; justify-content: center; font-size: 24px;
    box-shadow: 0 4px 14px rgba(37,99,235,0.3);
  }
  .adm-title { font-size: 1.5rem; font-weight: 800; color: #1e293b; }
  .adm-sub   { font-size: 0.82rem; color: #64748b; }

  .stat-card {
    background: white; border-radius: 18px; padding: 20px 22px;
    box-shadow: 0 2px 12px rgba(15,23,42,0.08); border: 1px solid #f1f5f9;
  }
  .stat-value { font-size: 2.2rem; font-weight: 800; color: #1e293b; }
  .stat-label { font-size: 0.78rem; font-weight: 600; color: #64748b;
                text-transform: uppercase; letter-spacing: 0.8px; margin-top: 2px; }

  .queue-card {
    background: white; border-radius: 16px; padding: 16px 18px;
    border: 1px solid #e2e8f0; margin-bottom: 10px;
    display: flex; align-items: center; justify-content: space-between;
  }
  .queue-num {
    font-size: 1.5rem; font-weight: 900;
    background: linear-gradient(135deg, #0AB4A0, #2563EB);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    min-width: 64px;
  }
  .queue-name  { font-weight: 700; color: #1e293b; font-size: 0.95rem; }
  .queue-unit  { font-size: 0.78rem; color: #64748b; }
  .queue-pos   { font-size: 0.75rem; font-weight: 700; color: #94a3b8;
                 background: #f1f5f9; border-radius: 8px; padding: 2px 8px; }

  .badge-next {
    background: linear-gradient(90deg, #0AB4A0, #2563EB);
    color: white; border-radius: 10px; padding: 4px 10px;
    font-size: 0.7rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px;
  }

  .login-wrap { max-width: 380px; margin: 80px auto 0; }
  [data-testid="stForm"] {
    background: white !important; border-radius: 24px !important;
    box-shadow: 0 10px 40px rgba(15,23,42,0.10) !important;
    border: 1px solid #f1f5f9 !important; padding: 28px !important;
  }
  .stTextInput > div > div > input {
    border-radius: 12px !important; border-color: #e2e8f0 !important;
    height: 46px !important;
  }
  .stFormSubmitButton > button {
    width: 100% !important; height: 52px !important;
    border-radius: 14px !important; font-weight: 700 !important; font-size: 1rem !important;
    background: linear-gradient(90deg, #0AB4A0, #2563EB) !important;
    border: none !important; color: white !important;
    box-shadow: 0 4px 14px rgba(37,99,235,0.28) !important;
  }
</style>
""", unsafe_allow_html=True)

# ── Sessão de login ────────────────────────────────────────────────────────────
if "admin_logged_in" not in st.session_state:
    st.session_state.admin_logged_in = False

# ══════════════════════════════════════════════════════════════════════════════
# LOGIN
# ══════════════════════════════════════════════════════════════════════════════
if not st.session_state.admin_logged_in:
    st.markdown("""
    <div style="text-align:center; margin-bottom:32px; margin-top:60px">
      <div style="font-size:3rem; margin-bottom:8px">🛡️</div>
      <div style="font-size:1.5rem; font-weight:800; color:#1e293b">Área Restrita</div>
      <div style="font-size:0.85rem; color:#64748b; margin-top:4px">Acesso exclusivo para funcionários da UBS</div>
    </div>
    """, unsafe_allow_html=True)

    with st.form("login_form"):
        st.markdown('<p style="font-weight:600;color:#334155;margin-bottom:4px">Usuário</p>', unsafe_allow_html=True)
        usuario = st.text_input("Usuário", placeholder="admin", label_visibility="collapsed")
        st.markdown('<p style="font-weight:600;color:#334155;margin-bottom:4px;margin-top:8px">Senha</p>', unsafe_allow_html=True)
        senha = st.text_input("Senha", type="password", placeholder="••••••••", label_visibility="collapsed")
        entrar = st.form_submit_button("Entrar no painel →")

    if entrar:
        if usuario == ADMIN_USER and senha == ADMIN_PASS:
            st.session_state.admin_logged_in = True
            st.rerun()
        else:
            st.markdown('<div style="background:#fef2f2;border:1px solid #fecaca;border-radius:12px;padding:12px 16px;color:#dc2626;font-weight:600;text-align:center;margin-top:8px">Usuário ou senha incorretos.</div>', unsafe_allow_html=True)

    st.markdown('<div style="text-align:center;font-size:0.75rem;color:#94a3b8;margin-top:24px">Usuário padrão: <b>admin</b> &nbsp;·&nbsp; Senha: <b>sus2025</b></div>', unsafe_allow_html=True)

    st.markdown("""
    <div style="text-align:center; margin-top:16px">
      <a href="/principal_paciente" target="_self"
         style="display:inline-block; width:100%; max-width:340px;
                padding:14px 0; border-radius:14px; font-size:0.95rem; font-weight:700;
                background:#f1f5f9; border:1.5px solid #e2e8f0; color:#1e293b;
                text-decoration:none; text-align:center;">
        ← Voltar ao Check-in
      </a>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# ══════════════════════════════════════════════════════════════════════════════
# PAINEL ADMIN
# ══════════════════════════════════════════════════════════════════════════════

fila_global   = db.obter_fila()
atendidos_hoje = db.obter_atendidos()

# ── Cabeçalho ──────────────────────────────────────────────────────────────────
st.markdown("""
<div class="adm-header">
  <div class="adm-logo">🛡️</div>
  <div>
    <div class="adm-title">Conecta SUS — Painel Admin</div>
    <div class="adm-sub">Gestão de fila e atendimentos</div>
  </div>
</div>
""", unsafe_allow_html=True)

col_back, col_logout, col_reset = st.columns([2, 1, 1])
with col_back:
    if st.button("← Voltar ao Check-in", use_container_width=True):
        st.switch_page("pages/1_principal_paciente.py")
with col_logout:
    if st.button("🚪 Sair", key="logout", use_container_width=True):
        st.session_state.admin_logged_in = False
        st.rerun()
with col_reset:
    if st.button("🔄 Zerar tudo", key="resetar", use_container_width=True):
        db.resetar_fila()
        st.success("Fila geral zerada com sucesso!")
        st.rerun()

st.markdown("---")

# ── Filtro por unidade ─────────────────────────────────────────────────────────
filtro_opcoes = ["Todas as unidades"] + TODAS_UNIDADES
filtro = st.selectbox("🏥 Filtrar por unidade", filtro_opcoes, key="filtro_unidade")

fila_filtrada = fila_global if filtro == "Todas as unidades" else [
    p for p in fila_global if p["unidade"] == filtro
]
atendidos_filtrados = atendidos_hoje if filtro == "Todas as unidades" else [
    p for p in atendidos_hoje if p["unidade"] == filtro
]

# Botão de reset por unidade (aparece somente quando uma unidade está selecionada)
if filtro != "Todas as unidades":
    pacientes_na_unidade = len(fila_filtrada)
    col_info, col_btn_reset = st.columns([3, 1])
    with col_info:
        if pacientes_na_unidade > 0:
            st.markdown(
                f'<div style="background:#fffbeb;border:1px solid #fde68a;border-radius:12px;'
                f'padding:10px 14px;font-size:0.85rem;color:#92400e;font-weight:600">'
                f'⚠️ <strong>{pacientes_na_unidade}</strong> paciente(s) aguardando nesta unidade.</div>',
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                '<div style="background:#f0fdf4;border:1px solid #bbf7d0;border-radius:12px;'
                'padding:10px 14px;font-size:0.85rem;color:#15803d;font-weight:600">'
                '✅ Nenhum paciente na fila desta unidade.</div>',
                unsafe_allow_html=True
            )
    with col_btn_reset:
        if st.button("🗑️ Zerar esta unidade",
                     key="resetar_unidade", use_container_width=True,
                     disabled=(pacientes_na_unidade == 0)):
            db.resetar_fila_unidade(filtro)
            st.success(f"Fila da {filtro} zerada!")
            st.rerun()

st.markdown("---")

# ── Estatísticas ───────────────────────────────────────────────────────────────
total_fila      = len(fila_filtrada)
total_atendidos = len(atendidos_filtrados)
total_geral     = total_fila + total_atendidos
vagas_livres    = 100 - len(fila_global)

if total_atendidos > 1:
    tempos = []
    for p in atendidos_filtrados:
        if p.get("timestamp") and p.get("atendido_em"):
            delta = (p["atendido_em"] - p["timestamp"]).total_seconds() / 60
            if delta > 0:
                tempos.append(delta)
    tempo_medio = f"{sum(tempos)/len(tempos):.0f} min" if tempos else "—"
else:
    tempo_medio = "—"

c1, c2, c3, c4, c5 = st.columns(5)
with c1:
    st.markdown(f'<div class="stat-card"><div class="stat-value">{total_fila}</div><div class="stat-label">Na fila agora</div></div>', unsafe_allow_html=True)
with c2:
    st.markdown(f'<div class="stat-card"><div class="stat-value" style="color:#16a34a">{total_atendidos}</div><div class="stat-label">Atendidos hoje</div></div>', unsafe_allow_html=True)
with c3:
    st.markdown(f'<div class="stat-card"><div class="stat-value" style="color:#2563eb">{total_geral}</div><div class="stat-label">Total do dia</div></div>', unsafe_allow_html=True)
with c4:
    cor_vagas = "#dc2626" if vagas_livres <= 5 else "#0AB4A0"
    st.markdown(f'<div class="stat-card"><div class="stat-value" style="color:{cor_vagas}">{vagas_livres}</div><div class="stat-label">Vagas livres (de 100)</div></div>', unsafe_allow_html=True)
with c5:
    st.markdown(f'<div class="stat-card"><div class="stat-value" style="font-size:1.6rem">{tempo_medio}</div><div class="stat-label">Tempo médio</div></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Fila atual ─────────────────────────────────────────────────────────────────
col_fila, col_hist = st.columns([3, 2])

with col_fila:
    st.markdown(f"### 📋 Fila atual ({total_fila}/100 pacientes)")

    if not fila_filtrada:
        st.markdown('<div style="background:white;border-radius:16px;padding:32px;text-align:center;color:#0f172a;border:1px solid #e2e8f0;font-weight:600">Nenhum paciente na fila no momento.</div>', unsafe_allow_html=True)
    else:
        if st.button("📣 Chamar próximo paciente", type="primary", use_container_width=True):
            proximo = fila_filtrada[0]
            unidade_filtro = None if filtro == "Todas as unidades" else filtro
            db.chamar_proximo(unidade=unidade_filtro)
            st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)

        for i, paciente in enumerate(fila_filtrada):
            pos = i + 1
            is_next = pos == 1
            entrada = paciente.get("timestamp")
            espera = ""
            if entrada:
                mins = int((datetime.now() - entrada).total_seconds() // 60)
                espera = f"⏱ {mins} min aguardando"

            badge_html = (
                '<span class="badge-next">Próximo</span>'
                if is_next else
                f'<span class="queue-pos">{pos}º</span>'
            )

            st.markdown(f"""
            <div class="queue-card">
              <div class="queue-num">{paciente["numero_chamado"]:02d}</div>
              <div style="flex:1; padding: 0 16px">
                <div class="queue-name">{paciente["nome"]}</div>
                <div class="queue-unit">{paciente["unidade"]}</div>
                {f'<div style="font-size:0.75rem;color:#94a3b8;margin-top:2px">{espera}</div>' if espera else ''}
              </div>
              {badge_html}
            </div>
            """, unsafe_allow_html=True)

            with st.expander(f"Ver detalhes — senha {paciente['numero_chamado']:02d}"):
                st.markdown(f"**Nome:** {paciente['nome']}")
                st.markdown(f"**CPF/SUS:** {paciente['cpf_sus']}")
                if paciente.get("telefone"):
                    st.markdown(f"**Telefone:** {paciente['telefone']}")
                st.markdown(f"**Unidade:** {paciente['unidade']}")
                st.markdown(f"**Sintomas:** {paciente.get('sintomas', '—')}")
                if entrada:
                    st.markdown(f"**Entrada:** {entrada.strftime('%H:%M:%S')}")

                if st.button(f"🗑️ Remover da fila", key=f"rem_{paciente['numero_chamado']}"):
                    db.remover_da_fila(paciente["numero_chamado"])
                    st.rerun()

# ── Histórico de atendidos ──────────────────────────────────────────────────────
with col_hist:
    st.markdown(f"### ✅ Atendidos hoje ({total_atendidos})")

    if not atendidos_filtrados:
        st.markdown('<div style="background:white;border-radius:16px;padding:32px;text-align:center;color:#0f172a;border:1px solid #e2e8f0;font-weight:600">Nenhum atendimento registrado ainda.</div>', unsafe_allow_html=True)
    else:
        for paciente in atendidos_filtrados:
            atendido_em = paciente.get("atendido_em")
            horario = atendido_em.strftime("%H:%M") if atendido_em else "—"
            st.markdown(f"""
            <div style="background:white;border-radius:14px;padding:12px 16px;
                        border:1px solid #e2e8f0;margin-bottom:8px;
                        display:flex;align-items:center;gap:12px">
              <div style="font-size:1.2rem;font-weight:800;color:#16a34a;min-width:54px">{paciente["numero_chamado"]:02d}</div>
              <div style="flex:1">
                <div style="font-weight:700;color:#1e293b;font-size:0.9rem">{paciente["nome"]}</div>
                <div style="font-size:0.75rem;color:#64748b">{paciente["unidade"]}</div>
              </div>
              <div style="font-size:0.75rem;color:#94a3b8;background:#f8fafc;
                           border-radius:8px;padding:2px 8px">{horario}</div>
            </div>
            """, unsafe_allow_html=True)

    # Exportar CSV
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 📥 Exportar dados")

    todos_registros = atendidos_filtrados + fila_filtrada

    if todos_registros:
        def _mascarar_cpf(cpf: str) -> str:
            digitos = re.sub(r"\D", "", cpf or "")
            if len(digitos) == 11:
                return f"***.{digitos[3:6]}.***-{digitos[9:]}"
            return "***"

        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=[
            "numero_chamado", "nome", "cpf_sus", "unidade",
            "sintomas", "telefone", "timestamp", "atendido_em", "status"
        ])
        writer.writeheader()
        for p in todos_registros:
            writer.writerow({
                "numero_chamado": f"{p.get('numero_chamado', ''):02d}" if isinstance(p.get("numero_chamado"), int) else p.get("numero_chamado", ""),
                "nome":           p.get("nome", ""),
                "cpf_sus":        _mascarar_cpf(p.get("cpf_sus", "")),
                "unidade":        p.get("unidade", ""),
                "sintomas":       p.get("sintomas", ""),
                "telefone":       p.get("telefone", ""),
                "timestamp":      p["timestamp"].strftime("%Y-%m-%d %H:%M:%S") if p.get("timestamp") else "",
                "atendido_em":    p["atendido_em"].strftime("%Y-%m-%d %H:%M:%S") if p.get("atendido_em") else "",
                "status":         p.get("status", "aguardando"),
            })

        hoje = datetime.now().strftime("%Y-%m-%d")
        st.download_button(
            label="⬇️ Baixar CSV do dia",
            data=output.getvalue().encode("utf-8-sig"),
            file_name=f"atendimentos_{hoje}.csv",
            mime="text/csv",
            use_container_width=True,
        )
    else:
        st.markdown('<div style="color:#0f172a;font-size:0.85rem;font-weight:600">Nenhum registro para exportar.</div>', unsafe_allow_html=True)

# Auto-refresh a cada 10 segundos
time.sleep(10)
st.rerun()
