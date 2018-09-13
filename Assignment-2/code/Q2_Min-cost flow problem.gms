$ title Min-cost flow problem

set i node /1*4/;
alias (i,j,k);

parameter cap(i,j)/
1.2 500
1.3 900
2.3 700
3.2 400
2.4 600
3.4 1000
/;

parameter cost(i,j)/
1.2 20
1.3 25
2.3 10
3.2 15
2.4 20
3.4 40
/;

parameter origin(i)/
1 1
/;

parameter destination(i)/
4 1
/;

parameter intermidate(i);
intermidate(i) = (1-origin(i))*(1-destination(i));

positive variable x(i,j);
variable z;

equations
obj
origin_flow_constraint(i)
intermidate_flow_constraint(i)
destination_flow_constraint(i)
cap_constraint(i,j)
;

obj.. z =e= sum((i,j)$(cap(i,j)>0),x(i,j)*cost(i,j));
origin_flow_constraint(i)$(origin(i)=1)..sum(j$(cap(i,j)>0),x(i,j)) =e= 1200;
intermidate_flow_constraint(i)$(intermidate(i)=1)..sum(k$(cap(k,i)>0),x(k,i)) =e= sum(j$(cap(i,j)>0),x(i,j));
destination_flow_constraint(i)$(destination(i)=1)..sum(k$(cap(k,i)>0),x(k,i)) =e= 1200;
cap_constraint(i,j)..x(i,j) =l= cap(i,j);

model Min_cost_flow_problem /all/;
solve Min_cost_flow_problem using LP minimizing z;

display x.l
display z.l
