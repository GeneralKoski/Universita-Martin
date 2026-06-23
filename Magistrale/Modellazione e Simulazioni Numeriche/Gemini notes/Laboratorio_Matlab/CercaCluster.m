function res = CercaCluster(L, p, input_matrice)
% res = CercaCluster(L, p, input_matrice)
% Versione modificata per l'esame: accetta una "input_matrice" esterna
% per permettere la validazione incrociata cieca con HK.

res.matrice = zeros(L + 2);

if nargin >= 3
    % Incolliamo la matrice pre-fornita
    res.matrice(2:end-1, 2:end-1) = input_matrice;
else
    % Modalita' classica, matrice casuale
    aux = rand(L) < p;
    res.matrice(2:end-1, 2:end-1) = aux;
end

res.percolazioneTB = 0;
res.percolazioneLR = 0;
res.p = p;
res.label = zeros(L + 2);
res.clusters = [];
labelC = 1;

valid = find(res.matrice);

for iter = 1:length(valid)
    ii = valid(iter);
    if (res.label(ii) == 0)
        pila = ii;
        res.label(ii) = labelC;
        j = 1;
        while (j <= length(pila))
            elemento = pila(j);
            
            if (res.matrice(elemento - 1) && res.label(elemento - 1) == 0)
                pila(end + 1) = elemento - 1;
                res.label(elemento - 1) = labelC;
            end
            if (res.matrice(elemento + 1) && res.label(elemento + 1) == 0)
                pila(end + 1) = elemento + 1;
                res.label(elemento + 1) = labelC;
            end
            if (res.matrice(elemento - L - 2) && res.label(elemento - L - 2) == 0)
                pila(end + 1) = elemento - L - 2;
                res.label(elemento - L - 2) = labelC;
            end
            if (res.matrice(elemento + L + 2) && res.label(elemento + L + 2) == 0)
                pila(end + 1) = elemento + L + 2;
                res.label(elemento + L + 2) = labelC;
            end
            j = j + 1;
        end
        res.clusters(end+1) = length(pila);
        labelC = labelC + 1;
    end
end

res.label = res.label(2 : end - 1, 2 : end - 1);
res.matrice = res.matrice(2 : end - 1, 2 : end - 1);

auxL = unique(res.label(1:L)); left = auxL(auxL > 0);
auxR = unique(res.label(L*(L-1) + 1:L*L)); right = auxR(auxR > 0);
if (~isempty(intersect(left, right)))
    res.percolazioneLR = 1;
end

auxT = unique(res.label(1:L:L*(L-1) + 1)); top = auxT(auxT > 0);
auxB = unique(res.label(L:L:L*L)); bottom = auxB(auxB > 0);
if (~isempty(intersect(top, bottom)))
    res.percolazioneTB = 1;
end
end
