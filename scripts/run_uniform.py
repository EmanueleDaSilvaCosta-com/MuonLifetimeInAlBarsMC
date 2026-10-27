import subprocess
from pathlib import Path
import os

import numpy as np
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent.parent
exe = ROOT / "build" / "uniform"
no_channels = 2048 # number of channels in the spectrum
mean = 1000 # mean of the uniform distribution
no_spectra = 1000 # number of spectra to generate
out_dir = ROOT / "data" / "uniform_spectra"  # directory to save the generated spectra

# mode = 0: read the generated spectra from the binary files, if they already exist
# mode = 1: run the C++ executable to generate the spectra and save them to binary files
mode = 1

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

i = 0  # Index of the spectrum to read back

# Load the generated spectrum from the binary file
bins = np.arange(no_channels) + 0.5
spectrum = np.fromfile(out_dir / f"spectrum{i}.bin", dtype="<u4")

plt.bar(bins, spectrum, width=1.0)
plt.show()