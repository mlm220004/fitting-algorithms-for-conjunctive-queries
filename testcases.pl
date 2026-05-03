/* PRESIDENTS */

businessman(donald).
businessman(fred).
businessman(james).
economist(baracksr).
democrat(barack).
democrat(franklin).
republican(donald).
father(baracksr, barack).
father(fred, donald).
father(james, franklin).

/* CASE 1 - unary examples */

example(1, positive, franklin).
example(1, positive, barack).
example(1, negative, donald).

/* CASE 2 - unary examples */

example(2, positive, franklin).
example(2, positive, donald).
example(2, negative, barack).

/* CASE 3 - unary examples with no fitting CQ   
   (should only be run against algorithm R)   */

example(3, positive, barack).
example(3, positive, donald).
example(3, negative, franklin).

/* CASE 4 - binary examples */

example(4, positive, baracksr, barack).
example(4, negative, fred, donald).

/* CASE 5 - binary examples */

example(5, positive, fred, donald).
example(5, negative, baracksr, barack).

/* CASE 6 - binary examples */

example(6, positive, james, franklin).
example(6, negative, baracksr, barack).
example(6, negative, fred, donald).

cq(1, positive, X1) :- example(1, positive, X1), father(X4, X2), father(X15, X7), democrat(X1), businessman(X17), businessman(X22), democrat(X2), father(X21, X13), father(X5, X3), father(X19, X12), businessman(X20), businessman(X18), businessman(X21), father(X22, X14), businessman(X16), businessman(X10), businessman(X8), father(X17, X8), businessman(X11), father(X6, X1), democrat(X14), economist(X4), democrat(X12), republican(X8), father(X18, X9).
cq(1, negative, X1) :- example(1, negative, X1).
cq(2, positive, X1) :- example(2, positive, X1), father(X15, X8), businessman(X17), businessman(X22), democrat(X2), father(X21, X13), father(X19, X12), businessman(X20), economist(X5), businessman(X18), businessman(X21), father(X22, X14), businessman(X16), father(X6, X3), businessman(X10), father(X18, X1), businessman(X9), father(X5, X2), father(X17, X9), businessman(X11), democrat(X14), democrat(X12), father(X7, X4), republican(X9), democrat(X4).
cq(2, negative, X1) :- example(2, negative, X1).
cq(4, positive, X1, X2) :- example(4, positive, X1, X2), businessman(X3), father(X6, X4), father(X5, X3), businessman(X6), father(X1, X2), republican(X3), businessman(X5), democrat(X2), democrat(X4), economist(X1).
cq(4, negative, X1, X2) :- example(4, negative, X1, X2).
cq(5, positive, X1, X2) :- example(5, positive, X1, X2), democrat(X3), businessman(X6), businessman(X1), father(X1, X2), economist(X4), democrat(X5), businessman(X2), father(X4, X3), father(X6, X5), republican(X2).
cq(5, negative, X1, X2) :- example(5, negative, X1, X2).
cq(6, positive, X1, X2) :- example(6, positive, X1, X2), democrat(X3), businessman(X6), businessman(X1), father(X1, X2), economist(X4), businessman(X5), democrat(X2), father(X4, X3), father(X6, X5), republican(X5).
cq(6, negative, X1, X2) :- example(6, negative, X1, X2).

dcq(1, positive, X1) :- distinct(cq(1, positive, X1)).
dcq(1, negative, X1) :- distinct(cq(1, negative, X1)).
dcq(2, positive, X1) :- distinct(cq(2, positive, X1)).
dcq(2, negative, X1) :- distinct(cq(2, negative, X1)).
dcq(4, positive, X1, X2) :- distinct(cq(4, positive, X1, X2)).
dcq(4, negative, X1, X2) :- distinct(cq(4, negative, X1, X2)).
dcq(5, positive, X1, X2) :- distinct(cq(5, positive, X1, X2)).
dcq(5, negative, X1, X2) :- distinct(cq(5, negative, X1, X2)).
dcq(6, positive, X1, X2) :- distinct(cq(6, positive, X1, X2)).
dcq(6, negative, X1, X2) :- distinct(cq(6, negative, X1, X2)).