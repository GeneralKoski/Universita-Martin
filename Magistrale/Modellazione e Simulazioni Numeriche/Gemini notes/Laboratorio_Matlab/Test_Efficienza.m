% Test_Efficienza.m
% Questo script confronta le prestazioni di due algoritmi di cluster finding:
% 1. CercaCluster (Flood-Fill): approccio ricorsivo standard.
% 2. HK (Hoshen-Kopelman): approccio ottimizzato basato su Union-Find.
% L'obiettivo è mostrare come HK sia molto più veloce al crescere della griglia.

clear; clc; close all;

%% 1. TEST DI SCALABILITÀ: Probabilità fissa, Taglia griglia (L) variabile
p_fisso = 0.55; % Usiamo una densità vicina alla soglia per mettere sotto sforzo i codici
L_array = [50, 100, 200, 300, 400, 600]; % Testiamo griglie da 50x50 fino a 600x600

tempi_base_L = zeros(1, length(L_array));
tempi_hk_L   = zeros(1, length(L_array));

disp('--- [1/2] Test su dimensione griglia (L) in corso ---');
for i = 1:length(L_array)
    L = L_array(i);
    M = rand(L) < p_fisso; % Generiamo una griglia casuale

    % Testiamo l'algoritmo ricorsivo (Flood-Fill)
    tic; CercaCluster(L, p_fisso, M); tempi_base_L(i) = toc;

    % Testiamo l'algoritmo di Hoshen-Kopelman
    tic; HK(L, p_fisso, M); tempi_hk_L(i) = toc;

    disp([' -> Griglia ' num2str(L) 'x' num2str(L) ' analizzata.']);
end

%% 2. TEST DI SFORZO: Taglia griglia (L) fissa, Probabilità (p) variabile
L_fisso = 400; % Griglia abbastanza grande da far sentire la differenza
p_array = 0.1:0.1:0.9;

tempi_base_p = zeros(1, length(p_array));
tempi_hk_p   = zeros(1, length(p_array));

disp('--- [2/2] Test su densità (p) in corso ---');
for i = 1:length(p_array)
    p = p_array(i);
    M = rand(L_fisso) < p;

    tic; CercaCluster(L_fisso, p, M); tempi_base_p(i) = toc;
    tic; HK(L_fisso, p, M); tempi_hk_p(i) = toc;

    disp([' -> Probabilità p = ' num2str(p) ' analizzata.']);
end

%% GENERAZIONE DEI GRAFICI DI CONFRONTO
figure('Name', 'Confronto Efficienza Algoritmica', 'Position', [100 100 1000 450]);

% Grafico 1: Tempo vs Dimensione griglia
subplot(1,2,1);
plot(L_array, tempi_base_L, 'r-o', 'LineWidth', 1.5, 'MarkerFaceColor','r'); hold on;
plot(L_array, tempi_hk_L, 'b-s', 'LineWidth', 1.5, 'MarkerFaceColor','b');
grid on;
title(sprintf('Esecuzione vs Taglia (p_{fisso} = %0.2f)', p_fisso));
xlabel('Taglia Reticolo (L)');
ylabel('Tempo d''Esecuzione (secondi)');
legend({'CercaCluster (Flood)', 'HK (Union-Find)'}, 'Location', 'NorthWest');

% Grafico 2: Tempo vs Densità di occupazione
subplot(1,2,2);
plot(p_array, tempi_base_p, 'r-o', 'LineWidth', 1.5, 'MarkerFaceColor','r'); hold on;
plot(p_array, tempi_hk_p, 'b-s', 'LineWidth', 1.5, 'MarkerFaceColor','b');
grid on;
title(sprintf('Esecuzione vs Densità (L = %d)', L_fisso));
xlabel('Probabilità Colorazione (p_{col})');
ylabel('Tempo d''Esecuzione (secondi)');
legend({'CercaCluster (Flood)', 'HK (Union-Find)'}, 'Location', 'NorthWest');

% Salvataggio dell'immagine per la relazione
disp('Confronti terminati correttamente.');
