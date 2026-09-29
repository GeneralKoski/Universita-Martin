function out=puntiRetta(lam,l,N,x)
% out=puntiRetta(lam,l,N,x)
% lam densità dei punti
% l ampiezza finestra di osservazione
% N numero di prove
% l0=l*x larghezza intervallo su cui sono distribuiti i punti
% out matrice 2xn con sulla prima riga le frequenze e sulla seconda i
% conteggi

if nargin<4
    x=1000;
end

if x<1000
    x=1000;
end

l0=l*x;

np=round(lam*l0);


punti=rand(np,1)*l0;
punti=sort(punti);

n=zeros(N,1);
for i=1:N
    finestra=rand()*(l0-l);
    n(i)=length(find(punti(find(punti>finestra))<(finestra+l)));

end
m=min(n):max(n);
nn=hist(n,m);

out(1,:)=nn/N;
out(2,:)=m;

end