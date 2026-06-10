import sqlite3
import re
from datetime import datetime, timedelta
from contextlib import contextmanager

DB_PATH = "fila_sus.db"

JANELA_SPAM_MINUTOS = 60
MAX_TENTATIVAS = 3


@contextmanager
def get_conn():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def init_db():
    with get_conn() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS fila (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                numero_chamado INTEGER NOT NULL,
                nome TEXT NOT NULL,
                cpf_sus TEXT NOT NULL,
                unidade TEXT NOT NULL,
                sintomas TEXT DEFAULT '',
                telefone TEXT DEFAULT '',
                timestamp TEXT NOT NULL,
                status TEXT DEFAULT 'aguardando',
                atendido_em TEXT
            )
        """)
        # Migração segura: adiciona coluna telefone em bases já existentes
        try:
            conn.execute("ALTER TABLE fila ADD COLUMN telefone TEXT DEFAULT ''")
        except Exception:
            pass
        conn.execute("""
            CREATE TABLE IF NOT EXISTS config (
                chave TEXT PRIMARY KEY,
                valor TEXT NOT NULL
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS tentativas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cpf_sus TEXT NOT NULL,
                timestamp TEXT NOT NULL
            )
        """)
        conn.execute(
            "INSERT OR IGNORE INTO config (chave, valor) VALUES ('proximo_numero', '1')"
        )
        conn.execute(
            "INSERT OR IGNORE INTO config (chave, valor) VALUES ('ultimo_avanco_fila', ?)",
            (datetime.now().isoformat(),)
        )


def _get_config(conn, chave):
    row = conn.execute("SELECT valor FROM config WHERE chave = ?", (chave,)).fetchone()
    return row["valor"] if row else None


def _set_config(conn, chave, valor):
    conn.execute(
        "INSERT OR REPLACE INTO config (chave, valor) VALUES (?, ?)",
        (chave, str(valor))
    )


def _parse_dt(s):
    if not s:
        return None
    try:
        return datetime.fromisoformat(s)
    except Exception:
        return None


def _row_to_dict(row):
    d = dict(row)
    d["timestamp"] = _parse_dt(d.get("timestamp"))
    d["atendido_em"] = _parse_dt(d.get("atendido_em"))
    return d


def _normalizar_cpf(cpf_sus: str) -> str:
    return re.sub(r"\D", "", cpf_sus or "")


# ── Número sequencial 1-100 ────────────────────────────────────────────────────

def _proximo_numero_disponivel(conn):
    numeros_em_uso = {
        row["numero_chamado"]
        for row in conn.execute(
            "SELECT numero_chamado FROM fila WHERE status = 'aguardando'"
        ).fetchall()
    }
    proximo = int(_get_config(conn, "proximo_numero") or "1")

    for _ in range(100):
        if proximo not in numeros_em_uso:
            _set_config(conn, "proximo_numero", str((proximo % 100) + 1))
            return proximo
        proximo = (proximo % 100) + 1

    return None


# ── Anti-spam (rate limiting) ──────────────────────────────────────────────────

def registrar_tentativa(cpf_sus: str):
    cpf = _normalizar_cpf(cpf_sus)
    with get_conn() as conn:
        conn.execute(
            "INSERT INTO tentativas (cpf_sus, timestamp) VALUES (?, ?)",
            (cpf, datetime.now().isoformat())
        )


def verificar_spam(cpf_sus: str) -> tuple[bool, int]:
    cpf = _normalizar_cpf(cpf_sus)
    janela = (datetime.now() - timedelta(minutes=JANELA_SPAM_MINUTOS)).isoformat()
    with get_conn() as conn:
        count = conn.execute(
            "SELECT COUNT(*) as c FROM tentativas WHERE cpf_sus = ? AND timestamp >= ?",
            (cpf, janela)
        ).fetchone()["c"]
    bloqueado = count >= MAX_TENTATIVAS
    return bloqueado, count


# ── Verificação de check-in duplicado ─────────────────────────────────────────

def ja_esta_na_fila(cpf_sus: str, unidade: str) -> bool:
    cpf = _normalizar_cpf(cpf_sus)
    with get_conn() as conn:
        row = conn.execute(
            "SELECT id FROM fila WHERE cpf_sus = ? AND unidade = ? AND status = 'aguardando'",
            (cpf, unidade)
        ).fetchone()
    return row is not None


# ── Operações públicas ─────────────────────────────────────────────────────────

def adicionar_na_fila(nome, cpf_sus, unidade, sintomas, telefone=""):
    cpf = _normalizar_cpf(cpf_sus)
    with get_conn() as conn:
        numero = _proximo_numero_disponivel(conn)
        if numero is None:
            return None
        agora = datetime.now().isoformat()
        conn.execute(
            """INSERT INTO fila (numero_chamado, nome, cpf_sus, unidade, sintomas, telefone, timestamp)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (numero, nome, cpf, unidade, sintomas, telefone, agora)
        )
        count = conn.execute(
            "SELECT COUNT(*) as c FROM fila WHERE status = 'aguardando'"
        ).fetchone()["c"]
        if count == 1:
            _set_config(conn, "ultimo_avanco_fila", agora)
        return numero


def obter_fila():
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT * FROM fila WHERE status = 'aguardando' ORDER BY timestamp ASC"
        ).fetchall()
        return [_row_to_dict(r) for r in rows]


def obter_atendidos():
    today = datetime.now().strftime("%Y-%m-%d")
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT * FROM fila WHERE status = 'atendido' AND date(atendido_em) = ? ORDER BY atendido_em DESC",
            (today,)
        ).fetchall()
        return [_row_to_dict(r) for r in rows]


def obter_posicao(numero_chamado):
    fila = obter_fila()
    for idx, p in enumerate(fila):
        if p["numero_chamado"] == numero_chamado:
            return idx + 1
    return None


def obter_paciente(numero_chamado):
    with get_conn() as conn:
        row = conn.execute(
            "SELECT * FROM fila WHERE numero_chamado = ? AND status = 'aguardando'",
            (numero_chamado,)
        ).fetchone()
        return _row_to_dict(row) if row else None


def remover_da_fila(numero_chamado):
    with get_conn() as conn:
        conn.execute(
            "UPDATE fila SET status = 'cancelado' WHERE numero_chamado = ? AND status = 'aguardando'",
            (numero_chamado,)
        )


def chamar_proximo(unidade=None):
    fila = obter_fila()
    if not fila:
        return None
    candidatos = [p for p in fila if p["unidade"] == unidade] if unidade else fila
    if not candidatos:
        return None
    proximo = candidatos[0]
    with get_conn() as conn:
        agora = datetime.now().isoformat()
        # Mantém nome, CPF, sintomas e telefone — apenas muda o status
        conn.execute(
            "UPDATE fila SET status = 'atendido', atendido_em = ? WHERE numero_chamado = ? AND status = 'aguardando'",
            (agora, proximo["numero_chamado"])
        )
        _set_config(conn, "ultimo_avanco_fila", agora)
    return proximo


def avancar_fila_automatico():
    with get_conn() as conn:
        ultimo_str = _get_config(conn, "ultimo_avanco_fila")
        count = conn.execute(
            "SELECT COUNT(*) as c FROM fila WHERE status = 'aguardando'"
        ).fetchone()["c"]

    if not ultimo_str or count == 0:
        return None

    ultimo = _parse_dt(ultimo_str)
    if ultimo and datetime.now() - ultimo > timedelta(seconds=60):
        return chamar_proximo()
    return None


def resetar_fila():
    with get_conn() as conn:
        conn.execute("DELETE FROM fila")
        conn.execute("DELETE FROM tentativas")
        _set_config(conn, "proximo_numero", "1")
        _set_config(conn, "ultimo_avanco_fila", datetime.now().isoformat())


def resetar_fila_unidade(unidade: str):
    with get_conn() as conn:
        conn.execute(
            "DELETE FROM fila WHERE unidade = ? AND status = 'aguardando'",
            (unidade,)
        )
        _set_config(conn, "ultimo_avanco_fila", datetime.now().isoformat())


def fila_cheia():
    fila = obter_fila()
    return len(fila) >= 100


init_db()
