clear
clc
format long

dim = 100000;
L = zeros(1, dim);
l = 5;
d = 0.2;
iterations = [1000 5000 10000 50000 100000 500000 1000000 5000000 10000000 50000000];
%Frequenze = [];

n = d*dim;
while n > 0
    i = ceil(rand()*dim);
    if(L(i) == 1)
        continue
    end
    L(i) = 1;
    n = n - 1;
end

Media_Punti_Attesa = l * d;
Densita = d;

for i = 1:numel(iterations)
    iter = iterations(i);
    Punti_Sottointervallo = [];
    while iter > 0
        idx = ceil(rand()*dim);
        if(idx > dim - l)
            continue
        end
        Punti_Sottointervallo(end+1) = sum(L(idx:idx+l-1));
        iter = iter - 1;
    end

    Iterazioni = iterations(i);
    
    Freq = hist(Punti_Sottointervallo,min(Punti_Sottointervallo):max(Punti_Sottointervallo));
    Frequenze{i} = Freq/Iterazioni;
    Misure{i} = min(Punti_Sottointervallo):max(Punti_Sottointervallo);

end
