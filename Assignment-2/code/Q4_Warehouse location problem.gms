$title Warehouse location problem

set i /1*3/;
set j /1*4/;

parameter c(i,j)/
1.1 4
1.2 5
1.3 7
1.4 8
2.1 5
2.2 3
2.3 5
2.4 9
3.1 6
3.2 5
3.3 6
3.4 7
/;

parameter f(i)/
1 300
2 250
3 200
/;

parameter M(i)/
1 150
2 200
3 250
/;

parameter d(j)/
1 70
2 230
3 100
4 150
/;

variable z;
positive variables x(i,j);
binary variables y(i)

equations
obj
demand_satifiscation(j)
suppy_faciliaty(i)
;

obj.. z =e= sum((i,j),c(i,j)*x(i,j))+sum(i,f(i)*y(i));
demand_satifiscation(j).. sum(i,x(i,j)) =e= d(j);
suppy_faciliaty(i).. sum(j,x(i,j))-y(i)*M(i) =l= 0;

Model Warehouse_facility_problem/all/ ;

solve Warehouse_facility_problem using MIP minimizing z;

display x.l;
display y.l;
display z.l;