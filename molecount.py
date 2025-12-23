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
print('''values for E:\n
       methyblue == 7\n
       potassium == 1.3''')
E=float(input('enter value of E :'))
ask=input("enter (yes) to continue : ")
if ask.lower() == 'yes':
    r2, y2, g2, b2=you()
    print(r2, y2, g2, b2)
    k2=[r2, y2, g2, b2]


wavelengths = [620, 570, 495, 450]
hv = []
for wl in wavelengths:
    hv.append(1240 / wl)


I0_values = k1   # reference (no sample)
I_values  = k2
L = 1
T = []
alpha = []
for i in range(4):
    T_val = I_values[i] / I0_values[i]
    T.append(T_val)
    alpha_val = - (1) * math.log10(T_val)
    alpha.append(alpha_val)

c=[a/(E*L) for a in alpha]
print(c)
print(round(abs(sum(c)/len(c)),6),'mol/liter')

plt.figure(figsize=(7,5))
plt.plot(hv, c, 'bo-', label='consentation respound')
plt.xlabel("Photon Energy hν (eV)")
plt.ylabel("concentration")
plt.title("'consentation respound'")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()

 
