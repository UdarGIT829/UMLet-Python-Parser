import ast
import xml.etree.ElementTree as ET
from xml.dom import minidom
import math

def arrange_boxes(boxes, shape):
    """
    Arrange a set of boxes in a specified geometric shape.

    This function arranges a dictionary of boxes, each represented by its dimensions ('w' for width and 'h' for height), 
    into a specified geometric shape. The shapes are determined by the 'shape' parameter: a line for 1 or 2, and regular 
    polygons for values greater than 2. The boxes are positioned so that their centers lie on the vertices of the shape. 
    The function ensures that all box positions are positive by offsetting them if necessary.

    Parameters:
    - boxes (dict): A dictionary of boxes, where each key is a unique identifier for the box and its value is a 
                    dictionary with keys 'w' (width) and 'h' (height).
    - shape (int): An integer representing the shape to arrange the boxes in. For 1 or 2, boxes are arranged in a line. 
                   For values greater than 2, boxes are arranged as vertices of a regular polygon with that many sides.

    Returns:
    - dict: A dictionary with the same keys as the input, where each value is a dictionary representing a box with updated 
            'x' and 'y' positions, as well as its original 'w' and 'h' values.

    Raises:
    - ValueError: If the shape parameter is less than 1 or not supported.

    Example:
    >>> boxes = {'box1': {'w': '10', 'h': '10'}, 'box2': {'w': '15', 'h': '15'}}
    >>> arrange_boxes(boxes, 3)
    {'box1': {'x': '...', 'y': '...', 'w': '10', 'h': '10'}, 'box2': {'x': '...', 'y': '...', 'w': '15', 'h': '15'}}
    """
    # Calculate the total width of all boxes
    total_width = sum(int(box['w']) for box in boxes.values())

    # Set the radius of the circle
    radius = total_width / 4

    arranged_boxes = {}

    # Function to calculate coordinates for regular polygons
    def polygon_coordinates(radius, sides, offset_angle=0):
        angle = 2 * math.pi / sides
        return [(radius * math.cos(i * angle + offset_angle), radius * math.sin(i * angle + offset_angle)) for i in range(sides)]

    # Calculate positions based on shape
    if shape == 1 or shape == 2:
        positions = [(i * (total_width / shape), 0) for i in range(shape)]  # Example: arrange in a horizontal line
    elif shape > 2:
        positions = polygon_coordinates(radius, shape)
    else:
        raise ValueError("Unsupported shape")

    # Adjust number of positions to match number of boxes
    positions = positions[:shape]

    # Arrange boxes and find minimum x and y
    min_x, min_y = float('inf'), float('inf')
    for (name, box), pos in zip(boxes.items(), positions):
        x_center, y_center = pos
        x = x_center - int(box['w']) // 2
        y = y_center - int(box['h']) // 2
        min_x, min_y = min(min_x, x), min(min_y, y)

        arranged_box = {
            'x': str(int(x)),
            'y': str(int(y)),
            'w': box['w'],
            'h': box['h']
        }
        arranged_boxes[name] = arranged_box

    # Offset all positions if minimum x or y is negative
    if min_x < 0 or min_y < 0:
        for name, box in arranged_boxes.items():
            box['x'] = int(int(box['x'])+ -min_x) if min_x < 0 else 0
            box['y'] = int(int(box['y'])+ -min_y) if min_y < 0 else 0

    return arranged_boxes

# Function to calculate the midpoint of a side
def calculate_midpoint(node, side, connectionNumber=None, totalConnections=None):
    """
    Calculate the midpoint or a specific point along a side of a rectangle.

    This function computes a point on one of the four sides ('north', 'south', 'east', 'west') 
    of a rectangular node. If 'connectionNumber' and 'totalConnections' are not provided, 
    the function returns the midpoint of the specified side. If these parameters are provided, 
    it calculates a specific point along the side based on the connection number and total number 
    of connections, effectively dividing the side into equal segments.

    Parameters:
    - node (dict): A dictionary representing a node with keys 'x', 'y', 'w' (width), and 'h' (height).
    - side (str): A string indicating the side of the rectangle ('north', 'south', 'east', 'west').
    - connectionNumber (int, optional): The specific connection number. Defaults to None.
    - totalConnections (int, optional): The total number of connections. Defaults to None.

    Returns:
    - tuple: A tuple (x, y) representing the coordinates of the calculated point on the specified side.

    Notice:
    - This function has a known cosmetic issue when specifying connection numbers. For instance, with two connections, 
      the expected division of the side would be into thirds (1/3 and 2/3), but the function instead returns positions 
      that correspond to a 1/2 and 2/3 division, which may not align exactly as expected.
    """
    x, y, w, h = int(node['x']), int(node['y']), int(node['w']), int(node['h'])
    if not connectionNumber and not totalConnections:
        if side == "north":
            return (x + w // 2, y)
        elif side == "south":
            return (x + w // 2, y + h)
        elif side == "east":
            return (x + w, y + h // 2)
        else:  # west
            return (x, y + h // 2)
    else:
        totalConnections += 1
        # Instead of the midpoint, divide the width/height by total connections, then multiply by connectionNumebr
        if side == "north":
            return (x + w // totalConnections * connectionNumber, y)
        elif side == "south":
            return (x + w // totalConnections * connectionNumber, y + h)
        elif side == "east":
            return (x + w, y + h // totalConnections * connectionNumber)
        else:  # west
            return (x, y + h // totalConnections * connectionNumber)

# Function to determine the closest sides between two nodes
def closest_sides(node1, node2):
    """
    Determine the closest sides between two rectangular nodes.

    This function identifies the sides of two rectangular nodes that are closest to each other.
    It considers all possible pairs of sides ('north', 'south', 'east', 'west') between the two nodes,
    calculates the midpoints of these sides, and then finds the pair of sides with the minimum distance
    between their midpoints.

    Parameters:
    - node1 (dict): A dictionary representing the first node with keys 'x', 'y', 'w' (width), and 'h' (height).
    - node2 (dict): A dictionary representing the second node with keys 'x', 'y', 'w' (width), and 'h' (height).

    Returns:
    - tuple: A tuple containing the names of the closest sides from each node. The first element of the tuple
             corresponds to the closest side of 'node1', and the second element corresponds to the closest side
             of 'node2'.

    Example:
    >>> node1 = {'x': '10', 'y': '20', 'w': '100', 'h': '50'}
    >>> node2 = {'x': '150', 'y': '30', 'w': '150', 'h': '60'}
    >>> closest_sides(node1, node2)
    ('east', 'west')
    """
    sides = ['north', 'south', 'east', 'west']
    min_distance = float('inf')
    closest_side_node1, closest_side_node2 = None, None

    for side1 in sides:
        for side2 in sides:
            midpoint1 = calculate_midpoint(node1, side1)
            midpoint2 = calculate_midpoint(node2, side2)
            distance = ((midpoint1[0] - midpoint2[0]) ** 2 + (midpoint1[1] - midpoint2[1]) ** 2) ** 0.5

            if distance < min_distance:
                min_distance = distance
                closest_side_node1, closest_side_node2 = side1, side2

    return closest_side_node1, closest_side_node2

def flatten_list(nested_list):
    """
    Flattens a list with any amount of nested lists/tuples.

    Args:
    nested_list (list): A potentially nested list of elements.

    Returns:
    list: A flattened version of the input list.
    """
    flat_list = []
    for element in nested_list:
        if isinstance(element, list) or isinstance(element, tuple):
            flat_list.extend(flatten_list(element))
        else:
            flat_list.append(element)
    return flat_list

def length_of_longest_element(class_info):
    """
    Calculate the length of the longest element in a class's information.

    This function takes a dictionary representing various elements of a class (such as class name, docstring,
    methods, attributes, and base classes) and calculates the length of the longest string representation 
    among these elements. This includes the longest line in multi-line strings (like docstrings), the full 
    representation of methods (including arguments and return type), and attributes (including type).

    Parameters:
    - class_info (dict): A dictionary containing the class's information. The dictionary should have keys 
                         'class_name', 'docstring', 'methods', 'attributes', and 'base_classes'. Each method 
                         and attribute should have its own 'docstring', 'input_types', 'return_type', etc.

    Returns:
    - int: The length of the longest string representation among the class's elements.

    Example:
    >>> class_info = {
            'class_name': 'MyClass',
            'docstring': 'A sample class.',
            'methods': [{'name': 'my_method', 'input_types': {'param1': 'int'}, 'return_type': 'str', 'docstring': 'A method.'}],
            'attributes': [{'name': 'my_attr', 'type': 'int'}],
            'base_classes': ['BaseClass']
        }
    >>> length_of_longest_element(class_info)
    28
    """
    max_length = len(class_info['class_name'])

    # Function to get the maximum length of lines in a multi-line string
    def max_line_length(multi_line_str):
        return max(len(line) for line in multi_line_str.split('\n'))

    if class_info['docstring']:
        max_length = max(max_length, max_line_length(class_info['docstring']))

    for method in class_info['methods']:
        argument_list = []
        for arg, arg_type in method['input_types'].items():
            arg_representation = f"{arg}: {arg_type}" if arg_type else arg
            argument_list.append(arg_representation)

        arguments = ', '.join(argument_list)
        method_representation = f"{method['name']}({arguments}): {method['return_type'] or 'Any'}"
        max_length = max(max_length, len(method_representation))

        if method['docstring']:
            max_length = max(max_length, max_line_length(method['docstring']))

    for attr in class_info['attributes']:
        attr_representation = f"{attr['name']}: {attr['type'] or 'Any'}"
        max_length = max(max_length, len(attr_representation))

        if 'docstring' in attr:
            max_length = max(max_length, max_line_length(attr['docstring']))

    if class_info['base_classes']:
        base_classes_representation = ', '.join(class_info['base_classes'])
        max_length = max(max_length, len(base_classes_representation))

    return max_length

def format_class_details(class_info):
    """
    Generate a formatted string representation of class details for XML documentation.

    This function takes a dictionary containing information about a class, including its name, 
    docstring, attributes, and methods. It formats this information into a structured string 
    suitable for XML documentation. The resulting string includes the class name, its docstring 
    (if available), a list of attributes with their types and docstrings, and a list of methods 
    with their signatures and docstrings.

    Parameters:
    - class_info (dict): A dictionary containing the class's information. Expected keys are 
                         'class_name', 'docstring', 'attributes', and 'methods'. Each attribute 
                         and method can have its own 'docstring', 'input_types', 'return_type', etc.

    Returns:
    - str: A formatted string containing the class details, suitable for XML documentation.
    """

    details = f"style=wordwrap\n"
    details += f"<<Class>>\n{class_info['class_name']}\n"
    if class_info['docstring']:
        details += f"{{Doc string: {class_info['docstring']}}}\n"
    details += "--\n*Attributes*\n"
    for attr in class_info['attributes']:
        details += f"- {attr['name']}: {attr['type'] or 'None'}\n"
        if 'docstring' in attr:  # If attribute docstrings are available
            details += f"={{Doc string: {attr['docstring']}}}\n"
    details += "--\n*Functions*\n"
    for method in class_info['methods']:
        argument_list = []
        for arg, arg_type in method['input_types'].items():
            arg_representation = f"{arg}: {arg_type}" if arg_type else arg
            argument_list.append(arg_representation)

        arguments = ', '.join(argument_list)
        ret_type = method['return_type'] or 'Any'
        
        details += f"- {method['name']}({arguments}): {ret_type}\n"
        if method['docstring']:
            details += f"={{Doc string: {method['docstring']}}}\n"
    return details

def format_docstring(docstring, max_line_length=40):
    """
    Formats a given docstring to a specified maximum line length.

    This function takes a string (docstring) and breaks it into lines, ensuring that each line 
    does not exceed a specified maximum length. If adding a word would exceed this limit, a new 
    line is started. If the remaining text is less than half of the maximum line length and not at 
    the start of the docstring, it is appended to the current line with a space. Otherwise, it starts 
    a new line. The function aims to maintain readability while ensuring line length constraints.

    Parameters:
    - docstring (str): The docstring to be formatted.
    - max_line_length (int, optional): The maximum allowed length of a line. Defaults to 40 characters.

    Returns:
    - str: The formatted docstring with line breaks inserted to comply with the maximum line length.
    """
    words = docstring.split()
    formatted_docstring = ''
    current_line_length = 0

    for i, word in enumerate(words):
        # Check if adding the next word would exceed the max line length
        if current_line_length + len(word) > max_line_length:
            # Check if the remaining text is more than half the max line length
            remaining_text = ' '.join(words[i:])
            if len(remaining_text) > max_line_length / 2:
                formatted_docstring += '\n'  # Start a new line
                current_line_length = 0
            elif formatted_docstring:
                # Add a space if it's not the start of the docstring
                formatted_docstring += ' '

        elif formatted_docstring:
            # Add a space before the word if it's not the start of the docstring
            formatted_docstring += ' '
            current_line_length += 1

        formatted_docstring += word
        current_line_length += len(word)

    return formatted_docstring

def get_function_argument_types(function_def):
    """
    Extracts and returns the type annotations of arguments from a function definition.

    This function takes an AST (Abstract Syntax Tree) node representing a function definition 
    and parses it to extract the type annotations of its arguments. It handles both simple type 
    annotations and more complex types. If an argument does not have a type annotation, it is 
    recorded as None. The function is useful for static analysis of Python code to understand the 
    types expected by a function.

    Parameters:
    - function_def (ast.FunctionDef): An AST node representing a function definition.

    Returns:
    - dict: A dictionary where keys are argument names and values are their respective type annotations 
            as strings. If an argument has no type annotation, its value is None.

    Note:
    - The function assumes that the input is an AST node of type FunctionDef. It is not designed to 
      handle other types of nodes.
    - For complex type annotations that cannot be directly accessed using 'id', this function converts 
      the AST node of the annotation into a string for representation.
    """
    argument_types = {}
    for arg in function_def.args.args:
        # Check if the argument has a type annotation
        if arg.annotation:
            # The type name can be directly accessed using 'id' for simple types
            arg_type = getattr(arg.annotation, 'id', None)
            if not arg_type:
                # For more complex types (like List[int]), you may need more complex logic
                arg_type = str(ast.dump(arg.annotation))
            argument_types[arg.arg] = arg_type
        else:
            argument_types[arg.arg] = None  # No type annotation

    return argument_types

def get_type_annotation(annotation_node):
    """Extract type annotation from an AST node."""
    if isinstance(annotation_node, ast.Name):
        return annotation_node.id
    elif isinstance(annotation_node, ast.Subscript):
        # For complex types like List[entity]
        base_type = get_type_annotation(annotation_node.value)
        
        if isinstance(annotation_node.slice, ast.Name):
            element_type = annotation_node.slice.id
            return (base_type, element_type)
        else:
            return base_type
    elif isinstance(annotation_node, ast.Str):  # For string annotations in Python 3.7 and earlier
        return annotation_node.s
    else:
        return str(ast.dump(annotation_node))  # Fallback to raw AST dump for unrecognized types


class ImportCollector(ast.NodeVisitor):
    """
    A custom AST node visitor to collect information about module imports.

    This class is designed to traverse an Abstract Syntax Tree (AST) representing Python source code and 
    collect data about all import statements. It identifies both simple imports (using the 'import' keyword) 
    and imports from a specific module (using the 'from ... import ...' construct).

    Attributes:
    - imports (list): A list where each element represents an import in the code. For simple imports, 
                      the element is a string representing the imported module's name. For imports from a 
                      specific module, the element is a tuple (module, name), where 'module' is the name 
                      of the module and 'name' is the name of the imported object.
    """

    def __init__(self):
        """
        Initializes the ImportCollector with an empty list to store import information.
        """
        self.imports = []

    def visit_Import(self, node):
        """
        Visits an 'Import' node in the AST and adds its details to the imports list.

        This method is automatically called by the NodeVisitor when it encounters an 'Import' node.
        It extracts the names of the imported modules and appends them to the 'imports' list.

        Parameters:
        - node (ast.Import): The AST node representing an 'import' statement.
        """
        for alias in node.names:
            self.imports.append(alias.name)

    def visit_ImportFrom(self, node):
        """
        Visits an 'ImportFrom' node in the AST and adds its details to the imports list.

        This method is automatically called by the NodeVisitor when it encounters an 'ImportFrom' node.
        It extracts the names of the objects imported from a specific module and appends them, along with 
        the module name, to the 'imports' list as tuples.

        Parameters:
        - node (ast.ImportFrom): The AST node representing a 'from ... import ...' statement.
        """
        module = node.module
        for alias in node.names:
            self.imports.append((module, alias.name))


def analyze_python_file(file_path):
    """
    Analyzes a Python file to collect information about its classes and imported modules.

    This function reads a Python file, parses it to an Abstract Syntax Tree (AST), and then traverses 
    the AST to extract information about all classes and their components (methods, attributes, docstrings, 
    and base classes) and all imported modules. The function also flattens the list of imports for easier 
    analysis. The analysis results for each class include its name, docstring, methods (with return types, 
    docstrings, and input types), attributes (with names and types), and base classes. The function is 
    suitable for static analysis of Python code for purposes like generating UML diagrams.

    Parameters:
    - file_path (str): The path to the Python file to be analyzed.

    Returns:
    - tuple: A tuple where the first element is a list of dictionaries, each representing a class in the 
             analyzed file. The second element is a flattened list of imported modules. Each dictionary 
             for a class contains keys 'class_name', 'docstring', 'methods', 'attributes', and 'base_classes'.

    Note:
    - This function relies on the 'ast' module for parsing and analyzing the Python file.
    - Custom helper functions like 'flatten_list', 'format_docstring', and 'get_function_argument_types' 
      are used to process and format the extracted data.
    """
    analysis_results = []
    with open(file_path, 'r') as file:
        tree = ast.parse(file.read())
    
    collector = ImportCollector()
    collector.visit(tree)
    imported_modules = flatten_list(collector.imports)

    classes = [node for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]

    root = ET.Element("diagram", program="umlet", version="15.1")
    ET.SubElement(root, "zoom_level").text = "10"

    for cls in classes:
        class_info = {
            'class_name': cls.name,
            'docstring': format_docstring(ast.get_docstring(cls)) if ast.get_docstring(cls) else str(),
            'methods': [],
            'attributes': [],
            'base_classes': [base.id for base in cls.bases if isinstance(base, ast.Name)]
        }

        for item in cls.body:
            if isinstance(item, ast.FunctionDef):
                if isinstance(item.returns, ast.Subscript):
                    thisReturnType = get_type_annotation(item.returns)
                else:
                    thisReturnType = getattr(item.returns, 'id', None)
                method_info = {
                    'name': item.name,
                    'return_type': thisReturnType if item.returns else None,
                    'docstring': format_docstring(ast.get_docstring(item)) if ast.get_docstring(item) else str(),
                    'input_types': get_function_argument_types(item)
                }
                class_info['methods'].append(method_info)

            elif isinstance(item, ast.AnnAssign) or isinstance(item, ast.Assign):
                attr_name = None
                attr_type = None
                if isinstance(item, ast.Assign):
                    for target in item.targets:
                        if isinstance(target, ast.Name):
                            attr_name = target.id
                            attr_type = getattr(item.value, 'id', None)
                else:
                    attr_name = item.target.id
                    attr_type = get_type_annotation(item.annotation)

                attr_info = {'name': attr_name, 'type': attr_type or str()}
                class_info['attributes'].append(attr_info)

        analysis_results.append(class_info)

    return analysis_results,imported_modules

def create_xml_output(analysis_results, xmlPath, imported_modules=None):
    """
    Generates an XML output representing UML class diagrams from the analysis results of Python code.

    This function processes the results of a static analysis of Python code, extracting information about 
    classes, their methods, attributes, and relationships. It then generates an XML structure suitable 
    for UML diagram tools, such as Umlet. The XML output includes class elements with their attributes and 
    methods, as well as relationship elements that illustrate inheritance and associations between classes.

    The function also determines the layout for these elements, calculating appropriate coordinates to 
    position them visually. Arrows representing relationships between classes are calculated for their 
    start and end points, as well as the direction of the arrow.

    Parameters:
    - analysis_results (list): A list of dictionaries, each containing details about a class extracted 
                               from static analysis of Python code.
    - xmlPath (str): The file path where the generated XML content will be saved.
    - imported_modules (list, optional): A list of module names that were imported in the analyzed code.

    Returns:
    - bool: True if the XML file is successfully written, False if an exception occurs during file writing.

    Raises:
    - Exception: If an unrecognized arrow type is encountered during the processing of relationship data.

    Note:
    - This function relies on external functions like 'flatten_list', 'length_of_longest_element', 
      'arrange_boxes', 'closest_sides', 'calculate_midpoint', and 'format_class_details' for processing 
      the analysis results and generating the XML content.
    """
    classNames = []

    for iterClass in analysis_results:
        classNames.append(iterClass.get("class_name"))

    relations = []
    for iterClass in analysis_results:
        if iterClass["base_classes"]:
            relations.append((iterClass["class_name"], iterClass["base_classes"][0], "Inherits from"))
        for iterMethod in iterClass["methods"]:
            if isinstance(iterMethod["return_type"],tuple):
                flattenedReturntypes = flatten_list(iterMethod["return_type"])
                for iterReturnType in flattenedReturntypes:
                    if iterReturnType in classNames:
                        relations.append((iterClass["class_name"], iterReturnType, f"Function <{iterMethod['name']}()> Returns container {flattenedReturntypes[0]} of Type"))
            elif iterMethod["return_type"] in classNames:
                relations.append((iterClass["class_name"], iterMethod["return_type"], f"Function <{iterMethod['name']}()> Return Type"))
            for iterInputArgName, iterInputType in iterMethod["input_types"].items():
                if iterInputType in classNames:
                    relations.append((iterClass["class_name"], iterInputType, f"Arg ({iterInputArgName}) of type"))
        for iterAttribute in iterClass["attributes"]:
            iterAttributeName = iterAttribute["name"]
            iterAttributeType = iterAttribute["type"]
            if isinstance(iterAttributeType, tuple):
                relations.append((iterClass["class_name"], iterAttributeType[1], f"Attribute <{iterAttributeName}> container of type"))
            elif iterAttributeType in classNames:
                relations.append((iterClass["class_name"], iterAttributeType, f"Attribute <{iterAttributeName}> of type"))

    #   Decide the coords of each node here
    #   nodeCoords should be in format: {classname: {"x":x_coord, "y":y_coord, "w":width, "h":height}}

    nodeCoords = {}
    starting_x = "50"
    for iterClass in analysis_results:
        longest_element_length = length_of_longest_element(iterClass)
        scale_factor = 10  # Adjust this factor as needed
        width = max(210, longest_element_length * scale_factor)
        thisNodeCoords = {
            "x":starting_x,
            "y":"30",
            "w":str(width),
            "h":"260"       
            }
        nodeCoords[iterClass["class_name"]] = thisNodeCoords
        starting_x = str( int(starting_x)+width+50)

    shape = len(analysis_results)
    nodeCoords = arrange_boxes(nodeCoords, shape)
       

    # List to store arrow data
    arrows = []
    # Initialize connection counts for each side of each node
    for node_name, node_data in nodeCoords.items():
        node_data['connectionCounts'] = {'north': 0, 'south': 0, 'east': 0, 'west': 0}

    # Function to increment connection count and get the connection number
    def get_connection_number(node, side):
        node['connectionCounts'][side] += 1
        return node['connectionCounts'][side]


    # Loop through each relation
    for relation in relations:
        sourceNode = relation[0]
        destinNode = relation[1]
        relationType = relation[2]

        # Get the nodes from the nodes dictionary
        if destinNode in imported_modules:
            pass
        else:
            node1 = nodeCoords[sourceNode]
            node2 = nodeCoords[destinNode]

            # Find the closest sides
            side1, side2 = closest_sides(node1, node2)

            # Increment connection counts and get connection numbers
            connectionNumber1 = get_connection_number(node1, side1)
            totalConnections1 = node1['connectionCounts'][side1]
            connectionNumber2 = get_connection_number(node2, side2)
            totalConnections2 = node2['connectionCounts'][side2]

            start_point = calculate_midpoint(node1, side1, connectionNumber1, totalConnections1)
            end_point = calculate_midpoint(node2, side2, connectionNumber2, totalConnections2)


            # Determine the direction of the arrow based on the sides
            direction = ""
            if side1 == "north":
                direction = "up"
            elif side1 == "south":
                direction = "down"
            elif side1 == "east":
                direction = "right"
            else:  # side1 == "west"
                direction = "left"

            offset = 20
            start_x = start_point[0] - offset
            end_x = end_point[0]
            x_travel = int(end_x - start_x)
            start_y = start_point[1] - offset
            end_y = end_point[1]
            y_travel = int(end_y - start_y)
            # Append the arrow data to the list
            arrow = {
                'start_x': start_x,
                'start_y': start_y,
                'end_x': end_x,
                'end_y': end_y,
                'travel_x':x_travel,
                'travel_y':y_travel,
                'direction': direction,
                'relation_type': relationType,
                'connecting':(sourceNode,destinNode),
                'lineOffset': 0 if connectionNumber1!=connectionNumber2 or connectionNumber1==1 else connectionNumber1*2
            }
            arrows.append(arrow)

    root = ET.Element("diagram", program="umlet", version="15.1")
    ET.SubElement(root, "zoom_level").text = "10"


    starting_x = "50"
    for class_info in analysis_results:
        class_name = class_info["class_name"]
        nodeInfo = nodeCoords.get(class_name)
        element = ET.SubElement(root, "element")
        ET.SubElement(element, "id").text = "UMLClass"
        coordinates = ET.SubElement(element, "coordinates")
        ET.SubElement(coordinates, "x").text = str(nodeInfo['x'])
        ET.SubElement(coordinates, "y").text = str(nodeInfo['y'])
        ET.SubElement(coordinates, "w").text = str(nodeInfo['w'])
        ET.SubElement(coordinates, "h").text = str(nodeInfo['h'])

        ET.SubElement(element, "panel_attributes").text = format_class_details(class_info)
        ET.SubElement(element, "additional_attributes")

    for arrow in arrows:
        element = ET.SubElement(root, "element")
        ET.SubElement(element, "id").text = "Relation"
        coordinates = ET.SubElement(element, "coordinates")
        ET.SubElement(coordinates, "x").text = str(arrow['start_x'])
        ET.SubElement(coordinates, "y").text = str(arrow['start_y'])
        ET.SubElement(coordinates, "w").text = str(arrow['travel_x'])
        ET.SubElement(coordinates, "h").text = str(arrow['travel_y'])

        panelText = ""
        # Set arrow direction
        # WORKING :)
        if arrow["direction"] == "left":
            panelText += "lt=<-\n"
        else:
            panelText += "lt=->\n"

        # Set arrow maintext based on relationship
        if arrow["lineOffset"]:
            for newlineIteration in range(arrow["lineOffset"]):
                panelText += "\n"
        if "inherits" in arrow["relation_type"].lower():
            panelText += arrow["relation_type"]
        elif "of type" in arrow["relation_type"].lower():
            panelText += arrow["relation_type"]
        elif "contain" in arrow["relation_type"].lower():
            panelText +=  f"m1=contains\nm2=0...n\n{arrow['relation_type']}"
        elif "return type" in arrow["relation_type"].lower():
            panelText += arrow["relation_type"]
        else:
            raise Exception(f"Non-recognized arrow: {str(arrow)}")
        ET.SubElement(element, "panel_attributes").text = panelText
        ET.SubElement(element, "additional_attributes").text = f"{str(offset)}.0;{str(offset)}.0;{str(arrow['travel_x'])}.0;{str(arrow['travel_y'])}.0"


    # Pretty print and write to XML file
    xml_str = minidom.parseString(ET.tostring(root)).toprettyxml(indent="    ")
    try:
        with open(xmlPath, "w") as f:
            f.write(xml_str)
        return True
    except Exception:
        return False


def analyseFile(file_path, xmlPath):
    analysis, importedModules = analyze_python_file(file_path)
    result = create_xml_output(analysis, xmlPath, importedModules)

    return result

if __name__ == "__main__":
    file_path = 'example.py'  # Replace with your file path
    xmlPath = file_path.replace(".py",".uxf")

    analysis = analyseFile(file_path, xmlPath)
    if analysis:
        print(f"Wrote to file: {xmlPath}")
    else:
        print(f"Something went wrong with writing the file.")