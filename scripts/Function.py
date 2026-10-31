import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import PlotStyle as graf

graf.set_style()
color = graf.get_colors()

# ==========================================
# FUNZIONI MATEMATICHE E STATISTICHE
# ==========================================
def constant(x, B):
    return B * np.ones_like(x)

def exponential(x, A, B):
    return A * np.exp(B * x)

def linear(x, m, q):
    return m * x + q

def quadratic(x, a, b, c):
    return a * x**2 + b * x + c

def power_law(x, A, n):
    return A * x**n

def logarithmic(x, A, B):
    return A * np.log(B * x)

def gaussian(x, A, mu, sigma):
    return A * np.exp(-(x - mu)**2 / (2 * sigma**2))

def chi2(function, xdata, ydata, sigma):
    return np.sum(((ydata - function(xdata)) / sigma) ** 2)

REGISTRO_FUNZIONI = {
    'constant': constant,
    'linear': linear,
    'exponential': exponential,
    'power_law': power_law,
    'quadratic': quadratic,
    'gaussian': gaussian,
    'logarithmic': logarithmic
}

# ==========================================
# ISTOGRAMMA
# ==========================================
class Histogram:
    def __init__(self, data, bins=10, range=None):
        if not range:
            range = (np.min(data), np.max(data))
        self.data = np.array(data)
        self.no_entries = len(data)
        self.bins = bins
        self.range = range
        self.width = (self.range[1] - self.range[0]) / self.bins
        
        self.bin_values, self.bin_edges = np.histogram(data, bins=self.bins, range=self.range)
        self.bin_centers = 0.5 * (self.bin_edges[1:] + self.bin_edges[:-1])
        
        self.popt = None
        self.pcov = None
        self.fit_func_name = None
        self.roi = None
        self.ax=None

    def stat(self):
        mean = np.mean(self.bin_values)
        std_dev = np.std(self.bin_values)
        return mean, std_dev

    def fit(self, func_name, x_min=None, x_max=None, p0=None):
        """Fitta una funzione a scelta"""
        if func_name not in REGISTRO_FUNZIONI:
            raise ValueError(f"Funzione '{func_name}' non trovata. Scegli tra: {list(REGISTRO_FUNZIONI.keys())}")
        
        modello = REGISTRO_FUNZIONI[func_name]
        self.fit_func_name = func_name
        
        if x_min is None: x_min = self.range[0]
        if x_max is None: x_max = self.range[1]
        self.roi = (x_min, x_max)

        mask = (self.bin_centers >= x_min) & (self.bin_centers <= x_max)
        x_roi = self.bin_centers[mask]
        y_roi = self.bin_values[mask]

        if len(y_roi) == 0:
            raise RuntimeError("ROI vuota, impossibile fittare.")
            
        y_err = np.sqrt(y_roi)
        y_err[y_err == 0] = 1.0 

        if p0 is None and func_name == 'gaussian':
            p0 = [np.max(y_roi), np.mean(x_roi), np.std(x_roi)]

        self.popt, self.pcov = curve_fit(modello, x_roi, y_roi, p0=p0, sigma=y_err, absolute_sigma=True)
        return self.popt, self.pcov

    def plot(self, ax=None, label=None, show_fit=True, title="Istogramma"):
        """Disegna l'istogramma, evidenzia l'eventuale ROI e sovrappone il fit"""
        if ax is None:
            ax = plt.gca()
        self.ax=ax
        ax.hist(self.data, bins=self.bins, range=self.range, 
                color=color.get("dati", "#084A8D"), histtype='stepfilled', alpha=0.7, label=label or 'Tutti i dati')
        
        ax.set_xlabel("Value", size=14)
        ax.set_ylabel("Counts", size=14)
        ax.set_title(title)

        if self.popt is not None and show_fit:
            x_min, x_max = self.roi
            modello = REGISTRO_FUNZIONI[self.fit_func_name]
            
            dati_roi = self.data[(self.data >= x_min) & (self.data <= x_max)]
            ax.hist(dati_roi, bins=self.bin_edges, color=color.get("dati", "#084A8D"), 
                    histtype='stepfilled', alpha=0.9, label='ROI', hatch='///')

            x_fit = np.linspace(x_min, x_max, 200)
            y_fit = modello(x_fit, *self.popt)
            ax.plot(x_fit, y_fit, color=color.get("fit", "#E74C3C"), linewidth=2.5, label=f'{self.fit_func_name.capitalize()} Fit')

            errori = np.sqrt(np.diag(self.pcov))
            if self.fit_func_name == 'gaussiana':
                testo = f"$\mu$ = {self.popt[1]:.2f} $\pm$ {errori[1]:.2f}\n$\sigma$ = {abs(self.popt[2]):.2f} $\pm$ {errori[2]:.2f}"
            else:
                testo = "\n".join([f"P{i} = {val:.2f} $\pm$ {err:.2f}" for i, (val, err) in enumerate(zip(self.popt, errori))])
            
            ax.text(0.05, 0.85, testo, transform=ax.transAxes, 
                    bbox=dict(facecolor='white', alpha=0.9, edgecolor=color.get("grid", "gray")))

        ax.legend()

    def integrate(self, x_min, x_max, draw=False, colore_area='green', ax=None):
        maschera_bins = (self.bin_centers >= x_min) & (self.bin_centers <= x_max)
        
        counts = np.sum(self.bin_values[maschera_bins])
        
        area = counts * self.width
        frac = counts / self.no_entries
        
        if draw:
            ax=ax or self.ax or plt.gca()
            self.ax.axvspan(x_min, x_max, color=colore_area, alpha=0.2, 
                            label=f'Area ({frac*100:.1f}%)')
            self.ax.legend()
            
        return area, counts, frac