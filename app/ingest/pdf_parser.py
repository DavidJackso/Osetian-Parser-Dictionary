import fitz
def parse_pdf(file_path):
    doc = fitz.open(file_path)
    dictionary = {}  
    for page in doc:
        text = page.get_text()
        lines = text.split('\n')
        for line in lines:
            line = line.strip()
            if not line:
                continue
            if '    ' in line:  
                parts = line.split('    ', 1)
            elif '   ' in line:  
                parts = line.split('   ', 1)
            elif '  ' in line: 
                parts = line.split('  ', 1)
            else:
                continue
            if len(parts) == 2:
                russian = parts[0].strip()
                ossetian = parts[1].strip()
                while russian and russian[0].isdigit():
                    russian = russian[1:].strip()
                if russian.startswith('.'):
                    russian = russian[1:].strip()
                ossetian = ossetian.lstrip('-')
                if russian and ossetian:
                    dictionary[ossetian] = russian
    doc.close()
    return dictionary
pdf_file = "файл.pdf"
result = parse_pdf(pdf_file)
print(result)
