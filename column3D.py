# Dashboard 3D Completo com Streamlit - CUSTOMIZAÇÃO AVANÇADA
import streamlit as st
import plotly.graph_objects as go
import numpy as np
import math
import pandas as pd
from io import StringIO

# ==========================================
# CONFIGURAÇÃO DA PÁGINA
# ==========================================
st.set_page_config(layout="wide", page_title="Dashboard 3D Avançado", page_icon="🌌")

# ==========================================
# DADOS E CONFIGURAÇÕES
# ==========================================
DADOS_PADRAO = {
    'x': ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta'],
    'y': [10, 15, 8, 20, 25]
}

# Esquemas de cores automáticas
ESQUEMAS_COR = [
    {'label': '🔥 Fogo (Vermelho→Amarelo)', 'value': 'fire'},
    {'label': '🌊 Oceano (Azul→Ciano)', 'value': 'ocean'},
    {'label': '🌿 Natureza (Verde→Lime)', 'value': 'nature'},
    {'label': '🌅 Sunset (Laranja→Rosa)', 'value': 'sunset'},
    {'label': '🌌 Galáxia (Roxo→Azul)', 'value': 'galaxy'},
    {'label': '🎨 Arco-íris', 'value': 'rainbow'}
]

# Layouts 3D
LAYOUTS_3D = [
    {'label': '📊 Linear', 'value': 'linear'},
    {'label': '🔄 Circular', 'value': 'circular'},
    {'label': '🌊 Onda Senoidal', 'value': 'wave'},
    {'label': '🌀 Espiral', 'value': 'spiral'},
    {'label': '🏔️ Montanha', 'value': 'mountain'},
    {'label': '💎 Diamante', 'value': 'diamond'}
]

# Tipos de marcadores 3D
MARCADORES_3D = [
    {'label': '⚫ Círculo', 'value': 'circle'},
    {'label': '⬛ Quadrado', 'value': 'square'},
    {'label': '♦️ Diamante', 'value': 'diamond'},
    {'label': '▲ Triângulo', 'value': 'triangle-up'},
    {'label': '⭐ Estrela', 'value': 'star'},
    {'label': '✚ Cruz', 'value': 'cross'}
]

# ==========================================
# FUNÇÕES AUXILIARES
# ==========================================
def criar_cores_esquema(esquema, num_pontos):
    """Cria cores baseadas no esquema escolhido"""
    cores = []
    
    for i in range(num_pontos):
        ratio = i / max(1, num_pontos - 1) if num_pontos > 1 else 0
        
        if esquema == 'fire':
            r, g, b = 255, int(50 + ratio * 205), int(ratio * 100)
        elif esquema == 'ocean':
            r, g, b = int(ratio * 100), int(100 + ratio * 155), 255
        elif esquema == 'nature':
            r, g, b = int(ratio * 150), 255, int(ratio * 100)
        elif esquema == 'sunset':
            r, g, b = 255, int(150 + ratio * 105), int(200 - ratio * 150)
        elif esquema == 'galaxy':
            r, g, b = int(150 + ratio * 105), int(50 + ratio * 100), 255
        elif esquema == 'rainbow':
            hue = ratio * 300
            r = int(255 * (1 + math.cos(math.radians(hue))) / 2)
            g = int(255 * (1 + math.cos(math.radians(hue + 120))) / 2)
            b = int(255 * (1 + math.cos(math.radians(hue + 240))) / 2)
        else:
            r, g, b = 0, int(100 + ratio * 155), 255
        
        cores.append(f'rgb({r}, {g}, {b})')
    
    return cores

def calcular_layout_3d(dados_x, dados_y, layout_tipo):
    """Calcula posições baseadas no layout 3D"""
    n = len(dados_x)
    
    if layout_tipo == 'circular':
        radius = max(3, n * 0.5)
        x_pos = [radius * math.cos(2 * math.pi * i / n) for i in range(n)]
        y_pos = [radius * math.sin(2 * math.pi * i / n) for i in range(n)]
    elif layout_tipo == 'wave':
        x_pos = [i * 2 for i in range(n)]
        y_pos = [3 * math.sin(2 * math.pi * i / n) for i in range(n)]
    elif layout_tipo == 'spiral':
        x_pos = [2 * (i + 1) / n * math.cos(3 * math.pi * i / n) for i in range(n)]
        y_pos = [2 * (i + 1) / n * math.sin(3 * math.pi * i / n) for i in range(n)]
    elif layout_tipo == 'mountain':
        center = n // 2
        x_pos = [i * 1.5 for i in range(n)]
        y_pos = [abs(i - center) * 0.8 for i in range(n)]
    elif layout_tipo == 'diamond':
        center = n // 2
        x_pos = [i - center for i in range(n)]
        y_pos = [abs(i - center) - center for i in range(n)]
    else:  # linear
        x_pos = [i * 1.5 for i in range(n)]
        y_pos = [0] * n
    
    return x_pos, y_pos

def criar_coluna_3d_avancada(x, y, altura, cor, marcador, tamanho, densidade, transparencia):
    """Cria coluna 3D com configurações avançadas"""
    pontos_x, pontos_y, pontos_z = [], [], []
    cores = []
    
    num_pontos = max(3, int(altura * densidade / 2))
    
    for i in range(num_pontos):
        z_atual = (altura * i) / (num_pontos - 1) if num_pontos > 1 else altura
        offset_x = 0.1 * math.sin(i * 0.5) if marcador in ['diamond', 'star'] else 0
        offset_y = 0.1 * math.cos(i * 0.5) if marcador in ['diamond', 'star'] else 0
        
        pontos_x.append(x + offset_x)
        pontos_y.append(y + offset_y)
        pontos_z.append(z_atual)
        
        intensity = 0.7 + 0.3 * (i / num_pontos) if num_pontos > 1 else 1.0
        if cor.startswith('rgb'):
            cores.append(cor.replace('rgb', f'rgba').replace(')', f', {transparencia * intensity})'))
        else:
            cores.append(cor)
    
    return pontos_x, pontos_y, pontos_z, cores

# ==========================================
# GERENCIAMENTO DE ESTADO
# ==========================================
if 'dados' not in st.session_state:
    st.session_state.dados = DADOS_PADRAO

# ==========================================
# HEADER
# ==========================================
st.title("🌌 Dashboard 3D Avançado")
st.markdown("Customização completa de gráficos 3D interativos")

# ==========================================
# SIDEBAR DE CONTROLES
# ==========================================
st.sidebar.header("🎛️ Controles Avançados")

# --- SEÇÃO: LAYOUT 3D ---
st.sidebar.subheader("🗂️ Layout 3D")
layout_idx = st.sidebar.selectbox(
    "Tipo de Layout",
    range(len(LAYOUTS_3D)),
    index=1,  # Padrão: Circular
    format_func=lambda x: LAYOUTS_3D[x]['label']
)
layout = LAYOUTS_3D[layout_idx]['value']

# --- SEÇÃO: CORES ---
st.sidebar.subheader("🎨 Cores")
esquema_idx = st.sidebar.selectbox(
    "Esquema de Cores",
    range(len(ESQUEMAS_COR)),
    index=4,  # Padrão: Galáxia
    format_func=lambda x: ESQUEMAS_COR[x]['label']
)
esquema_cor = ESQUEMAS_COR[esquema_idx]['value']

# --- SEÇÃO: MARCADORES ---
st.sidebar.subheader("📦 Marcadores")
marcador_idx = st.sidebar.selectbox(
    "Tipo de Marcador",
    range(len(MARCADORES_3D)),
    index=0,
    format_func=lambda x: MARCADORES_3D[x]['label']
)
marcador = MARCADORES_3D[marcador_idx]['value']
tamanho = st.sidebar.slider("Tamanho dos Marcadores", min_value=5, max_value=30, value=12, step=1)

# --- SEÇÃO: CONFIGURAÇÕES 3D ---
st.sidebar.subheader("⚙️ Configurações 3D")
densidade = st.sidebar.slider("Densidade dos Pontos", min_value=2, max_value=15, value=6, step=1)
escala = st.sidebar.slider("Escala Vertical", min_value=0.3, max_value=3.0, value=1.0, step=0.1)
transparencia = st.sidebar.slider("Transparência", min_value=0.2, max_value=1.0, value=0.8, step=0.05)

# --- SEÇÃO: CÂMERA 3D ---
st.sidebar.subheader("📹 Controle de Câmera")
cam_x = st.sidebar.slider("Ângulo X", min_value=-3.0, max_value=3.0, value=1.2, step=0.1)
cam_y = st.sidebar.slider("Ângulo Y", min_value=-3.0, max_value=3.0, value=1.2, step=0.1)
cam_z = st.sidebar.slider("Ângulo Z (Zoom)", min_value=0.3, max_value=4.0, value=1.2, step=0.1)

# --- SEÇÃO: APARÊNCIA ---
st.sidebar.subheader("🎭 Aparência")
titulo = st.sidebar.text_input("Título do Gráfico", value="🌌 Gráfico 3D Personalizado")

# --- SEÇÃO: OPÇÕES VISUAIS ---
st.sidebar.subheader("🎯 Opções Visuais")
opcoes = st.sidebar.multiselect(
    "Opções",
    options=['grid', 'eixos', 'dark', 'bordas'],
    default=['grid', 'eixos', 'bordas']
)

# --- SEÇÃO: UPLOAD E DADOS ---
st.sidebar.subheader("📁 Gerenciar Dados")
uploaded_file = st.sidebar.file_uploader(
    "Upload arquivo TXT/CSV",
    type=['txt', 'csv']
)

if uploaded_file is not None:
    try:
        string_data = uploaded_file.read().decode('utf-8')
        lines = [line.strip() for line in string_data.split('\n') if line.strip()]
        
        x_data, y_data = [], []
        for line in lines:
            parts = [p.strip() for p in line.replace('\t', ',').split(',')]
            if len(parts) >= 2:
                try:
                    x_data.append(parts[0])
                    y_data.append(float(parts[1]))
                except ValueError:
                    continue
        
        if len(x_data) > 1:
            st.session_state.dados = {'x': x_data, 'y': y_data}
            st.sidebar.success(f"✅ Arquivo '{uploaded_file.name}' carregado!")
        else:
            st.sidebar.error("⚠ Formato inválido ou poucos dados.")
    except Exception as e:
        st.sidebar.error(f"⚠ Erro ao ler arquivo: {e}")

if st.sidebar.button("🔄 Restaurar Dados Originais"):
    st.session_state.dados = DADOS_PADRAO
    st.sidebar.success("Dados originais restaurados!")

# ==========================================
# LÓGICA PRINCIPAL E GERAÇÃO DO GRÁFICO
# ==========================================
try:
    # 1. Obter dados do session_state
    dados = st.session_state.dados
    x_data = dados['x']
    y_data = [y * escala for y in dados['y']]

    # 2. Determinar cores
    cores = criar_cores_esquema(esquema_cor, len(x_data))
    
    # 3. Calcular posições 3D
    x_pos, y_pos = calcular_layout_3d(x_data, y_data, layout)
    
    # 4. Gerar pontos 3D para cada coluna
    all_x, all_y, all_z, all_colors = [], [], [], []
    all_text = []
    
    for i, (x, y, altura_col, cor) in enumerate(zip(x_pos, y_pos, y_data, cores)):
        px, py, pz, pc = criar_coluna_3d_avancada(
            x, y, altura_col, cor, marcador, tamanho, densidade, transparencia
        )
        all_x.extend(px)
        all_y.extend(py)
        all_z.extend(pz)
        all_colors.extend(pc)
        
        for _ in range(len(px)):
            all_text.append(f'{x_data[i]}: {dados["y"][i]:.1f}')

    # 5. Criar a figura Plotly
    fig = go.Figure()
    
    fig.add_trace(go.Scatter3d(
        x=all_x, y=all_y, z=all_z,
        mode='markers',
        marker=dict(
            size=tamanho,
            color=all_colors,
            symbol=marcador,
            opacity=transparencia,
            line=dict(
                width=2 if 'bordas' in opcoes else 0,
                color='black'
            )
        ),
        text=all_text,
        textposition='middle center',
        hovertemplate='<b>%{text}</b><br>Valor (com escala): %{z:.1f}<extra></extra>',
        showlegend=False
    ))
    
    # 6. Configurar layout do gráfico
    dark_mode = 'dark' in opcoes
    
    fig.update_layout(
        title={'text': f'<b>{titulo}</b>', 'x': 0.5, 'font': {'size': 18}},
        scene=dict(
            xaxis_title='<b>Posição X</b>',
            yaxis_title='<b>Posição Y</b>',
            zaxis_title='<b>Valores</b>',
            camera=dict(eye=dict(x=cam_x, y=cam_y, z=cam_z)),
            aspectmode='data',
            xaxis=dict(
                showgrid='grid' in opcoes, 
                showline='eixos' in opcoes, 
                gridcolor='rgba(255,255,255,0.4)' if dark_mode else 'lightgray'
            ),
            yaxis=dict(
                showgrid='grid' in opcoes, 
                showline='eixos' in opcoes, 
                gridcolor='rgba(255,255,255,0.4)' if dark_mode else 'lightgray'
            ),
            zaxis=dict(
                showgrid='grid' in opcoes, 
                showline='eixos' in opcoes, 
                gridcolor='rgba(255,255,255,0.4)' if dark_mode else 'lightgray'
            ),
            bgcolor='rgba(0,0,0,0.9)' if dark_mode else 'white'
        ),
        margin=dict(l=10, r=10, t=60, b=10),
        paper_bgcolor='rgba(0,0,0,0.8)' if dark_mode else 'white',
        font=dict(size=12, color='white' if dark_mode else 'black'),
        height=600
    )
    
    # 7. Exibir o gráfico no Streamlit
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': True})

    # --- SEÇÃO: ESTATÍSTICAS ---
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("📊 Total de Pontos", len(x_data))
    with col2:
        st.metric("📈 Valor Máximo", f"{max(dados['y']):.1f}")
    with col3:
        st.metric("📉 Valor Mínimo", f"{min(dados['y']):.1f}")
    with col4:
        st.metric("🧮 Média", f"{sum(dados['y'])/len(dados['y']):.1f}")

    # --- SEÇÃO: DOWNLOAD ---
    @st.cache_data
    def get_html_download(figure):
        html_buffer = StringIO()
        figure.write_html(html_buffer, include_plotlyjs='cdn')
        return html_buffer.getvalue()

    html_str = get_html_download(fig)
    st.sidebar.download_button(
        label="💾 Baixar Gráfico como HTML",
        data=html_str,
        file_name=f"{titulo.replace(' ', '_').lower()}.html",
        mime="text/html",
    )

except Exception as e:
    st.error(f"Ocorreu um erro ao gerar o gráfico: {e}")

# ==========================================
# INSTRUÇÕES DE USO
# ==========================================
with st.expander("📋 Instruções de Uso"):
    st.markdown("""
    ### 📁 Upload de Dados
    Formatos aceitos: TXT e CSV
    
    **Formato esperado:**
    ```
    Nome,Valor
    Segunda,10
    Terça,15
    Quarta,8
    Quinta,20
    Sexta,25
    ```
    
    ### 🎛️ Controles Disponíveis
    - **Layout 3D**: Define como os pontos são organizados no espaço 3D
    - **Cores**: Esquemas automáticos de cores
    - **Marcadores**: Diferentes símbolos para representar os pontos
    - **Densidade**: Controla quantos pontos formam cada coluna 3D
    - **Câmera**: Ajusta o ângulo de visualização do gráfico
    - **Aparência**: Título e opções visuais
    
    ### 💾 Download
    Use o botão "Baixar Gráfico como HTML" na sidebar para salvar o gráfico como um arquivo HTML interativo.
    """)
