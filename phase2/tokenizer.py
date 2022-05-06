import re

def extract_imports(line,files):
    m = re.match(r"(?P<import>import)(\s+)\"(?P<library>[^\n]*)\"", line.strip())
    if(m == None):
        return "not import" 
    # print("library: ",m.group('library'))
    importLib = m.group('library')
    if(not(importLib in files)):
        return importLib
    return "repeated import"
    
def embedLib(libFile):
    
    try:
        with open("tests/" + libFile, 'r') as f:
            return f.readlines()
    except Exception:
        return []

def preprocess(inputfile):

    with open("tests/" + inputfile, "r") as input_file:
        lines = input_file.readlines()

    importSectionFinished = False 
    finalResult = []
    libFiles = []
    for line in lines:
        
        if(importSectionFinished):
            finalResult.extend(line)
            continue

        if(not(importSectionFinished)):
            currImport = extract_imports(line,libFiles)
            if( (currImport != "not import") and (currImport != "repeated import") ):
                finalResult.extend(embedLib(currImport))
            
            if(currImport == "not import"):
                importSectionFinished = True
                finalResult.extend(line)
        

    file_name = inputfile.split('.')[0] + '.pre'
    with open("pre/" + file_name, 'w') as f:
        for line in finalResult:
            f.write(line)

    with open("pre/" + file_name, 'r') as f:
        return f.read()