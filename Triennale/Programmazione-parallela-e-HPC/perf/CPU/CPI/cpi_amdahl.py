import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt 

tnp=1.00050
tp=21.74374

Qp=int(100*tp/(tp+tnp))
etichetta="Amdahl  %d%% parallelizzabile " % (Qp)

N=[1,2,4,8,16,32]  # numero processori
Samdahl=[(tnp+tp)/(tnp+tp/n) for n in N]

plt.title('CPI -  Legge di Amdahl')
plt.grid()
plt.xlabel('Processors')
plt.ylabel('Speedup')
plt.plot(N,Samdahl,'g-o',label=etichetta)
plt.plot(N,N,'r-',label='ideal')
plt.legend(shadow=True)
plt.savefig('cpi_amdahl.png')
