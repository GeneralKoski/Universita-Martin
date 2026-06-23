#!/usr/bin/env python3

import matplotlib
matplotlib.use('Agg')   # Backend per PNG
import matplotlib.pyplot as plt
import pandas as pd

# Legge i dati dal file heat_gpu_mat_scaling.dat
df = pd.read_csv("heat_gpu_mat_scaling.dat", 
                 names=["device", "matrix_dim_x", "matrix_dim_y", "block_dim_x", "block_dim_y", "grid_dim_x", "grid_dim_y", "iterations", "time"])

# Filtra i dati per il dispositivo GPU
df_gpu = df[df["device"] == "GPU"]

# Verifica i dati filtrati
print(df_gpu)

# Crea il grafico
plt.figure(figsize=(10, 6))
plt.title('Heat GPU Matrix Scaling')
plt.grid(True)
plt.xlabel('Matrix Dimension (N x N)')
plt.ylabel('Time (seconds)')

# Plot dei dati
plt.plot(df_gpu["matrix_dim_x"], df_gpu["time"], '-o', label="GPU")

# Aggiunge la legenda
plt.legend(shadow=True, loc="best")

# Salva il grafico in un file PNG
plt.savefig("heat_gpu_mat_scaling.png")

