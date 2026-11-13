persona(a).
persona(b).

bugiardo(X) :- persona(X), not onesto(X).
onesto(X) :- persona(X), not bugiardo(X).

% a dice: (a è bugiardo AND B è bugiardo).

persona_dice_che(a, bugiardo_a).
persona_dice_che(a, bugiardo_b).

onesto(a) :- onesto(a), persona_dice_che(a, onesto_a).
onesto(b) :- onesto(a), persona_dice_che(a, onesto_b).
bugiardo(a) :- onesto(a), persona_dice_che(a, bugiardo_a).
bugiardo(b) :- onesto(a), persona_dice_che(a, bugiardo_b).

%%%% tutto quello che dice a è falso
% bugiardo(a) :- bugiardo(a), persona_dice_che(a, onesto_a).
% bugiardo(b) :- bugiardo(a), persona_dice_che(a, onesto_b).
% onesto(a) :- bugiardo(a), persona_dice_che(a, bugiardo_a).
% onesto(b) :- bugiardo(a), persona_dice_che(a, bugiardo_b).

%%%% almento una affermazione di a è falsa (se a è bugiardo)
bugiardo(a) :- bugiardo(a), persona_dice_che(a, onesto_a),f1.
bugiardo(b) :- bugiardo(a), persona_dice_che(a, onesto_b),f2.
onesto(a) :- bugiardo(a), persona_dice_che(a, bugiardo_a),f3.
onesto(b) :- bugiardo(a), persona_dice_che(a, bugiardo_b),f4.


possibile(f1).
possibile(f2).
possibile(f3).
possibile(f4).

f1 :- possibile(f1), not f1_falso.
f2 :- possibile(f2), not f2_falso.
f3 :- possibile(f3), not f3_falso.
f4 :- possibile(f4), not f4_falso.

f1_falso :- possibile(f1), not f1.
f2_falso :- possibile(f2), not f2.
f3_falso :- possibile(f3), not f3.
f4_falso :- possibile(f4), not f4.


% persona_dice_che(a, bugiardo_a).
% persona_dice_che(a, bugiardo_b).

% limitare le scelte dei flag se non ci sono affermazioni
f1_falso :- not persona_dice_che(a, onesto_a).
f2_falso :- not persona_dice_che(a, onesto_b).
f3_falso :- not persona_dice_che(a, bugiardo_a).
f4_falso :- not persona_dice_che(a, bugiardo_b).

:- f1_falso, f2_falso, f3_falso, f4_falso.

#show bugiardo/1.
#show f1/0.
#show f2/0.
#show f3/0.
#show f4/0.
