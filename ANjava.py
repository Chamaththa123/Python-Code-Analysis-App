from javalang import parse
from javalang.tree import *

java_code = """
class Example {
    public static void main(String[] args) {
        int x = 10;
        int y = 20;
        x = 10; // Redundant assignment
        System.out.println(x + y);
    }
}
"""

def remove_redundant_assignments(java_code):
    tree = parse.parse(java_code)

    # Create a dictionary to track variable assignments
    assignments = {}

    for _, node in tree.filter(Assignment):
        if isinstance(node.value, Literal) and isinstance(node.target, VariableDeclarator):
            variable_name = node.target.name
            variable_value = node.value.value

            # Check if the variable has been assigned the same value before
            if variable_name in assignments and assignments[variable_name] == variable_value:
                # Remove the redundant assignment
                node.remove()
            else:
                # Update the variable's value in the dictionary
                assignments[variable_name] = variable_value

    return tree

if __name__ == "__main__":
    optimized_tree = remove_redundant_assignments(java_code)
    optimized_code = optimized_tree.encode()
    print(optimized_code)
