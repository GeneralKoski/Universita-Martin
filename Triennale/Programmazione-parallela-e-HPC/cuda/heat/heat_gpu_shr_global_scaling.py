#!/usr/bin/env python

import matplotlib
matplotlib.use('Agg')  # Backend per PNG
import matplotlib.pyplot as plt
import pandas as pd

# Legge i dati dal file heat_gpu_scaling.dat
df_global = pd.read_csv("heat_gpu_scaling.dat",
                        names=["device", "matrix_dim_x", "matrix_dim_y", "block_dim_x", "block_dim_y", "n_block_x", "n_block_y", "iter", "time"])

df_shr = pd.read_csv("heat_gpu_shr_scaling.dat",
                     names=["device", "matrix_dim_x", "matrix_dim_y", "block_dim_x", "block_dim_y", "n_block_x", "n_block_y", "iter", "time"])

# Filtra i dati per il dispositivo GPU
df_gpu_global = df_global[df_global["device"] == "GPU"]
df_gpu_shr = df_shr[df_shr["device"] == "GPU"]

# Verifica i dati filtrati
print(df_gpu_global)
print(df_gpu_shr)

# Crea il grafico
plt.figure(figsize=(10, 8))
plt.title('Heat GPU Scaling')
plt.grid(True)
plt.xlabel('Matrix Dimension (N x N)')
plt.ylabel('Time (seconds)')

# Plot dei dati
plt.plot(df_gpu_global["matrix_dim_x"], df_gpu_global["time"], '-o', label="GPU_global")
plt.plot(df_gpu_shr["matrix_dim_x"], df_gpu_shr["time"], '-o', label="GPU_shared")

# Aggiunge la legenda
plt.legend(shadow=True, loc="best")

# Salva il grafico in un file PNG
plt.savefig("heat_gpu_shr_global_scaling.png")

