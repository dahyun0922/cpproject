!pip install root

import ROOT
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from ROOT import TGraph, TF1

df = pd.read_excel("research_data.xlsx")

year = np.array(df["year"], float)
papers = np.array(df["papers"], float)
budget = np.array(df["budget"], float)
researchers = np.array(df["researchers"], float)

print("Budget r =", round(np.corrcoef(budget, papers)[0,1], 4))
print("Researchers r =", round(np.corrcoef(researchers, papers)[0,1], 4))

class Linear:
    def __call__(self, x, par):
        return par[0] + par[1] * x[0]

g1 = TGraph(len(budget), budget, papers)
f1 = TF1("f1", Linear(), min(budget), max(budget), 2)
g1.Fit(f1, "Q")

g2 = TGraph(len(researchers), researchers, papers)
f2 = TF1("f2", Linear(), min(researchers), max(researchers), 2)
g2.Fit(f2, "Q")

print("Papers = %.2f + %.2f × Budget"
      % (f1.GetParameter(0), f1.GetParameter(1)))

print("Papers = %.2f + %.2f × Researchers"
      % (f2.GetParameter(0), f2.GetParameter(1)))

x1 = np.linspace(min(budget), max(budget), 50)
y1 = f1.GetParameter(0) + f1.GetParameter(1) * x1

x2 = np.linspace(min(researchers), max(researchers), 50)
y2 = f2.GetParameter(0) + f2.GetParameter(1) * x2

fig, ax = plt.subplots(2, 2, figsize=(10, 8))

ax[0,0].scatter(budget, papers)
ax[0,0].plot(x1, y1)
ax[0,0].set_title("Budget")
ax[0,0].set_xlabel("Budget")
ax[0,0].set_ylabel("Papers")

ax[0,1].scatter(researchers, papers)
ax[0,1].plot(x2, y2)
ax[0,1].set_title("Researchers")
ax[0,1].set_xlabel("Researchers")
ax[0,1].set_ylabel("Papers")

ax[1,0].plot(year, budget, "o-")
ax[1,0].set_title("Budget vs Year")
ax[1,0].set_xlabel("Year")
ax[1,0].set_ylabel("Budget")

ax[1,1].plot(year, researchers, "o-")
ax[1,1].set_title("Researchers vs Year")
ax[1,1].set_xlabel("Year")
ax[1,1].set_ylabel("Researchers")

plt.tight_layout()
plt.show()
