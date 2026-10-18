import numpy as np


def solve_transport_tabu():
    costs_D1 = np.array([7, 3, 4])
    costs_D2 = np.array([6, 7, 2])
    demands = np.array([4, 5, 8])
    supply_D1 = 8

    def evaluate(s):
        s_d2 = demands - s
        return np.sum(s * costs_D1) + np.sum(s_d2 * costs_D2)

   
    current_sol = np.array([4, 4, 0])
    best_sol = np.copy(current_sol)
    best_cost = evaluate(best_sol)

    tabu_list = []
    tabu_tenure = 3
    max_iter = 30

    for it in range(max_iter):
        neighborhood = []
        
        for a in range(3):
            for b in range(3):
                if a != b and current_sol[a] > 0 and current_sol[b] < demands[b]:
                    neighbor = np.copy(current_sol)
                    neighbor[a] -= 1
                    neighbor[b] += 1
                    move = (a, b)
                    cost = evaluate(neighbor)
                    neighborhood.append((neighbor, move, cost))

        
        neighborhood.sort(key=lambda x: x[2])

        
        moved = False
        for neighbor, move, cost in neighborhood:
            inverse_move = (move[1], move[0])
            if (inverse_move not in tabu_list) or (cost < best_cost):
                current_sol = neighbor
                tabu_list.append(move)
                if len(tabu_list) > tabu_tenure:
                    tabu_list.pop(0)

                if cost < best_cost:
                    best_cost = cost
                    best_sol = np.copy(neighbor)
                moved = True
                break

        if not moved:
            break

    sol_d2 = demands - best_sol
    print("=== Résultat Recherche Tabou (Exercice 2) ===")
    print(f"Livraisons D1 (M1, M2, M3) : {best_sol}")
    print(f"Livraisons D2 (M1, M2, M3) : {sol_d2}")
    print(f"Coût minimal trouvé         : {best_cost}")


solve_transport_tabu()