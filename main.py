import streamlit as st
from PIL import Image
import pandas as pd
import datetime
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go

#---Page Config---#
st.set_page_config(page_title = 'Personal Finances Application',
                   page_icon = ':chart:',
                   layout = 'wide',
                   menu_items = {'About': 'https://github.com/TheStructureNavigator'}
                   )

#---Header Logo---#
header_logo = Image.open('icons/Header.png')
st.image(header_logo, 
        use_column_width = True)

#---Columns---#
col1, col2, col3 = st.columns([1, 3, 1])

# ---loader---#
with col1:

    # ---loader Text---#
    st.write(
        """
        <div class='bordered-box1'>
            <h1 class='centered-text1'>
            In order to ensure proper functionality, 
            it is necessary to provide a data with an 
            appropriate structure. 
            <br><br>
            Provided dataframe must have these columns:
            <br>
            - Transaction Date
            <br>
            - Contractor
            <br>
            - Title
            <br>
            - Transaction Amount
            <br>
            - Balance
            </h1>
        </div>
        """,
        unsafe_allow_html = True
    )
    #---File Loader---#
    st.write("""
            <div style="text-align: center;">
                <h5>Load Prepared Data</h5>
            </div>
            """,
            unsafe_allow_html=True)
    
    loaded_file = st.file_uploader(label = 'Load Prepared Data', 
                                   label_visibility = 'collapsed',
                                   accept_multiple_files = False)


if loaded_file is not None:

    loaded_df = pd.read_csv(loaded_file)

    if 'Transaction Date' in loaded_df.columns:
        loaded_df = loaded_df.set_index('Transaction Date')

    #---Initialize session state---#
    if 'loaded_df' not in st.session_state:
        st.session_state['loaded_df'] = pd.DataFrame()

        #---Update session state---#
        st.session_state['editable_df'] = loaded_df.copy()

    if 'editable_df' not in st.session_state:
        st.session_state['editable_df'] = pd.DataFrame()

    #---Update session state---#
    st.session_state['loaded_df'] = loaded_df

    #---Dataframe---#
    with col2:
        st.dataframe(st.session_state['editable_df'],
                     height = 560,
                     use_container_width = True,
                     )
    
    #---Methods---#
    with col3:

        st.write("""
            <div class='bordered-box3'>
                <h1 class='centered-text3'>
                Methods
                </h1>
            </div>
            """,
            unsafe_allow_html = True)
        
        methods = st.radio(label = 'Methods',
                 label_visibility = 'collapsed',
                 options = ['Filtering Methods', 
                            'Sorting Methods'],
                 horizontal = True)

        if methods == 'Filtering Methods':
        
            st.write("""
                <div style="text-align: left;">
                    <h5>Filter By:</h5>
                </div>
                """,
                unsafe_allow_html = True)
            
            filter_by = st.selectbox(label = 'Filter By',
                                    label_visibility = 'collapsed',
                        options = ['Transaction Date',
                                    'Contractor',
                                    'Title',
                                    'Transaction Amount',
                                    'Balance'])

            if filter_by == 'Transaction Date':
                
                st.write("""
                <div style="text-align: left;">
                    <h5>Provide Date Range Or Date Element:</h5>
                </div>
                """,
                unsafe_allow_html = True)

                min_date = datetime.strptime(loaded_df.index.min(), '%Y-%m-%d')
                max_date = datetime.strptime(loaded_df.index.max(), '%Y-%m-%d')

                date_input = st.date_input(label = 'Date Range',
                                        label_visibility = 'visible',
                                        value = (min_date, max_date),
                                        min_value = min_date,
                                        max_value = max_date)
                
                date_string_input = st.text_input(label = 'Date Element (lowercased)',
                                            label_visibility = 'visible')
                
                if st.button(label = 'Confirm'):
                    
                    #---Filtering By Date Range---#
                    st.session_state['editable_df'] = loaded_df.loc[date_input[1].strftime('%Y-%m-%d'):date_input[0].strftime('%Y-%m-%d')]
                    
                    #---Filtering By String---#
                    date_string_mask = st.session_state['editable_df'].index.str.lower().str.contains(date_string_input)
                    st.session_state['editable_df'] = st.session_state['editable_df'][date_string_mask]

                    #---Rerun---#
                    st.experimental_rerun()

            elif filter_by == 'Contractor':    

                st.write("""
                <div style="text-align: left;">
                    <h5>Provide Contractor Element:</h5>
                </div>
                """,
                unsafe_allow_html = True)

                contractor_string_input = st.text_input(label = 'Contractor Element (lowercased)',
                                            label_visibility = 'visible')
                
                if st.button(label = 'Confirm'):
                    
                    #---Filtering By String---#
                    contractor_string_mask = st.session_state['editable_df']['Contractor'].str.lower().str.contains(contractor_string_input)
                    st.session_state['editable_df'] = st.session_state['editable_df'][contractor_string_mask]

                    #---Rerun---#
                    st.experimental_rerun()

            elif filter_by == 'Title':

                st.write("""
                <div style="text-align: left;">
                    <h5>Provide Title Element:</h5>
                </div>
                """,
                unsafe_allow_html = True)

                title_string_input = st.text_input(label = 'Title Element (lowercased)',
                                            label_visibility = 'visible')
                
                if st.button(label = 'Confirm'):
                    
                    #---Filtering By String---#
                    title_string_mask = st.session_state['editable_df']['Title'].str.lower().str.contains(title_string_input)
                    st.session_state['editable_df'] = st.session_state['editable_df'][title_string_mask]

                    #---Rerun---#
                    st.experimental_rerun()

            elif filter_by == 'Transaction Amount':   
                
                st.write("""
                <div style="text-align: left;">
                    <h5>Choose Filter Type:</h5>
                </div>
                """,
                unsafe_allow_html = True)

                filter_type = st.radio(label = 'Filter Type',
                                       label_visibility = 'collapsed',
                                       options = ['Exact', 
                                                  'Greater Than', 
                                                  'Less Than', 
                                                  'Range'],
                                                  horizontal = True)
                
                if filter_type == 'Exact':

                    st.write("""
                    <div style="text-align: left;">
                    <h5>Provide Exact Transaction Value:</h5>
                    </div>
                    """,
                    unsafe_allow_html = True)

                    income_outcome = st.radio(label = 'Income/Outcome', 
                                              label_visibility = 'collapsed', 
                                              options = ['Income', 
                                                         'Outcome'], 
                                                         horizontal = True)

                    exact_value_input = st.text_input(label = 'Exact Value',
                                            label_visibility = 'visible')
                    
                    if st.button(label = 'Confirm'):

                        if income_outcome == 'Income':
                    
                            #---Filtering By Exact Value---#
                            exact_value_mask = st.session_state['editable_df']['Transaction Amount'] == float(exact_value_input)
                            st.session_state['editable_df'] = st.session_state['editable_df'].loc[exact_value_mask]

                        if income_outcome == 'Outcome':

                            #---Filtering By Exact Value---#
                            exact_value_mask = st.session_state['editable_df']['Transaction Amount'] == float(exact_value_input) * -1
                            st.session_state['editable_df'] = st.session_state['editable_df'].loc[exact_value_mask]

                        #---Rerun---#
                        st.experimental_rerun()
                    
                if filter_type == 'Greater Than':

                    st.write("""
                    <div style="text-align: left;">
                    <h5>Provide Minimum Transaction Value:</h5>
                    </div>
                    """,
                    unsafe_allow_html = True)

                    income_outcome = st.radio(label = 'Income/Outcome', 
                                              label_visibility = 'collapsed', 
                                              options = ['Income', 
                                                         'Outcome'], 
                                                         horizontal = True)
                
                    greaterthan_value_input = st.text_input(label = 'Values Greater Than',
                                            label_visibility = 'visible')
                    
                    if st.button(label = 'Confirm'):
                        
                        if income_outcome == 'Income':

                            #---Filtering Values Greater Than---#
                            greaterthan_value_mask = st.session_state['editable_df']['Transaction Amount'] >= float(greaterthan_value_input)
                            st.session_state['editable_df'] = st.session_state['editable_df'].loc[greaterthan_value_mask]

                        if income_outcome == 'Outcome':

                            #---Filtering Values Greater Than---#
                            greaterthan_value_mask = st.session_state['editable_df']['Transaction Amount'] <= float(greaterthan_value_input) * -1
                            st.session_state['editable_df'] = st.session_state['editable_df'].loc[greaterthan_value_mask]

                        #---Rerun---#
                        st.experimental_rerun()
                
                if filter_type == 'Less Than':

                    st.write("""
                    <div style="text-align: left;">
                    <h5>Provide Maximum Transaction Value:</h5>
                    </div>
                    """,
                    unsafe_allow_html = True)

                    income_outcome = st.radio(label = 'Methods', 
                                              label_visibility = 'collapsed', 
                                              options = ['Income', 
                                                         'Outcome'], 
                                                         horizontal = True)
                    
                    lessthan_value_input = st.text_input(label = 'Values Less Than',
                                            label_visibility = 'visible')
                    
                    if st.button(label = 'Confirm'):
                    
                        if income_outcome == 'Income':

                            #---Filtering Values Less Than---#
                            incomes_mask = st.session_state['editable_df']['Transaction Amount'] > 0
                            incomes = st.session_state['editable_df'].loc[incomes_mask]

                            lessthan_value_mask = incomes['Transaction Amount'] <= float(lessthan_value_input)
                            st.session_state['editable_df'] = incomes.loc[lessthan_value_mask]

                        if income_outcome == 'Outcome':

                            #---Filtering Values Less Than---#
                            outcomes_mask = st.session_state['editable_df']['Transaction Amount'] < 0
                            outcomes = st.session_state['editable_df'].loc[outcomes_mask]

                            lessthan_value_mask = outcomes['Transaction Amount'] >= float(lessthan_value_input) * -1
                            st.session_state['editable_df'] = outcomes.loc[lessthan_value_mask]

                        #---Rerun---#
                        st.experimental_rerun()

                if filter_type == 'Range':

                    st.write("""
                    <div style="text-align: left;">
                    <h5>Provide Transaction Values Range:</h5>
                    </div>
                    """,
                    unsafe_allow_html = True)

                    income_outcome = st.radio(label = 'Methods', 
                                              label_visibility = 'collapsed', 
                                              options = ['Income', 
                                                         'Outcome'], 
                                                         horizontal = True)

                    rangecol1, rangecol2 = st.columns([1, 1])

                    with rangecol1:
                        
                        range1_value_input = st.text_input(label = 'Values More Than',
                                            label_visibility = 'visible')
                    
                    with rangecol2:
                        
                        range2_value_input = st.text_input(label = 'Values Less Than',
                                            label_visibility = 'visible')
                    
                    if st.button(label = 'Confirm'):

                        if income_outcome == 'Income':
                    
                            #---Filtering By Values Range---#
                            incomes_mask = st.session_state['editable_df']['Transaction Amount'] > 0
                            incomes = st.session_state['editable_df'].loc[incomes_mask]

                            range_value_mask = (incomes['Transaction Amount'] >= float(range1_value_input)) & (incomes['Transaction Amount'] <= float(range2_value_input))
                            st.session_state['editable_df'] = incomes.loc[range_value_mask]

                        if income_outcome == 'Outcome':

                            #---Filtering By Values Range---#
                            outcomes_mask = st.session_state['editable_df']['Transaction Amount'] < 0
                            outcomes = st.session_state['editable_df'].loc[outcomes_mask]

                            range_value_mask = (outcomes['Transaction Amount'] <= float(range1_value_input) * -1) & (outcomes['Transaction Amount'] >= float(range2_value_input) * -1)
                            st.session_state['editable_df'] = outcomes.loc[range_value_mask]

                        #---Rerun---#
                        st.experimental_rerun()

            elif filter_by == 'Balance':

                st.write("""
                <div style="text-align: left;">
                    <h5>Choose Filter Type:</h5>
                </div>
                """,
                unsafe_allow_html = True)

                filter_type = st.radio(label = 'Filter Type',
                                       label_visibility = 'collapsed',
                                       options = ['Exact', 
                                                  'Greater Than', 
                                                  'Less Than', 
                                                  'Range'],
                                                  horizontal = True)
                
                if filter_type == 'Exact':

                    st.write("""
                    <div style="text-align: left;">
                    <h5>Provide Exact Balance Value:</h5>
                    </div>
                    """,
                    unsafe_allow_html = True)

                    exact_value_input = st.text_input(label = 'Exact Value',
                                            label_visibility = 'visible')
                    
                    if st.button(label = 'Confirm'):
                    
                        #---Filtering By Exact Value---#
                        exact_value_mask = st.session_state['editable_df']['Balance'] == float(exact_value_input)
                        st.session_state['editable_df'] = st.session_state['editable_df'].loc[exact_value_mask]

                        #---Rerun---#
                        st.experimental_rerun()
                    
                if filter_type == 'Greater Than':

                    st.write("""
                    <div style="text-align: left;">
                    <h5>Provide Minimum Balance Value:</h5>
                    </div>
                    """,
                    unsafe_allow_html = True)

                    greaterthan_value_input = st.text_input(label = 'Values Greater Than',
                                            label_visibility = 'visible')
                    
                    if st.button(label = 'Confirm'):
                        
                        #---Filtering Values Greater Than---#
                        greaterthan_value_mask = st.session_state['editable_df']['Balance'] >= float(greaterthan_value_input)
                        st.session_state['editable_df'] = st.session_state['editable_df'].loc[greaterthan_value_mask]

                        #---Rerun---#
                        st.experimental_rerun()
                
                if filter_type == 'Less Than':

                    st.write("""
                    <div style="text-align: left;">
                    <h5>Provide Maximum Balance Value:</h5>
                    </div>
                    """,
                    unsafe_allow_html = True)
                    
                    lessthan_value_input = st.text_input(label = 'Values Less Than',
                                            label_visibility = 'visible')
                    
                    if st.button(label = 'Confirm'):
                    
                        #---Filtering Values Less Than---#
                        lessthan_value_mask = st.session_state['editable_df']['Balance'] <= float(lessthan_value_input)
                        st.session_state['editable_df'] = st.session_state['editable_df'].loc[lessthan_value_mask]

                        #---Rerun---#
                        st.experimental_rerun()

                if filter_type == 'Range':

                    st.write("""
                    <div style="text-align: left;">
                    <h5>Provide Balance Values Range:</h5>
                    </div>
                    """,
                    unsafe_allow_html = True)

                    rangecol1, rangecol2 = st.columns([1, 1])

                    with rangecol1:
                        
                        range1_value_input = st.text_input(label = 'Values More Than',
                                            label_visibility = 'visible')
                    
                    with rangecol2:
                        
                        range2_value_input = st.text_input(label = 'Values Less Than',
                                            label_visibility = 'visible')
                    
                    if st.button(label = 'Confirm'):

                        #---Filtering By Values Range---#
                        range_value_mask = (st.session_state['editable_df']['Balance'] >= float(range1_value_input)) & (st.session_state['editable_df']['Balance'] <= float(range2_value_input))
                        st.session_state['editable_df'] = st.session_state['editable_df'].loc[range_value_mask]

                        #---Rerun---#
                        st.experimental_rerun()

        if methods == 'Sorting Methods':

            st.write("""
                <div style="text-align: left;">
                    <h5>Sort By:</h5>
                </div>
                """,
                unsafe_allow_html = True)
            
            sort_by = st.selectbox(label = 'Sort By',
                                    label_visibility = 'collapsed',
                        options = ['Transaction Date',
                                    'Contractor',
                                    'Title',
                                    'Transaction Amount',
                                    'Balance'])
            
            sort_type = st.radio(label = 'Sort Type',
                                 label_visibility = 'collapsed',
                                 options = ['Ascending', 
                                            'Descending'],
                                 horizontal = True)
            
            if st.button(label = 'Confirm'):
                        
                if sort_type == 'Ascending':
                    st.session_state['editable_df'] = st.session_state['editable_df'].sort_values(by = sort_by,
                                                                                                  ascending = True)
                if sort_type == 'Descending':
                    st.session_state['editable_df'] = st.session_state['editable_df'].sort_values(by = sort_by,
                                                                                                  ascending = False)
                #---Rerun---#
                st.experimental_rerun()
            


        reset_df = st.button(label = 'Reset Methods',
                use_container_width = True)

        if reset_df:

            #---Reset Dataframe---#
            st.session_state['editable_df'] = loaded_df

            #---Rerun---#
            st.experimental_rerun()

    tab1, tab2 = st.tabs(['Total Transactions', 'Contractors'])

    
    col7, col8, col9 = st.columns([0.2, 0.2, 0.2])

    with tab1:

        col4, col5, col6 = st.columns([0.2, 0.2, 0.2])

        with col4:
            
            net_sum = st.session_state['editable_df']['Transaction Amount'].sum()

            if net_sum > 0:
                st.metric(label = 'Total Transactions',
                        value = len(st.session_state.editable_df),
                        delta = f'Net Transaction Total: {net_sum:.2f}')
            
            else:
                st.metric(label = 'Total Transactions',
                        value = len(st.session_state.editable_df),
                        delta = f'Net Transaction Sum: {net_sum:.2f}',
                        delta_color = 'inverse')
            
        with col5:

            income = st.session_state['editable_df'].loc[st.session_state['editable_df']['Transaction Amount'] >= 0]
            income_sum = income['Transaction Amount'].sum()

            st.metric(label = 'Total Incomes',
                    value = len(income),
                    delta = f'Income Sum: {income_sum:.2f}')
            
        with col6:

            outcome = st.session_state['editable_df'].loc[st.session_state['editable_df']['Transaction Amount'] <= 0]
            outcome_sum = outcome['Transaction Amount'].sum()

            st.metric(label = 'Total Outcomes',
                    value = len(outcome),
                    delta = f'Outcome Sum: {outcome_sum:.2f}',
                    delta_color = 'inverse')

        col7, col8, col9 = st.columns ([0.6, 0.2, 0.2])

        with col7:

            # Create the line plot
            fig = go.Figure(data=go.Scatter(
            x = st.session_state['editable_df'].index,
            y = st.session_state['editable_df']['Balance'],
            mode = 'lines',
            line = dict(
                #color = 'black',  # Line color
                width = 2,  # Line width
                dash = 'solid'  # Line style ('solid', 'dash', 'dot', 'dashdot')
            ),
            marker = dict(
                symbol = 'circle',  # Marker symbol ('circle', 'square', 'diamond', 'cross', etc.)
                size = 6,  # Marker size
                #color = 'red',  # Marker color
                line = dict(
                    #color = 'black',  # Marker border color
                    width = 2  # Marker border width
                )
            )
        ))

            # Customize the layout
            fig.update_layout(
                title='Account Balance',
                yaxis_title='Balance',
                xaxis=dict(
                    title = 'Date',
                    tickformat = '%Y-%m-%d',  # Format for x-axis tick labels (e.g., YYYY-MM-DD)
                    showgrid = True,
                    gridcolor = 'lightgray'
                ),
                yaxis = dict(
                    title = 'Balance',
                    showgrid = True,
                    gridcolor = 'lightgray',
                    gridwidth = 0.8
                )
            )

            st.plotly_chart(fig, theme = 'streamlit', use_container_width = True)

        with col8:

            # Create the line plot
            fig = go.Figure(data=go.Bar(
            x = st.session_state['editable_df']['Transaction Amount'].groupby('Transaction Date').sum().index,
            y = st.session_state['editable_df']['Transaction Amount'].groupby('Transaction Date').sum().values,
            marker = dict(#color = 'black',  # Set the color of the bars
                          opacity = 0.8  # Set the opacity of the bars
                        )))

            # Customize the layout
            fig.update_layout(
                title='Sum of Transactions',
                bargap = 0.1,
                xaxis=dict(
                    tickformat = '%Y-%m-%d',  # Format for x-axis tick labels (e.g., YYYY-MM-DD)
                    showgrid = True,
                    gridcolor = 'lightgray'
                ),
                yaxis = dict(
                    showgrid = True,
                    gridcolor = 'lightgray',
                    gridwidth = 0.8
                )
            )


            st.plotly_chart(fig, theme = 'streamlit', use_container_width = True)

        with col9:

            # Create the line plot
            fig = go.Figure(data=go.Bar(
            x = st.session_state['editable_df']['Transaction Amount'].groupby('Transaction Date').size().index,
            y = st.session_state['editable_df']['Transaction Amount'].groupby('Transaction Date').size().values,
            marker = dict(#color = 'black',  # Set the color of the bars
                          opacity = 0.8  # Set the opacity of the bars
                        )))

            # Customize the layout
            fig.update_layout(
                title='Number of Transactions',
                bargap = 0.1,
                xaxis=dict(
                    tickformat = '%Y-%m-%d',  # Format for x-axis tick labels (e.g., YYYY-MM-DD)
                    showgrid = True,
                    gridcolor = 'lightgray'
                ),
                yaxis = dict(
                    showgrid = True,
                    gridcolor = 'lightgray',
                    gridwidth = 0.8
                )
            )


            st.plotly_chart(fig, theme = 'streamlit', use_container_width = True)

    with tab2:

        col10, col11 = st.columns([0.2, 0.4])

        with col10:

            num_of_contr = st.session_state['editable_df']['Contractor'].nunique()

            st.metric(label = 'Number of  Unique Contractors',
                    value = num_of_contr)
            
            # Create bar plot
            fig = go.Figure(data=go.Bar(
            x = abs(st.session_state['editable_df'].groupby('Contractor')['Transaction Amount'].sum()).sort_values(ascending = False).head(10).index,
            y = abs(st.session_state['editable_df'].groupby(['Contractor'])['Transaction Amount'].sum()).sort_values(ascending = False).head(10).values,
            marker = dict(#color = 'black',  # Set the color of the bars
                          opacity = 0.8  # Set the opacity of the bars
                        )))

            # Customize the layout
            fig.update_layout(
                title='Top Contractors',
                bargap = 0.1,
                xaxis=dict(
                    tickformat = '%Y-%m-%d',  # Format for x-axis tick labels (e.g., YYYY-MM-DD)
                    showgrid = True,
                    gridcolor = 'lightgray'
                ),
                yaxis = dict(
                    showgrid = True,
                    gridcolor = 'lightgray',
                    gridwidth = 0.8
                )
            )

            st.plotly_chart(fig, theme = 'streamlit', use_container_width = True)

        with col11:

            
            df = pd.DataFrame(st.session_state['editable_df'].groupby(['Contractor']).size()).rename(columns={0: 'Transaction Count'})
            df['Sum of Transactions'] = st.session_state['editable_df'].groupby(['Contractor'])['Transaction Amount'].sum().values

            contractors = st.dataframe(df,
                     height = 600,
                     use_container_width = True)

else:

    with col2:
        st.write("""
            <div class='bordered-box2'>
                <h1 class='centered-text2'>
                Load data to show content
                </h1>
            </div>
            """,
            unsafe_allow_html = True)
    
    with col3:
        st.write("""
            <div class='bordered-box3'>
                <h1 class='centered-text3'>
                Methods
                </h1>
            </div>
            """,
            unsafe_allow_html = True)

# ---CSS Styling---#

# ---Loader---#
col1.write(
    """
    <style>
    .centered-text1 {
        text-align: left;
        font-size: 20px;
        font-weight: 600;
        padding: 10px;
    }

    .bordered-box1 {
        border: 4px solid black;
        border-radius: 10px;
        padding: 10px;
        margin-bottom: 10px;
        background: '#F0FFFF'
    }
    </style>
    """,
    unsafe_allow_html = True
)

# ---Dataframe---#
col2.write(
    """
    <style>
    .centered-text2 {
        text-align: center;
        font-size: 20px;
        font-weight: 600;
        padding: 10px;
    }

    .bordered-box2 {
        border: 2px solid black;
        border-radius: 20px;
        padding: 230px;
        margin-bottom: 10px;
        background: '#F0FFFF'
    }
    </style>
    """,
    unsafe_allow_html = True
)

# ---Filtering---#
col3.write(
    """
    <style>
    .centered-text3 {
        text-align: center;
        font-size: 20px;
        font-weight: 600;
        padding: 10px;
    }

    .bordered-box3 {
        border: 4px solid black;
        border-radius: 20px;
        padding: 0px;
        margin-bottom: 10px;
        background: '#F0FFFF'
    }
    </style>
    """,
    unsafe_allow_html = True
)

#---Metrics---#
st.write("""
        <style>
        div[data-testid="metric-container"] {
        border: 3px solid rgb(0, 0, 0);
        border-radius: 20px;
        padding: 2% 2% 2% 5%;
        border-radius: 30px;
        overflow-wrap: break-word;
        }

        /* breakline for metric text */
        div[data-testid="metric-container"] > label[data-testid="stMetricLabel"] > div {
        overflow-wrap: break-word;
        white-space: break-spaces;
        }
        </style>
        """
        , unsafe_allow_html=True)

