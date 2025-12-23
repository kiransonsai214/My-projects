# -----------------------------------------------------------
# Optical Absorption, Bandgap (Eg), and Urbach (EU) Calculation
# Without NumPy — using only 4 data points
# -----------------------------------------------------------

import math
import matplotlib.pyplot as plt
from grex import intake
import time
def you():
    line=intake()
    values = line.split(',')
    if len(values) == 4:
        a,b,c,d = map(int, values)
        return a,b,c,d

r1, y1, g1, b1=you()
print(r1, y1, g1, b1)
k1=[r1, y1, g1, b1]
time.sleep(2)
print("place the sample!\nclose the box")
ask=input("enter (yes) to continue : ")
if ask.lower() == 'yes':
    r2, y2, g2, b2=you()
    print(r2, y2, g2, b2)
    k2=[r2, y2, g2, b2]

# ---------------- INPUT SECTION ----------------
# Enter 4 wavelength values (in nanometers)
wavelengths = [620, 570, 495, 450]

# Corresponding incident (reference) and transmitted (sample) intensities
I0_values = k1   # reference (no sample)
I_values  = k2   # measured through sample

# Sample thickness in meters (example: 100 micrometers = 1e-4 m)
d = 1e-4

# ---------------- CALCULATIONS ----------------

# Step 1: Photon energy hν (eV)
hv = []
for wl in wavelengths:
    hv.append(1240 / wl)

# Step 2: Transmittance (T) and Absorption Coefficient (α)
T = []
alpha = []
for i in range(4):
    T_val = I_values[i] / I0_values[i]
    T.append(T_val)
    alpha_val = - (1 / d) * math.log(T_val)
    alpha.append(alpha_val)

# Step 3: Tauc plot values (for direct bandgap)
tauc_y = []
for i in range(4):
    val = (alpha[i] * hv[i]) ** 2
    tauc_y.append(val)

# Step 4: Estimate Bandgap Eg (roughly by interpolating between last two points)
Eg = hv[2] - ((tauc_y[2]) / (tauc_y[3] - tauc_y[2])) * (hv[3] - hv[2])

# Step 5: Urbach Energy EU (slope of ln(alpha) vs hv in low-energy region)
ln_alpha = [math.log(abs(a)) if a !=0 else 0 for a in alpha]
slope = (ln_alpha[1] - ln_alpha[0]) / (hv[1] - hv[0])
EU = 1 / slope

# ---------------- OUTPUT TABLE ----------------
print("---------------------------------------------------")
print("Wavelength (nm) | hν (eV) | T | α (1/m) | (αhν)^2")
print("---------------------------------------------------")
for i in range(4):
    print(f"{wavelengths[i]:>8}        {hv[i]:>6.2f}   {T[i]:.2f}   {alpha[i]:.2e}   {tauc_y[i]:.2e}")
print("---------------------------------------------------")
print(f"Estimated Bandgap Energy (Eg) ≈ {Eg:.3f} eV")
print(f"Estimated Urbach Energy (EU)  ≈ {EU:.3f} eV")
print("---------------------------------------------------")

# ---------------- PLOTTING ----------------

# Plot 1: Tauc plot
plt.figure(figsize=(7,5))
plt.plot(hv, tauc_y, 'bo-', label='(αhν)^2 data')
plt.xlabel("Photon Energy hν (eV)")
plt.ylabel("(αhν)² (arbitrary units)")
plt.title("Tauc Plot — Bandgap Estimation")
plt.grid(True)
plt.legend()
plt.tight_layout()

# Plot 2: Urbach plot
plt.figure(figsize=(7,5))
plt.plot(hv, ln_alpha, 'ro-', label='ln(α) data')
plt.xlabel("Photon Energy hν (eV)")
plt.ylabel("ln(α)")
plt.title("Urbach Plot — Disorder Estimation")
plt.grid(True)
plt.legend()
plt.tight_layout()

plt.show()