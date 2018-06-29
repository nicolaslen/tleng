if (true) {
if (false)
if (false) {
if (true)
a=0;
}
}

if (true) if (false) if (false) if (true) {
a=0;
}
else
a=1;

if (true) {
if (false)
if (false)
if (true)
a=0;
else {
a=1;
}
} else { a=3; }

a = 0;

# Estos deben fallar:

# else sin if
# else {a=2;}

# else sin if
# if (true) a=5; b=2; else a=2;
