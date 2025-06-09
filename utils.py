import xml.etree.ElementTree as ET
import xmlschema

def bookings_to_xml(bookings):
    # creeaza elementul radacina <bookings>
    root = ET.Element("bookings")

    # parcurge fiecare rezervare si creeaza noduri XML pentru fiecare camp
    for b in bookings:
        booking_el = ET.SubElement(root, "booking")
        ET.SubElement(booking_el, "id").text = b["id"]
        ET.SubElement(booking_el, "name").text = b["name"]
        ET.SubElement(booking_el, "room").text = b["room"]
        ET.SubElement(booking_el, "date").text = b["date"]

    # scrie arborele XML într-un fișier local bookings.xml
    tree = ET.ElementTree(root)
    tree.write("bookings.xml", encoding="utf-8", xml_declaration=True)

    # returneaza continutul XML ca string (pentru afisare sau raspuns HTTP)
    return ET.tostring(root, encoding="unicode")


def validate_xml(xml_path="bookings.xml", xsd_path="schema.xsd"):
    # Incarca schema XSD folosind biblioteca xmlschema
    schema = xmlschema.XMLSchema(xsd_path)
    try:
        # Incearca validarea fisierului XML in functie de schema
        schema.validate(xml_path)
        return True, "XML is valid according to schema."
    except xmlschema.XMLSchemaException as e:
        # Daca apare eroare, returneaza mesajul de eroare
        return False, f"XML validation error: {str(e)}"

