from dash import dcc


def get_graphs():
    return [
        # ... other graphs ...
        
        # Chart 1
        dcc.Graph(id='chart-hourly-borough-trend', className='mb-4'),

    ]