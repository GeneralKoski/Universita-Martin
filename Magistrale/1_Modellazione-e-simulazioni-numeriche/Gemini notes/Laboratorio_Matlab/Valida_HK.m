% Valida_HK.m
% Script Autodiagnostico (da testare) per mostrare l'equivalenza
% tra l'algoritmo classico flood e Hoshen-Kopelman, stampando tempi ed efficacia.

clear; clc;

% Impostazioni iniziali
L = 500;
p = 0.59; % Piazzato vicino alla soglia asintotica bidimensionale per pesare l'array tree

disp(['Generazione Matrice Cieca: ', num2str(L), 'x', num2str(L), ' al ', num2str(p*100), '% di percolazione']);
matrice_test = rand(L) < p;
disp('----------------------------------');

%% 1) TEST: RICERCA STANDARD CON LA PILA INFLOODING
disp('Esecuzione: CercaCluster (Visto a Lezione, metodo Pila)');
tic;
res_base = CercaCluster(L, p, matrice_test);
tempi_base = toc;
disp(['Completato in: ', num2str(tempi_base), ' sec']);

disp(' ');

%% 2) TEST: HOSHEN-KOPELMAN (Union-Find)
disp('Esecuzione: Hoshen-Kopelman (HK UNION-FIND)');
tic;
res_HK = HK(L, p, matrice_test);
tempi_hk = toc;
disp(['Completato in: ', num2str(tempi_hk), ' sec']);

disp('----------------------------------');
%% VERDETTO ED EQUIVALENZE LOGICHE
disp('... Verifica incrociata in corso ...');

% Sort delle taglie dei cluster poiché vengono numerati con ID generativi diversi
% ma topologicamente la spartizione delle masse deve essere categorica
cluster_base = sort(res_base.clusters);
cluster_hk = sort(res_HK.clusters);

perc_base = (res_base.percolazioneLR + res_base.percolazioneTB) > 0;
perc_hk = (res_HK.percolazioneLR + res_HK.percolazioneTB) > 0;

validity = true;

if length(cluster_base) ~= length(cluster_hk) || any(cluster_base ~= cluster_hk)
    disp(' > ERRORE: Le cluster map estratte non combaciano');
    validity = false;
end

if perc_base ~= perc_hk
    disp(' > ERRORE: Divergenza di opinione su check percolante bordo-bordo');
    validity = false;
end

if validity
    disp('>>> VERDETTO: SUPERATO!');
    disp('Entrambi gli algoritmi producono identica segmentazione frattale dei cluster.');
    disp(['Aumento di Efficienza (Speedup HK): x', num2str(tempi_base / tempi_hk)]);
else
    disp('====== TEST FALLITO ====== ');
end
