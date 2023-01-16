import pandas as pd
import plotly.express as px  # (version 4.7.0 or higher)
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output  # pip install dash (version 2.0.0 or higher)


app = Dash(__name__)
server = app.server
# -- Import and clean data (importing csv into pandas)
# df = pd.read_csv("intro_bees.csv")
df = pd.read_csv("final_data.csv")

bp_df = df.drop(['PREDICTED_SBP', 'PREDICTED_DBP'], axis=1)
sd_bp_df = pd.DataFrame()
for cols in bp_df:
  #print(cols)
  if cols not in ['MSR_ID', 'CYC_ID','SBP', 'DBP']:
    sd_bp_df[cols] = bp_df.groupby('MSR_ID')[cols].std().reset_index()[cols]

f_columns = [col for col in sd_bp_df]

# ------------------------------------------------------------------------------
# App layout
app.layout = html.Div([

    html.H1("FEATURE ANALYTICS DASHBOARD", style={'text-align': 'center'}),

    dcc.Dropdown(id="slct_year",
                 options = f_columns,
                 multi=False,
                 value='PTT_PPG_DIASTOLIC',
                 style={'width': "40%"}
                 ),

    html.Div(id='output_container', children=[]),
    html.Br(),
    
    html.Div(id='plots', children=[
        html.Div(id='plot1', children=[
            dcc.Graph(id='sd_plot', figure={}, style={'width': "40%"})
        ]),
        html.Div(id='plot2', children=[
            dcc.Graph(id='scatter_sys', figure={}, style={'width': "40%"})
        ]),
        html.Div(id='plot3', children=[
            dcc.Graph(id='scatter_dia', figure={}, style={'width': "40%"})
        ])
    ])
    
])


# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components
@app.callback(
    [Output(component_id='output_container', component_property='children'),
     Output(component_id='sd_plot', component_property='figure'),
     Output(component_id='scatter_sys', component_property='figure'),
     Output(component_id='scatter_dia', component_property='figure')],
    [Input(component_id='slct_year', component_property='value')]
)
def update_graph(option_slctd):
    print(option_slctd)
    print(type(option_slctd))

    container = "FEATURE SELECTED: {}".format(option_slctd)

    sd_dff = sd_bp_df.copy()
    bp_dff = bp_df.copy()
    # dff = dff[dff["Year"] == option_slctd]
    # dff = dff[dff["Affected by"] == "Varroa_mites"]

    # Plotly Express
    fig1 = px.histogram(sd_dff, x=option_slctd, nbins=50)
    fig2 = px.scatter(bp_dff, x=option_slctd, y='DBP')
    fig3 = px.scatter(bp_dff, x=option_slctd, y='SBP')
   

    return container, fig1, fig2, fig3


# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)