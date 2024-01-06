import streamlit as st
import pandas as pd
import numpy as np
pip install millify
pip install streamlit_extras.metric_cards
pip install plotly.graph_objects
pip install altair
from millify import millify # shortens values (10_000 ---> 10k)
from streamlit_extras.metric_cards import style_metric_cards # beautify metric card with css
import plotly.graph_objects as go
import altair as alt 
import warnings 
warnings.filterwarnings('ignore')

# Load data
df1 = pd.read_csv('project_data/Shiny.csv')
image = "project_data/CGHPI.png"

# Main page content
st.set_page_config(page_title = 'Haiti HIV Dashboard', page_icon=':bar_chart',layout='wide')
# Use columns for side-by-side layout
col1, col2 = st.columns([1, 8])  # Adjust the width ratio as needed

# Place the image and title in the columns
with col1:
    st.image(image, width=120)

with col2:
    st.title('Haiti HIV Dashboard')
    st.sidebar.title('Choose the variables to help you explore the dashboard')

# Sidebar
with st.sidebar:
    status = st.sidebar.multiselect(label='Treatment Status', options=['Actif', 'PIT'], default=['Actif','PIT'])
    sex = st.sidebar.multiselect(label='Gender', options=['F', 'M'], default=['F','M'])
    age = st.slider(label="Age", min_value=0, max_value=107, value=(0,107), step=1)
    year = st.slider(label="Diagnosis Year", min_value=1990, max_value=2023, value=(1990,2023), step=1)

# Filtered dataset
df = df1[(df1.outcomeStats.isin(status))&(df1.DEM_Sexe.isin(sex))&(df1.DEM_age.between(*age))&(df1.Diag_year.between(*year))]

# Create five new tabs with centered labels
listTabs = ['📖 Introduction', '😷 Patient', '💊 Dispensation', '🏥 Visit', '🥼 Diagnostics']
tab1, tab2, tab3, tab4, tab5 = st.tabs([f'{s}&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;' for s in listTabs])

# Introduction tab
with tab1:
    st.write("Welcome to the Introduction tab!")
    st.write("This dashboard allows you to explore HIV data in Haiti.")
    st.write("You can customize your exploration using the sidebar options.")
    st.write("Feel free to analyze patient data, dispensation records, visit information, and diagnostics.")

# Patient tab
with tab2:
    # creates the container for page title
    dash_1 = st.container()

    with dash_1:
        st.write("Welcome to the Patient tab!")

    # creates the container for metric card
    dash_2 = st.container()
    
    with dash_2:
        # Get Description data
        total_ppl = df['jointID'].count()
        total_actif = df[df.outcomeStats=='Actif']['jointID'].count()
        total_pit = df[df.outcomeStats=='PIT']['jointID'].count()

        col1, col2, col3 = st.columns(3)
        # create column span
        col1.metric(label="Total Patients", value= millify(total_ppl, precision=2))
    
        col2.metric(label="Actif Patients", value= millify(total_actif, precision=2))
    
        col3.metric(label="PIT Patients", value= millify(total_pit, precision=2))
    
        # this is used to style the metric card
        style_metric_cards(border_left_color="#DBF227")
    
    # creates the container for metric card
    dash_3 = st.container()

    with dash_3:
        # create columns for both graphs
        col1, col2 = st.columns(2)
    
        # get the top 10 frequent occupations
        df['Occupation'] = [str(i).capitalize() if not pd.isna(i) else 'Unknown' for i in df.DEM_OccupationCategory]
        df['Occupation'] = [i if i not in ['no data', 'No data'] else 'Unknown' for i in df.Occupation]
    
        top_occupation = df.groupby('Occupation')['jointID'].count()
        top_occupation = top_occupation.nlargest(10)
        top_occupation = pd.DataFrame(top_occupation).reset_index()

        # get the distribution of marital status
        df['Marital'] = [str(i).capitalize() if not pd.isna(i) else 'Unknown' for i in df.DEM_statutMarital]

        top_marital = df.groupby('Marital')['jointID'].count()
        top_marital = pd.DataFrame(top_marital).reset_index()

        # create the altair chart for top occupations
        with col1:
            chart = alt.Chart(top_occupation).mark_bar(opacity=0.9,color="#9FC131").encode(
                    x=alt.X('sum(jointID):Q', title='Number of Patients'),  # Rename x-axis
                    y=alt.Y('Occupation:N', sort='-x', title='Occupation Category')  # Rename y-axis 
                )
            chart = chart.properties(title="Distribution of Top 10 Frequent Occupations" )

            st.altair_chart(chart,use_container_width=True)

        # create the altair chart for marital status
        with col2:
            chart = alt.Chart(top_marital).mark_bar(opacity=0.9,color="#9FC131").encode(
                    x=alt.X('sum(jointID):Q', title='Number of Patiemts'),  # Rename x-axis
                    y=alt.Y('Marital:N', sort='-x', title='Marital Status')  # Rename y-axis
                )
            chart = chart.properties(title="Distribution of Marital Status" )

            st.altair_chart(chart,use_container_width=True)

    # creates the container for metric card
    dash_4 = st.container()

    with dash_4:
        # create columns for both graphs
        col1, col2 = st.columns(2)
    
        # get the distribution of age band    
        top_ageband = df.groupby('DEM_ageBand')['jointID'].count()
        top_ageband = pd.DataFrame(top_ageband).reset_index()

        # get the distribution of diagnosed age band
        top_diaage = df.groupby('DX_ageAtDxBand')['jointID'].count()
        top_diaage = pd.DataFrame(top_diaage).reset_index()

        # create the altair chart for top occupations
        with col1:
            chart = alt.Chart(top_ageband).mark_bar(opacity=0.9,color="#9FC131").encode(
                    x=alt.X('sum(jointID):Q', title='Number of Patients'),  # Rename x-axis
                    y=alt.Y('DEM_ageBand:N', sort='-x', title='Age Band')  # Rename y-axis 
                )
            chart = chart.properties(title="Distribution of Age Band" )

            st.altair_chart(chart,use_container_width=True)

        # create the altair chart for marital status
        with col2:
            chart = alt.Chart(top_diaage).mark_bar(opacity=0.9,color="#9FC131").encode(
                    x=alt.X('sum(jointID):Q', title='Number of Patiemts'),  # Rename x-axis
                    y=alt.Y('DX_ageAtDxBand:N', sort='-x', title='Age Band at Diagnosis')  # Rename y-axis
                )
            chart = chart.properties(title="Distribution of Age Band at Diagnosis" )

            st.altair_chart(chart,use_container_width=True)

    # creates the container for metric card
    dash_5 = st.container()

    with dash_5:
        # create columns for both graphs
        col1, col2 = st.columns([3,4])
    
        # get the distribution of the facility situation
        df['DEM_sameCityFacility'] = df['DEM_sameCityFacility'].fillna('Unknown')
    
        same = df.groupby('DEM_sameCityFacility')['jointID'].count()
        same = pd.DataFrame(same).reset_index()

        # Calculate mean for Actif and PIT groups
        mean_actif = df['DX_yearsSinceDx'][df.outcomeStats == 'Actif'].mean()
        mean_pit = df['DX_yearsSinceDx'][df.outcomeStats == 'PIT'].mean()

        # create the altair chart for top occupations
        with col1:
            chart = alt.Chart(same).mark_bar(opacity=0.9,color="#9FC131").encode(
                    x=alt.X('sum(jointID):Q', title='Number of Patients'),  # Rename x-axis
                    y=alt.Y('DEM_sameCityFacility:N', sort='-x', title='Same City Facility')  # Rename y-axis 
                )
            chart = chart.properties(title="Distribution of Patients' Same City Facility Situation" )

            st.altair_chart(chart,use_container_width=True)

        # create the altair chart for year since diagnosis
        with col2:
            # Create Altair chart
            chart = alt.Chart(df).transform_density(
                'DX_yearsSinceDx',
                as_=['DX_yearsSinceDx', 'density'],
                groupby=['outcomeStats']
            ).mark_area(opacity=0.5).encode(
                x=alt.X('DX_yearsSinceDx:Q', title='Year(s)'),
                y=alt.Y('density:Q', title='Density'),
                color=alt.Color('outcomeStats:N', scale=alt.Scale(domain=['Actif', 'PIT'], range=['lightcoral', 'darkturquoise']))
            ).properties(
                title='Density Plot of Duration since Patients have Diagnosed with HIV'
            )

            # Add vertical lines for means
            vlines = alt.Chart(pd.DataFrame({'mean_actif': [mean_actif], 'mean_pit': [mean_pit]})).mark_rule().encode(
                x='mean_actif:Q',
                size=alt.value(2),
                color=alt.value('lightcoral'),
                strokeDash=alt.value([5, 5])
            ) + alt.Chart(pd.DataFrame({'mean_actif': [mean_actif], 'mean_pit': [mean_pit]})).mark_rule().encode(
                x='mean_pit:Q',
                size=alt.value(2),
                color=alt.value('darkturquoise'),
                strokeDash=alt.value([5, 5])
            )

            # Add text labels for means
            labels = alt.Chart(pd.DataFrame({'mean_actif': [mean_actif], 'mean_pit': [mean_pit]})).mark_text(
                align='left', baseline='middle', dy=-10
            ).encode(
                x='mean_actif:Q',
                y=alt.value(0),
                text=alt.value(f'Actif mean: {mean_actif:.2f} years'),
                color=alt.value('lightcoral')
            ) + alt.Chart(pd.DataFrame({'mean_actif': [mean_actif], 'mean_pit': [mean_pit]})).mark_text(
                align='left', baseline='middle', dy=10
            ).encode(
                x='mean_pit:Q',
                y=alt.value(0),
                text=alt.value(f'PIT mean: {mean_pit:.2f} years'),
                color=alt.value('darkturquoise')
            )

            # Combine all components
            chart = chart + vlines + labels

            # Show the chart
            st.altair_chart(chart, use_container_width=True)


# Dispensation tab
with tab3:
    st.write("Welcome to the Dispensation tab!")

    # creates the container for metric card
    dash_1 = st.container()

    with dash_1:
        # create columns for both graphs
        col1, col2 = st.columns(2)

        # Calculate mean for Actif and PIT groups
        mean_actif = df['DISP_totalNumDispHist'][df.outcomeStats == 'Actif'].mean()
        mean_pit = df['DISP_totalNumDispHist'][df.outcomeStats == 'PIT'].mean()

        # create the altair chart for year since diagnosis
        with col1:
            # Create Altair chart
            chart = alt.Chart(df).transform_density(
                'DISP_totalNumDispHist',
                as_=['DISP_totalNumDispHist', 'density'],
                groupby=['outcomeStats']
            ).mark_area(opacity=0.5).encode(
                x=alt.X('DISP_totalNumDispHist:Q', title='Time(s)'),
                y=alt.Y('density:Q', title='Density'),
                color=alt.Color('outcomeStats:N', scale=alt.Scale(domain=['Actif', 'PIT'], range=['lightcoral', 'darkturquoise']))
            ).properties(
                title='Density Plot of Total Number of Dispensation History'
            )

            # Add vertical lines for means
            vlines = alt.Chart(pd.DataFrame({'mean_actif': [mean_actif], 'mean_pit': [mean_pit]})).mark_rule().encode(
                x='mean_actif:Q',
                size=alt.value(2),
                color=alt.value('lightcoral'),
                strokeDash=alt.value([5, 5])
            ) + alt.Chart(pd.DataFrame({'mean_actif': [mean_actif], 'mean_pit': [mean_pit]})).mark_rule().encode(
                x='mean_pit:Q',
                size=alt.value(2),
                color=alt.value('darkturquoise'),
                strokeDash=alt.value([5, 5])
            )

            # Add text labels for means
            labels = alt.Chart(pd.DataFrame({'mean_actif': [mean_actif], 'mean_pit': [mean_pit]})).mark_text(
                align='left', baseline='middle', dy=-10
            ).encode(
                x='mean_actif:Q',
                y=alt.value(0),
                text=alt.value(f'Actif mean: {mean_actif:.2f} times'),
                color=alt.value('lightcoral')
            ) + alt.Chart(pd.DataFrame({'mean_actif': [mean_actif], 'mean_pit': [mean_pit]})).mark_text(
                align='left', baseline='middle', dy=10
            ).encode(
                x='mean_pit:Q',
                y=alt.value(0),
                text=alt.value(f'PIT mean: {mean_pit:.2f} times'),
                color=alt.value('darkturquoise')
            )

            # Combine all components
            chart = chart + vlines + labels

            # Show the chart
            st.altair_chart(chart, use_container_width=True)

        # Calculate mean for Actif and PIT groups
        mean_actif1 = df['DISP_firstDispDistYrs'][df.outcomeStats == 'Actif'].mean()
        mean_pit1 = df['DISP_firstDispDistYrs'][df.outcomeStats == 'PIT'].mean()

        # create the altair chart for year since diagnosis
        with col2:
            # Create Altair chart
            chart = alt.Chart(df).transform_density(
                'DISP_firstDispDistYrs',
                as_=['DISP_firstDispDistYrs', 'density'],
                groupby=['outcomeStats']
            ).mark_area(opacity=0.5).encode(
                x=alt.X('DISP_firstDispDistYrs:Q', title='Year(s)'),
                y=alt.Y('density:Q', title='Density'),
                color=alt.Color('outcomeStats:N', scale=alt.Scale(domain=['Actif', 'PIT'], range=['lightcoral', 'darkturquoise']))
            ).properties(
                title='Density Plot of Duration since First Dispensation'
            )

            # Add vertical lines for means
            vlines = alt.Chart(pd.DataFrame({'mean_actif1': [mean_actif1], 'mean_pit1': [mean_pit1]})).mark_rule().encode(
                x='mean_actif1:Q',
                size=alt.value(2),
                color=alt.value('lightcoral'),
                strokeDash=alt.value([5, 5])
            ) + alt.Chart(pd.DataFrame({'mean_actif1': [mean_actif1], 'mean_pit1': [mean_pit1]})).mark_rule().encode(
                x='mean_pit1:Q',
                size=alt.value(2),
                color=alt.value('darkturquoise'),
                strokeDash=alt.value([5, 5])
            )

            # Add text labels for means
            labels = alt.Chart(pd.DataFrame({'mean_actif1': [mean_actif1], 'mean_pit1': [mean_pit1]})).mark_text(
                align='left', baseline='middle', dy=-10
            ).encode(
                x='mean_actif1:Q',
                y=alt.value(0),
                text=alt.value(f'Actif mean: {mean_actif1:.2f} years'),
                color=alt.value('lightcoral')
            ) + alt.Chart(pd.DataFrame({'mean_actif1': [mean_actif1], 'mean_pit1': [mean_pit1]})).mark_text(
                align='left', baseline='middle', dy=10
            ).encode(
                x='mean_pit1:Q',
                y=alt.value(0),
                text=alt.value(f'PIT mean: {mean_pit1:.2f} years'),
                color=alt.value('darkturquoise')
            )

            # Combine all components
            chart = chart + vlines + labels

            # Show the chart
            st.altair_chart(chart, use_container_width=True)

    # creates the container for metric card
    dash_2 = st.container()

    with dash_2:
        # create columns for both graphs
        col1, col2 = st.columns(2)

        # Calculate mean for Actif and PIT groups
        mean_actif = df['DISP_timeSincePrevDispYrs'][df.outcomeStats == 'Actif'].mean()
        mean_pit = df['DISP_timeSincePrevDispYrs'][df.outcomeStats == 'PIT'].mean()

        # create the altair chart for year since diagnosis
        with col1:
            # Create Altair chart
            chart = alt.Chart(df).transform_density(
                'DISP_timeSincePrevDispYrs',
                as_=['DISP_timeSincePrevDispYrs', 'density'],
                groupby=['outcomeStats']
            ).mark_area(opacity=0.5).encode(
                x=alt.X('DISP_timeSincePrevDispYrs:Q', title='Year(s)'),
                y=alt.Y('density:Q', title='Density'),
                color=alt.Color('outcomeStats:N', scale=alt.Scale(domain=['Actif', 'PIT'], range=['lightcoral', 'darkturquoise']))
            ).properties(
                title='Density Plot of Duration since Previous Dispensation'
            )

            # Add vertical lines for means
            vlines = alt.Chart(pd.DataFrame({'mean_actif': [mean_actif], 'mean_pit': [mean_pit]})).mark_rule().encode(
                x='mean_actif:Q',
                size=alt.value(2),
                color=alt.value('lightcoral'),
                strokeDash=alt.value([5, 5])
            ) + alt.Chart(pd.DataFrame({'mean_actif': [mean_actif], 'mean_pit': [mean_pit]})).mark_rule().encode(
                x='mean_pit:Q',
                size=alt.value(2),
                color=alt.value('darkturquoise'),
                strokeDash=alt.value([5, 5])
            )

            # Add text labels for means
            labels = alt.Chart(pd.DataFrame({'mean_actif': [mean_actif], 'mean_pit': [mean_pit]})).mark_text(
                align='left', baseline='middle', dy=-10
            ).encode(
                x='mean_actif:Q',
                y=alt.value(0),
                text=alt.value(f'Actif mean: {mean_actif:.2f} years'),
                color=alt.value('lightcoral')
            ) + alt.Chart(pd.DataFrame({'mean_actif': [mean_actif], 'mean_pit': [mean_pit]})).mark_text(
                align='left', baseline='middle', dy=10
            ).encode(
                x='mean_pit:Q',
                y=alt.value(0),
                text=alt.value(f'PIT mean: {mean_pit:.2f} years'),
                color=alt.value('darkturquoise')
            )

            # Combine all components
            chart = chart + vlines + labels

            # Show the chart
            st.altair_chart(chart, use_container_width=True)

        # Calculate mean for Actif and PIT groups
        mean_actif1 = df['DISP_numDaysEarlyLate'][df.outcomeStats == 'Actif'].mean()
        mean_pit1 = df['DISP_numDaysEarlyLate'][df.outcomeStats == 'PIT'].mean()

        # create the altair chart for year since diagnosis
        with col2:
            # Create Altair chart
            chart = alt.Chart(df).transform_density(
                'DISP_numDaysEarlyLate',
                as_=['DISP_numDaysEarlyLate', 'density'],
                groupby=['outcomeStats']
            ).mark_area(opacity=0.5).encode(
                x=alt.X('DISP_numDaysEarlyLate:Q', title='Day(s)'),
                y=alt.Y('density:Q', title='Density'),
                color=alt.Color('outcomeStats:N', scale=alt.Scale(domain=['Actif', 'PIT'], range=['lightcoral', 'darkturquoise']))
            ).properties(
                title='Density Plot of Number of Days Early or Late to Pick up Drugs'
            )

            # Add vertical lines for means
            vlines = alt.Chart(pd.DataFrame({'mean_actif1': [mean_actif1], 'mean_pit1': [mean_pit1]})).mark_rule().encode(
                x='mean_actif1:Q',
                size=alt.value(2),
                color=alt.value('lightcoral'),
                strokeDash=alt.value([5, 5])
            ) + alt.Chart(pd.DataFrame({'mean_actif1': [mean_actif1], 'mean_pit1': [mean_pit1]})).mark_rule().encode(
                x='mean_pit1:Q',
                size=alt.value(2),
                color=alt.value('darkturquoise'),
                strokeDash=alt.value([5, 5])
            )

            # Add text labels for means
            labels = alt.Chart(pd.DataFrame({'mean_actif1': [mean_actif1], 'mean_pit1': [mean_pit1]})).mark_text(
                align='left', baseline='middle', dy=-10
            ).encode(
                x='mean_actif1:Q',
                y=alt.value(0),
                text=alt.value(f'Actif mean: {mean_actif1:.2f} days'),
                color=alt.value('lightcoral')
            ) + alt.Chart(pd.DataFrame({'mean_actif1': [mean_actif1], 'mean_pit1': [mean_pit1]})).mark_text(
                align='left', baseline='middle', dy=10
            ).encode(
                x='mean_pit1:Q',
                y=alt.value(0),
                text=alt.value(f'PIT mean: {mean_pit1:.2f} days'),
                color=alt.value('darkturquoise')
            )

            # Combine all components
            chart = chart + vlines + labels

            # Show the chart
            st.altair_chart(chart, use_container_width=True)

    # creates the container for metric card
    dash_3 = st.container()

    with dash_3:
        # create columns for both graphs
        col1, col2 = st.columns(2)

        # Calculate mean for Actif and PIT groups
        mean_actif = df['DISP_averageDaysDispenseDelay'][df.outcomeStats == 'Actif'].mean()
        mean_pit = df['DISP_averageDaysDispenseDelay'][df.outcomeStats == 'PIT'].mean()

        # create the altair chart for year since diagnosis
        with col1:
            # Create Altair chart
            chart = alt.Chart(df).transform_density(
                'DISP_averageDaysDispenseDelay',
                as_=['DISP_averageDaysDispenseDelay', 'density'],
                groupby=['outcomeStats']
            ).mark_area(opacity=0.5).encode(
                x=alt.X('DISP_averageDaysDispenseDelay:Q', title='Day(s)'),
                y=alt.Y('density:Q', title='Density'),
                color=alt.Color('outcomeStats:N', scale=alt.Scale(domain=['Actif', 'PIT'], range=['lightcoral', 'darkturquoise']))
            ).properties(
                title='Density Plot of Average Dispensation Delay Duration'
            )

            # Add vertical lines for means
            vlines = alt.Chart(pd.DataFrame({'mean_actif': [mean_actif], 'mean_pit': [mean_pit]})).mark_rule().encode(
                x='mean_actif:Q',
                size=alt.value(2),
                color=alt.value('lightcoral'),
                strokeDash=alt.value([5, 5])
            ) + alt.Chart(pd.DataFrame({'mean_actif': [mean_actif], 'mean_pit': [mean_pit]})).mark_rule().encode(
                x='mean_pit:Q',
                size=alt.value(2),
                color=alt.value('darkturquoise'),
                strokeDash=alt.value([5, 5])
            )

            # Add text labels for means
            labels = alt.Chart(pd.DataFrame({'mean_actif': [mean_actif], 'mean_pit': [mean_pit]})).mark_text(
                align='left', baseline='middle', dy=-10
            ).encode(
                x='mean_actif:Q',
                y=alt.value(0),
                text=alt.value(f'Actif mean: {mean_actif:.2f} days'),
                color=alt.value('lightcoral')
            ) + alt.Chart(pd.DataFrame({'mean_actif': [mean_actif], 'mean_pit': [mean_pit]})).mark_text(
                align='left', baseline='middle', dy=10
            ).encode(
                x='mean_pit:Q',
                y=alt.value(0),
                text=alt.value(f'PIT mean: {mean_pit:.2f} days'),
                color=alt.value('darkturquoise')
            )

            # Combine all components
            chart = chart + vlines + labels

            # Show the chart
            st.altair_chart(chart, use_container_width=True)

        # Calculate mean for Actif and PIT groups
        mean_actif1 = df['DISP_pEarlyDisp'][df.outcomeStats == 'Actif'].mean()
        mean_pit1 = df['DISP_pEarlyDisp'][df.outcomeStats == 'PIT'].mean()

        # create the altair chart for year since diagnosis
        with col2:
            # Create Altair chart
            chart = alt.Chart(df).transform_density(
                'DISP_pEarlyDisp',
                as_=['DISP_pEarlyDisp', 'density'],
                groupby=['outcomeStats']
            ).mark_area(opacity=0.5).encode(
                x=alt.X('DISP_pEarlyDisp:Q', title='%'),
                y=alt.Y('density:Q', title='Density'),
                color=alt.Color('outcomeStats:N', scale=alt.Scale(domain=['Actif', 'PIT'], range=['lightcoral', 'darkturquoise']))
            ).properties(
                title='Density Plot of Percentage of Time Patients are Early for Pick-ups'
            )

            # Add vertical lines for means
            vlines = alt.Chart(pd.DataFrame({'mean_actif1': [mean_actif1], 'mean_pit1': [mean_pit1]})).mark_rule().encode(
                x='mean_actif1:Q',
                size=alt.value(2),
                color=alt.value('lightcoral'),
                strokeDash=alt.value([5, 5])
            ) + alt.Chart(pd.DataFrame({'mean_actif1': [mean_actif1], 'mean_pit1': [mean_pit1]})).mark_rule().encode(
                x='mean_pit1:Q',
                size=alt.value(2),
                color=alt.value('darkturquoise'),
                strokeDash=alt.value([5, 5])
            )

            # Add text labels for means
            labels = alt.Chart(pd.DataFrame({'mean_actif1': [mean_actif1], 'mean_pit1': [mean_pit1]})).mark_text(
                align='left', baseline='middle', dy=-10
            ).encode(
                x='mean_actif1:Q',
                y=alt.value(0),
                text=alt.value(f'Actif mean: {mean_actif1:.2f} %'),
                color=alt.value('lightcoral')
            ) + alt.Chart(pd.DataFrame({'mean_actif1': [mean_actif1], 'mean_pit1': [mean_pit1]})).mark_text(
                align='left', baseline='middle', dy=10
            ).encode(
                x='mean_pit1:Q',
                y=alt.value(0),
                text=alt.value(f'PIT mean: {mean_pit1:.2f} %'),
                color=alt.value('darkturquoise')
            )

            # Combine all components
            chart = chart + vlines + labels

            # Show the chart
            st.altair_chart(chart, use_container_width=True)

    # creates the container for metric card
    dash_4 = st.container()

    with dash_4:
        # create columns for both graphs
        col1, col2 = st.columns(2)

        # Calculate mean for Actif and PIT groups
        mean_actif = df['DISP_pOnTimeDisp'][df.outcomeStats == 'Actif'].mean()
        mean_pit = df['DISP_pOnTimeDisp'][df.outcomeStats == 'PIT'].mean()

        # create the altair chart for year since diagnosis
        with col1:
            # Create Altair chart
            chart = alt.Chart(df).transform_density(
                'DISP_pOnTimeDisp',
                as_=['DISP_pOnTimeDisp', 'density'],
                groupby=['outcomeStats']
            ).mark_area(opacity=0.5).encode(
                x=alt.X('DISP_pOnTimeDisp:Q', title='%'),
                y=alt.Y('density:Q', title='Density'),
                color=alt.Color('outcomeStats:N', scale=alt.Scale(domain=['Actif', 'PIT'], range=['lightcoral', 'darkturquoise']))
            ).properties(
                title='Density Plot of Percentage of Time Patients are On Time for Pick-ups'
            )

            # Add vertical lines for means
            vlines = alt.Chart(pd.DataFrame({'mean_actif': [mean_actif], 'mean_pit': [mean_pit]})).mark_rule().encode(
                x='mean_actif:Q',
                size=alt.value(2),
                color=alt.value('lightcoral'),
                strokeDash=alt.value([5, 5])
            ) + alt.Chart(pd.DataFrame({'mean_actif': [mean_actif], 'mean_pit': [mean_pit]})).mark_rule().encode(
                x='mean_pit:Q',
                size=alt.value(2),
                color=alt.value('darkturquoise'),
                strokeDash=alt.value([5, 5])
            )

            # Add text labels for means
            labels = alt.Chart(pd.DataFrame({'mean_actif': [mean_actif], 'mean_pit': [mean_pit]})).mark_text(
                align='left', baseline='middle', dy=-10
            ).encode(
                x='mean_actif:Q',
                y=alt.value(0),
                text=alt.value(f'Actif mean: {mean_actif:.2f} %'),
                color=alt.value('lightcoral')
            ) + alt.Chart(pd.DataFrame({'mean_actif': [mean_actif], 'mean_pit': [mean_pit]})).mark_text(
                align='left', baseline='middle', dy=10
            ).encode(
                x='mean_pit:Q',
                y=alt.value(0),
                text=alt.value(f'PIT mean: {mean_pit:.2f} %'),
                color=alt.value('darkturquoise')
            )

            # Combine all components
            chart = chart + vlines + labels

            # Show the chart
            st.altair_chart(chart, use_container_width=True)

        # Calculate mean for Actif and PIT groups
        mean_actif1 = df['DISP_pLateDisp'][df.outcomeStats == 'Actif'].mean()
        mean_pit1 = df['DISP_pLateDisp'][df.outcomeStats == 'PIT'].mean()

        # create the altair chart for year since diagnosis
        with col2:
            # Create Altair chart
            chart = alt.Chart(df).transform_density(
                'DISP_pLateDisp',
                as_=['DISP_pLateDisp', 'density'],
                groupby=['outcomeStats']
            ).mark_area(opacity=0.5).encode(
                x=alt.X('DISP_pLateDisp:Q', title='%'),
                y=alt.Y('density:Q', title='Density'),
                color=alt.Color('outcomeStats:N', scale=alt.Scale(domain=['Actif', 'PIT'], range=['lightcoral', 'darkturquoise']))
            ).properties(
                title='Density Plot of Percentage of Time Patients are Late for Pick-ups'
            )

            # Add vertical lines for means
            vlines = alt.Chart(pd.DataFrame({'mean_actif1': [mean_actif1], 'mean_pit1': [mean_pit1]})).mark_rule().encode(
                x='mean_actif1:Q',
                size=alt.value(2),
                color=alt.value('lightcoral'),
                strokeDash=alt.value([5, 5])
            ) + alt.Chart(pd.DataFrame({'mean_actif1': [mean_actif1], 'mean_pit1': [mean_pit1]})).mark_rule().encode(
                x='mean_pit1:Q',
                size=alt.value(2),
                color=alt.value('darkturquoise'),
                strokeDash=alt.value([5, 5])
            )

            # Add text labels for means
            labels = alt.Chart(pd.DataFrame({'mean_actif1': [mean_actif1], 'mean_pit1': [mean_pit1]})).mark_text(
                align='left', baseline='middle', dy=-10
            ).encode(
                x='mean_actif1:Q',
                y=alt.value(0),
                text=alt.value(f'Actif mean: {mean_actif1:.2f} %'),
                color=alt.value('lightcoral')
            ) + alt.Chart(pd.DataFrame({'mean_actif1': [mean_actif1], 'mean_pit1': [mean_pit1]})).mark_text(
                align='left', baseline='middle', dy=10
            ).encode(
                x='mean_pit1:Q',
                y=alt.value(0),
                text=alt.value(f'PIT mean: {mean_pit1:.2f} %'),
                color=alt.value('darkturquoise')
            )

            # Combine all components
            chart = chart + vlines + labels

            # Show the chart
            st.altair_chart(chart, use_container_width=True)

    # creates the container for metric card
    dash_5 = st.container()

    with dash_5:
        # create columns for both graphs
        col1, col2 = st.columns(2)

        # Calculate mean for Actif and PIT groups
        mean_actif = df['DISP_daysTilNextDisp'][df.outcomeStats == 'Actif'].mean()
        mean_pit = df['DISP_daysTilNextDisp'][df.outcomeStats == 'PIT'].mean()

        # create the altair chart for year since diagnosis
        with col1:
            # Create Altair chart
            chart = alt.Chart(df).transform_density(
                'DISP_daysTilNextDisp',
                as_=['DISP_daysTilNextDisp', 'density'],
                groupby=['outcomeStats']
            ).mark_area(opacity=0.5).encode(
                x=alt.X('DISP_daysTilNextDisp:Q', title='Day(s)'),
                y=alt.Y('density:Q', title='Density'),
                color=alt.Color('outcomeStats:N', scale=alt.Scale(domain=['Actif', 'PIT'], range=['lightcoral', 'darkturquoise']))
            ).properties(
                title='Density Plot of Duration to Next Dispensation'
            )

            # Add vertical lines for means
            vlines = alt.Chart(pd.DataFrame({'mean_actif': [mean_actif], 'mean_pit': [mean_pit]})).mark_rule().encode(
                x='mean_actif:Q',
                size=alt.value(2),
                color=alt.value('lightcoral'),
                strokeDash=alt.value([5, 5])
            ) + alt.Chart(pd.DataFrame({'mean_actif': [mean_actif], 'mean_pit': [mean_pit]})).mark_rule().encode(
                x='mean_pit:Q',
                size=alt.value(2),
                color=alt.value('darkturquoise'),
                strokeDash=alt.value([5, 5])
            )

            # Add text labels for means
            labels = alt.Chart(pd.DataFrame({'mean_actif': [mean_actif], 'mean_pit': [mean_pit]})).mark_text(
                align='left', baseline='middle', dy=-10
            ).encode(
                x='mean_actif:Q',
                y=alt.value(0),
                text=alt.value(f'Actif mean: {mean_actif:.2f} days'),
                color=alt.value('lightcoral')
            ) + alt.Chart(pd.DataFrame({'mean_actif': [mean_actif], 'mean_pit': [mean_pit]})).mark_text(
                align='left', baseline='middle', dy=10
            ).encode(
                x='mean_pit:Q',
                y=alt.value(0),
                text=alt.value(f'PIT mean: {mean_pit:.2f} days'),
                color=alt.value('darkturquoise')
            )

            # Combine all components
            chart = chart + vlines + labels

            # Show the chart
            st.altair_chart(chart, use_container_width=True)

        # Calculate mean for Actif and PIT groups
        mean_actif1 = df['DISP_aveTimeBetweenDisp'][df.outcomeStats == 'Actif'].mean()
        mean_pit1 = df['DISP_aveTimeBetweenDisp'][df.outcomeStats == 'PIT'].mean()

        # create the altair chart for year since diagnosis
        with col2:
            # Create Altair chart
            chart = alt.Chart(df).transform_density(
                'DISP_aveTimeBetweenDisp',
                as_=['DISP_aveTimeBetweenDisp', 'density'],
                groupby=['outcomeStats']
            ).mark_area(opacity=0.5).encode(
                x=alt.X('DISP_aveTimeBetweenDisp:Q', title='Day(s)'),
                y=alt.Y('density:Q', title='Density'),
                color=alt.Color('outcomeStats:N', scale=alt.Scale(domain=['Actif', 'PIT'], range=['lightcoral', 'darkturquoise']))
            ).properties(
                title='Density Plot of Average Days between Dispensations'
            )

            # Add vertical lines for means
            vlines = alt.Chart(pd.DataFrame({'mean_actif1': [mean_actif1], 'mean_pit1': [mean_pit1]})).mark_rule().encode(
                x='mean_actif1:Q',
                size=alt.value(2),
                color=alt.value('lightcoral'),
                strokeDash=alt.value([5, 5])
            ) + alt.Chart(pd.DataFrame({'mean_actif1': [mean_actif1], 'mean_pit1': [mean_pit1]})).mark_rule().encode(
                x='mean_pit1:Q',
                size=alt.value(2),
                color=alt.value('darkturquoise'),
                strokeDash=alt.value([5, 5])
            )

            # Add text labels for means
            labels = alt.Chart(pd.DataFrame({'mean_actif1': [mean_actif1], 'mean_pit1': [mean_pit1]})).mark_text(
                align='left', baseline='middle', dy=-10
            ).encode(
                x='mean_actif1:Q',
                y=alt.value(0),
                text=alt.value(f'Actif mean: {mean_actif1:.2f} days'),
                color=alt.value('lightcoral')
            ) + alt.Chart(pd.DataFrame({'mean_actif1': [mean_actif1], 'mean_pit1': [mean_pit1]})).mark_text(
                align='left', baseline='middle', dy=10
            ).encode(
                x='mean_pit1:Q',
                y=alt.value(0),
                text=alt.value(f'PIT mean: {mean_pit1:.2f} days'),
                color=alt.value('darkturquoise')
            )

            # Combine all components
            chart = chart + vlines + labels

            # Show the chart
            st.altair_chart(chart, use_container_width=True)

    # creates the container for metric card
    dash_6 = st.container()

    with dash_6:
        # create columns for both graphs
        col1 = st.columns(1)[0]

        # Calculate mean for Actif and PIT groups
        mean_actif = df['DISP_numYearsActiveContinuous'][df.outcomeStats == 'Actif'].mean()
        mean_pit = df['DISP_numYearsActiveContinuous'][df.outcomeStats == 'PIT'].mean()

        # create the altair chart for year since diagnosis
        with col1:
            # Create Altair chart
            chart = alt.Chart(df).transform_density(
                'DISP_numYearsActiveContinuous',
                as_=['DISP_numYearsActiveContinuous', 'density'],
                groupby=['outcomeStats']
            ).mark_area(opacity=0.5).encode(
                x=alt.X('DISP_numYearsActiveContinuous:Q', title='Year(s)'),
                y=alt.Y('density:Q', title='Density'),
                color=alt.Color('outcomeStats:N', scale=alt.Scale(domain=['Actif', 'PIT'], range=['lightcoral', 'darkturquoise']))
            ).properties(
                title='Density Plot of Percentage of Time Patients are On Time for Pick-ups'
            )

            # Add vertical lines for means
            vlines = alt.Chart(pd.DataFrame({'mean_actif': [mean_actif], 'mean_pit': [mean_pit]})).mark_rule().encode(
                x='mean_actif:Q',
                size=alt.value(2),
                color=alt.value('lightcoral'),
                strokeDash=alt.value([5, 5])
            ) + alt.Chart(pd.DataFrame({'mean_actif': [mean_actif], 'mean_pit': [mean_pit]})).mark_rule().encode(
                x='mean_pit:Q',
                size=alt.value(2),
                color=alt.value('darkturquoise'),
                strokeDash=alt.value([5, 5])
            )

            # Add text labels for means
            labels = alt.Chart(pd.DataFrame({'mean_actif': [mean_actif], 'mean_pit': [mean_pit]})).mark_text(
                align='left', baseline='middle', dy=-10
            ).encode(
                x='mean_actif:Q',
                y=alt.value(0),
                text=alt.value(f'Actif mean: {mean_actif:.2f} years'),
                color=alt.value('lightcoral')
            ) + alt.Chart(pd.DataFrame({'mean_actif': [mean_actif], 'mean_pit': [mean_pit]})).mark_text(
                align='left', baseline='middle', dy=10
            ).encode(
                x='mean_pit:Q',
                y=alt.value(0),
                text=alt.value(f'PIT mean: {mean_pit:.2f} years'),
                color=alt.value('darkturquoise')
            )

            # Combine all components
            chart = chart + vlines + labels

            # Show the chart
            st.altair_chart(chart, use_container_width=True)

    
# Visit tab
with tab4:
    st.write("Welcome to the Visit tab!")

    # creates the container for metric card
    dash_1 = st.container()

    with dash_1:
        # create columns for both graphs
        col1 = st.columns(1)[0]

        # Calculate mean for Actif and PIT groups
        mean_actif = df['VISITS_visitCount'][df.outcomeStats == 'Actif'].mean()
        mean_pit = df['VISITS_visitCount'][df.outcomeStats == 'PIT'].mean()

        # create the altair chart for year since diagnosis
        with col1:
            # Create Altair chart
            chart = alt.Chart(df).transform_density(
                'VISITS_visitCount',
                as_=['VISITS_visitCount', 'density'],
                groupby=['outcomeStats']
            ).mark_area(opacity=0.5).encode(
                x=alt.X('VISITS_visitCount:Q', title='Time(s)'),
                y=alt.Y('density:Q', title='Density'),
                color=alt.Color('outcomeStats:N', scale=alt.Scale(domain=['Actif', 'PIT'], range=['lightcoral', 'darkturquoise']))
            ).properties(
                title='Density Plot of Total Number of Visit History'
            )

            # Add vertical lines for means
            vlines = alt.Chart(pd.DataFrame({'mean_actif': [mean_actif], 'mean_pit': [mean_pit]})).mark_rule().encode(
                x='mean_actif:Q',
                size=alt.value(2),
                color=alt.value('lightcoral'),
                strokeDash=alt.value([5, 5])
            ) + alt.Chart(pd.DataFrame({'mean_actif': [mean_actif], 'mean_pit': [mean_pit]})).mark_rule().encode(
                x='mean_pit:Q',
                size=alt.value(2),
                color=alt.value('darkturquoise'),
                strokeDash=alt.value([5, 5])
            )

            # Add text labels for means
            labels = alt.Chart(pd.DataFrame({'mean_actif': [mean_actif], 'mean_pit': [mean_pit]})).mark_text(
                align='left', baseline='middle', dy=-10
            ).encode(
                x='mean_actif:Q',
                y=alt.value(0),
                text=alt.value(f'Actif mean: {mean_actif:.2f} times'),
                color=alt.value('lightcoral')
            ) + alt.Chart(pd.DataFrame({'mean_actif': [mean_actif], 'mean_pit': [mean_pit]})).mark_text(
                align='left', baseline='middle', dy=10
            ).encode(
                x='mean_pit:Q',
                y=alt.value(0),
                text=alt.value(f'PIT mean: {mean_pit:.2f} times'),
                color=alt.value('darkturquoise')
            )

            # Combine all components
            chart = chart + vlines + labels

            # Show the chart
            st.altair_chart(chart, use_container_width=True)


    # creates the container for metric card
    dash_2 = st.container()

    with dash_2:
        # create columns for both graphs
        col1 = st.columns(1)[0]

        # Calculate mean for Actif and PIT groups
        mean_actif = df['VISITS_meanVisGap'][df.outcomeStats == 'Actif'].mean()
        mean_pit = df['VISITS_meanVisGap'][df.outcomeStats == 'PIT'].mean()

        # create the altair chart for year since diagnosis
        with col1:
            # Create Altair chart
            chart = alt.Chart(df).transform_density(
                'VISITS_meanVisGap',
                as_=['VISITS_meanVisGap', 'density'],
                groupby=['outcomeStats']
            ).mark_area(opacity=0.5).encode(
                x=alt.X('VISITS_meanVisGap:Q', title='Day(s)'),
                y=alt.Y('density:Q', title='Density'),
                color=alt.Color('outcomeStats:N', scale=alt.Scale(domain=['Actif', 'PIT'], range=['lightcoral', 'darkturquoise']))
            ).properties(
                title='Density Plot of Average Visit Gap'
            )

            # Add vertical lines for means
            vlines = alt.Chart(pd.DataFrame({'mean_actif': [mean_actif], 'mean_pit': [mean_pit]})).mark_rule().encode(
                x='mean_actif:Q',
                size=alt.value(2),
                color=alt.value('lightcoral'),
                strokeDash=alt.value([5, 5])
            ) + alt.Chart(pd.DataFrame({'mean_actif': [mean_actif], 'mean_pit': [mean_pit]})).mark_rule().encode(
                x='mean_pit:Q',
                size=alt.value(2),
                color=alt.value('darkturquoise'),
                strokeDash=alt.value([5, 5])
            )

            # Add text labels for means
            labels = alt.Chart(pd.DataFrame({'mean_actif': [mean_actif], 'mean_pit': [mean_pit]})).mark_text(
                align='left', baseline='middle', dy=-10
            ).encode(
                x='mean_actif:Q',
                y=alt.value(0),
                text=alt.value(f'Actif mean: {mean_actif:.2f} days'),
                color=alt.value('lightcoral')
            ) + alt.Chart(pd.DataFrame({'mean_actif': [mean_actif], 'mean_pit': [mean_pit]})).mark_text(
                align='left', baseline='middle', dy=10
            ).encode(
                x='mean_pit:Q',
                y=alt.value(0),
                text=alt.value(f'PIT mean: {mean_pit:.2f} days'),
                color=alt.value('darkturquoise')
            )

            # Combine all components
            chart = chart + vlines + labels

            # Show the chart
            st.altair_chart(chart, use_container_width=True)

        

    # creates the container for metric card
    dash_3 = st.container()

    with dash_3:
        # create columns for both graphs
        col1 = st.columns(1)[0]

        # Calculate mean for Actif and PIT groups
        mean_actif = df['VISITS_meanAppGap'][df.outcomeStats == 'Actif'].mean()
        mean_pit = df['VISITS_meanAppGap'][df.outcomeStats == 'PIT'].mean()

        # create the altair chart for year since diagnosis
        with col1:
            # Create Altair chart
            chart = alt.Chart(df).transform_density(
                'VISITS_meanAppGap',
                as_=['VISITS_meanAppGap', 'density'],
                groupby=['outcomeStats']
            ).mark_area(opacity=0.5).encode(
                x=alt.X('VISITS_meanAppGap:Q', title='Day(s)'),
                y=alt.Y('density:Q', title='Density'),
                color=alt.Color('outcomeStats:N', scale=alt.Scale(domain=['Actif', 'PIT'], range=['lightcoral', 'darkturquoise']))
            ).properties(
                title='Density Plot of Average Appointment Gap'
            )

            # Add vertical lines for means
            vlines = alt.Chart(pd.DataFrame({'mean_actif': [mean_actif], 'mean_pit': [mean_pit]})).mark_rule().encode(
                x='mean_actif:Q',
                size=alt.value(2),
                color=alt.value('lightcoral'),
                strokeDash=alt.value([5, 5])
            ) + alt.Chart(pd.DataFrame({'mean_actif': [mean_actif], 'mean_pit': [mean_pit]})).mark_rule().encode(
                x='mean_pit:Q',
                size=alt.value(2),
                color=alt.value('darkturquoise'),
                strokeDash=alt.value([5, 5])
            )

            # Add text labels for means
            labels = alt.Chart(pd.DataFrame({'mean_actif': [mean_actif], 'mean_pit': [mean_pit]})).mark_text(
                align='left', baseline='middle', dy=-10
            ).encode(
                x='mean_actif:Q',
                y=alt.value(0),
                text=alt.value(f'Actif mean: {mean_actif:.2f} days'),
                color=alt.value('lightcoral')
            ) + alt.Chart(pd.DataFrame({'mean_actif': [mean_actif], 'mean_pit': [mean_pit]})).mark_text(
                align='left', baseline='middle', dy=10
            ).encode(
                x='mean_pit:Q',
                y=alt.value(0),
                text=alt.value(f'PIT mean: {mean_pit:.2f} days'),
                color=alt.value('darkturquoise')
            )

            # Combine all components
            chart = chart + vlines + labels

            # Show the chart
            st.altair_chart(chart, use_container_width=True)



# Diagnostics tab
with tab5:
    st.write("Welcome to the Diagnostics tab!")

    # creates the container for metric card
    dash_1 = st.container()

    with dash_1:
        # create columns for both graphs
        col1 = st.columns(1)[0]

        # Calculate mean for Actif and PIT groups
        mean_actif = df['VLS_totalVLTests'][df.outcomeStats == 'Actif'].mean()
        mean_pit = df['VLS_totalVLTests'][df.outcomeStats == 'PIT'].mean()

        # create the altair chart for year since diagnosis
        with col1:
            # Create Altair chart
            chart = alt.Chart(df).transform_density(
                'VLS_totalVLTests',
                as_=['VLS_totalVLTests', 'density'],
                groupby=['outcomeStats']
            ).mark_area(opacity=0.5).encode(
                x=alt.X('VLS_totalVLTests:Q', title='Time(s)'),
                y=alt.Y('density:Q', title='Density'),
                color=alt.Color('outcomeStats:N', scale=alt.Scale(domain=['Actif', 'PIT'], range=['lightcoral', 'darkturquoise']))
            ).properties(
                title='Density Plot of Total Number of Viral Test History'
            )

            # Add vertical lines for means
            vlines = alt.Chart(pd.DataFrame({'mean_actif': [mean_actif], 'mean_pit': [mean_pit]})).mark_rule().encode(
                x='mean_actif:Q',
                size=alt.value(2),
                color=alt.value('lightcoral'),
                strokeDash=alt.value([5, 5])
            ) + alt.Chart(pd.DataFrame({'mean_actif': [mean_actif], 'mean_pit': [mean_pit]})).mark_rule().encode(
                x='mean_pit:Q',
                size=alt.value(2),
                color=alt.value('darkturquoise'),
                strokeDash=alt.value([5, 5])
            )

            # Add text labels for means
            labels = alt.Chart(pd.DataFrame({'mean_actif': [mean_actif], 'mean_pit': [mean_pit]})).mark_text(
                align='left', baseline='middle', dy=-10
            ).encode(
                x='mean_actif:Q',
                y=alt.value(0),
                text=alt.value(f'Actif mean: {mean_actif:.2f} times'),
                color=alt.value('lightcoral')
            ) + alt.Chart(pd.DataFrame({'mean_actif': [mean_actif], 'mean_pit': [mean_pit]})).mark_text(
                align='left', baseline='middle', dy=10
            ).encode(
                x='mean_pit:Q',
                y=alt.value(0),
                text=alt.value(f'PIT mean: {mean_pit:.2f} times'),
                color=alt.value('darkturquoise')
            )

            # Combine all components
            chart = chart + vlines + labels

            # Show the chart
            st.altair_chart(chart, use_container_width=True)

    # creates the container for metric card
    dash_2 = st.container()

    with dash_2:
        # Get Description data
        total_ppl = df['jointID'].count()
        total_t = df[df.VLS_testWithinYr==True]['jointID'].count()
        total_f = df[df.VLS_testWithinYr==False]['jointID'].count()

        col1, col2, col3 = st.columns(3)
        # create column span
        col1.metric(label="Total Patients", value= millify(total_ppl, precision=2))
    
        col2.metric(label="% Took Test within 1 Year", value= millify(total_t, precision=2))
    
        col3.metric(label="% Did not Take Test within 1 Year", value= millify(total_f, precision=2))
    
        # this is used to style the metric card
        style_metric_cards(border_left_color="#DBF227")

    # creates the container for metric card
    dash_3 = st.container()

    with dash_3:
        # Get Description data
        total_d = df[df.VLS_recentResult=='DETECTABLE']['jointID'].count()
        total_i = df[df.VLS_recentResult=='INDETECTABLE']['jointID'].count()
        total_u = df[df.VLS_recentResult=='UNKNOWN']['jointID'].count()

        col1, col2, col3 = st.columns(3)
        # create column span
        col1.metric(label="% with Detectable Test Result ", value= millify(total_d, precision=2))
    
        col2.metric(label="% with Indetectable Test Result", value= millify(total_i, precision=2))
    
        col3.metric(label="% with Unknown Test Result", value= millify(total_u, precision=2))
    
        # this is used to style the metric card
        style_metric_cards(border_left_color="#DBF227")


    # creates the container for metric card
    dash_4 = st.container()

    # Generate a new df contains the proportion of Actif or PIT patients' recent test status
    df['VLS_testWithinYr'] = df['VLS_testWithinYr'].replace(True, 'True').replace(False, 'False')
    df_rr = df.groupby(['VLS_testWithinYr','outcomeStats']).agg(count=('VLS_testWithinYr','count')).reset_index()
    df_rr['group_sum'] = df_rr.groupby('outcomeStats')['count'].transform('sum')
    df_rr['proportion'] = round(df_rr['count'] / df_rr['group_sum'] *100,2)
    df_rr = df_rr.rename(columns={'VLS_testWithinYr':'Test within 1 Year'})

    # Generate a new df contains the proportion of Actif or PIT patients' recent test status
    df['VLS_rr'] = df.VLS_recentResult.replace('UNKNOWN',np.nan)
    df_rro = df.groupby(['VLS_rr','outcomeStats']).agg(count=('VLS_rr','count')).reset_index()
    df_rro['group_sum'] = df_rro.groupby('outcomeStats')['count'].transform('sum')
    df_rro['proportion'] = round(df_rro['count'] / df_rro['group_sum'] *100,2)
    df_rro = df_rro.rename(columns={'VLS_rr':'Recent HIV Test Result'})

    with dash_4:
        # create columns for both graphs
        col1, col2 = st.columns(2)

        # create the altair chart for year since diagnosis
        with col1:
            # Create Altair chart
            chart = alt.Chart(df_rr).mark_bar().encode(
                x=alt.X('outcomeStats:N', title='Outcome Status'),
                y=alt.Y('proportion:Q', title='Proportion (%)'),
                color=alt.Color('Test within 1 Year:N', scale=alt.Scale(domain=['True', 'False'], range=['lightcoral', 'darkturquoise'])),
                tooltip=['proportion:Q'] 
            ).properties(
                title='Proportion of Patients Took Test within 1 Year by Treatment Status'          
            )

            # Show the chart
            st.altair_chart(chart, use_container_width=True)

        # create the altair chart for year since diagnosis
        with col2:
            # Create Altair chart
            chart = alt.Chart(df_rro).mark_bar().encode(
                x=alt.X('outcomeStats:N', title='Outcome Status'),
                y=alt.Y('proportion:Q', title='Proportion (%)'),
                color=alt.Color('Recent HIV Test Result:N', scale=alt.Scale(domain=['DETECTABLE', 'INDETECTABLE'], range=['lightcoral', 'darkturquoise'])),
                tooltip=['proportion:Q']
            ).properties(
                title='Proportion of Recent HIV Test Result by Treatment Status'          
            )

            # Show the chart
            st.altair_chart(chart, use_container_width=True)

    

css = '''
<style>
    .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
    font-size:18px;
    }
</style>
'''

st.markdown(css, unsafe_allow_html=True)


