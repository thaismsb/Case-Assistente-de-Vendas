import os
import requests
import streamlit as st

st.set_page_config(page_title="Petlove - Assistente de Vendas", page_icon="static/coracao.png", layout="centered")

# URL API 
API_URL = os.getenv("API_URL", "http://petlove-backend-dev.us-west-2.elasticbeanstalk.com/api/question-and-answer")

# Persona fixa 
SALES_PERSONA = os.getenv(
    "SALES_PERSONA",
    (
        "Você é um assistente de vendas de e-commerce da Petlove. "
        "Seu objetivo é entender a necessidade do tutor e recomendar produtos adequados "
        "(rações, petiscos, medicamentos, higiene, brinquedos), sempre com tom amigável, "
        "objetivo e consultivo. Faça perguntas de qualificação quando necessário "
        "(espécie, porte, idade, alergias, restrições, preferências de marca, orçamento) "
        "e ofereça cross-sell/upsell de forma natural. "
        "Forneça o porquê da recomendação e como usar. "
        "Se o usuário pedir algo fora do escopo de vendas, responda brevemente e traga de volta para a compra."
    ),
)

# ---------------- Sidebar ----------------
with st.sidebar:
    st.image("static/petlove-logo.png", use_column_width=True)
    st.divider()
    st.subheader("Sugestões de perguntas")
    if st.button("Ração para filhote de porte pequeno"):
        st.session_state["pre_prompt"] = "Quero ração para cachorro filhote de porte pequeno."
    if st.button("Brinquedos para gato ansioso"):
        st.session_state["pre_prompt"] = "Meu gato é ansioso; preciso brinquedos que gastem energia."
    if st.button("Kit higiene para shih-tzu"):
        st.session_state["pre_prompt"] = "Quero um kit de higiene para shih-tzu (pelo longo)."
    st.divider()
    if st.button("Limpar conversa"):
        st.session_state.clear()
        st.rerun()

# ---------------- Estado ----------------
if "messages" not in st.session_state:
    st.session_state.messages = []  # [{"role": "user"/"assistant", "content": "..."}]

# Pre-preenche input via sidebar
pre_prompt = st.session_state.pop("pre_prompt", "")

# ---------------- Header ----------------

st.markdown(
    """
    <h2 style='color: #6b1e9d;'>
        Assistente de Vendas Petlove 🐾 
    </h2>
    """,
    unsafe_allow_html=True
)

st.markdown(
    "<p style='text-align: left; color: #555;'>Faça perguntas e receba recomendações de produtos com explicações e dicas de uso.</p>",
    unsafe_allow_html=True
)

# ---------------- Chat history ----------------
for msg in st.session_state.messages:
    with st.chat_message("user" if msg["role"] == "user" else "assistant"):
        st.markdown(msg["content"])

# ---------------- Input ----------------
user_input = st.chat_input("Descreva a necessidade do seu pet...", max_chars=800)
if not user_input and pre_prompt:
    user_input = pre_prompt

if user_input:

    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    # monta conteúdo com persona (sem alterar o backend)
    composed = f"{SALES_PERSONA}\n\nPergunta do cliente: {user_input}"

    try:
        resp = requests.post(
            st.session_state.get("api_url", API_URL),
            json={"message": composed},
            timeout=60,
        )
        resp.raise_for_status()
        data = resp.json()
        answer = data.get("resposta", "").strip() or "Desculpe, não consegui gerar uma resposta agora."

    except requests.exceptions.HTTPError as http_err:
        if resp.status_code == 500:
            answer = (
                "🐾 **Ops! Nosso servidor está tirando um cochilo agora.**\n\n"
                "Tente novamente em alguns instantes 💜"
            )
        else:
            answer = f"⚠️ Erro ao chamar a API: {resp.status_code} — {http_err}"

    except requests.exceptions.ConnectionError:
        answer = (
            "**Não foi possível se conectar à API.**\n\n"
            "Verifique se ela está rodando e tente novamente."
        )

    except requests.exceptions.Timeout:
        answer = (
            "⏳ **A API demorou demais para responder.**\n\n"
            "Por favor, tente novamente daqui a pouco!"
        )

    except Exception as e:
        answer = f"**Erro inesperado:** {e}"

    with st.chat_message("assistant"):
        st.markdown(answer)
    st.session_state.messages.append({"role": "assistant", "content": answer})


# ---------------- Rodapé ----------------
st.markdown("---")