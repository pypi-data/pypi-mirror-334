# CyVer
[![License](https://img.shields.io/badge/License-CC_BY_SA_4.0-blue.svg)](https://creativecommons.org/licenses/by-sa/4.0/)
<div align="center">
    <img src="https://gitlab.com/netmode/CyVer/-/raw/main/logoCyVer.jpg?ref_type=heads" alt="CyVer" width="300">
</div>


**CyVer** is a Python library designed to validate Cypher queries against a given Knowledge Graph schema in Neo4j. It ensures correctness in terms of syntax, schema validity, and property access. 

## Features

* **Syntax Validation**: Validates Cypher queries for correct syntax and detects conflicting labels in nodes and relationships.

* **Schema Validation**: Checks query alignment with a predefined KG schema structure.

* **Property Validation**: Ensures property accesses are correct based on the predefined KG schema structure.

## 📖 Documentation

For documentation read [Wiki](https://gitlab.com/netmode/CyVer/-/wikis/CyVer-Documentation).

## 📋 Requirements

Before installing, make sure you have the following Python packages installed, with Python version >= 3.10:

* regex>=2024.11.6
* neo4j>=5.27


## 📦 Installation

To install the latest stable version from [PyPI](https://pypi.org/project/CyVer/), run:

```sh
pip install CyVer
```
Alternatively, if you prefer to install the latest development version, you can install it directly from GitLab:

```sh
pip install git+https://gitlab.com/netmode/CyVer.git
```

Or, you can manually clone the repository and run:

```sh
git clone https://gitlab.com/netmode/CyVer.git
cd CyVer
pip install .
```



## 💻 Example Usage 

### Importing the Library

``` sh
import CyVer
from CyVer.validators import SyntaxValidator,PropertiesValidator,SchemaValidator
```

### Connect to Neo4j Database instance
```sh
from neo4j import GraphDatabase,basic_auth

driver = GraphDatabase.driver(database_url, auth=basic_auth(database_username, database_password))
```

### Syntax Validator

```sh
syntax_validator =  SyntaxValidator(driver)
query = 'MATCH (g:Goal) RETURN COUNT(g) AS output'
is_valid = syntax_validator.validate(query)
print(f"Syntax Valid: {is_valid}")
```

### Schema Validator
```sh
schema_validator =  SchemaValidator(driver)
query = 'MATCH (g:Goal)-[:HAS_TARGET]->(t:Target) RETURN g, t'
# Extraction
extracted_node_labels, extracted_rel_labels, extracted_paths = schema_validator.extract(query)
print(f"Extracted Node Labels : {extracted_node_labels}")
print(f"Extracted Relationships Labels : {extracted_rel_labels}")
print(f"Extracted One-hop Paths : {extracted_paths}")
# Validation 
schema_score = schema_validator.validate(query)
print(f"Schema Validation Score: {schema_score}")

```


### Properties Validator
```sh
props_validator =  PropertiesValidator(driver)
query = 'MATCH (g:Goal)-[:HAS_TARGET]-(t:Target) WHERE g.code =1 RETURN t'
# Extraction
variables_properties , labels_properties = props_validator.extract(query)
print(f"Accessed properties by variables: {variables_properties}")
print(f"Accessed properties by labels (including inferred): {labels_properties}")

# Validation 
props_score = props_validator.validate(query)
print(f"Properties Validation Score: {props_score}")
```


## License

This project is licensed under the [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/) license.

## 🤝 Contributing

Contributions are welcome! Please submit a pull request or open an issue.

## Cite

To cite this work, please use:

## Contact

For any request for detailed information or expression of interest for participating at this initiative, you may contact:

- Ioanna Mandilara - ioannamand (at) netmode (dot) ntua (dot) gr
- Christina Maria Androna - andronaxm (at) netmode (dot) ntua (dot) gr
- Eleni Fotopoulou - efotopoulou (at) netmode (dot) ntua (dot) gr
- Anastasios Zafeiropoulos - tzafeir (at) cn (dot) ntua (dot) gr

---