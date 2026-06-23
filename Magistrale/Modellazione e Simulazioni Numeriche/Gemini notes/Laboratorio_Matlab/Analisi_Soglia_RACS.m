% Analisi_Soglia_RACS.m
% Questo script esegue uno studio statistico completo sulla percolazione:
% 1. Individua la soglia critica tramite la curva a "S" (Sigmoide)
% 2. Calcola la forza del cluster gigante (Parametro d'ordine P1)
% 3. Analizza la dimensione media dei cluster (RACS) per vedere il "picco" critico

clear; clc; close all;

%% == IMPOSTAZIONE SIMULAZIONE ==
L = 100;                % Lato della griglia (100x100)
N_proved = 1000;        % Numero di simulazioni per ogni punto (campione Monte Carlo)

% Definiamo i valori di probabilità 'p' da testare (più fitti vicino alla soglia 0.59)
p_color = [0.1:0.1:0.4, 0.45:0.02:0.7, 0.75:0.05:0.9];
num_p = length(p_color);

%% Inizializzazione degli array per i risultati (Medie ed Errori)
perc_med = zeros(1, num_p); perc_err = zeros(1, num_p);
P1_med   = zeros(1, num_p); P1_err   = zeros(1, num_p);
racs_med = zeros(1, num_p); racs_err = zeros(1, num_p);

disp(['== AVVIO SIMULAZIONE (Griglia ' num2str(L) 'x' num2str(L) ', Prove=' num2str(N_proved) ') ==']);
tic;

%% CICLO MONTE CARLO
% Per ogni valore di densità p, eseguiamo N_proved simulazioni indipendenti
for k = 1:num_p
    p = p_color(k);

    val_perc = zeros(1, N_proved);
    val_P1   = zeros(1, N_proved);
    val_RACS = zeros(1, N_proved);

    for i = 1:N_proved
        % Eseguiamo l'algoritmo di Hoshen-Kopelman
        res = HK(L, p);

        % Verifichiamo se il sistema percola (in orizzontale o verticale)
        val_perc(i) = (res.percolazioneTB + res.percolazioneLR) > 0;

        if isempty(res.clusters)
             val_P1(i) = 0;
             val_RACS(i) = 0;
             continue;
        end

        tutti_i_cluster = res.clusters;
        s_mas = max(tutti_i_cluster);

        % P1: Frazione di siti occupata dal cluster più grande
        val_P1(i) = s_mas / (L^2);

        % RACS: Dimensione media dei cluster escludendo quello gigante
        dim_denom = sum(tutti_i_cluster);
        if length(tutti_i_cluster) <= 1
            val_RACS(i) = 0;
        else
            % Togliamo il cluster gigante per analizzare la massa rimanente
            s_rimanenti = tutti_i_cluster;
            idx_smax = find(s_rimanenti == s_mas, 1);
            s_rimanenti(idx_smax) = [];

            % Formula del RACS (media pesata sulla massa totale)
            val_RACS(i) = sum(s_rimanenti.^2) / dim_denom;
        end
    end

    % Calcolo delle medie e dell'errore statistico (deviazione standard della media)
    perc_med(k) = mean(val_perc);
    perc_err(k) = std(val_perc) / sqrt(N_proved);

    P1_med(k) = mean(val_P1);
    P1_err(k) = std(val_P1) / sqrt(N_proved);

    racs_med(k) = mean(val_RACS);
    racs_err(k) = std(val_RACS) / sqrt(N_proved);

    disp(sprintf('-> Densità %.2f completata', p));
end

time_tot = toc;
disp(sprintf('Simulazione conclusa in %.1f secondi.', time_tot));

%% CREAZIONE DEI GRAFICI
figure('Name', 'Analisi Termodinamica della Percolazione', 'Position', [100 100 1400 450]);

% Pannello 1: Probabilità di Percolazione (Curva a S)
subplot(1, 3, 1);
errorbar(p_color, perc_med, perc_err, 'g-o', 'LineWidth', 1.5, 'MarkerFaceColor','g');
grid on; hold on;
plot([0 1], [0.5 0.5], 'r--', 'HandleVisibility', 'off');
title(sprintf('Transizione di Fase (L = %d)', L));
xlabel('Densità Colorazione (p_{col})');
ylabel('P_{perc} (Prob. di Percolamento)');

% Pannello 2: Parametro d'ordine P1 (Crescita del cluster gigante)
subplot(1, 3, 2);
errorbar(p_color, P1_med, P1_err, 'b-d', 'LineWidth', 1.5, 'MarkerFaceColor', 'b');
grid on;
title(sprintf('Rateo Cluster Dominante P_1 (L = %d)', L));
xlabel('Densità Colorazione (p_{col})');
ylabel('s_{max} / L^2 (Frazione Occupata)');

% Pannello 3: RACS (Il picco critico o "vulcano")
subplot(1, 3, 3);
errorbar(p_color, racs_med, racs_err, 'm-p', 'LineWidth', 1.5, 'MarkerFaceColor', 'm');
grid on;
title(sprintf('Reduced Average Cluster Size (L = %d)', L));
xlabel('Densità Colorazione (p_{col})');
ylabel('RACS');

% Salvataggio dell'immagine per la relazione
disp('Simulazione terminata.');
