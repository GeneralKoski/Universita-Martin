function res = TreCarteDULL(N,plotFLAG)
%res = TreCarteDULL(N,plotFLAG)
%Esperimento su N realizzazioni del
%gioco delle tre carte;
%se passiamo un plotFLAG~=0, disegna gli istogrammi
%con le frequenze di vincita delle 
%diverse strategie (aggiornate al momento)


if nargin==1
    plotFLAG=0;
end

W_1stchoice = 0;
W_change = 0;
W_rand = 0;

cards0 = [0 0 1];

for i = 1:N,

% Disponiamo le carte a caso
    cards = cards0(randperm(3));

% Scegliamo una carta a caso
    choice = ceil(3*rand);
    first_choice = cards(choice);
% Ecco le carte rimanenti
    others = cards(find([1 2 3]~=choice));

% Questa sicuramente perde, e la scopriamo
    out = min(find(~others));
% Questa è quella che rimane coperta
    left = others(find([1 2]~=out));

% Ecco la scelta fra le due rimaste coperte
    cards2 = [first_choice left];
    rand_choice = cards2(ceil(2*rand));
    
    if first_choice,
        W_1stchoice = W_1stchoice + 1;
    end;
    
    if left,
        W_change = W_change + 1;
    end;
    
    if rand_choice,
        W_rand = W_rand + 1;
    end;
    
    W_1st = W_1stchoice/i;
    W_ch = W_change/i;
    W_ra  = W_rand/i;
    
    WW = [W_1st W_ch W_ra];
    
    if plotFLAG
        bar(WW);
        hold on
        axis([0.5 3.5 0 0.9]);
        title(num2str(i))
        plot([0 3.5],[1/3 1/3],'b')
        plot([0 3.5],[2/3 2/3],'r')
        plot([0 3.5],[1/2 1/2],'g')
        pause(0.001)
        hold off
    end
    
end;

res(1) = W_1stchoice/N;
res(2) = W_change/N;
res(3) = W_rand/N;
