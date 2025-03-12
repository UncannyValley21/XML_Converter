import converter

in_data = converter.read_file("data.txt")
xml = converter.convert_to_xml(in_data)
xml.write("export.xml")