import os
import glob
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

from Function import Histogram, gaussian, linear

def Read_Plot_Histo(file_list, output_dr):
    os.makedirs(output_dr, exist_ok=True)

    for path in file_list:
        dati = np.fromfile(path, dtype=np.int32) 
        file_name = os.path.basename(path)
    
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.hist(dati, bins=100, color='blue', alpha=0.7)
        ax.set_title(f"Istogramma: {file_name}", size=16)
    
        saving_path = os.path.join(output_dr, f"plot_{file_name}.pdf")
    
        plt.savefig(saving_path)
        plt.close(fig)

def Baseline(file_list, out_dir, ch_min=None, ch_max=None, i=0):
    B=[]
    err_B=[]
    for path in file_list:
        data = np.fromfile(path, dtype=np.int32)
        canali = np.arange(len(data))
        if (ch_min!=None and ch_max!=None):
            mask = (canali >= ch_min) & (canali <= ch_max)
            canali_roi = canali[mask]
            data_roi = data[mask]
        else:
            canali_roi=canali
            data_roi=data

        popt, pcov = curve_fit(linear, canali_roi, data_roi, p0=[0,1000])

        B.append(popt[1])
        err = np.sqrt(pcov[1,1])
        err_B.append(err)
        if path==str(out_dir / f"spectrum{i}.bin"):
            q=popt[1]
            err_q=np.sqrt(pcov[1,1])
            m=popt[0]
            err_m=np.sqrt(pcov[0,0])

    
    print(f"For the spectrum {i}, the calculated values are:", 
          f"\nB = {q:.4f} ± {err_q:.4f}", 
          f"\nm (angular coeff.) = {m:.4f} ± {err_m:.4f}")

    bins = np.arange(len(canali_roi)) + 0.5
    spectrum = np.fromfile(out_dir / f"spectrum{i}.bin", dtype="<u4")
    plt.bar(bins, spectrum, width=1.0)
    plt.plot(bins, q+bins*m, color="Red")
    plt.show()

    return np.array(B), np.array(err_B)

def Distribution(file_list, output_dr, save=False):
    B = []
    err_B = []

    for path in file_list:
        data = np.fromfile(path, dtype=np.int32) 
        valid_data = data[np.isfinite(data)]
    
        if len(valid_data) > 0:
            isto = Histogram(valid_data, bins=50)
        
            try:
                par, cov = isto.fit("gaussian")
                B.append(par[1])
                err=np.sqrt(cov[1,1])
                err_B.append(abs(err))
            
            except RuntimeError:
                print(f"Fit not successful for file {os.path.basename(path)}")

    fig, ax = plt.subplots(1, 2, figsize=(8, 4))

    if len(B) > 0:
        isto_B = Histogram(B, bins=50)
        par_mu, cov_mu = isto_B.fit("gaussian")
        isto_B.plot(ax=ax[0], title="Mean Value Distribution", label="Mean Value (Fit)", show_fit=True)

        err_mu = np.sqrt(cov_mu[1, 1])
        err_dev_mu = np.sqrt(cov_mu[2, 2])
        
        print(f"The average value (mu distribution fit) is {par_mu[1]:.4f} ± {err_mu:.4f}")
        print(f"The standard dev. (mu distribution fit) is {abs(par_mu[2]):.4f} ± {err_dev_mu:.4f}")

        ax[0].ticklabel_format(useOffset=False, style='plain')

    if len(err_B) > 0:
        isto_dev = Histogram(err_B, bins=50)
        par_sigma, cov_sigma = isto_dev.fit("gaussian")
        isto_dev.plot(ax=ax[1], title="Standard Dev. Distribution", label="Standard Dev. (Fit)", show_fit=False)
    
        err_mu = np.sqrt(cov_sigma[1, 1])
        err_dev_sigma = np.sqrt(cov_sigma[2, 2])
        
        print(f"The average value (sigma distribution fit) is {par_sigma[1]:.4f} ± {err_mu:.4f}")
        print(f"The standard dev. (sigma distribution fit) is {abs(par_sigma[2]):.4f} ± {err_dev_sigma:.4f}")

    plt.tight_layout()
    if save==True:
        plt.savefig(str(output_dr /"distribution_plots.pdf"), dpi=300)
        plt.show()

    return par_mu, par_sigma, np.array(B), np.array(err_B)

def pull(B, dev, B_true, output_dr ,show=False, save=False):
    pull = (B - B_true) / dev

    fig, ax = plt.subplots(1, 1, figsize=(8,4))
    isto_pull = Histogram(pull, bins=100)
    par_pull, cov_pull = isto_pull.fit("gaussian")

    err_pull = np.sqrt(cov_pull[1, 1])
    err_dev_pull = np.sqrt(cov_pull[2, 2])

    print(f"The average value (pull) is {par_pull[1]:.4f} ± {err_pull:.4f}")
    print(f"The standard dev. (pull) is {abs(par_pull[2]):.4f} ± {err_dev_pull:.4f}")

    isto_pull.plot(ax=ax ,title=f"Pull Distribution for B_true={B_true}", label="Pull")
    if save:
        plt.savefig(str(output_dr /f"Pull_Plot_{B_true}.pdf"), dpi=300)
    if show and (par_pull[1]>-3 and par_pull[1]<3):
        plt.show()
    else:
        plt.close()

    return par_pull, cov_pull, np.array(pull)
    