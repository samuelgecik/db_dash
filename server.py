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

# Define layout
app.layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    html.H1("Data Filter", className="text-center text-primary, mb-4"),
                    width=12,
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
                            placeholder="Filter rows...",
                            className="mb-3",
                        ),
                        dbc.Button(
                            "Submit",
                            id="filter-button",
                            color="primary",
                            className="mt-1",
                        ),
                    ],
                    width=12,
                )
            ]
        ),
        dbc.Row([dbc.Col(html.Div(id="table-container"), width=12)]),
        html.Div(
            style={"display": "none"},
            children=[
                html.Div(
                    children=[
                        """
            <style>
                .table tbody tr:nth-child(even) {
                    background-color: lightgray;
                }
            </style>
            """
                    ]
                )
            ],
        ),
    ]
)


# Define callback
@app.callback(
    Output("table-container", "children"),
    [Input("filter-button", "n_clicks")],
    [State("filter-input", "value")],
)
def update_table(n_clicks, value):
    if value is not None:
        filtered_df = df[
            df.apply(lambda row: row.astype(str).str.contains(value).any(), axis=1)
        ]
    else:
        filtered_df = df

    return [
        dbc.Table.from_dataframe(filtered_df, striped=True, bordered=True, hover=True)
    ]


# Run app
if __name__ == "__main__":
    app.run_server(port=3000)
