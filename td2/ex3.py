from collections import deque
from itertools import permutations
import math
import random



random.seed(1)

INF = float("inf")


aretes = {
    (1, 2): 14,
    (1, 3): 15,
    (1, 8): 17,
    (2, 3): 13,
    (2, 4): 14,
    (2, 5): 20,
    (2, 8): 21,
    (3, 4): 11,
    (3, 5): 21,
    (3, 6): 17,
    (3, 7): 9,
    (3, 8): 9,
    (4, 5): 11,
    (4, 6): 10,
    (4, 7): 8,
    (4, 8): 20,
    (5, 6): 15,
    (5, 7): 18,
    (6, 7): 9,
    (7, 8): 13,
}

VILLES = list(range(1, 9))
SOLUTION_INITIALE = [1, 2, 3, 4, 5, 6, 7, 8]





def distance(a, b):
  """Retourne le coût d'une liaison directe, ou INF si absente."""
  return aretes.get((a, b), aretes.get((b, a), INF))


def cout_tour(tour):
  """Calcule la distance totale du circuit fermé (retour au départ inclus)."""
  total = 0
  n = len(tour)
  for i in range(n):
    c = distance(tour[i], tour[(i + 1) % n])
    if c == INF:
      return INF
    total += c
  return total


def tour_valide(tour):
  """Vérifie si toutes les arêtes consécutives du circuit existent."""
  return cout_tour(tour) != INF


def afficher_tour(tour):
  """Formate le circuit sous la forme 1 -> ... -> 1."""
  return " -> ".join(map(str, tour + [tour[0]]))


def echanger(tour, i, j):
  """Génère un voisin par permutation de deux sommets (Swap)."""
  res = tour[:]
  res[i], res[j] = res[j], res[i]
  return res





def recherche_taboue(nb_iter=100, taille_tabou=7):
  courant = SOLUTION_INITIALE[:]
  meilleur = courant[:]
  meilleur_cout = cout_tour(meilleur)

  liste_taboue = deque(maxlen=taille_tabou)

  print("\n" + "=" * 55)
  print("1. RECHERCHE TABOUE")
  print("=" * 55)
  print("Circuit initial :", afficher_tour(courant))
  print("Coût initial    :", meilleur_cout)

  for iteration in range(1, nb_iter + 1):
    meilleur_voisin = None
    cout_voisin = INF
    mouvement_choisi = None

  
    for i in range(1, len(courant) - 1):
      for j in range(i + 1, len(courant)):
        voisin = echanger(courant, i, j)

        if not tour_valide(voisin):
          continue

        mouvement = tuple(sorted((courant[i], courant[j])))
        est_tabou = mouvement in liste_taboue
        cout = cout_tour(voisin)

       
        if est_tabou and cout >= meilleur_cout:
          continue

        if cout < cout_voisin:
          meilleur_voisin = voisin
          cout_voisin = cout
          mouvement_choisi = mouvement

    if meilleur_voisin is None:
      print("Aucun voisin admissible trouvé. Arrêt prématuré.")
      break

    courant = meilleur_voisin
    liste_taboue.append(mouvement_choisi)

    if cout_voisin < meilleur_cout:
      meilleur = courant[:]
      meilleur_cout = cout_voisin

    if iteration <= 10 or iteration % 20 == 0:
      print(
          f"Itération {iteration:3d} | Coût courant = {cout_voisin:3.0f} |"
          f" Meilleur coût = {meilleur_cout:3.0f}"
      )

  print("\nMeilleur circuit Tabou :", afficher_tour(meilleur))
  print("Meilleur coût Tabou    :", meilleur_cout)
  return meilleur, meilleur_cout



def recuit_simule(nb_iter=5, temperature_initiale=50.0, alpha=0.85):
  courant = SOLUTION_INITIALE[:]
  meilleur = courant[:]
  cout_courant = cout_tour(courant)
  meilleur_cout = cout_courant
  temperature = temperature_initiale

  print("\n" + "=" * 55)
  print(f"2. RECUIT SIMULÉ ({nb_iter} ITÉRATIONS)")
  print("=" * 55)
  print("Circuit initial        :", afficher_tour(courant))
  print("Coût initial           :", cout_courant)
  print("Température initiale   :", temperature_initiale)
  print("Taux de refroidissement :", alpha)
  print("-" * 55)

  for iteration in range(1, nb_iter + 1):
    
    i, j = random.sample(range(1, len(courant)), 2)
    candidat = echanger(courant, i, j)
    cout_candidat = cout_tour(candidat)

    if cout_candidat == INF:
      print(
          f"Itération {iteration:2d} | T = {temperature:6.2f} | Arête absente"
          " (INF) -> Mouvement rejeté"
      )
      temperature *= alpha
      continue

    delta = cout_candidat - cout_courant

    if delta <= 0:
      probabilite = 1.0
      accepte = True
    else:
      probabilite = math.exp(-delta / temperature)
      tirage = random.random()
      accepte = tirage < probabilite

    if accepte:
      courant = candidat
      cout_courant = cout_candidat
      if cout_courant < meilleur_cout:
        meilleur = courant[:]
        meilleur_cout = cout_courant

    decision = "ACCEPTÉ" if accepte else "REFUSÉ"
    print(
        f"Itération {iteration:2d} | T = {temperature:6.2f} | delta = {delta:+3.0f}"
        f" | P = {probabilite:5.3f} | {decision:7s} | Coût courant ="
        f" {cout_courant:3.0f}"
    )

    temperature *= alpha

  print("\nMeilleur circuit Recuit :", afficher_tour(meilleur))
  print("Meilleur coût Recuit    :", meilleur_cout)
  return meilleur, meilleur_cout




def generer_tour_valide():
  """Génère un circuit aléatoire valide débutant par la ville 1."""
  autres = VILLES[1:]
  for _ in range(5000):
    random.shuffle(autres)
    candidat = [1] + autres
    if tour_valide(candidat):
      return candidat
  return SOLUTION_INITIALE[:]


def croisement_ox(parent1, parent2):
  """Opérateur Order Crossover (OX) adapté aux permutations."""
  taille = len(parent1)
  i, j = sorted(random.sample(range(1, taille), 2))

  enfant = [None] * taille
  enfant[0] = 1
  
  enfant[i : j + 1] = parent1[i : j + 1]

 
  villes_restantes = [v for v in parent2[1:] if v not in enfant]
  pos_libres = [k for k in range(1, taille) if enfant[k] is None]

  for pos, val in zip(pos_libres, villes_restantes):
    enfant[pos] = val

  return enfant


def mutation_swap(tour, probabilite=0.2):
  """Mutation par échange de deux sommets."""
  res = tour[:]
  if random.random() < probabilite:
    i, j = random.sample(range(1, len(res)), 2)
    res[i], res[j] = res[j], res[i]
  return res


def algorithme_genetique(
    taille_pop=40, nb_generations=150, taux_mutation=0.2
):
  print("\n" + "=" * 55)
  print("3. ALGORITHME GÉNÉTIQUE")
  print("=" * 55)

 
  population = [SOLUTION_INITIALE[:]]
  while len(population) < taille_pop:
    candidat = generer_tour_valide()
    if candidat not in population:
      population.append(candidat)

  meilleur = min(population, key=cout_tour)
  meilleur_cout = cout_tour(meilleur)

  for gen in range(1, nb_generations + 1):
    population.sort(key=cout_tour)

    if cout_tour(population[0]) < meilleur_cout:
      meilleur = population[0][:]
      meilleur_cout = cout_tour(meilleur)

    
    nouvelle_pop = [population[0][:], population[1][:]]

    
    while len(nouvelle_pop) < taille_pop:
      p1 = min(random.sample(population, 3), key=cout_tour)
      p2 = min(random.sample(population, 3), key=cout_tour)

      enfant = croisement_ox(p1, p2)
      enfant = mutation_swap(enfant, taux_mutation)

      if tour_valide(enfant):
        nouvelle_pop.append(enfant)
      else:
        nouvelle_pop.append(generer_tour_valide())

    population = nouvelle_pop

    if gen % 30 == 0 or gen == 1:
      print(f"Génération {gen:3d} | Meilleur coût = {meilleur_cout:.0f}")

  print("\nMeilleur circuit Génétique :", afficher_tour(meilleur))
  print("Meilleur coût Génétique    :", meilleur_cout)
  return meilleur, meilleur_cout



def optimum_exact():
  """Exploration exhaustive de toutes les permutations (Force Brute)."""
  meilleur = None
  meilleur_cout = INF
  for p in permutations(range(2, 9)):
    t = [1] + list(p)
    c = cout_tour(t)
    if c < meilleur_cout:
      meilleur_cout = c
      meilleur = t[:]
  return meilleur, meilleur_cout


if __name__ == "__main__":

  best_tabou, cost_tabou = recherche_taboue(nb_iter=100, taille_tabou=7)


  best_recuit, cost_recuit = recuit_simule(
      nb_iter=5, temperature_initiale=50.0, alpha=0.85
  )


  best_ga, cost_ga = algorithme_genetique(
      taille_pop=40, nb_generations=150, taux_mutation=0.2
  )


  best_exact, cost_exact = optimum_exact()


  print("\n" + "=" * 55)
  print("SYNTHÈSE ET COMPARAISON DES RÉSULTATS")
  print("=" * 55)
  print(f"{'Recherche Taboue':<22}: {afficher_tour(best_tabou)} | Coût = {cost_tabou}")
  print(f"{'Recuit Simulé':<22}: {afficher_tour(best_recuit)} | Coût = {cost_recuit}")
  print(f"{'Algorithme Génétique':<22}: {afficher_tour(best_ga)} | Coût = {cost_ga}")
  print(f"{'Optimum Exact':<22}: {afficher_tour(best_exact)} | Coût = {cost_exact}")