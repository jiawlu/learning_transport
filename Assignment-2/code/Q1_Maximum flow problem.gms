$ title Maximum flow problem

set i node /1*6/;
alias (i,j);

parameter cap(i,j) cost /
1.2 5
1.3 10
2.5 5
3.4 5
2.4 4
3.5 5
5.6 10
4.6 8
6.1 inf
/;

variable x(i,j);
variable z;

equations
obj
flow_constraint(i)
cap_constraint(i,j)
;

obj.. z =e= x('6','1');
flow_constraint(i)..sum(j$(cap(j,i)>0),x(j,i)) =e= sum(j$(cap(i,j)>0),x(i,j));
cap_constraint(i,j)$(cap(i,j)>0)..x(i,j) =l= cap(i,j);

model maximum_flow_problem /all/;
solve maximum_flow_problem using LP maxmizing z;

display x.l
display z.l
