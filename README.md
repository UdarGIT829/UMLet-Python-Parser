# UMLet-Python-Parser

## Project Overview

This project provides a static analysis tool for Python script files, focusing on the generation of UML (Unified Modeling Language) diagrams. These diagrams effectively represent the structure of Python code, highlighting information about classes and their interrelationships, including methods and attributes.

The tool analyzes Python scripts to extract information about classes, methods, attributes, and their documentation. It identifies and displays the relationships between classes, such as inheritance and associations, and also details how methods across different classes are interconnected.

A key feature of this tool is the visualization of connections between classes and their methods. This aspect is particularly useful for understanding and documenting the architecture of Python applications. The tool is beneficial for developers and teams working with Python code, assisting in navigating new codebases, documenting projects, or teaching Python programming concepts.

By automating the generation of UML diagrams, the tool aims to streamline the process of code analysis and documentation. It is designed to save time and reduce the effort typically required for manual documentation, enhancing comprehension of complex Python projects.

## Installation and Setup

This project is built using Python's standard library, which means there are no additional external dependencies to install. However, to ensure compatibility, it's important to use the correct version of Python. Here's how you can set up and run the tool:

Ensure Python is Installed: This tool is compatible with Python 3.x (recommended version: 3.8 or newer). You can download and install Python from python.org.

Verify Python Installation: To verify that Python is installed, open your terminal or command prompt and type:
```bash
python --version
```

This should display the Python version number.

Download the Project: Clone or download the project repository from GitHub to your local machine.

Running the Tool: Navigate to the project directory in your terminal or command prompt and run the Python script as follows:

```bash
python main.py example.py
```

Replace example.py with the appropriate filename.

## Usage
To use this static analysis tool and generate UML diagrams from Python scripts, follow these simple steps:

### Running the Tool:

Open your terminal or command prompt and navigate to the directory where the tool's script is located.
Ensure you have the Python script file you wish to analyze in an accessible location, as you might need to specify the path to this file when running the tool.

### Viewing the UML Diagram:

After running the tool, it will generate a UML diagram in the form of a .uxf file.
To view and interact with the generated UML diagram, use the UMLet application. UMLet is an open-source UML tool designed for fast UML diagrams. If you don't have UMLet installed, you can download it from the UMLet website.
Open UMLet, then choose 'Open' from the file menu and navigate to the location of the generated .uxf file.
The UML diagram should now be visible in UMLet, where you can view, edit, or export it as needed.
This process will allow you to visualize the structure and relationships within your Python code through a UML diagram, making it easier to understand complex codebases and enhance documentation.