function res = HK(L, p, input_matrice)
% HK implementa l'algoritmo di Hoshen-Kopelman per trovare
% tutti i cluster di percolazione senza utilizzare la ricorsione (backtracking)
% Efficienza massima garantita dalla struttura "Union-Find".

res.matrice = zeros(L + 2);
if nargin >= 3
    res.matrice(2:end-1, 2:end-1) = input_matrice;
else
    aux = rand(L) < p;
    res.matrice(2:end-1, 2:end-1) = aux;
end

res.percolazioneTB = 0;
res.percolazioneLR = 0;
res.p = p;
res.label = zeros(L + 2);

% --- START PASS 1 (Costruzione del Parent Array Union-Find) ---
% Allocazione larga per i parent (al massimo N/2 clusters se "a scacchiera")
parent = zeros(1, ceil(L*L/2) + 1);
largest_label = 0;

for col = 2:L+1
    for row = 2:L+1
        if res.matrice(row, col)
            % Guardo solo "Indietro": Alto e Sinistra.
            up = res.label(row-1, col);
            left = res.label(row, col-1);

            if up == 0 && left == 0
                % Sono Isolato: Creo Nuova Etichetta
                largest_label = largest_label + 1;
                res.label(row, col) = largest_label;
                parent(largest_label) = largest_label;
            elseif up ~= 0 && left == 0
                res.label(row, col) = up;
            elseif up == 0 && left ~= 0
                res.label(row, col) = left;
            else
                % COLLISIONE: Uniamo le due radici "Union"
                root_up = find_root(up, parent);
                root_left = find_root(left, parent);

                min_root = min(root_up, root_left);
                max_root = max(root_up, root_left);

                res.label(row, col) = min_root;

                if min_root ~= max_root
                    parent(max_root) = min_root;
                end
            end
        end
    end
end

% --- START PASS 2 (Appiattimento delle Labels) ---
% Path compression massiva: ricollochi ognuno alla radice nuda
new_labels = zeros(1, largest_label);
current_label = 0;

for i = 1:largest_label
    root = find_root(i, parent);
    if new_labels(root) == 0
        current_label = current_label + 1;
        new_labels(root) = current_label;
    end
    % Mappatura densificata
    new_labels(i) = new_labels(root);
end

res.clusters = zeros(1, current_label);

% Ricostruzione ed estrazione densità matriciali
for col = 2:L+1
    for row = 2:L+1
        if res.label(row, col) > 0
            lab = new_labels(res.label(row, col));
            res.label(row, col) = lab;
            res.clusters(lab) = res.clusters(lab) + 1;
        end
    end
end

% Purge come in CercaCluster.m
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

% Eliminiamo zero-clusters
res.clusters = res.clusters(res.clusters > 0);

end

% HELPER FUNCTION (Find root recursivo per array)
function root = find_root(node, parent)
    root = node;
    while parent(root) ~= root
        root = parent(root);
    end
end
