import streamlit as st
import requests
import pandas as pd

# Configuración de la página
st.set_page_config(
    page_title="LootRadar | Tu Rastreador de Ofertas",
    page_icon="🏹",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Estilo Personalizado (Premium Dark Mode)
st.markdown("""
    <style>
    /* Estilo General */
    .main {
        background-color: #0e1117;
        color: #ffffff;
    }
    
    /* Títulos con Gradiente */
    .title-text {
        font-family: 'Outfit', sans-serif;
        font-weight: 800;
        background: linear-gradient(90deg, #00d2ff 0%, #3a7bd5 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3.5rem !important;
        margin-bottom: 0px;
    }
    
    .subtitle-text {
        color: #8892b0;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }

    /* Cards de Juegos */
    .game-card {
        background: rgba(23, 25, 35, 0.8);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 20px;
        transition: transform 0.3s ease, border-color 0.3s ease;
        text-align: center;
        margin-bottom: 20px;
        height: 500px; /* Tamaño fijo de card */
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    
    .game-card:hover {
        transform: translateY(-5px);
        border-color: #00d2ff;
        background: rgba(23, 25, 35, 1);
    }

    .game-card img {
        width: 100%;
        height: 150px; /* Altura fija para alineación */
        object-fit: cover;
        border-radius: 10px;
        margin-bottom: 15px;
    }

    .savings-badge {
        background-color: #22c55e;
        color: white;
        padding: 4px 10px;
        border-radius: 8px;
        font-weight: bold;
        font-size: 0.8rem;
    }

    .price-text {
        font-size: 1.5rem;
        font-weight: bold;
        color: #ffffff;
    }

    .retail-price {
        text-decoration: line-through;
        color: #64748b;
        font-size: 0.9rem;
    }

    .store-label {
        font-size: 0.7rem;
        color: #8892b0;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-top: -5px;
        margin-bottom: 10px;
    }

    /* Botón personalizado */
    .stButton>button {
        background: linear-gradient(90deg, #3a7bd5 0%, #00d2ff 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.5rem 2rem;
        font-weight: bold;
        transition: 0.3s;
    }
    </style>
""", unsafe_allow_html=True)

# --- LÓGICA DE API ---

STORE_MAP = {
    "1": "Steam", "2": "GamersGate", "3": "GreenManGaming", "7": "GOG",
    "11": "Humble Store", "15": "Fanatical", "21": "Epic Games", "25": "Epic Games",
    "23": "GameStop", "24": "Direct2Drive", "32": "Origin"
}

def get_currency_rate():
    return 0.95 # Simplificado

def get_games(title):
    try:
        url = f"https://www.cheapshark.com/api/1.0/games?title={title}&limit=12"
        response = requests.get(url)
        return response.json()
    except: return []

def get_game_deals(game_id):
    try:
        url = f"https://www.cheapshark.com/api/1.0/games?id={game_id}"
        response = requests.get(url)
        return response.json()
    except: return None

import urllib.parse

def get_external_links(game_name):
    encoded_name = urllib.parse.quote_plus(game_name)
    return {
        "Eneba": f"https://www.eneba.com/store/all?text={encoded_name}&regions[]=europe&regions[]=global",
        "Instant Gaming": f"https://www.instant-gaming.com/pt/pesquisar/?query={encoded_name}",
        "Steam": f"https://store.steampowered.com/search/?term={encoded_name}&cc=pt",
        "Humble Bundle": f"https://www.humblebundle.com/store/search?sort=bestselling&search={encoded_name}",
        "Fanatical": f"https://www.fanatical.com/en/search?search={encoded_name}"
    }

# --- INTERFAZ ---

st.markdown('<h1 class="title-text">LootRadar 🏹</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle-text">Portugal Edition: Compras focadas no mercado local 🇵🇹</p>', unsafe_allow_html=True)

with st.sidebar:
    st.header("Configuración")
    currency = st.selectbox("Moneda", ["EUR (€)", "USD ($)"])
    rate = get_currency_rate() if currency == "EUR (€)" else 1.0
    symbol = "€" if currency == "EUR (€)" else "$"
    st.divider()
    st.info("💡 Consejo: Los 'Packs' o 'Sagas' suelen aparecer en Steam o Fanatical con mejores precios totales.")

col1, col2 = st.columns([3, 1])
with col1:
    search_query = st.text_input("Buscar Juego", placeholder="¿Qué buscas hoy?", label_visibility="collapsed")
with col2:
    search_button = st.button("Explorar Ofertas", use_container_width=True)

if search_query:
    ext_links = get_external_links(search_query)
    
    # Reemplazamos el JS problemático por botones nativos seguros
    st.write("### ⚡ Búsqueda rápida en tiendas:")
    b_col1, b_col2, b_col3, b_col4 = st.columns(4)
    with b_col1:
        st.link_button("Eneba PT 💎", ext_links["Eneba"], use_container_width=True)
    with b_col2:
        st.link_button("Instant Gaming ⚡", ext_links["Instant Gaming"], use_container_width=True)
    with b_col3:
        st.link_button("Steam Store 🎮", ext_links["Steam"], use_container_width=True)
    with b_col4:
        # Link específico para buscar "Packages" (Packs/Bundles) en Steam
        steam_bundle_url = f"https://store.steampowered.com/search/?term={urllib.parse.quote_plus(search_query)}&category1=996"
        st.link_button("Steam PACKS 📦", steam_bundle_url, use_container_width=True)
    
    st.divider()

    games = get_games(search_query)
    
    if not games:
        st.warning("Sin resultados oficiales en CheapShark. Usa la Búsqueda Masiva de arriba.")
    else:
        # Usamos 4 columnas para aprovechar mejor el espacio en pantallas anchas
        cols = st.columns(4)
        for i, game in enumerate(games):
            with cols[i % 4]:
                details = get_game_deals(game['gameID'])
                if details:
                    deal = details['deals'][0]
                    store_name = STORE_MAP.get(deal['storeID'], "Tienda")
                    # Detección mejorada de packs
                    is_bundle = (deal['storeID'] in ['1', '15', '24'] or 
                                any(word in game['external'].lower() for word in ['pack', 'saga', 'bundle', 'collection', 'anthology']))
                    
                    s_price = float(deal['price']) * rate
                    r_price = float(deal['retailPrice']) * rate
                    save = float(deal['savings'])
                    
                    # Buscar específicamente el precio de Steam en la lista de ofertas
                    steam_price_val = None
                    for d in details['deals']:
                        if d['storeID'] == '1': # ID de Steam
                            steam_price_val = float(d['price']) * rate
                            break
                    
                    el = get_external_links(game['external'])
                    badge = f'<span class="savings-badge" style="background:#8b5cf6; margin-left:5px;">PACK/SAGA 📦</span>' if is_bundle else ""
                    
                    # Línea de precio Steam si existe
                    steam_html = f'<div style="font-size: 0.8rem; color: #171a21; background: #66c0f4; border-radius: 4px; padding: 2px 5px; display: inline-block; margin-top: 5px;">Steam: {symbol}{steam_price_val:.2f}</div>' if steam_price_val else ""

                    card_html = (
                        f'<div class="game-card">'
                        f'<div>'
                        f'<img src="{game["thumb"]}">'
                        f'<h4 style="height: 40px; overflow: hidden; margin-bottom: 5px; font-size: 0.95rem;">{game["external"]}</h4>'
                        f'<div class="store-label">Tienda: {store_name}</div>'
                        f'<div style="margin: 5px 0;"><span class="retail-price">{symbol}{r_price:.2f}</span><span class="price-text"> {symbol}{s_price:.2f}</span></div>'
                        f'<div style="margin-bottom: 5px;"><span class="savings-badge">-{int(save)}% OFF</span>{badge}</div>'
                        f'{steam_html}'
                        f'</div>'
                        f'<div style="display: flex; flex-direction: column; gap: 8px; margin-top: 10px;">'
                        f'<a href="https://www.cheapshark.com/redirect?dealID={deal["dealID"]}" target="_blank" style="text-decoration:none; background:#3a7bd5; color:white; padding:8px 5px; border-radius:8px; font-weight:bold; display:block; font-size: 0.75rem; text-align: center;">Ir a {store_name} 🚀</a>'
                        f'<div style="display: flex; gap: 5px;">'
                        f'<a href="{el["Eneba"]}" target="_blank" style="text-decoration:none; background:#2A2D37; color:#FFAD33; padding:5px; border-radius:5px; font-weight:bold; flex:1; font-size: 0.65rem; border: 1px solid #FFAD33; text-align: center;">Eneba</a>'
                        f'<a href="{el["Instant Gaming"]}" target="_blank" style="text-decoration:none; background:#2A2D37; color:#FF5400; padding:5px; border-radius:5px; font-weight:bold; flex:1; font-size: 0.65rem; border: 1px solid #FF5400; text-align: center;">IG PT</a>'
                        f'</div>'
                        f'<a href="{el["Humble Bundle"]}" target="_blank" style="text-decoration:none; background:#2A2D37; color:#CB2D3E; padding:5px; border-radius:5px; font-weight:bold; display:block; font-size: 0.65rem; border: 1px solid #CB2D3E; text-align: center;">Sagas & Bundles 📦</a>'
                        f'</div></div>'
                    )
                    st.markdown(card_html, unsafe_allow_html=True)
else:
    # Vista inicial mejorada para usar el espacio
    st.markdown("""
        <div style="background: rgba(23, 25, 35, 0.5); padding: 40px; border-radius: 20px; text-align: center; border: 1px dashed rgba(255,255,255,0.1);">
            <h2 style="color: #00d2ff;">¡Bem-vindo ao LootRadar! 🏹</h2>
            <p style="color: #8892b0; font-size: 1.1rem;">Tu centro de control para pechinchas en Portugal.</p>
            <div style="margin-top: 30px; display: flex; justify-content: center; gap: 20px;">
                <div style="text-align: left; max-width: 300px;">
                    <h4 style="color: white; margin-bottom: 10px;">🛡️ Compra segura</h4>
                    <p style="font-size: 0.9rem; color: #64748b;">Enlaces directos a Steam PT, Eneba e Instant Gaming.</p>
                </div>
                <div style="text-align: left; max-width: 300px;">
                    <h4 style="color: white; margin-bottom: 10px;">📦 Packs & Sagas</h4>
                    <p style="font-size: 0.9rem; color: #64748b;">Detección automática de colecciones completas a bajo precio.</p>
                </div>
            </div>
            <p style="margin-top: 40px; color: #3a7bd5; font-style: italic;">Prueba buscando "Resident Evil", "Monster Hunter" o "Elden Ring".</p>
        </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center; color: #8892b0;'>Optimizado para o mercado de Portugal 🇵🇹 | Desenvolvido por Antigravity</p>", unsafe_allow_html=True)
