persona(a).
persona(b).

bugiardo(X) :- persona(X), not onesto(X).
onesto(X) :- persona(X), not bugiardo(X).

% a dice: (a è bugiardo AND B è bugiardo).

persona_dice_che(a, bugiardo_a ).
persona_dice_che(a, bugiardo_b ).

onesto(a) :- onesto(a), persona_dice_che(a, onesto_a).
onesto(b) :- onesto(a), persona_dice_che(a, onesto_b).
bugiardo(a) :- onesto(a), persona_dice_che(a, bugiardo_a).
bugiardo(b) :- onesto(a), persona_dice_che(a, bugiardo_b).