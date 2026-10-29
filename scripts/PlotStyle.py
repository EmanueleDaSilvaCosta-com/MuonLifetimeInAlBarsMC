# Questo modulo definisce lo stile grafico per i nostri plot. Bisogna usarlo all'inizio di ogni script per avere un aspetto coerente e professionale.
import matplotlib.pyplot as plt
import matplotlib as mpl

# --- 1. PALETTE COLORI (Modifica qui per cambiare tutto) ---
PALETTE = {
    'dati': "#084A8D",       # Blu scuro (dati sperimentali)
    'fit': '#E74C3C',        # Rosso (curva di fit)
    'fit_conf': '#E74C3C',   # Colore per la fascia di errore (useremo alpha)
    'grid': '#BDC3C7',       # Grigio chiaro per la griglia
    'sfondo': 'white'
}

def set_style(big_fonts=False, latex=False):
    
    plt.style.use('default') 
    
    base_size = 14 if big_fonts else 8
    
    params = {
        # Font e Testi
        'font.family': 'serif' if latex else 'sans-serif',
        'font.size': base_size,
        'axes.labelsize': base_size+1,
        'axes.titlesize': base_size + 2,
        'legend.fontsize': base_size,
        'xtick.labelsize': base_size,
        'ytick.labelsize': base_size,
        
        # Linee e Marker
        'lines.linewidth': 2,
        'lines.markersize': 4,
        'errorbar.capsize': 3,  # I "cappelli" sulle barre di errore
        
        # Assi e Griglia
        'axes.grid': True,
        'grid.color': PALETTE['grid'],
        'grid.linestyle': '--',
        'grid.alpha': 0.6,
        'axes.axisbelow': True, # Mette la griglia SOTTO i dati (importante!)
        
        # Legenda
        'legend.frameon': True,
        'legend.framealpha': 0.9,
        'legend.facecolor': 'white',
        'legend.edgecolor': 'gray',
        'legend.loc': 'best',
        
        # Output
        'figure.figsize': (6, 4), # Dimensione standard in pollici
        'figure.dpi': 120,        # Risoluzione a schermo
        'savefig.dpi': 300,       # Risoluzione salvataggio (alta qualità)
        'savefig.bbox': 'tight',  # Taglia i bordi bianchi inutili
        'savefig.format': 'pdf'   # Formato vettoriale di default
    }
    
    mpl.rcParams.update(params)
    #print("🎨 Stile grafico caricato con successo!")

def get_colors():
    """Restituisce il dizionario dei colori per usarli manualmente nel codice"""
    return PALETTE