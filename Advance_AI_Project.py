import matplotlib.pyplot as plt
import networkx as nx
import matplotlib
matplotlib.use("TkAgg")
iran_map = {
    "Tehran": ["Alborz", "Qom", "Semnan", "Mazandaran", "Markazi"],
    "Alborz": ["Tehran", "Mazandaran", "Qazvin"],
    "Qom": ["Tehran", "Markazi", "Isfahan"],
    "Semnan": ["Tehran", "Mazandaran", "Golestan", "Razavi Khorasan", "Isfahan"],
    "Mazandaran": ["Tehran", "Alborz", "Semnan", "Golestan"],
    "Markazi": ["Tehran", "Qom", "Isfahan", "Lorestan", "Hamedan", "Qazvin"],
    "Qazvin": ["Alborz", "Mazandaran", "Hamedan", "Zanjan", "Markazi"],
    "Isfahan": ["Qom", "Semnan", "Yazd", "South Khorasan", "Chaharmahal", "Kohgiluyeh", "Lorestan", "Markazi"],
    "Golestan": ["Mazandaran", "Semnan", "Razavi Khorasan"],
    "Razavi Khorasan": ["Golestan", "Semnan", "South Khorasan"],
    "South Khorasan": ["Razavi Khorasan", "Yazd", "Isfahan"],
}
colors = ["red", "blue", "green", "yellow"]
all_provinces = set(iran_map.keys()) | {neighbor for neighbors in iran_map.values() for neighbor in neighbors}
domain = {province: list(colors) for province in all_provinces}
def is_valid_coloring(province, color, assignment):
    for neighbor in iran_map.get(province, []):
        if neighbor in assignment and assignment[neighbor] == color:
            return False
    return True
def select_unassigned_variable(assignment):
    unassigned = [v for v in iran_map if v not in assignment]
    return min(unassigned, key=lambda var: len(domain[var]))
def forward_checking(province, color):
    temp = {}
    for neighbor in iran_map.get(province, []):
        if color in domain[neighbor]:
            temp[neighbor] = domain[neighbor][:]
            domain[neighbor].remove(color)
    return temp
def restore_domain(temp):
    for neighbor, values in temp.items():
        domain[neighbor] = values
def backtracking(assignment):
    if len(assignment) == len(iran_map):
        return assignment
    province = select_unassigned_variable(assignment)
    for color in domain[province]:
        if is_valid_coloring(province, color, assignment):
            assignment[province] = color
            temp = forward_checking(province, color)
            result = backtracking(assignment)
            if result:
                return result
            restore_domain(temp)
            del assignment[province]
    return None
solution = backtracking({})
if solution:
    print("حل پیدا شد:", solution)
else:
    print("هیچ راه‌حلی یافت نشد!")
def draw_colored_map(solution):
    G = nx.Graph()
    for province, neighbors in iran_map.items():
        for neighbor in neighbors:
            G.add_edge(province, neighbor)
    plt.figure(figsize=(10, 8))
    pos = nx.spring_layout(G, seed=42)
    colors_map = [solution.get(node, "gray") for node in G.nodes()]
    nx.draw(G, pos, with_labels=True, node_color=colors_map, node_size=3000, edge_color="gray", font_size=10)
    plt.savefig("iran_map_coloring.png")
    print("📌 نقشه رنگ‌آمیزی‌شده ذخیره شد به نام 'iran_map_coloring.png'")
draw_colored_map(solution)
