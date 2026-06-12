import streamlit as st
import os

st.set_page_config(page_title="MetaGPT Configurator", layout="centered")

st.title("🛠️ MetaGPT UI – Configuração da Ferramenta")
st.caption("Preencha os campos abaixo para configurar o agente MetaGPT.")

# LLM Provider selection
provider = st.selectbox(
    "Provedor LLM",
    options=["OpenAI", "Anthropic", "Local (llama.cpp)", "HuggingFace"],
    index=0
)

api_key = None
model_name = None
temperature = None

if provider == "OpenAI":
    api_key = st.text_input("API Key (OpenAI)", type="password", help="Obtenha em https://platform.openai.com/account/api-keys")
    model_name = st.selectbox("Modelo", options=["gpt-4o", "gpt-4-turbo", "gpt-3.5-turbo"], index=0)
    temperature = st.slider("Temperatura", 0.0, 2.0, 0.7, 0.1)

elif provider == "Anthropic":
    api_key = st.text_input("API Key (Anthropic)", type="password", help="Obtenha em https://console.anthropic.com/")
    model_name = st.selectbox("Modelo", options=["claude-3-opus-20240229", "claude-3-sonnet-20240229", "claude-3-haiku-20240307"], index=0)
    temperature = st.slider("Temperatura", 0.0, 2.0, 0.7, 0.1)

elif provider == "Local (llama.cpp)":
    st.info("Para uso local, especifique o caminho para o modelo GGUF.")
    model_path = st.text_input("Caminho do modelo GGUF", placeholder="/caminho/para/model.gguf")
    model_name = model_path  # treat as path
    temperature = st.slider("Temperatura", 0.0, 2.0, 0.7, 0.1)
    api_key = ""  # not used

elif provider == "HuggingFace":
    api_key = st.text_input("API Key (HuggingFace)", type="password", help="Token de acesso em https://huggingface.co/settings/tokens")
    model_name = st.text_input("Modelo HF (ex: mistralai/Mixtral-8x7B-Instruct-v0.1)", value="mistralai/Mixtral-8x7B-Instruct-v0.1")
    temperature = st.slider("Temperatura", 0.0, 2.0, 0.7, 0.1)

st.divider()
st.subheader("🤖 Configuração dos Agentes")
num_agents = st.number_input("Número de agentes (roles)", min_value=1, max_value=10, value=3, step=1)
agent_roles = []
for i in range(int(num_agents)):
    role = st.text_input(f"Role {i+1} (ex: Product Manager, Developer, Tester)", key=f"role_{i}", value=["Product Manager", "Developer", "Tester"][i] if i < 3 else "")
    agent_roles.append(role)

st.divider()
if st.button("Salvar Configuração"):
    config = {
        "provider": provider,
        "api_key": api_key if provider != "Local (llama.cpp)" else "",
        "model_name": model_name,
        "temperature": temperature,
        "agent_roles": agent_roles
    }
    # Save to file
    import json
    with open("config.json", "w") as f:
        json.dump(config, f, indent=2)
    st.success("Configuração salva em config.json")
    st.json(config)

# Show current config if exists
if os.path.exists("config.json"):
    st.divider()
    st.subheader("📄 Configuração atual")
    with open("config.json", "r") as f:
        current = json.load(f)
    st.json(current)
