import math
from matplotlib import pyplot as plt

def get_chance(a_string, age):
    if a_string == "Reproduction":
        a = 28
        b = 36
    elif a_string == "Marriage":
        a = 30
        b = 70
    else:
        a = 80
        b = 200
    formula_a = (age - a)**2
    formula_b = -(formula_a/b)
    chance = float(math.pow(math.e, formula_b))
    return chance

str_ = "HCGF"
plot = []
print(get_chance(str_, 15))

for i in range(100):
    plot.append(get_chance(str_, i))

plt.plot(plot)
plt.show()