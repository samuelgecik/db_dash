import dash
from dash import html
import dash_bootstrap_components as dbc
from dash import dcc
from dash.dependencies import Input, Output, State
import pandas as pd

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
df = pd.read_excel("db.xlsx")
columns = [{"name": col, "id": col} for col in df.columns]
print(columns)

# merge last three columns to one
# [{'name': 'Account Holder Name', 'id': 'Account Holder Name'}, 
# {'name': 'Company Registration Nr of Account Holder', 'id': 'Company Registration Nr of Account Holder'}, 
# {'name': 'LEI', 'id': 'LEI'}, {'name': 'MS Registry', 'id': 'MS Registry'}, 
# {'name': 'Installation ID', 'id': 'Installation ID'}, {'name': 'Installation Name', 'id': 'Installation Name'}, 
# {'name': 'Activity Type', 'id': 'Activity Type'}, {'name': 'Permit ID', 'id': 'Permit ID'}, 
# {'name': 'PERMIT_REVOCATION_DATE', 'id': 'PERMIT_REVOCATION_DATE'}, 
# {'name': 'Permit Expiry/Revocation Date ', 'id': 'Permit Expiry/Revocation Date '}, 
# {'name': 'Contact Country', 'id': 'Contact Country'}, {'name': 'Contact City', 'id': 'Contact City'}, 
# {'name': 'Contact PCode', 'id': 'Contact PCode'}, {'name': 'Contact Address L1', 'id': 'Contact Address L1'}, 
# {'name': 'Contact Address L2', 'id': 'Contact Address L2'}]

# merge address columns
df['Contact Address'] = df['Contact City'] + ', ' + df['Contact PCode'] + ', ' + df['Contact Address L1']
df.drop(['Contact City', 'Contact PCode', 'Contact Address L1', 'Contact Address L2'], axis=1, inplace=True)

app.layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    html.H1("EU ETS Registered Operators", className="text-center text-primary, mb-4"),
                    width={"size": 12, "offset": 0},
                )
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Input(
                            id="filter-input",
                            type="text",
                            placeholder="Filter word...",
                            className="mb-3",
                        ),
                        dbc.Button(
                            "Submit",
                            id="filter-button",
                            color="primary",
                            className="mt-1",
                        ),
                    ],
                    md=6,
                ),
                dbc.Col(
                    dcc.Dropdown(
                                id='country-dropdown',
                                options=[{'label': i, 'value': i} for i in df['Contact Country'].unique()],
                                placeholder="Select a country",
                            ),
                    md=6,
                )
            ]
        ),
        dbc.Row([dbc.Col(html.Div(id="table-container", style={'margin-top': '5px'}), md=12)]),
    ],
    fluid=True,
)


@app.callback(
    Output('table-container', 'children'),
    [Input('filter-button', 'n_clicks')],
    [State('country-dropdown', 'value'), State('filter-input', 'value')]
)
def update_table(n_clicks, selected_country, input_value):
    if selected_country is not None:
        filtered_df = df[df['Contact Country'] == selected_country]
    else:
        filtered_df = df

    if input_value is not None:
        lowercased_value = input_value.lower()
        filtered_df = filtered_df[filtered_df.apply(lambda row: row.astype(str).str.lower().str.contains(lowercased_value).any(), axis=1)]

    return [dash.dash_table.DataTable(
        data=filtered_df.to_dict('records'),
        columns=[{'name': i, 'id': i} for i in filtered_df.columns],
        page_action='native',
        page_size=50,
        virtualization=True,
        style_data_conditional=[
            {
                'if': {'row_index': 'odd'},
                'backgroundColor': 'lightgray'
            }
        ],
        style_table={'minHeight': '800px', 'height': '800px', 'maxHeight': '800px'}
    )]


# Run app
if __name__ == "__main__":
    app.run_server(host='0.0.0.0', port=3000)
