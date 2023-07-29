
from dash import Dash, html, dcc, Input, Output, callback
import dash_bootstrap_components as dbc
import dash_bio as dashbio
from dash_bio.utils import PdbParser, create_mol3d_style


# Initialize the app
app = Dash(__name__, external_stylesheets=[dbc.themes.MORPH])

# Panel
panel = html.Div([
    html.Span(
        children = [html.B('Protein')]
    ),
    dcc.RadioItems(['Wild Type', 'L858R mutation'], 'Wild Type',
                   id = 'Protein_type'),
    html.Br(),
    html.Span(
        children = [html.B('Ligand')]
    ),
    dcc.RadioItems(
        options=[
            {'label':'ANP', 'value':'ANP'},
            {'label':'Gefitinib', 'value':'IRE'}
        ], value = 'ANP', id = 'Ligand_type'
    )
])

Three_visual = html.Div([
    dbc.Row([
        html.Span(
        children = [html.B('3D Model')]
    )]),
    dbc.Row(id = '3D_viewer',
    children=[])
])

# Layout components
content = html.Div([
    dbc.Row([
            dbc.Col([Three_visual])
    ])
])

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(panel, width = 2),
        dbc.Col(content, width = 10)
    ])
],
fluid=True
)

# Protein Callbacks
@app.callback(
    Output('3D_viewer', 'children'),
    Input('Protein_type', 'value'),
    Input('Ligand_type', 'value'),
)

def Protein_visualization(protein, ligand):
    # Each PDB file contains the 3D coordinates of the protein-ligand complex and was processed using PyMOL.        
    pdb_files = {
        ('Wild Type', 'ANP'): '2ITX.pdb',
        ('Wild Type', 'IRE'): '2ITY.pdb',
        ('L858R mutation', 'ANP'): '2ITV.pdb',
        ('L858R mutation', 'IRE'): '2ITZ.pdb'
    }

    # Check if the provided combination exists in the 'files' dictionary
    if (protein, ligand) in pdb_files:
        file_name = pdb_files[(protein, ligand)]
        parser = PdbParser(file_name)
        data = parser.mol3d_data()

        protein_atoms = [atom for atom in data['atoms'] if atom['residue_name'] != ligand]
        
        protein_style = create_mol3d_style(protein_atoms, visualization_type='cartoon', color_element='residue')

        return dashbio.Molecule3dViewer(
            modelData=data,
            styles=protein_style
            )

    else:
        return None


if __name__ == '__main__':
    app.run_server(debug=True)