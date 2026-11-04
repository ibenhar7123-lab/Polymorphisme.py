import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from exo02_formes.forme import Forme, Cercle, Rectangle, Triangle, Carre

formes = [
    Cercle(3),
    Rectangle(4, 5),
    Triangle(6, 2),
    Carre(4),       # extension
]

for fo in formes:
    print(fo)

print("\n=== Classe abstraite : instanciation impossible ===")
try:
    Forme()
except TypeError as e:
    print("Erreur :", e)
