function res = processoEstrazione2(startConfig, T)
% 1 = biglia nera
%0 = biglia bianca
%startConfig = vettore di 5 elementii

configurazione = startConfig;

for i = 1:T
    estrattaU3 = randi(3);
    ii = find(~((1:3)==estrattaU3));

    
    temp = configurazione(ii);
    configurazione(ii) = configurazione(4:5);
    configurazione(4:5) = temp;
    
    res(i) = sum(configurazione(1:3));
end
end

