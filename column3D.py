# Dashboard 3D com Streamlit
import streamlit as st
import plotly.graph_objects as go
import numpy as np
import pandas as pd
from io import StringIO

# ==========================================
# CONFIGURAÇÃO DA PÁGINA
# ==========================================
st.set_page_config(
    layout="wide", 
    page_title="Dashboard 3D", 
    page_icon="📊"
)

# ==========================================
# INICIALIZAÇÃO DE DADOS
# ==========================================
@st.cache_data
def criar_dados_exemplo():
    """Cria dados de exemplo para o gráfico"""
    categorias = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho']
    valores = [45, 52, 38, 65, 59, 72]
    return pd.DataFrame({'Mês': categorias, 'Valor': valores})

# ==========================================
# FUNÇÕES DE CRIAÇÃO DO GRÁFICO
# ==========================================
def criar_grafico_3d(df, config):
    """Cria o gráfico 3D com as configurações especificadas"""
    
    # Preparar dados
    x = list(range(len(df)))
    y = [0] * len(df)
    z = df['Valor'].tolist()
    
    # Criar figura
    fig = go.Figure()
    
    # Adicionar barras 3D
    for i in range(len(df)):
        # Base da barra
        x_bar = [x[i]-0.4, x[i]+0.4, x[i]+0.4, x[i]-0.4, x[i]-0.4]
        y_bar = [-0.4, -0.4, 0.4, 0.4, -0.4]
        z_bar_bottom = [0, 0, 0, 0, 0]
        z_bar_top = [z[i], z[i], z[i], z[i], z[i]]
        
        # Cor da barra
        if config['cor_unica']:
            cor = config['cor_barras']
        else:
            # Gradiente de cores
            cor = f'rgb({int(255 * i/len(df))}, {int(100 + 155 * (1-i/len(df)))}, {int(200)})'
        
        # Adicionar faces da barra
        # Face frontal
        fig.add_trace(go.Mesh3d(
            x=[x[i]-0.4, x[i]+0.4, x[i]+0.4, x[i]-0.4],
            y=[-0.4, -0.4, -0.4, -0.4],
            z=[0, 0, z[i], z[i]],
            color=cor,
            opacity=config['opacidade'],
            showscale=False,
            hovertemplate=f'<b>{df.iloc[i]["Mês"]}</b><br>Valor: {z[i]}<extra></extra>'
        ))
        
        # Face traseira
        fig.add_trace(go.Mesh3d(
            x=[x[i]-0.4, x[i]+0.4, x[i]+0.4, x[i]-0.4],
            y=[0.4, 0.4, 0.4, 0.4],
            z=[0, 0, z[i], z[i]],
            color=cor,
            opacity=config['opacidade'],
            showscale=False,
            hovertemplate=f'<b>{df.iloc[i]["Mês"]}</b><br>Valor: {z[i]}<extra></extra>'
        ))
        
        # Face lateral esquerda
        fig.add_trace(go.Mesh3d(
            x=[x[i]-0.4, x[i]-0.4, x[i]-0.4, x[i]-0.4],
            y=[-0.4, 0.4, 0.4, -0.4],
            z=[0, 0, z[i], z[i]],
            color=cor,
            opacity=config['opacidade'],
            showscale=False,
            hovertemplate=f'<b>{df.iloc[i]["Mês"]}</b><br>Valor: {z[i]}<extra></extra>'
        ))
        
        # Face lateral direita
        fig.add_trace(go.Mesh3d(
            x=[x[i]+0.4, x[i]+0.4, x[i]+0.4, x[i]+0.4],
            y=[-0.4, 0.4, 0.4, -0.4],
            z=[0, 0, z[i], z[i]],
            color=cor,
            opacity=config['opacidade'],
            showscale=False,
            hovertemplate=f'<b>{df.iloc[i]["Mês"]}</b><br>Valor: {z[i]}<extra></extra>'
        ))
        
        # Face superior
        fig.add_trace(go.Mesh3d(
            x=[x[i]-0.4, x[i]+0.4, x[i]+0.4, x[i]-0.4],
            y=[-0.4, -0.4, 0.4, 0.4],
            z=[z[i], z[i], z[i], z[i]],
            color=cor,
            opacity=config['opacidade'],
            showscale=False,
            hovertemplate=f'<b>{df.iloc[i]["Mês"]}</b><br>Valor: {z[i]}<extra></extra>'
        ))
    
    # Configurar layout
    fig.update_layout(
        title={
            'text': config['titulo'],
            'x': 0.5,
            'xanchor': 'center'
        },
        scene=dict(
            xaxis=dict(
                title='Categorias',
                ticktext=df['Mês'].tolist(),
                tickvals=list(range(len(df))),
                showgrid=config['mostrar_grid'],
                gridcolor='lightgray',
                showbackground=True,
                backgroundcolor='rgba(230, 230, 230, 0.1)'
            ),
            yaxis=dict(
                title='',
                showgrid=False,
                showticklabels=False,
                showbackground=False
            ),
            zaxis=dict(
                title='Valores',
                showgrid=config['mostrar_grid'],
                gridcolor='lightgray',
                showbackground=True,
                backgroundcolor='rgba(230, 230, 230, 0.1)'
            ),
            camera=dict(
                eye=dict(
                    x=config['camera_x'],
                    y=config['camera_y'],
                    z=config['camera_z']
                )
            ),
            aspectmode='manual',
            aspectratio=dict(x=2, y=1, z=1)
        ),
        showlegend=False,
        height=config['altura_grafico'],
        margin=dict(l=0, r=0, t=40, b=0)
    )
    
    return fig

# ==========================================
# INTERFACE PRINCIPAL
# ==========================================
st.title("📊 Dashboard 3D Interativo")
st.markdown("---")

# Criar colunas para layout
col1, col2 = st.columns([1, 3])

# ==========================================
# BARRA LATERAL - CONTROLES
# ==========================================
with col1:
    st.header("⚙️ Configurações")
    
    # Configurações de Dados
    st.subheader("📁 Dados")
    
    # Upload de arquivo
    uploaded_file = st.file_uploader(
        "Carregar CSV",
        type=['csv'],
        help="Formato: primeira coluna = categorias, segunda coluna = valores"
    )
    
    # Processar arquivo ou usar dados de exemplo
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            if len(df.columns) >= 2:
                df.columns = ['Mês', 'Valor']
                st.success("✅ Arquivo carregado!")
            else:
                st.error("❌ O arquivo deve ter pelo menos 2 colunas")
                df = criar_dados_exemplo()
        except Exception as e:
            st.error(f"❌ Erro ao ler arquivo: {e}")
            df = criar_dados_exemplo()
    else:
        df = criar_dados_exemplo()
        st.info("💡 Usando dados de exemplo")
    
    # Editor de dados
    st.subheader("✏️ Editar Dados")
    df_editado = st.data_editor(
        df,
        num_rows="dynamic",
        use_container_width=True
    )
    df = df_editado
    
    st.markdown("---")
    
    # Configurações Visuais
    st.subheader("🎨 Visual")
    
    titulo = st.text_input("Título do Gráfico", "Análise de Dados 3D")
    
    cor_unica = st.checkbox("Usar cor única", value=False)
    if cor_unica:
        cor_barras = st.color_picker("Cor das barras", "#3498db")
    else:
        cor_barras = "#3498db"
    
    opacidade = st.slider("Opacidade", 0.1, 1.0, 0.8, 0.1)
    
    mostrar_grid = st.checkbox("Mostrar grade", value=True)
    
    altura_grafico = st.slider("Altura do gráfico", 400, 800, 600, 50)
    
    st.markdown("---")
    
    # Configurações de Câmera
    st.subheader("📹 Câmera 3D")
    
    camera_x = st.slider("Posição X", -3.0, 3.0, 1.5, 0.1)
    camera_y = st.slider("Posição Y", -3.0, 3.0, -1.5, 0.1)
    camera_z = st.slider("Posição Z", 0.5, 3.0, 1.5, 0.1)
    
    if st.button("🔄 Resetar Câmera"):
        camera_x = 1.5
        camera_y = -1.5
        camera_z = 1.5

# ==========================================
# ÁREA PRINCIPAL - GRÁFICO
# ==========================================
with col2:
    # Preparar configurações
    config = {
        'titulo': titulo,
        'cor_unica': cor_unica,
        'cor_barras': cor_barras,
        'opacidade': opacidade,
        'mostrar_grid': mostrar_grid,
        'altura_grafico': altura_grafico,
        'camera_x': camera_x,
        'camera_y': camera_y,
        'camera_z': camera_z
    }
    
    # Criar e exibir gráfico
    try:
        fig = criar_grafico_3d(df, config)
        st.plotly_chart(fig, use_container_width=True)
        
        # Estatísticas
        st.markdown("---")
        col_stat1, col_stat2, col_stat3, col_stat4 = st.columns(4)
        
        with col_stat1:
            st.metric("Total de Itens", len(df))
        with col_stat2:
            st.metric("Valor Máximo", f"{df['Valor'].max():.0f}")
        with col_stat3:
            st.metric("Valor Mínimo", f"{df['Valor'].min():.0f}")
        with col_stat4:
            st.metric("Média", f"{df['Valor'].mean():.1f}")
        
        # Download
        st.markdown("---")
        st.subheader("💾 Exportar")
        
        # Botão para download do HTML
        html_str = fig.to_html(include_plotlyjs='cdn')
        st.download_button(
            label="📥 Baixar como HTML",
            data=html_str,
            file_name="grafico_3d.html",
            mime="text/html"
        )
        
    except Exception as e:
        st.error(f"❌ Erro ao criar gráfico: {e}")
        st.info("Por favor, verifique se os dados estão no formato correto.")

# ==========================================
# RODAPÉ
# ==========================================
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: gray;'>
        Dashboard 3D Interativo | Desenvolvido com Streamlit e Plotly
    </div>
    """,
    unsafe_allow_html=True
)
