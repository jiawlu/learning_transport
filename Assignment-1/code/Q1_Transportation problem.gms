$ title Transportaion problem

set i city /1*2/;
set j airport /1*2/;

parameter c(i,j) driving time /
1.1 60
1.2 65
2.1 55
2.2 45
/;

parameter d(i) demand of city i /
1 100
2 200
/;

parameter s(j) supply of airport j /
1 150
2 150
/;

integer variables
x(i,j) number of passenger traveling from city i to airport j;

variable z;

equations
obj
demand_constraint(i)
supply_constraint(j)
;

obj.. z =e= sum((i,j),x(i,j)*c(i,j));
demand_constraint(i)..sum(j,x(i,j)) =e= d(i);
supply_constraint(j)..sum(i,x(i,j)) =e= s(j);

model transportaion_problem /all/;

solve transportaion_problem using MIP minizing z;

display x.l
display z.l