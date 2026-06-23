#!/usr/bin/env python3

import matplotlib
matplotlib.use('Agg')   # Backend per PNG
import matplotlib.pyplot as plt
import pandas as pd
import glob

# Lista dei file da leggere
files = glob.glob("heat_gpu_block_*_scaling.dat")

# Lista per contenere tutti i DataFrame
df_list = []

# Legge i dati da ogni file e li aggiunge alla lista
for file in files:
    df = pd.read_csv(file, names=["device", "matrix_dim_x", "matrix_dim_y", "block_dim_x", "block_dim_y", "grid_dim_x", "grid_dim_y", "iterations", "time"])
    df["blocksize"] = file.split('_')[3]  # Estrae la dimensione del blocco dal nome del file
    df_list.append(df)

# Concatena tutti i DataFrame in uno solo
df_all = pd.concat(df_list)

# Filtra i dati per il dispositivo GPU
df_gpu = df_all[df_all["device"] == "GPU"]

# Verifica i dati filtrati
print(df_gpu)

# Crea il grafico
plt.figure(figsize=(10, 6))
plt.title('Heat GPU Matrix Scaling')
plt.grid(True)
plt.xlabel('Matrix Dimension (N x N)')
plt.ylabel('Time (seconds)')

# Plot dei dati per ogni dimensione di blocco
for blocksize in df_gpu["blocksize"].unique():
    df_block = df_gpu[df_gpu["blocksize"] == blocksize]
    plt.plot(df_block["matrix_dim_x"], df_block["time"], '-o', label="Blocksize {}".format(blocksize))

# Aggiunge la legenda
plt.legend(shadow=True, loc="best")

# Salva il grafico in un file PNG
plt.savefig("heat_gpu_block_scaling.png")

