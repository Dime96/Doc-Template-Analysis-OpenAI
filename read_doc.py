import zipfile
import xml.etree.ElementTree as ET

ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}

def is_heading1_section(p):
    """Returns True if the given paragraph section has been styled as a Heading1"""
    return_val = False
    heading_style_elem = p.find(".//w:pStyle[@w:val='Heading1']", ns)
    if heading_style_elem is not None:
        return_val = True
    return return_val

def get_section(p):
    """Returns the joined text of the text elements under the given paragraph tag"""
    return_val = ''
    text_elems = p.findall('.//w:t', ns)
    if text_elems is not None:
        return_val = ''.join([t.text for t in text_elems])
    return return_val

def get_section_text(section_labels, p_sections):
    section_text = []
    title = ""
    text = []

    for i, t in enumerate(section_labels):
            
        if len(t) > 0:     
            section_text.append({'title': title, 'text':text})
            title = t
            text = []
            
        else:
            text.append(get_section(p_sections[i]))

    return section_text

def get_section_paragraph(section_text):
    section_paragraph = {}

    for i in section_text:
        title = i["title"]
        text = i["text"]
        paragraph = ""
        
        if len(title) > 0:
            for j in text:
                paragraph += j
                paragraph += "\n\n"
                
            section_paragraph[title]=paragraph
    
    return section_paragraph


def read_doc(uploaded_file):
    doc = zipfile.ZipFile(uploaded_file).read('word/document.xml')
    root = ET.fromstring(doc)

    # Microsoft's XML makes heavy use of XML namespaces; thus, we'll need to reference that in our code
    body = root.find('w:body', ns)  # find the XML "body" tag
    p_sections = body.findall('w:p', ns)  # under the body tag, find all the paragraph sections

    section_labels = [get_section(s) if is_heading1_section(s) else '' for s in p_sections]
    section_text = get_section_text(section_labels, p_sections)
    section_paragraph = get_section_paragraph(section_text)
    
    return section_paragraph

