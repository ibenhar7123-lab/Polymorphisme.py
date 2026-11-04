import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from exo01_animaux.animal import Animal, Chien, Chat, Vache, Robot, faire_parler

print("=== Exemple de base ===")
animaux = [Chien(), Chat(), Chien()]
for a in animaux:
    faire_parler(a)

print("\n=== Extensions : Vache + Robot (duck typing) ===")
tous = [Chien(), Chat(), Vache(), Robot()]
for x in tous:
    faire_parler(x)   # on ne connaît pas le type, on sait juste qu'il a parler()

print("\n=== Méthode non redéfinie ===")
try:
    faire_parler(Animal())
except NotImplementedError as e:
    print("Erreur :", e)
