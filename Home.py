import streamlit as st
import pandas as pd

plt.rcParams['text.usetex'] = True

# Callback functions
if 'clicked_geo' not in st.session_state:
    st.session_state.clicked_geo = False

def click_button_geo():
    st.session_state.clicked_geo = True

if 'r_text' not in st.session_state:
    st.session_state.r_text = '1/2'

if 'clicked_p' not in st.session_state:
    st.session_state.clicked_p = False

def click_button_p():
    st.session_state.clicked_p = True

if 'p_text' not in st.session_state:
    st.session_state.p_text = '1/2'

# Variables
choices = ['Geometric', 'P-Series']
df = pd.DataFrame(columns=['i', 'i-th Partial Sum'])

# Math functions
def geo_partial_sum(a,r,i):
    return a * ((1-(r**(i+1))) / (1-r))

def p_partial_sum(p,i):
    s = 0
    for t in range(i):
        s += 1/((t+1)**p)
    return s

##########

# Title
st.title('Diving into Infinity! 🤿')
st.write('Get your math goggles on as we\'ll explore two famous infinite series! How this works: Choose a series, enter your parameters, and click the \'Investigate\' button!')

with st.container(border=True):
    choice = st.radio('Choose the type of your series!', choices, index=None)

# Choice
with st.container(border=True):
    if choice == 'Geometric':
        # Input
        a = st.number_input('What is the first term of your series?', value=1)
        st.session_state.r_text = st.text_input('What is the common ratio of your series? Fraction or decimal is alright!', st.session_state.r_text)

        # Expression
        st.latex(r'''
            a + ar + a r^2 + a r^3 + \cdots + a r^{n-1} =
            \sum_{k=0}^{n-1} ar^k =
            a \left(\frac{1-r^{n}}{1-r}\right)
            ''')
    
    if choice == 'P-Series':
        # Input 
        st.session_state.p_text = st.text_input('What is the p of your series? Fraction or decimal is alright!', st.session_state.p_text)

        # Expression
        st.latex(r'''
        \frac{1}{1^p} + \frac{1}{2^p} + \frac{1}{3^p} + \cdots + \frac{1}{n^p} = 
        \sum_{n=1}^{\infty}\frac{1}{n^p}
        ''')

if choice == 'Geometric':
    st.button('Investigate my series', on_click=click_button_geo)
    if st.session_state.clicked_geo:
        with st.container(border=True):
            try:
                r = float(st.session_state.r_text) if st.session_state.r_text.find('/') == -1 else int(st.session_state.r_text.split('/')[0])/int(st.session_state.r_text.split('/')[-1])
            except ValueError:
                st.warning('Please enter your input correctly and try again! Examples include 2/3 or 0.5')
            for i in range(3):
                row = {'i':i+1, 'i-th Partial Sum': geo_partial_sum(a,r,i)}
                df.loc[len(df.index)] = row

            calculate = st.slider('Find the i-th partial sum! Do you think your series converges?', 3)
            if calculate > len(df.index):
                for i in range(4,calculate+1):
                    row = {'i':i+1, 'i-th Partial Sum': geo_partial_sum(a,r,i)}
                    df.loc[len(df.index)] = row   
            else:
                df = df.iloc[:calculate+1]

        with st.container(border=True):
            col1, col2 = st.columns([0.3,0.7])
            # Table
            with col1:
                st.dataframe(df, hide_index=True)

            # Graph
            with col2:
                with st.container(border=True):    
                    st.line_chart(data=df, x='i', y='i-th Partial Sum')

if choice == 'P-Series':
    st.button('Investigate my series', on_click=click_button_p)
    if st.session_state.clicked_p:
        with st.container(border=True):
            try:
                p = float(st.session_state.p_text) if st.session_state.p_text.find('/') == -1 else int(st.session_state.p_text.split('/')[0])/int(st.session_state.p_text.split('/')[-1])
            except ValueError:
                st.warning('Please enter your input correctly and try again! Examples include 2/3 or 0.5')
            for i in range(0,3):
                row = {'i':i+1, 'i-th Partial Sum': p_partial_sum(p,i+1)}
                df.loc[len(df.index)] = row

            calculate = st.slider('Find the i-th partial sum! Do you think your series converges?', 3)
            if calculate > len(df.index):
                for i in range(4,calculate+1):
                    row = {'i':i+1, 'i-th Partial Sum': p_partial_sum(p,i+1)}
                    df.loc[len(df.index)] = row   
            else:
                df = df.iloc[:calculate+1]

        with st.container(border=True):
            col1, col2 = st.columns([0.3,0.7])
            # Table
            with col1:
                st.dataframe(df, hide_index=True)

            # Graph
            with col2:
                with st.container(border=True):    
                    st.line_chart(data=df, x='i', y='i-th Partial Sum')