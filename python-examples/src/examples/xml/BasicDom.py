import xml.dom.minidom

document = open("basic-dom.xml")

dom = xml.dom.minidom.parse(document)

root = dom.getElementsByTagName("root")[0]

aChilds = root.getElementsByTagName("aChild")
bChilds = root.getElementsByTagName("bChild")
for node in aChilds:
    print node.getAttribute("attr")
    
for node in bChilds:
    print node.getAttribute("attr2")