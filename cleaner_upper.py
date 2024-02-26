import re

## Minimal working script for cleaning up big .bib files with a lot of unused references.

## Find all instances of \cite{foo} in the .tex document
## OBS: If your document contains a lot of commented citations %%% \cite{foo} this method will include these as well
def find_citations(tex_file) : 
    # Open file and read 
    with open(tex_file, 'r',encoding='utf-8') as file:
        # Read all lines into a string
        file_content = file.read()
    
    # Regular expression pattern to find citations of the form \cite{foo}
    citation_pattern = r'\\cite\{([^}]*)\}'        
    citations = re.findall(citation_pattern, file_content)
    print('Citations in the document: ')
    print(len(citations))
    unique_citations = set()
    for citation in citations:
        # Split multiple citations separated by commas
        multiple_citations = citation.split(',')
        for cit in multiple_citations:
            # Remove leading and trailing whitespace
            cit = cit.strip()
            # Check if the citation is not commented out
            if '%' not in cit:
                # Add the citation to the set
                unique_citations.add(cit)
    print("Number of unique citations:")
    print(len(unique_citations))
    new_citations = list(unique_citations)
    return new_citations

## Grab the references from the .bib file
# If your file contains multiple instances of the same reference these will 
def get_references(bib_file) : 
    with open(bib_file, 'r',encoding='utf-8') as file:
        # Read all lines into a string
        file_content = file.read()
    #split along @'s since the each reference is of the form @foo{}
    references=file_content.split('@')
    # Returns a list of all references but without the @ (i.e. not @foo{} but only foo{})
    # When we write the used_references to a new file these will be added back
    # The first element in the list will be an empty object since the reference file starts with a '@'
    print("Number of references in the .bib-file")
    print(len(references)-1)
    return references[1:]


def get_used_references(all_references,citations): 
    used_refs =[]
    # Regular expression pattern to find citations the string bar in e.g. @foo{bar, ... }
    pattern = r'\{([^,]+),'
    for ref in all_references : 
        # Search for the pattern in the input string
        match = re.search(pattern, ref)    
        # Extract the matched string
        if match:
            citation_id = match.group(1)
            for citation in citations :
                ## Check if the citation id in the .bib file is used in the .tex file. 
                if citation_id == citation :
                    used_refs.append("@"+ref)
    return used_refs

def create_new_bib_file(used_references) :
    print("Writing to file new_references.bib")
    # Clears the file each time you write 
    with open('new_references.bib', 'w', encoding='utf-8') as file:
    # Clear file before writing 
        file.truncate(0)
    # Write content to the file
        for ref in used_references : 
            file.write(ref)
    print('Done writing')

######################### HERE IS THE START OF THE PROGRAM ###############

### Add the required file paths ###
reference_file_name ="references.bib"
tex_file_path = "application.tex"
# Get the citations, references and then find all used references
cites = find_citations(tex_file_path)
refs = get_references(reference_file_name)
used_references=get_used_references(refs, cites)


#Write to a new .bib-file
create_new_bib_file(used_references)


