function res = processoEstrazione(startConfig, T)
% 1 = biglia nera
%0 = biglia bianca
%startConfig = vettore di 5 elementii

configurazione = startConfig;

for i = 1:T
    estrattaU3 = randi(3);
    estrattaU2 = randi(2) + 3;
    
    temp = configurazione(estrattaU3);
    configurazione(estrattaU3) = configurazione(estrattaU2);
    configurazione(estrattaU2) = temp;
    
    res(i) = sum(configurazione(1:3));
end
end

