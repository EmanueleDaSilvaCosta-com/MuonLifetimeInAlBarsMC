import subprocess
from pathlib import Path
import os
import glob
import numpy as np
import matplotlib.pyplot as plt
import sys

from Function import Histogram
import Baseline_func as bf

print("---SPECTRA GENERATION---")
ROOT = Path(__file__).resolve().parent.parent
exe = ROOT / "build" / "uniform"
no_channels = 2048 # number of channels in the spectrum
mean = 1000 # mean of the uniform distribution
no_spectra = 1000 # number of spectra to generate
out_dir = ROOT / "data" / "uniform_spectra"  # directory to save the generated spectra

output_dr = ROOT / "output_plots" #directory to save the output plots
os.makedirs(output_dr, exist_ok=True)

# mode = 0: read the generated spectra from the binary files, if they already exist
# mode = 1: run the C++ executable to generate the spectra and save them to binary files
mode = 0

if(mode):
    # Run the C++ executable to generate the spectra
    subprocess.run(
        [str(exe), str(no_channels), str(mean), str(no_spectra), str(out_dir)],
        check=True,
    )
else:
    if( not os.path.exists(out_dir)):
        print(f"Output directory '{out_dir}' does not exist. Run the C++ executable first to generate the spectra.")
        raise SystemExit(0) # Ends the program if the output directory does not exist

'''mean = []
std = []
for i in range(no_spectra):
    spectrum = np.fromfile(out_dir / f"spectrum{i}.bin", dtype="<u4").astype(np.float64)
    mean.append(np.sum(spectrum[0:1023])/2048)
    std.append(np.std(spectrum[0:1023]))
print(mean)
pull = (np.array(mean) - 500)/np.array(std)
print(pull)
plt.hist(pull, bins=10)
plt.show()
plt.clf()
sys.exit()'''

print("--- FIT ANALYSIS ---")

#PARAMETRI DA CAMBIARE
ch_min=0
ch_max=2048
save_gauss=True
save_pull=True
show_pull=False

file_path = str(out_dir / "*.bin")
file_list = glob.glob(file_path)

print("Insert the mode you want to calculate the baseline and the errors:" ,
      "\n0 for a gaussian fit in the bin_counts histogram", 
      "\n1 for a linear fit in the channel histogram",
      "\n2 for a simple mean and std numpy functions")
fit=input()
while not fit.isdigit(): 
    print("Error! Insert a number!")
    fit = input()
fit=int(fit)  

if fit==0:
    print("You have chosen the GAUSSIAN FIT")
    par_mu, par_sigma, averages, deviations = bf.Distribution(file_list, output_dr, ch_min=ch_min, ch_max=ch_max, save=save_gauss)
elif fit==1:
    print("You have chosen the LINEAR FIT")
    averages, deviations = bf.Baseline(file_list, out_dir, ch_min, ch_max, mean=mean)
elif fit==2:
    print("You have chosen the MEAN and STD method")
    averages, deviations = bf.Mean(out_dir, no_spectra, ch_min, ch_max)
else:
    print("Number not valid")
    sys.exit()

print("--- PULL ANALYSIS ---")

r=5 #Range of searching B_true
r_inf=mean-r
r_sup=mean+r

for i in range(r_inf ,r_sup ,1):
    print(f"Value of tested B_true = {i}")
    par_pull, cov_pull, pull = bf.pull(averages, deviations, i, output_dr=output_dr, fit=fit, show=show_pull, save=save_pull)

    num_sigma=3

    range_inf_pull = -num_sigma
    range_sup_pull = +num_sigma

    isto_pull=Histogram(pull, bins=50)
    area_pull, events_pull, prob_pull = isto_pull.integrate(range_inf_pull, range_sup_pull)

    print(f"\n--- INTEGRATION RANGE [{range_inf_pull:.2f} a {range_sup_pull:.2f}] ---")
    print(f"Area: {area_pull:.4f}")
    print(f"Events in the range: {events_pull} su {len(averages)} ({prob_pull*100:.1f}%)")
    print("\n----------------------------------------------------------------------------")