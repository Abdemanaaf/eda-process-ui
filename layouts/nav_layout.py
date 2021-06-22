import dash_bootstrap_components as dbc


left_side_nav_layout = dbc.Nav([
    dbc.Card([
        dbc.CardHeader(
            dbc.NavItem(dbc.NavLink('Step By Step Process', active=True, href='/', style={'color': 'white'}), style={'font-size': '1.7rem'}),
        ),
        dbc.CardBody([
            dbc.NavItem(dbc.NavLink('Upload Data Files', href='/', style={'color': 'grey'}), style={'font-size': '1.5rem'}),
            dbc.NavItem(dbc.NavLink('1. Input Files Upload', href='/', style={'color': 'grey'}), style={'font-size': '1rem'}),
            dbc.NavItem(dbc.NavLink('2. Input Files Table', href='/', style={'color': 'grey'}), style={'font-size': '1rem'}),
            dbc.NavItem(dbc.NavLink('3. Mapping Files Upload', href='/', style={'color': 'grey'}), style={'font-size': '1rem'}),
            dbc.NavItem(dbc.NavLink('4. Mapping Files Table', href='/', style={'color': 'grey'}), style={'font-size': '1rem'}),

            dbc.NavItem(dbc.NavLink('EDA Functions List', href='/eda-page', style={'color': 'grey'}), style={'font-size': '1.5rem'}),
            dbc.NavItem(dbc.NavLink('Output Data Files', href='/output-page', style={'color': 'grey'}), style={'font-size': '1.5rem'}),
        ]),
    ], color="dark", inverse=True),
], vertical='md')


top_navbar_layout = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink('Data Analytics (EDA)', href='/'), className='mr-5 mt-2 active'),
        dbc.NavItem(dbc.NavLink('Data Visualization (Graphs)', href='/data-visualization'), className='mr-5 mt-2'),
        dbc.NavItem(dbc.NavLink('Contact Us', href='/contact-us', className='mt-2'))
    ],
    brand='EASE EDA', brand_href='/', color='dark', dark=True, fixed='top', sticky='top', style={'font-size': '1.4rem'},
    brand_style={'font-size': '1.5rem'}
)