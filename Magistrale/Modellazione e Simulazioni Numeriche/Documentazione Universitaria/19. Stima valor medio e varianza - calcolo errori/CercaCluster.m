function res = CercaCluster(L, p)
% res = CercaCluster(L, p)
% CercaCluster trova i cluster su un reticolo L x L con probabilità p di
% avere un sito colorato
%
% input:
%       L: lunghezza lato matrice
%       p: probabilità di colorare un sito della matrice
%
% ritorna:
%       res.p: probabilità di avere un sito colorato
%       res.matrice: matrice dei siti colorati
%       res.label: matrice delle etichette dei cluster trovati
%       res.percolazioneTB: valore di esistenza di percolazione partendo
%       dal bordo superiore al bordo inferiore       
%       res.percolazioneLR: valore di esistenza di percolazione partendo
%       dal bordo sinistro al bordo destro


res.matrice = zeros(L + 2);
aux = rand(L) < p;
res.matrice(2:end-1, 2:end-1) = aux;

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
        % nuovo cluster, esploro i vicini

        pila = ii;
        res.label(ii) = labelC;

        j = 1;
        while (j <= length(pila))
            elemento = pila(j);
            
            % aggiungo i vicini alla pila
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

auxL = unique(res.label(1:L));
left = auxL(auxL > 0);

auxR = unique(res.label(L*(L-1) + 1:L*L));
right = auxR(auxR > 0);

if (~isempty(intersect(left, right)))
    res.percolazioneLR = 1;
end

auxT = unique(res.label(1:L:L*(L-1) + 1));
top = auxT(auxT > 0);

auxB = unique(res.label(L:L:L*L));
bottom = auxB(auxB > 0);

if (~isempty(intersect(top, bottom)))
    res.percolazioneTB = 1;
end
end