$ title Integer programming model

set i para /1*4/;
set j var /1*2/;

parameter coefficient_objective(j)/
1 3
2 4
/;

parameter coefficient_constraint(i,j)/
1.1 1
1.2 2
2.1 2.5
2.2 1
3.1 1
3.2 0
4.1 0
4.2 -1
/;

parameter source (i)/
1 10
2 12
3 3
4 -4
/;

positive variable x(j);
variable z;

equations
obj
constraint(i)
;

obj.. z =e= sum(j,coefficient_objective(j)*x(j));
constraint(i)..sum(j,coefficient_constraint(i,j)*x(j)) =l= source(i);


model integer_programming_problem /all/;
solve integer_programming_problem using LP maxmizing z;

display x.l
display z.l
