import xml.etree.ElementTree as ET
from typing import Final
from xml.dom.minidom import Element

MISSING_VALUE: Final[str] = "missing value"

# Read and return content of file name
def read_file(name: str) -> str:
    with open(name, 'r') as file:
        return file.read()


# Try to retrieve value from list at given index, returns "missing value" if missing or empty value
def try_get_value(data: list[str], index: int) -> str:
    try:
        value = data[index]
    except IndexError:
        return MISSING_VALUE

    if value.isspace():
        return MISSING_VALUE

    else:
        return value


#Take a line of data, strip it of prefix and split, and insert the correct elements under the parent element
def insert_elements(data: str, parent: Element, prefix: str, elements: list) -> None:
    stripped_data = data.removeprefix(prefix + "|").split("|")
    for i in range(len(elements)):
        ET.SubElement(parent, elements[i]).text = try_get_value(stripped_data, i)


#Converts incoming data to XML
def convert_to_xml(data: str) -> ET.ElementTree:

   #First step is to convert the data into an easier format to work with
    people_list: list = []
    family_mode: bool = False

    for line in data.splitlines():
        if line[0] == "P":
            family_mode = False
            people_list.append([[line]])  # append a new person in the people list
        elif line[0] == "F":
            family_mode = True
            people_list[-1].append([line])  # append additional line into person list
        else:
            if family_mode:
                people_list[-1][-1].append(line)  ##append one layer deeper for family values
            else:
                people_list[-1].append([line])  # append additional line into person list

    # Create root element of XML File
    root_element: Element = ET.Element("people")

    for person in people_list:
        person_element: Element = ET.SubElement(root_element, "person")
        for entry in person:
            if entry[0][0] == "P":
                insert_elements(entry[0], person_element, "P", ["firstname", "lastname"])
            elif entry[0][0] == "T":
                phone_element: Element = ET.SubElement(person_element, "phone")
                insert_elements(entry[0], phone_element, "T", ["mobile", "landline"])
            elif entry[0][0] == "A":
                address_element: Element = ET.SubElement(person_element, "address")
                insert_elements(entry[0], address_element, "A", ["street", "city", "zip"])
            elif entry[0][0] == "F":
                family_element: Element = ET.SubElement(person_element, "family")
                for family_data in entry:
                    if family_data[0] == "F":
                        insert_elements(family_data, family_element, "F", ["name", "born"])
                    elif family_data[0] == "T":
                        phone_element: Element = ET.SubElement(family_element, "phone")
                        insert_elements(family_data, phone_element, "T", ["mobile", "landline"])
                    elif family_data[0] == "A":
                        address_element: Element = ET.SubElement(family_element, "address")
                        insert_elements(family_data, address_element, "A", ["street", "city", "zip"])

    return ET.ElementTree(root_element)