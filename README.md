# Metaheuritcs for Tetris

Ovaj projekat implementira **genetski algoritam (GA)** za igranje Tetrisa.  
Cilj algoritma je da optimizuje parametre **heurističke funkcije** koja odlučuje kako će AI postaviti i rotirati figure tokom igre.  
Na taj način, kroz više generacija, populacija agenata evoluira tako da postiže sve veći skor i duže preživljava u igri.  

Trening se izvodi tako što se svaka jedinka (genome) ocenjuje na osnovu broja poena koje ostvari u simulaciji igre.  
Tokom iteracija, koriste se standardni operatorski mehanizmi GA:
- **Selekcija** (ruletska i turnirska selekcija su implementirane i poređene u eksperimentima),
- **Ukrstanje** (ukrštanje genoma),
- **Mutacija** (nasumična promena vrednosti gena).

Vizuelizacija igre realizovana je pomoću **Pygame**, dok se rezultati treninga beleže u log fajlovima i kasnije grafički analiziraju.  
Za generisanje plotova koristi se **Matplotlib**, a grafici prikazuju poređenje najboljeg i prosečnog fitnesa kroz generacije, kao i razlike između ruletske i turnirske selekcije.  

Cilj projekta je da ilustruje kako se genetski algoritmi mogu primeniti na optimizaciju heuristika u složenim igrama poput Tetrisa, i da obezbedi osnovu za dalje eksperimente sa metaheuristikama i podešavanjem hiperparametara.

---
## Struktura projekta

- `game/main.py` – pokretanje genetskog algoritma
- `game/gui2.py` – vizuelizacija najboljeg genoma na Tetris tabli
- `game/roulette_selection.txt` – log rezultata treninga sa ruletskom selekcijom
- `game/tournament_selection.txt` – log rezultata treninga sa turnirskom selekcijom
- `game/plots/` – direktorijum sa generisanim grafikonima (poređenje selekcija, rast fitnesa po generacijama itd.)

---

## Kako pokrenuti?
1. Klonirati repozitorijum:
   ```bash
   git clone https://github.com/doktorfilip1/MetaheuristicsForTetris.git
   cd MetaheuristicsForTetris/game
---
2. Instalirati zavisnosti:
   ```bash
   pip install pygame matplotlib
---
3. Pokrenuti main.py, zatim gui2.py
   ```bash
   python main.py
   python gui2.py
---
Napomena: U config.py namestiti parametre za algoritam (broj generacija, velicinu populacije, stopu mutacije ...)


---

## Rezultati:
Eksperimentisano je sa dve metode selekcije:
- Ruletska selekcija
- Turnirska selekcija
    
Na osnovu 25, 50 i 100 generacija, posmatran je rast najboljeg i prosečnog fitnesa.  
Grafikoni su dostupni u folderu (game/plots)

---

### Projekat radili:
- **Filip Dramićanin 303/2023**
- **Vuk Vukmirović 305/2023**
