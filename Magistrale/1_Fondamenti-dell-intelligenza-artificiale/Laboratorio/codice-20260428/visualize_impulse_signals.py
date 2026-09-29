import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Carica il dataset
df = pd.read_csv('data/impulse_signals_dataset_noisy.csv')

# Separa i segnali per classe
class_0 = df[df['label'] == 0].drop('label', axis=1).values
class_1 = df[df['label'] == 1].drop('label', axis=1).values

# Crea figura con sottotrame
fig, axes = plt.subplots(4, 2, figsize=(14, 10))
fig.suptitle('Dataset di Segnali di Impulsi Acustici', fontsize=16, fontweight='bold')

# Visualizza 4 segnali per classe
for i in range(4):
    # Classe 0 - impulsi nella prima metà
    ax = axes[i, 0]
    ax.plot(class_0[i], 'b-', linewidth=1.5)
    ax.set_title(f'Classe 0 - Segnale {i+1}\n(Impulsi prima metà)', fontsize=10)
    ax.set_xlabel('Tempo (sample)')
    ax.set_ylabel('Ampiezza')
    ax.grid(True, alpha=0.3)
    ax.axvline(x=50, color='r', linestyle='--', alpha=0.5, label='Metà')
    ax.legend()
    
    # Classe 1 - impulsi nella seconda metà
    ax = axes[i, 1]
    ax.plot(class_1[i], 'g-', linewidth=1.5)
    ax.set_title(f'Classe 1 - Segnale {i+1}\n(Impulsi seconda metà)', fontsize=10)
    ax.set_xlabel('Tempo (sample)')
    ax.set_ylabel('Ampiezza')
    ax.grid(True, alpha=0.3)
    ax.axvline(x=50, color='r', linestyle='--', alpha=0.5, label='Metà')
    ax.legend()

plt.tight_layout()
plt.show()

# Crea una visualizzazione media dei segnali per classe
fig, axes = plt.subplots(1, 2, figsize=(14, 5))
fig.suptitle('Media dei Segnali per Classe', fontsize=14, fontweight='bold')

# Media classe 0
mean_class_0 = np.mean(class_0, axis=0)
axes[0].plot(mean_class_0, 'b-', linewidth=2, marker='o', markersize=3)
axes[0].fill_between(range(len(mean_class_0)), mean_class_0, alpha=0.3)
axes[0].set_title('Media - Classe 0 (Impulsi prima metà)', fontsize=12)
axes[0].set_xlabel('Tempo (sample)')
axes[0].set_ylabel('Ampiezza media')
axes[0].grid(True, alpha=0.3)
axes[0].axvline(x=50, color='r', linestyle='--', alpha=0.5, label='Metà', linewidth=2)
axes[0].legend()

# Media classe 1
mean_class_1 = np.mean(class_1, axis=0)
axes[1].plot(mean_class_1, 'g-', linewidth=2, marker='o', markersize=3)
axes[1].fill_between(range(len(mean_class_1)), mean_class_1, alpha=0.3)
axes[1].set_title('Media - Classe 1 (Impulsi seconda metà)', fontsize=12)
axes[1].set_xlabel('Tempo (sample)')
axes[1].set_ylabel('Ampiezza media')
axes[1].grid(True, alpha=0.3)
axes[1].axvline(x=50, color='r', linestyle='--', alpha=0.5, label='Metà', linewidth=2)
axes[1].legend()

plt.tight_layout()
plt.show()

print("Statistiche del dataset:")
print(f"Classe 0 - Media: {np.mean(class_0):.4f}, Std: {np.std(class_0):.4f}")
print(f"Classe 1 - Media: {np.mean(class_1):.4f}, Std: {np.std(class_1):.4f}")
