%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%% DATI INPUT

% persona(a).
% persona(b).
% persona_dice_che(a, bugiardo(a)).
% persona_dice_che(a, bugiardo(b)).


persona(a).
persona(b).
persona(c).
persona_dice_che(a, onesto(b)).
persona_dice_che(a, onesto(c)).
persona_dice_che(b, bugiardo(a)).
persona_dice_che(b, onesto(c)).



%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%% PROGRAMMA -> Proprietà generali sempre vere

bugiardo(X) :- persona(X), not onesto(X).
onesto(X) :- persona(X), not bugiardo(X).

% onesto(X) :- onesto(Y), persona_dice_che(Y, onesto(X)).
% bugiardo(X) :- onesto(Y), persona_dice_che(Y, bugiardo(X)).

%% modello falsità totale del bugiardo
%bugiardo(X) :- bugiardo(Y), persona_dice_che(Y, onesto(X)).
%onesto(X) :- bugiardo(Y), persona_dice_che(Y, bugiardo(X)).

valuto_affermazione(X, onesto(Y), vero):- persona_dice_che(X, onesto(Y)), 
                                          onesto(Y).
valuto_affermazione(X, bugiardo(Y), vero):- persona_dice_che(X, bugiardo(Y)), 
                                            bugiardo(Y).
valuto_affermazione(X, onesto(Y), falso):- persona_dice_che(X, onesto(Y)), 
                                          bugiardo(Y).
valuto_affermazione(X, bugiardo(Y), falso):- persona_dice_che(X, bugiardo(Y)), 
                                            onesto(Y).                                            


valutazione_onesta(X, bugiardo):- persona(X), 
                                  valuto_affermazione(X, _ , falso).
valutazione_onesta(X, onesto):- persona(X), 
                                not valutazione_onesta(X, bugiardo),
                                persona_dice_che(X, _ ).
valutazione_onesta(X, non_so):- not valutazione_onesta(X, bugiardo),
                                not valutazione_onesta(X, onesto),
                                persona(X).

:- onesto(X), valutazione_onesta(X, bugiardo).
:- bugiardo(X), valutazione_onesta(X, onesto).

#show valuto_affermazione/3.
#show onesto/1.
#show bugiardo/1.
#show valutazione_onesta/2.