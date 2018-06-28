print(2);

print("Hola" + " " + "Mundo!");

print(false);

a = [1,2,3];

b = colineales(a,[4,5,6]);

multiplicacionEscalar(a,10);

c = multiplicacionEscalar([2,4,6],10*10,b);

print(capitalizar("hOLA"));

print(length(multiplicacionEscalar(a,length(capitalizar("x")),colineales(a,a))));

# Estos deben fallar:

# print sin parametros
# print();

# print con dos parametros
# print(1,2);

# colienales: parametros incorrectos
# colienales();
# colienales([1,2,3]);
# colienales("1,2,3",[5]);
# colienales([1,2,3],[5],true);

# multiplicacionEscalar: parametros incorrectos
# multiplicacionEscalar();
# multiplicacionEscalar("1,2,3");
# multiplicacionEscalar([1,2,3],"5");
# multiplicacionEscalar([1,2,3],[5]);
# multiplicacionEscalar([1,2,3],5,1);

# capitalizar: parametros incorrectos
# capitalizar();
# capitalizar("Hola","Mundo!");
# capitalizar(16);

# length: parametros incorrectos
# length();
# length(16);
# length([1,2,3],true);
