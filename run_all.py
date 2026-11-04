"""Lance le main.py de chaque exercice à la suite."""
import os, runpy

racine = os.path.dirname(os.path.abspath(__file__))
for dossier in sorted(os.listdir(racine)):
    main = os.path.join(racine, dossier, "main.py")
    if os.path.isfile(main):
        print(f"\n===== {dossier} =====")
        runpy.run_path(main, run_name="__main__")
