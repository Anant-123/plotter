import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Set page configuration
st.set_page_config(page_title='Dynamic Excel Plotter', layout='wide', initial_sidebar_state='expanded')

# Sidebar info
st.sidebar.title("About 📘")
st.sidebar.info("Upload an Excel file, visualize its data dynamically.")

# Main content
st.title('Dynamic Excel Plotter 📈')
st.subheader('Upload your Excel file and choose visualization settings! ')

uploaded_file = st.file_uploader('Choose an XLSX file 📁', type='xlsx')

if uploaded_file:
    st.markdown('---')
    df = pd.read_excel(uploaded_file, engine='openpyxl')
    st.dataframe(df.style.highlight_max(axis=0))
    
    st.markdown('### Data Analysis 🔍')
    available_columns = df.columns.tolist()
    numerical_columns = df.select_dtypes(include=['number']).columns.tolist()
    
    if numerical_columns:
        x_axis_column = st.selectbox('Select X-axis column:', available_columns)
        y_axis_columns = st.multiselect('Select Y-axis columns for visualization 📊:', numerical_columns)
        line_columns = st.multiselect('Select columns for Line plot:', y_axis_columns)
        bar_columns = [col for col in y_axis_columns if col not in line_columns]
        
        if y_axis_columns:
            df[y_axis_columns] = df[y_axis_columns].apply(pd.to_numeric, errors='coerce')
            df = df.dropna(subset=y_axis_columns)
            
            fig = go.Figure()
            for col in line_columns:
                fig.add_trace(go.Scatter(x=df[x_axis_column], y=df[col], mode='lines+markers+text', name=col, text=df[col].astype(str), textposition='top center'))
            for col in bar_columns:
                fig.add_trace(go.Bar(x=df[x_axis_column], y=df[col], name=col, text=df[col].astype(str), textposition='auto'))
            
            fig.update_layout(title='Visualization', template='plotly_dark', xaxis_title=x_axis_column, yaxis_title='Values')
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Please select at least one column for visualization.")
    else:
        st.warning("No numerical columns found in the uploaded file.")
