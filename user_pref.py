# user_pref.py
#
# Author: Corbin Bremmeyr
# Date: 21 April 2021
#
# CIS 320 Final Project: Best time for boating on lake Michigan
# Generate star chart to show the user set weights

import numpy as np
import matplotlib.pyplot as plt

# User set weights
# Bigger numbers indecate that the consideration of that metric is more important
# positive values if the value is perfered to be higher, negative if values are perfered to be smaller
# My personal values for dinghie sailboating
user_weights = [
        0.80,   # Wind speed
       -0.65,   # Wave height
        0.75,   # Air temp
        0.70,   # Water temp
        ]
abs_user_weights = []
for w in user_weights:
    abs_user_weights.append(abs(w))
abs_user_weights += abs_user_weights[:1]

labels = ["Wind\nSpeed", "Wave\nHeight", "Air\nTemperature", "Water\nTemperature"]
angles = np.linspace(0, 2*np.pi, len(labels), endpoint=False).tolist()
angles += angles[:1]

fig, ax = plt.subplots(figsize=(6,6), subplot_kw=dict(polar=True))

ax.plot(angles, abs_user_weights, linewidth=1)
ax.fill(angles, abs_user_weights, alpha=0.25)

ax.set_theta_offset(np.pi/2)
ax.set_theta_direction(-1)
ax.set_ylim(bottom=0.0, top=1.0)

#ax.set_rgrids([])
ax.set_thetagrids(np.degrees(angles[:-1]), labels)

plt.show()

