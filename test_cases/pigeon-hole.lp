% Taken from clingo sources, dot propagator example :
%  https://github.com/potassco/clingo/tree/master/examples/clingo/dot-propagator
#const n=6.
p(1..n).
h(1..(n-1)).
1 { a(P,H) : h(H) } 1 :- p(P).
:- 2 { a(P,H) }, h(H).
