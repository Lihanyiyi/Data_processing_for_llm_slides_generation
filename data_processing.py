import os

os.system("arxiv_latex_cleaner arXiv-2407.07454v3")

import re
import json

def get_full_text(file_path):
    with open(file_path, 'r') as file:
        data = file.read()
    return data

def get_authors(tex_content):
    author_pattern=re.compile(r'\\title{.*?\\begin{abstract}', re.DOTALL)
    author_match=author_pattern.search(tex_content)
    if author_match:
        author_content=author_match.group(0)
    else:
        author_content=""
    return author_content

def extract_title(tex_content):
    title_pattern = re.compile(r'\\title{([^}]*)}', re.DOTALL)
    title_match = title_pattern.search(tex_content)
    if title_match:
        title_content = title_match.group(1)
    else:
        title_content = ""
    
    return title_content

def extract_abstract(tex_content):
    abstract_pattern = re.compile(r'\\begin{abstract}.*?\\end{abstract}', re.DOTALL)
    
    abstract_match = abstract_pattern.search(tex_content)
    if abstract_match:
        abstract_content = abstract_match.group(0)
    else:
        abstract_content = ""
    
    return abstract_content

def extract_sections_names(tex_content):
    section_pattern = re.compile(r'\\section\{([^}]*)\}', re.DOTALL)
    sections = section_pattern.findall(tex_content)
    return sections

def extract_sections(tex_content, section_names):
    section_dict={}
    for i in range(len(section_names)):
        if i==len(section_names)-1:
            section_pattern=re.compile(r'\\section\{'+section_names[i]+r'\}(.*?)\\end{document}', re.DOTALL)
        else:   
            section_pattern=re.compile(r'\\section\{'+section_names[i]+r'\}(.*?)\\section', re.DOTALL)
        section_match=section_pattern.search(tex_content)
        if section_match:
            section_content=section_match.group(1)
        else:
            section_content=""
        section_dict[section_names[i]]=section_content
    return section_dict
    
def main(file_path):
    tex_content = get_full_text(file_path)
    authors = get_authors(tex_content)
    title = extract_title(tex_content)
    abstract = extract_abstract(tex_content)
    section_names = extract_sections_names(tex_content)
    sections = extract_sections(tex_content, section_names)
    
    data = {
        "authors": authors,
        "title": title,
        "abstract": abstract,
    }
    for section_name, section_content in sections.items():
        data[section_name] = section_content
    json_data = json.dumps(data, ensure_ascii=False, indent=4)
    with open(f"{title}.json", "w") as file:
        file.write(json_data)
    return data

main("arXiv-2407.07454v3_arXiv/main.tex")
print("Data processing completed!")
