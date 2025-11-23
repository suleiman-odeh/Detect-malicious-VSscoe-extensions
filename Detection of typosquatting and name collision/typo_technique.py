import enchant


"""
These are the elements to detect qwerty keyboard mistyping
"""
adjacent_keys = {
    'e': ['r', 's'],
    'E': ['R', 'S'],
    's': ['e', 'd'],
    'S': ['E', 'D'],
    'd': ['s', 'r'],
    'D': ['S', 'R'],
    'f': ['g'],
    'F': ['G'],
    'g': ['f'],
    'G': ['F'],
    'p': ['o'],
    'P': ['O'],
    'r': ['e', 't'],
    'R': ['E', 'T'],
    'u': ['i'],
    'U': ['I'],
    'i': ['u'],
    'I': ['U'],
    'o': ['p', '0'],
    'O': ['P', '0'],
    '0': ['o', 'O'],
}

""" 
    These are removed with their identifiers from the all_extensions.txt and all_extensions_identifier.txt
    These are choosen based on the order in the Marketplace 

"""
first100_extension_names = [
    "Python",
    "Pylance",
    "Jupyter",
    "C/C++",
    "Jupyter Keymap",
    "Jupyter Notebook Renderers",
    "Live Server",
    "Prettier - Code formatter",
    "IntelliCode",
    "Jupyter Cell Tags",
    "Jupyter Slide Show",
    "Python Debugger",
    "Language Support for Java(TM) by Red Hat",
    "ESLint",
    "Docker",
    "CMake",
    "CMake Tools",
    "GitLens — Git supercharged",
    "Chinese (Simplified) (简体中文) Language Pack for Visual Studio Code",
    "Debugger for Java",
    "C/C++ Themes",
    "C/C++ Extension Pack",
    "Maven for Java",
    "Test Runner for Java",
    "Project Manager for Java",
    "C#",
    "IntelliCode API Usage Examples",
    "Extension Pack for Java",
    "WSL",
    "Code Runner",
    "Dev Containers",
    "Material Icon Theme",
    "GitHub Pull Requests",
    "isort",
    "Remote - SSH",
    "HTML CSS Support",
    "Remote - SSH: Editing Configuration Files",
    "GitHub Copilot",
    "Auto Rename Tag",
    "vscode-icons",
    "Live Share",
    "YAML",
    "JavaScript (ES6) code snippets",
    ".NET Install Tool",
    "Vetur",
    "GitHub Theme",
    "Remote Explorer",
    "Path Intellisense",
    "GitHub Copilot Chat",
    "Auto Close Tag",
    "Go",
    "PHP Intelephense",
    "ES7+ React/Redux/React-Native snippets",
    "PHP Debug",
    "Git History",
    "PowerShell",
    "Django",
    "Better C++ Syntax",
    "Code Spell Checker",
    "Doxygen Documentation Generator",
    "HTML Snippets",
    "EditorConfig for VS Code",
    "Python Indent",
    "[Deprecated] Debugger for Chrome",
    "open in browser",
    "Jinja",
    "autoDocstring - Python Docstring Generator",
    "Beautify",
    "Dart",
    "One Dark Pro",
    "Japanese Language Pack for Visual Studio Code",
    "Markdown All in One",
    "Python Extension Pack",
    "Flutter",
    "Git Graph",
    "Python Environment Manager",
    "npm Intellisense",
    "indent-rainbow",
    "Rainbow CSV",
    "Azure Account",
    "Spanish Language Pack for Visual Studio Code",
    "IntelliSense for CSS class names in HTML",
    "Tabnine: AI Chat & Autocomplete for JavaScript, Python, Typescript, Java, PHP, Go, and more",
    "Bracket Pair Colorizer",
    "Dracula Theme Official",
    "markdownlint",
    "Better Comments",
    "Color Highlight",
    "Tailwind CSS IntelliSense",
    "Angular Language Service",
    "SQL Server (mssql)",
    "npm",
    "Vim",
    "XML",
    "CodeLLDB",
    "Portuguese (Brazil) Language Pack for Visual Studio Code",
    "[Deprecated] Bracket Pair Colorizer 2",
    "Russian Language Pack for Visual Studio Code",
    "XML Tools",
    "CSS Peek"
]

# This method removes all consecutive identical characters after an index of a string
def remove_repeated_characters(extensionname):
    new_text = ""

    i = 0
    while i < len(extensionname):

        new_text += extensionname[i]
        
        while i + 1 < len(extensionname) and extensionname[i] == extensionname[i + 1]:
            i += 1
        
        i += 1
    return new_text


"""
This method will remove all identical charachters in the same index and then check if the 
last two charachters of every string is swapped

"""
def swapped_characters(badextension,goodextension):
    
    if len(badextension)!= len(goodextension):
        return False
    i=0
    while i< len(badextension):
        if badextension[i] == goodextension[i]:
            badextension = badextension[:i] + badextension[i + 1:]
            goodextension = goodextension[:i] + goodextension[i + 1:]
        else:
            i += 1
    
    if len(badextension)==2:
        if(badextension[0]==goodextension[1] and badextension[1]==goodextension[0]):
            return True       

    return False         


"""
This method will remove all identical charachters in the same index and then check if the 
last charachter is adjancet to any of the charachters on the adjacent_keys

"""
def common_typo(badextension,goodextension):

    if len(badextension)!= len(goodextension):
        return False
    i=0
    while i< len(badextension):
        if badextension[i] == goodextension[i]:
            badextension = badextension[:i] + badextension[i + 1:]
            goodextension = goodextension[:i] + goodextension[i + 1:]
        else:
            i += 1    

    if len(badextension) != len(goodextension):
        return False
    if len(badextension)==1:
        if badextension[0] in adjacent_keys.get(goodextension[0], []):
            return True

    return False


"""

In the Main function it will check every display name with the list first100_extension_names 
"""
def main():
    with open('typoresults.txt', 'w',encoding='utf-8') as typoresult:
        suspicious_counter=0
        with open('all_extensions.txt','r', encoding="utf8") as all_extensions:
            with open('all_extensions_identifier.txt','r',encoding="utf8") as all_identifiers:
                all_extensions_list = [line.strip() for line in all_extensions]
                all_identifiers_list = [line.strip() for line in all_identifiers]
                for i in range(len(all_extensions_list)):
                        line = all_extensions_list[i]
                        line2= all_identifiers_list[i]

                        """
                        It check first for name collision and then for typosquatting
                        It will be checked for Levenshtein distance at the end
                        """
                        for j,legitimate_extension, in enumerate(first100_extension_names,start=0):                        
                                if (line==legitimate_extension):
                                    typoresult.write(f"for {line} with the identifier {line2} there is collision with {legitimate_extension}\n")
                                    print(f"for {line} with the identifier {line2} there is collision with {legitimate_extension}\n")
                                    suspicious_counter+=1
                                    break

                                elif(remove_repeated_characters(line)==remove_repeated_characters(legitimate_extension)):
                                    typoresult.write(f"{line} with the identifier {line2} is typosquatting (remove repeated charchater) {legitimate_extension}\n")
                                    print(f"{line} with the identifier {line2} is typosquatting (remove repeated charchater) {legitimate_extension}\n")  
                                    suspicious_counter+=1
                                    break 
                                        
                                elif(swapped_characters(line,legitimate_extension)):
                                    typoresult.write(f"{line} with the identifier {line2} is typosquatting (swapped charchater) {legitimate_extension}\n")
                                    print(f"{line} with the identifier {line2} is typosquatting (swapped charchater) {legitimate_extension}\n")
                                    suspicious_counter+=1    
                                    break

                                elif(common_typo(line,legitimate_extension)):
                                    typoresult.write(f"{line} with the identifier {line2} is typosquatting (commontypo) {legitimate_extension}\n")
                                    print(f"{line} with the identifier {line2} is typosquatting (commontypo) {legitimate_extension}\n")
                                    suspicious_counter+=1 
                                    break 

                                elif(len(legitimate_extension)<=4):
                                    if(enchant.utils.levenshtein(line,legitimate_extension)<=1):
                                        typoresult.write(f"{line} with the identifier {line2} is typosquatting (Levenshtein) {legitimate_extension}\n" )
                                        print(f"{line} with the identifier {line2} is typosquatting (Levenshtein) {legitimate_extension}\n" )
                                        suspicious_counter+=1  
                                        break 
                                    
                                elif(enchant.utils.levenshtein(line,legitimate_extension)<=2):
                                    typoresult.write(f"{line} with the identifier {line2} is typosquatting (Levenshtein) {legitimate_extension}\n" )
                                    print(f"{line} with the identifier {line2} is typosquatting (Levenshtein) {legitimate_extension}\n" )
                                    suspicious_counter+=1  
                                    break          
        typoresult.write(f"{suspicious_counter} were detected")
        print(f"{suspicious_counter} were detected")
            

if __name__ == '__main__':
    main()
    print("finish")




