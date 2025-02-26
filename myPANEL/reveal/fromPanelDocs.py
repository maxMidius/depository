import hvplot.pandas
import numpy as np
import panel as pn
import pandas as pd

pn.extension(design=pn.theme.Material)

xs = np.linspace(0, np.pi)

freq = pn.widgets.FloatSlider(name="Frequency", start=0, end=10, value=2)
phase = pn.widgets.FloatSlider(name="Phase", start=0, end=np.pi)

widgets = pn.WidgetBox(freq, phase, horizontal=True)

def sine(freq, phase):
    return pd.DataFrame(dict(y=np.sin(xs*freq+phase)), index=xs)

def cosine(freq, phase):
    return pd.DataFrame(dict(y=np.cos(xs*freq+phase)), index=xs)

dfi_sine = hvplot.bind(sine, freq, phase).interactive()
dfi_cosine = hvplot.bind(cosine, freq, phase).interactive()

plot_opts = dict(responsive=True, min_height=400)


template = pn.template.SlidesTemplate(
    title='The slide title', logo='https://raw.githubusercontent.com/holoviz/panel/main/doc/_static/logo_stacked.png' ,
    reveal_theme='night',  # simple, sky, beige, serif, solarized, blood, moon, night, black, league, white    
    header_background='#f1f1f1',  sidebar_width=200,
)

template.main.extend([   
    pn.pane.Markdown('Slides Template', styles={'font-size': '3em'}, align='center'),
    pn.Card(dfi_sine.hvplot(**plot_opts).output(), widgets, title='Sine', margin=20, tags=['fragment']),
])

template.main.append(
    pn.Card(dfi_cosine.hvplot(**plot_opts).output(), widgets, title='Cosine', margin=20),
)

template.servable();