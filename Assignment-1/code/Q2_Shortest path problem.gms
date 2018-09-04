$ title Shortest path problem

set i node /1*4/;
alias (i,j);

parameter w(i,j) cost /
1.2 5
1.3 2
3.2 2
2.4 1
3.4 4
/;

parameter origin(i) /
1 1
/;

parameter destination(i) /
4 1
/;

parameter intermediate(i);
intermediate(i) = (1-origin(i))*(1-destination(i));


binary variables
x(i,j) if link is selected;

variable z;

equations
obj
comm_flow_on_node_origin(i)
comm_flow_on_node_intermediate(i)
comm_flow_on_node_destination(i)
;

obj.. z =e= sum((i,j)$(w(i,j)>0),x(i,j)*w(i,j));
comm_flow_on_node_origin(i)$(origin(i)=1)..sum(j$(w(i,j)>0),x(i,j)) =e= origin(i);
comm_flow_on_node_intermediate(i)$(intermediate(i)=1)..sum(j$(w(i,j)>0),x(i,j)) =e= sum(j$(w(j,i)>0),x(j,i));
comm_flow_on_node_destination(i)$(destination(i)=1)..sum(j$(w(j,i)>0),x(j,i)) =e= destination(i);

model shortest_path_problem /all/;

solve shortest_path_problem using MIP minizing z;

display x.l
display z.l
