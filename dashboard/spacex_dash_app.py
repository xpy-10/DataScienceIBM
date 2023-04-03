# Import required libraries
import pandas as pd
import dash
# import dash_html_components as html
# import dash_core_components as dcc
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()
site_df = spacex_df.groupby(["Launch Site"], as_index=False)['class'].mean()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown', options=[{'label': 'All Sites', 'value': 'ALL'}, 
                                #                                         {'label': 'CCAFS LC-40', 'value':site_df.loc['CCAFS LC-40']},
                                #                                         {'label': 'CCAFS SLC-40', 'value': site_df.loc['CCAFS SLC-40']},
                                #                                         {'label':'KSC LC-39A', 'value':site_df.loc['KSC LC-39A']},
                                #                                         {'label': 'VAFB SLC-4E', 'value': site_df.loc['VAFB SLC-4E']}],
                                #                                         value = 'All Sites',
                                #                                         placeholder='Select a Launch Site here', searchable=True),
                                dcc.Dropdown(['All Sites', *spacex_df['Launch Site'].unique()], id='site-dropdown', 
                                            value='All Sites', placeholder='Select a Launch Site here', searchable=True),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                                min=0, max=10000, step=1000, 
                                                value=[min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
            Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    if entered_site == 'All Sites':
        dff = spacex_df
        fig = px.pie(dff , values='class',
        names='Launch Site', 
        title='Success by Launch Site')
        return fig
    else:
        dff = pd.DataFrame(spacex_df.loc[spacex_df['Launch Site']==entered_site]['class'].value_counts())
        dff = dff.reset_index()
        dff.columns = ['class', 'counts']
        fig = px.pie(dff, values='counts',
        names='class',
        title='Success at '+ entered_site)
        return fig
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
            [Input(component_id='site-dropdown', component_property='value'),
            Input(component_id='payload-slider', component_property='value')]
            )
def get_scatter_chart(entered_site, entered_range):
    if entered_site == 'All Sites':
        dff = spacex_df[(spacex_df['Payload Mass (kg)']<entered_range[1]) & (spacex_df['Payload Mass (kg)']>entered_range[0])]
        fig = px.scatter(dff, x='Payload Mass (kg)', y='class', 
                        title='Correlation between Payload and Success for all Sites', color='Booster Version Category')
        return fig
    else:
        dff = spacex_df.loc[spacex_df['Launch Site']==entered_site]
        dff = spacex_df[spacex_df['Payload Mass (kg)']<entered_range[1]]
        dff = spacex_df[spacex_df['Payload Mass (kg)']>entered_range[0]]
        fig = px.scatter(dff, x='Payload Mass (kg)', y='class',
                        title='Correlation between Payload and Success for '+ entered_site, color='Booster Version Category')
        return fig
# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
