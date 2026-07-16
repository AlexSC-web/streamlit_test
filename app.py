import pandas as pd
import scipy.stats
import streamlit as st
import time

# 1. Variables de estado (La memoria de la app)
if 'experiment_no' not in st.session_state:
    st.session_state['experiment_no'] = 0

if 'df_experiment_results' not in st.session_state:
    st.session_state['df_experiment_results'] = pd.DataFrame(columns=['no', 'iteraciones', 'media'])

st.header('Lanzar una moneda')

# 2. Reemplazamos el gráfico directo por un contenedor dinámico para evitar el error de add_rows
chart_placeholder = st.empty()

def toss_coin(n):
    trial_outcomes = scipy.stats.bernoulli.rvs(p=0.5, size=n)

    mean = None
    outcome_no = 0
    outcome_1_count = 0
    history = [0.5]  # Punto inicial de la gráfica

    for r in trial_outcomes:
        outcome_no += 1
        if r == 1:
            outcome_1_count += 1
        mean = outcome_1_count / outcome_no
        
        # Guardamos en el historial y redibujamos en el contenedor
        history.append(mean)
        chart_placeholder.line_chart(history)
        
        time.sleep(0.05)

    return mean

# Interfaz de usuario
number_of_trials = st.slider('¿Número de intentos?', 1, 1000, 10)
start_button = st.button('Ejecutar')

# 3. Lógica del experimento (Tu estructura original corregida)
if start_button:
    st.write(f'Experimento con {number_of_trials} intentos en curso.')
    st.session_state['experiment_no'] += 1
    
    # Se ejecuta la animación en el contenedor
    mean = toss_coin(number_of_trials)
    
    # Concatenación y reinicio de índice tal como lo diseñaste
    st.session_state['df_experiment_results'] = pd.concat([
        st.session_state['df_experiment_results'],
        pd.DataFrame(data=[[st.session_state['experiment_no'],
                            number_of_trials,
                            mean]],
                     columns=['no', 'iteraciones', 'media'])
        ],
        axis=0)
    st.session_state['df_experiment_results'] = st.session_state['df_experiment_results'].reset_index(drop=True)

# 4. Mostramos el DataFrame histórico
st.write(st.session_state['df_experiment_results'])