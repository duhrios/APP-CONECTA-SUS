import time
import streamlit as st
from streamlit_geolocation import streamlit_geolocation
from geopy.distance import geodesic
from datetime import datetime, timedelta
import database as db
import validators as v
from validators import validar_telefone, formatar_telefone

st.set_page_config(page_title="Conecta SUS - Check-in",
                   page_icon="❤️",
                   layout="centered")

UNIDADES_SAUDE = {
    "UBS Valo Velho":             {"lat": -23.699849,  "lon": -46.801071},
    "UBS Macedonia":              {"lat": -23.6532318, "lon": -46.7902413},
    "UBS Parque Santo Antonio":   {"lat": -23.6570302, "lon": -46.7560585},
    "UBS/AMA Parque Figueira Grande": {"lat": -23.6790884, "lon": -46.7491433},
    "UBS Jardim Maracá":          {"lat": -23.6716433, "lon": -46.7727496},
    "UBS Santa Margarida":        {"lat": -23.6786990, "lon": -46.7554927},
    "UBS/AMA Capão Redondo":      {"lat": -23.6738223, "lon": -46.7738791},
    "UBS Jardim Germania":        {"lat": -23.6542119, "lon": -46.7597582},
    "UBS São Bento":              {"lat": -23.6856040, "lon": -46.7837911},
    "UBS Luar do Sertão":         {"lat": -23.6927286, "lon": -46.7943789},
}

if "stage" not in st.session_state:
    st.session_state.stage = "privacy"
if "numero_chamado" not in st.session_state:
    st.session_state.numero_chamado = None
if "tempo_entrada_posicao_3" not in st.session_state:
    st.session_state.tempo_entrada_posicao_3 = None
if "passou_posicao_3" not in st.session_state:
    st.session_state.passou_posicao_3 = False
if "privacy_accepted" not in st.session_state:
    st.session_state.privacy_accepted = False


def calcular_distancia(lat1, lon1, lat2, lon2):
    return geodesic((lat1, lon1), (lat2, lon2)).km


def verificar_cancelamento_automatico(numero_chamado, localizacao_atual):
    posicao = db.obter_posicao(numero_chamado)
    if posicao is None:
        return True, "Chamado não encontrado na fila."

    paciente = db.obter_paciente(numero_chamado)
    if not paciente:
        return True, "Dados do paciente não encontrados."

    if posicao == 3:
        if not localizacao_atual:
            return True, "Não foi possível obter sua localização. Você precisa estar na unidade (raio de 1 km) quando estiver na posição 3."

        unidade_coords = UNIDADES_SAUDE[paciente["unidade"]]
        distancia = calcular_distancia(
            localizacao_atual["latitude"], localizacao_atual["longitude"],
            unidade_coords["lat"], unidade_coords["lon"]
        )

        if distancia > 1.0:
            return True, f"Você está a {distancia:.2f} km da unidade. Você precisa estar num raio de 1 km quando estiver na posição 3."

        if not st.session_state.passou_posicao_3:
            st.session_state.passou_posicao_3 = True
            st.session_state.tempo_entrada_posicao_3 = datetime.now()

    if st.session_state.passou_posicao_3 and st.session_state.tempo_entrada_posicao_3:
        tempo_decorrido = datetime.now() - st.session_state.tempo_entrada_posicao_3
        total_na_fila = len(db.obter_fila())
        limite = timedelta(minutes=20) if total_na_fila <= 3 else timedelta(minutes=3)
        if tempo_decorrido > limite:
            minutos = 20 if total_na_fila <= 3 else 3
            return True, f"Chamado cancelado: passou mais de {minutos} minutos após a posição 3."

    return False, ""


# ── CSS ────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
  .stApp { background-color: #f8fafc; }
  .block-container { max-width: 480px !important; padding-top: 2rem; padding-bottom: 2rem; }

  .sus-header {
    display: flex; flex-direction: column; align-items: center;
    gap: 8px; margin-bottom: 24px;
  }
  .sus-logo {
    width: 68px; height: 68px; border-radius: 50%;
    background: linear-gradient(135deg, #0AB4A0, #2563EB);
    display: flex; align-items: center; justify-content: center;
    font-size: 32px; box-shadow: 0 8px 24px rgba(37,99,235,0.25);
  }
  .sus-title { font-size: 1.6rem; font-weight: 800; color: #1e293b; letter-spacing: -0.5px; }
  .sus-sub { font-size: 0.875rem; color: #64748b; font-weight: 500; }

  .sus-progress-bar {
    width: 100%; height: 5px; background: #e2e8f0;
    border-radius: 99px; margin-bottom: 20px; overflow: hidden;
  }
  .sus-progress-fill {
    height: 100%;
    background: linear-gradient(90deg, #0AB4A0, #2563EB);
    border-radius: 99px; transition: width 0.5s ease;
  }

  [data-testid="stForm"] {
    background: white !important; border-radius: 24px !important;
    box-shadow: 0 10px 40px rgba(15,23,42,0.10) !important;
    border: 1px solid #f1f5f9 !important; padding: 24px !important;
  }

  .sus-step-title { font-size: 1.2rem; font-weight: 700; color: #1e293b; margin-bottom: 4px; }
  .sus-step-sub { font-size: 0.85rem; color: #64748b; margin-bottom: 16px; }

  .sus-label {
    font-size: 0.85rem; font-weight: 600; color: #334155;
    display: flex; align-items: center; gap: 6px; margin-bottom: 6px;
  }

  .stTextInput > div > div > input,
  .stTextArea > div > div > textarea {
    border-radius: 12px !important; border-color: #e2e8f0 !important;
    height: 48px !important; font-size: 0.95rem !important;
  }
  .stTextInput > div > div > input:focus,
  .stTextArea > div > div > textarea:focus {
    border-color: #0AB4A0 !important;
    box-shadow: 0 0 0 3px rgba(10,180,160,0.15) !important;
  }
  .stSelectbox > div > div {
    border-radius: 12px !important; border-color: #e2e8f0 !important;
    min-height: 48px !important;
  }

  .stFormSubmitButton > button,
  .stButton > button[kind="primary"] {
    width: 100% !important; height: 56px !important;
    border-radius: 16px !important; font-size: 1.05rem !important; font-weight: 700 !important;
    background: linear-gradient(90deg, #0AB4A0, #2563EB) !important;
    border: none !important; color: white !important;
    box-shadow: 0 4px 16px rgba(37,99,235,0.30) !important;
  }
  .stFormSubmitButton > button:hover,
  .stButton > button[kind="primary"]:hover { opacity: 0.88 !important; }

  .stButton > button[kind="secondary"] {
    border-radius: 12px !important; border-color: #e2e8f0 !important;
    color: #475569 !important;
  }

  .sus-info-box {
    background: #f0fdf4; border: 1px solid #bbf7d0; border-radius: 16px;
    padding: 14px 16px; display: flex; gap: 10px; align-items: flex-start;
    font-size: 0.85rem; color: #15803d; font-weight: 500; line-height: 1.5; width: 100%;
  }
  .sus-alert {
    background: #fef2f2; border: 1px solid #fecaca; border-radius: 16px;
    padding: 14px 16px; font-size: 0.85rem; color: #dc2626; font-weight: 600; line-height: 1.5;
    margin-bottom: 12px;
  }
  .sus-warn {
    background: #fffbeb; border: 1px solid #fde68a; border-radius: 16px;
    padding: 14px 16px; font-size: 0.85rem; color: #92400e; font-weight: 500; line-height: 1.5;
    margin-bottom: 12px;
  }
  .sus-privacy {
    background: #f0f9ff; border: 1px solid #bae6fd; border-radius: 16px;
    padding: 16px 18px; font-size: 0.82rem; color: #0c4a6e; line-height: 1.7;
    margin-bottom: 16px;
  }

  .sus-footer { text-align: center; font-size: 0.78rem; color: #94a3b8; margin-top: 24px; }

  #MainMenu, footer, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)


def progress_bar(pct):
    st.markdown(f"""
    <div class="sus-progress-bar">
      <div class="sus-progress-fill" style="width:{pct}%"></div>
    </div>
    """, unsafe_allow_html=True)


st.markdown("""
<div class="sus-header">
  <div class="sus-logo">❤️</div>
  <div class="sus-title">Conecta SUS</div>
  <div class="sus-sub">Check-in rápido e humanizado</div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# ESTÁGIO: Aviso de Privacidade
# ══════════════════════════════════════════════════════════════════════════════
if st.session_state.stage == "privacy":
    progress_bar(10)

    st.markdown("""
    <div class="sus-step-title">🔒 Aviso de Privacidade</div>
    <div class="sus-step-sub">Leia antes de continuar.</div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="sus-privacy">
      <strong>Como usamos seus dados:</strong><br><br>
      • Seus dados (nome, CPF/Cartão SUS, unidade e sintomas) são coletados <strong>exclusivamente</strong> para organizar o atendimento nesta visita.<br><br>
      • As informações são apagadas automaticamente após o seu atendimento ser concluído.<br><br>
      • Seus dados <strong>não são compartilhados</strong> com terceiros nem armazenados permanentemente.<br><br>
      • A coleta de localização serve apenas para confirmar sua proximidade à unidade de saúde e <strong>não é salva</strong>.<br><br>
      • Ao continuar, você concorda com o uso temporário dessas informações para fins de atendimento no SUS, conforme a <strong>Lei Geral de Proteção de Dados (LGPD — Lei 13.709/2018)</strong>.
    </div>
    """, unsafe_allow_html=True)

    if st.button("✅ Entendi e aceito — Continuar", type="primary", use_container_width=True):
        st.session_state.privacy_accepted = True
        st.session_state.stage = "form"
        st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# ESTÁGIO: Formulário
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.stage == "form":
    progress_bar(30)

    st.markdown("""
    <div class="sus-step-title">Seus dados</div>
    <div class="sus-step-sub">Preencha para iniciar seu atendimento.</div>
    """, unsafe_allow_html=True)

    if db.fila_cheia():
        st.markdown('<div class="sus-alert">⚠️ A fila está cheia no momento (máximo 100 pacientes). Por favor, aguarde e tente novamente em instantes.</div>', unsafe_allow_html=True)
        st.stop()

    # Recupera dados já preenchidos anteriormente
    nome_salvo = st.session_state.get("nome_completo", "")
    cpf_salvo = st.session_state.get("cpf_sus", "")
    unidade_salva = st.session_state.get("unidade_selecionada", list(UNIDADES_SAUDE.keys())[0])
    voltando_para_trocar_unidade = bool(nome_salvo and cpf_salvo)

    if voltando_para_trocar_unidade:
        st.markdown(
            '<div class="sus-info-box">✅ Dados já salvos — apenas escolha uma unidade mais próxima de você.</div>',
            unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

    with st.form("form_cadastro"):
        st.markdown('<div class="sus-label">👤 Nome Completo</div>', unsafe_allow_html=True)
        nome_completo = st.text_input("Nome", value=nome_salvo, placeholder="Maria Silva", label_visibility="collapsed")

        st.markdown('<div class="sus-label">💳 CPF ou Cartão do SUS</div>', unsafe_allow_html=True)
        cpf_sus = st.text_input("CPF", value=cpf_salvo, placeholder="000.000.000-00 ou 15 dígitos do Cartão SUS", label_visibility="collapsed")

        st.markdown('<div class="sus-label">📱 Telefone (com DDD)</div>', unsafe_allow_html=True)
        telefone_salvo = st.session_state.get("telefone", "")
        telefone = st.text_input("Telefone", value=telefone_salvo, placeholder="(11) 98765-4321", label_visibility="collapsed")

        st.markdown('<div class="sus-label">🏥 Unidade de Saúde</div>', unsafe_allow_html=True)
        unidade_idx = list(UNIDADES_SAUDE.keys()).index(unidade_salva) if unidade_salva in UNIDADES_SAUDE else 0
        unidade_selecionada = st.selectbox("Unidade", options=list(UNIDADES_SAUDE.keys()), index=unidade_idx, label_visibility="collapsed")

        st.markdown('<div class="sus-label" style="margin-top:6px">📍 Localização</div>', unsafe_allow_html=True)
        st.markdown('<p style="font-size:0.85rem;color:#0f172a;margin:0">Clique em continuar para compartilhar sua localização atual</p>', unsafe_allow_html=True)

        submitted = st.form_submit_button("Confirmar Check-in →", type="primary", use_container_width=True)

    if submitted:
        erros = []

        nome_limpo = v.sanitizar(nome_completo, max_len=100)
        cpf_limpo = v.sanitizar(cpf_sus, max_len=20)
        tel_limpo = v.sanitizar(telefone, max_len=20)

        ok_nome, msg_nome = v.validar_nome(nome_limpo)
        if not ok_nome:
            erros.append(msg_nome)

        ok_cpf, msg_cpf = v.validar_campo_sus(cpf_limpo)
        if not ok_cpf:
            erros.append(msg_cpf)

        ok_tel, msg_tel = validar_telefone(tel_limpo)
        if not ok_tel:
            erros.append(msg_tel)

        if ok_cpf and not voltando_para_trocar_unidade:
            bloqueado, tentativas = db.verificar_spam(cpf_limpo)
            if bloqueado:
                erros.append(f"Muitas tentativas de check-in. Aguarde 1 hora antes de tentar novamente.")

        if ok_cpf and not erros:
            if db.ja_esta_na_fila(cpf_limpo, unidade_selecionada):
                erros.append("Você já está na fila desta unidade. Aguarde ser chamado.")

        if erros:
            for e in erros:
                st.markdown(f'<div class="sus-alert">⚠️ {e}</div>', unsafe_allow_html=True)
        else:
            if not voltando_para_trocar_unidade:
                db.registrar_tentativa(cpf_limpo)
            st.session_state.nome_completo = nome_limpo
            st.session_state.cpf_sus = cpf_limpo
            st.session_state.unidade_selecionada = unidade_selecionada
            st.session_state.telefone = formatar_telefone(tel_limpo)
            st.session_state.stage = "location"
            st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# ESTÁGIO: Localização
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.stage == "location":
    progress_bar(55)

    st.markdown("""
    <div class="sus-step-title">📍 Verificando localização</div>
    <div class="sus-step-sub">Você precisa estar a até 10 km da unidade selecionada.</div>
    """, unsafe_allow_html=True)

    geo_cache = st.session_state.get("geo_location_cache")

    # ── MODO: Aguardando GPS ───────────────────────────────────────────────────
    if geo_cache is None:
        st.markdown("""
        <div class="sus-warn">
          📡 Clique no botão abaixo e <strong>permita o acesso à localização</strong> quando o navegador solicitar.
        </div>
        """, unsafe_allow_html=True)

        location = streamlit_geolocation()

        if location and location.get("latitude") is not None:
            st.session_state.geo_location_cache = {
                "latitude": location["latitude"],
                "longitude": location["longitude"],
            }
            st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)

        unidade_coords = UNIDADES_SAUDE[st.session_state.get("unidade_selecionada", list(UNIDADES_SAUDE.keys())[0])]
        maps_url = f"https://www.google.com/maps/dir/?api=1&destination={unidade_coords['lat']},{unidade_coords['lon']}&travelmode=driving"
        st.markdown(
            f'<div style="text-align:center;margin-top:8px">'
            f'<a href="{maps_url}" target="_blank" '
            f'style="font-size:0.82rem;color:#0AB4A0;text-decoration:none;font-weight:600">'
            f'🗺️ Ver rota até a unidade no Maps</a></div>',
            unsafe_allow_html=True
        )

        col1, col2 = st.columns([3, 2])
        with col2:
            if st.button("← Voltar", use_container_width=True):
                st.session_state.stage = "form"
                st.rerun()

    # ── MODO: GPS capturado — validar distância ────────────────────────────────
    else:
        lat_usuario = geo_cache["latitude"]
        lon_usuario = geo_cache["longitude"]

        unidade_coords = UNIDADES_SAUDE[st.session_state.unidade_selecionada]
        distancia_km = calcular_distancia(lat_usuario, lon_usuario,
                                          unidade_coords["lat"], unidade_coords["lon"])

        if distancia_km > 10.0:
            st.markdown(
                f'<div class="sus-alert">📍 Você está a <strong>{distancia_km:.2f} km</strong> da unidade.<br>'
                f'A distância máxima permitida é de <strong>10 km</strong>. Aproxime-se para continuar.</div>',
                unsafe_allow_html=True)
            st.markdown('<div class="sus-warn">💡 Escolha uma unidade mais próxima de você ou tente capturar a localização novamente.</div>', unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            with col1:
                if st.button("🏥 Escolher outra unidade", use_container_width=True):
                    st.session_state.stage = "form"
                    st.session_state.pop("geo_location_cache", None)
                    st.rerun()
            with col2:
                if st.button("🔄 Tentar novamente", type="primary", use_container_width=True):
                    st.session_state.pop("geo_location_cache", None)
                    st.rerun()
        else:
            st.markdown(
                f'<div class="sus-info-box">✅ Localização confirmada — você está a <strong>{distancia_km:.2f} km</strong> da unidade. Distância válida!</div>',
                unsafe_allow_html=True)
            st.session_state.localizacao = {"latitude": lat_usuario, "longitude": lon_usuario}
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Continuar →", type="primary", use_container_width=True):
                st.session_state.stage = "symptoms"
                st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# ESTÁGIO: Sintomas
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.stage == "symptoms":
    progress_bar(80)

    st.markdown("""
    <div class="sus-step-title">🩺 O que você está sentindo?</div>
    <div class="sus-step-sub">Descreva brevemente seus sintomas principais.</div>
    """, unsafe_allow_html=True)

    st.markdown(f'<div style="font-size:0.85rem;color:#64748b;margin-bottom:8px">Paciente: <strong style="color:#1e293b">{st.session_state.nome_completo}</strong> &nbsp;·&nbsp; {st.session_state.unidade_selecionada}</div>', unsafe_allow_html=True)

    with st.form("form_sintomas"):
        sintomas = st.text_area("Sintomas", placeholder="Ex: dor de cabeça, febre há 2 dias, tosse...",
                                height=130, label_visibility="collapsed")
        submitted_sintomas = st.form_submit_button("✅ Confirmar Check-in", type="primary", use_container_width=True)

    if submitted_sintomas:
        sintomas_limpos = v.sanitizar(sintomas, max_len=500)
        if not sintomas_limpos or len(sintomas_limpos.strip()) < 5:
            st.markdown('<div class="sus-alert">Por favor, descreva seus sintomas antes de continuar (mínimo 5 caracteres).</div>', unsafe_allow_html=True)
        else:
            numero = db.adicionar_na_fila(
                nome=st.session_state.nome_completo,
                cpf_sus=st.session_state.cpf_sus,
                unidade=st.session_state.unidade_selecionada,
                sintomas=sintomas_limpos,
                telefone=st.session_state.get("telefone", ""),
            )
            if numero is None:
                st.markdown('<div class="sus-alert">⚠️ A fila está cheia (máximo 100 pacientes). Tente novamente em instantes.</div>', unsafe_allow_html=True)
            else:
                st.session_state.numero_chamado = numero
                st.session_state.stage = "queue"
                st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# ESTÁGIO: Fila
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.stage == "queue":
    progress_bar(100)

    chamado = db.avancar_fila_automatico()

    if chamado and chamado["numero_chamado"] == st.session_state.numero_chamado:
        st.markdown("""
        <div style="background:white;border-radius:24px;box-shadow:0 10px 40px rgba(15,23,42,0.10);
                    border:1px solid #f1f5f9;padding:24px;text-align:center;margin-bottom:16px">
          <p style="font-size:1.4rem;font-weight:800;color:#16a34a;margin:0">🎉 Você foi chamado!</p>
          <p style="font-size:0.9rem;color:#64748b;margin:8px 0 0">Dirija-se ao balcão de atendimento da unidade.</p>
        </div>
        """, unsafe_allow_html=True)
        st.balloons()
        if st.button("Fazer novo check-in", type="primary", use_container_width=True):
            for key in ["stage", "numero_chamado", "nome_completo", "cpf_sus",
                        "unidade_selecionada", "localizacao", "passou_posicao_3",
                        "tempo_entrada_posicao_3", "geo_location_cache", "geo_queue_cache"]:
                st.session_state.pop(key, None)
            st.rerun()
        st.stop()

    posicao_atual = db.obter_posicao(st.session_state.numero_chamado)
    localizacao_atual = st.session_state.get("geo_queue_cache")

    # Captura GPS na fila quando próximo de ser chamado
    if posicao_atual is not None and posicao_atual <= 4 and localizacao_atual is None:
        location_fila = streamlit_geolocation()
        if location_fila and location_fila.get("latitude") is not None:
            localizacao_atual = {
                "latitude": location_fila["latitude"],
                "longitude": location_fila["longitude"],
            }
            st.session_state.geo_queue_cache = localizacao_atual

    cancelado, motivo = verificar_cancelamento_automatico(
        st.session_state.numero_chamado, localizacao_atual)

    if cancelado:
        st.markdown(f"""
        <div style="background:white;border-radius:24px;box-shadow:0 10px 40px rgba(15,23,42,0.10);
                    border:1px solid #fecaca;padding:24px;text-align:center;margin-bottom:16px">
          <p style="font-size:1.2rem;font-weight:800;color:#dc2626;margin:0">🚫 Chamado Cancelado</p>
          <p style="font-size:0.85rem;color:#64748b;margin:8px 0 0">{motivo}</p>
        </div>
        """, unsafe_allow_html=True)
        db.remover_da_fila(st.session_state.numero_chamado)
        if st.button("Fazer novo check-in", type="primary", use_container_width=True):
            for key in ["stage", "numero_chamado", "nome_completo", "cpf_sus",
                        "unidade_selecionada", "localizacao", "passou_posicao_3",
                        "tempo_entrada_posicao_3", "geo_location_cache", "geo_queue_cache"]:
                st.session_state.pop(key, None)
            st.rerun()
    else:
        posicao = db.obter_posicao(st.session_state.numero_chamado)

        if posicao is None:
            st.markdown('<div class="sus-alert">Erro: chamado não encontrado na fila.</div>', unsafe_allow_html=True)
            if st.button("← Voltar ao início"):
                st.session_state.stage = "form"
                st.rerun()
        else:
            tempo_espera_min = max(1, (posicao - 1)) * 5
            primeiro_nome = st.session_state.nome_completo.split()[0]

            st.markdown(
                f'<div style="text-align:center;margin-bottom:12px">'
                f'<p style="font-size:1.2rem;font-weight:700;color:#1e293b;margin:0">Tudo certo, {primeiro_nome}!</p>'
                f'<p style="font-size:0.85rem;color:#64748b;margin:4px 0 0">Seu check-in foi realizado com sucesso.</p>'
                f'</div>',
                unsafe_allow_html=True
            )

            st.markdown(
                f'<div style="display:flex;flex-direction:column;align-items:center;margin:16px 0">'
                f'<div style="width:180px;height:180px;border-radius:50%;border:3px solid rgba(10,180,160,0.15);'
                f'display:flex;flex-direction:column;align-items:center;justify-content:center;'
                f'background:white;box-shadow:0 12px 40px rgba(37,99,235,0.18);">'
                f'<p style="font-size:0.7rem;font-weight:700;color:#94a3b8;text-transform:uppercase;'
                f'letter-spacing:1.5px;margin:0 0 2px">SUA SENHA</p>'
                f'<p style="font-size:3.8rem;font-weight:900;line-height:1;margin:0;color:#1e293b">'
                f'{st.session_state.numero_chamado:02d}</p>'
                f'</div></div>',
                unsafe_allow_html=True
            )

            col_a, col_b = st.columns(2)
            with col_a:
                st.markdown(
                    f'<div style="background:#f8fafc;border:1px solid #f1f5f9;border-radius:16px;'
                    f'padding:16px 12px;text-align:center">'
                    f'<p style="font-size:1.8rem;font-weight:800;color:#334155;margin:0">{posicao - 1}</p>'
                    f'<p style="font-size:0.65rem;font-weight:700;text-transform:uppercase;'
                    f'letter-spacing:1px;color:#94a3b8;margin:4px 0 0">PESSOAS NA FRENTE</p></div>',
                    unsafe_allow_html=True
                )
            with col_b:
                st.markdown(
                    f'<div style="background:#eff6ff;border:1px solid #dbeafe;border-radius:16px;'
                    f'padding:16px 12px;text-align:center">'
                    f'<p style="font-size:1.4rem;font-weight:800;color:#1d4ed8;margin:0">~{tempo_espera_min} min</p>'
                    f'<p style="font-size:0.65rem;font-weight:700;text-transform:uppercase;'
                    f'letter-spacing:1px;color:#3b82f6;margin:4px 0 0">TEMPO ESTIMADO</p></div>',
                    unsafe_allow_html=True
                )

            st.markdown("<br>", unsafe_allow_html=True)

            st.markdown(
                '<div style="background:#f0fdf4;border:1px solid #bbf7d0;border-radius:16px;'
                'padding:14px 16px;font-size:0.85rem;color:#15803d;font-weight:500;line-height:1.5">'
                '📋 Aguarde na recepção. Você será chamado em breve pelo painel.</div>',
                unsafe_allow_html=True
            )

            total_na_fila_agora = len(db.obter_fila())
            fila_pequena = total_na_fila_agora <= 3

            if posicao == 3:
                st.markdown('<div class="sus-alert">🚨 Você está na posição 3! Você DEVE estar num raio de 1 km da unidade, caso contrário seu chamado será cancelado.</div>', unsafe_allow_html=True)
                if fila_pequena:
                    if localizacao_atual:
                        unidade_coords_chk = UNIDADES_SAUDE[st.session_state.unidade_selecionada]
                        dist_chk = calcular_distancia(localizacao_atual["latitude"],
                                                      localizacao_atual["longitude"],
                                                      unidade_coords_chk["lat"],
                                                      unidade_coords_chk["lon"])
                        if dist_chk > 1.0:
                            st.markdown(
                                '<div class="sus-warn">⚠️ A fila está com poucas pessoas. Dirija-se à unidade agora — você precisa estar a menos de 1 km para não perder sua vez.</div>',
                                unsafe_allow_html=True)
                    else:
                        st.markdown(
                            '<div class="sus-warn">⚠️ A fila está com poucas pessoas. Dirija-se à unidade agora para não perder sua vez.</div>',
                            unsafe_allow_html=True)
            elif posicao <= 3:
                st.markdown('<div class="sus-warn">⚡ Você está próximo de ser chamado! Certifique-se de estar na unidade.</div>', unsafe_allow_html=True)

            if st.session_state.passou_posicao_3 and st.session_state.tempo_entrada_posicao_3 and not fila_pequena:
                tempo_restante = timedelta(minutes=3) - (datetime.now() - st.session_state.tempo_entrada_posicao_3)
                if tempo_restante.total_seconds() > 0:
                    minutos = int(tempo_restante.total_seconds() // 60)
                    segundos = int(tempo_restante.total_seconds() % 60)
                    st.markdown(f'<div class="sus-warn">⏱️ Tempo restante: {minutos}m {segundos}s para chegar à unidade.</div>', unsafe_allow_html=True)

            if localizacao_atual:
                unidade_coords = UNIDADES_SAUDE[st.session_state.unidade_selecionada]
                distancia_atual = calcular_distancia(localizacao_atual["latitude"],
                                                     localizacao_atual["longitude"],
                                                     unidade_coords["lat"],
                                                     unidade_coords["lon"])
                st.markdown(f'<div style="font-size:0.8rem;color:#64748b;text-align:center;margin-bottom:8px">📍 Distância atual da unidade: <strong>{distancia_atual:.2f} km</strong></div>', unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("❌ Cancelar Check-in", use_container_width=True):
                db.remover_da_fila(st.session_state.numero_chamado)
                for key in ["stage", "numero_chamado", "nome_completo", "cpf_sus",
                            "unidade_selecionada", "localizacao", "passou_posicao_3",
                            "tempo_entrada_posicao_3", "geo_location_cache", "geo_queue_cache"]:
                    st.session_state.pop(key, None)
                st.rerun()

            time.sleep(15)
            st.rerun()

# ── Footer ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="sus-footer">
  Sistema Conecta SUS &nbsp;·&nbsp; Seus dados são protegidos pela LGPD &nbsp;·&nbsp;
  <a href="/admin" target="_self" style="color:#0AB4A0;text-decoration:none;font-weight:600">Área Admin</a>
</div>
""", unsafe_allow_html=True)
