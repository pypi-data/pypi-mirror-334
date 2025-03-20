def generate_latex_article(data):
    latex_article = """
\\documentclass[12pt]{article}
\\usepackage{amsmath}
\\usepackage{graphicx}
\\usepackage{hyperref}
\\usepackage{biblatex}  % Add biblatex package for bibliography management
\\addbibresource{mybibliography.bib}  % biblatex file for references

\\begin{document}

\\title{Research Paper Title}
\\author{Author Name}
\\date{Date}
\\maketitle

\\begin{abstract}
{abstract_content}
\\end{abstract}

""".replace("{abstract_content}", data["abstract"])

    for section in data["sections"]:
        title = section["title"]
        content = section["content"]

        latex_article += f"""
\\section{{{title}}}
{content}

"""
    
    latex_article += """
\\section{References}
% Uncomment the next line to include the bibliography.
% \\printbibliography
% Make sure to create a 'mybibliography.bib' file with your references.

\\end{document}
"""

    return latex_article


if __name__ == '__main__':
    # Example usage:
    data = {
        "title": "Applied math",
        "description": "This format is common for applied mathematics, numerical analysis, and mathematical modeling papers. It focuses on theory, methods, numerical validation, and analysis of results.",
        "abstract": "Use the format:\n1. General context of the mathematical or numerical problem.\n2. Mathematical formulation or model being studied.\n3. Methods or numerical techniques applied to solve the problem.\n4. Validation of the proposed methods or model through numerical experiments.\n5. Analysis and discussion of the results obtained, including their implications.",
        "sections": [
            {"title":"Introduction", "content": "A brief overview of the research problem, objectives, and motivation."},
            {"title":"Theoretical Basis", "content": "Background on the mathematical theory, methods, or models that are used in the paper."},
            {"title":"Methodology", "content": "Explanation of the approach or methods developed or applied in the research."},
            {"title":"Numerical Results", "content": "Presentation of numerical experiments, data, and results obtained using the proposed methods."},
            {"title":"Analysis", "content": "Interpretation of the numerical results, comparison with theory or other methods."},
            {"title":"Acknowledgment", "content": "Acknowledgment of any support or funding received during the research."},
            {"title":"Conclusions", "content": "Summary of the findings and potential directions for future research."}
        ]
    }

    latex_code = generate_latex_article(data)
    print(latex_code)

