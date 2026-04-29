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
