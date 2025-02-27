import json

class SalesExecutive:
    def _init_(self, id, data):
        self.id = id
        self.data = data
        self.left = None
        self.right = None

def build_sales_organization(data):
    """Recursively builds the sales organization tree from the input dictionary."""
    if not data:
        return None
    node = SalesExecutive(data["id"], data["data"])
    if "left" in data:
        node.left = build_sales_organization(data["left"])
    if "right" in data:
        node.right = build_sales_organization(data["right"])
    return node

def find_max_sales_line(root):
    """
    Finds the path from the root to a leaf that produces the highest total sales.
    Returns the list of SalesExecutive nodes along that path.
    """
    max_sales = 0
    max_line = []

    def dfs(node, path, current_sales):
        nonlocal max_sales, max_line
        if not node:
            return

        # Add current node to the path and update current sales
        path.append(node)
        current_sales += node.data

        # If leaf node, check if this path has the highest total sales so far
        if not node.left and not node.right:
            if current_sales > max_sales:
                max_sales = current_sales
                max_line = path.copy()

        # Recurse on children
        dfs(node.left, path, current_sales)
        dfs(node.right, path, current_sales)

        # Backtrack to explore other paths
        path.pop()

    dfs(root, [], 0)
    return max_line

def calculate_bonus_distribution(line, bonus):
    """
    Given the highest-sales line and a bonus amount,
    calculates each executive’s bonus using two components:
      - Budget Efficiency (25%): based on number of subordinates in the line.
      - Sales Efficiency (75%): based on individual sales contributions.
    
    For a line of L nodes, the node at index i has (L - 1 - i) subordinates.
    """
    L = len(line)
    # Total subordinate count for the line
    total_subordinates = sum(L - 1 - i for i in range(L))
    total_sales = sum(se.data for se in line)
    
    bonus_distribution = []
    for i, se in enumerate(line):
        # Each node's subordinate count is (L-1-i)
        subordinate_count = L - 1 - i
        
        # Budget Efficiency Reward: if total_subordinates is zero, then no budget share.
        budget_share = (subordinate_count / total_subordinates) * (0.25 * bonus) if total_subordinates > 0 else 0
        
        # Sales Efficiency Reward
        sales_share = (se.data / total_sales) * (0.75 * bonus)
        
        total_bonus = round(budget_share + sales_share)
        bonus_distribution.append({"id": se.id, "bonus": total_bonus})
        
    return bonus_distribution

def main():
    bonus = 3000000  # Rs.3,000,000 bonus
    input_json = input("Enter the sales organization structure in JSON format: ")
    
    try:
        data = json.loads(input_json)
        # Build the tree from JSON input
        root = build_sales_organization(data)
        # Determine the highest-sales line (path from root to leaf)
        max_sales_line = find_max_sales_line(root)
        # Calculate bonus distribution for each sales executive in the line
        bonus_distribution = calculate_bonus_distribution(max_sales_line, bonus)
        print("Result:", json.dumps(bonus_distribution, indent=2))
    except json.JSONDecodeError:
        print("Invalid JSON input. Please provide a valid JSON structure.")

if _name_ == "_main_":
    main()