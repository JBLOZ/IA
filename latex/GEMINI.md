# GEMINI Project Context: LaTeX Academic Papers

## Directory Overview

This directory contains the LaTeX source code and configuration for two academic documents authored by Jordi Blasco Lozano:

1.  A detailed technical report on a **Hierarchical Reasoning Model (HRM)**, likely for a Final Degree Project (`TFG.tex`).
2.  A practical report on an introduction to **OpenMP** for parallel computing (`mi_paper.tex`).

The project is configured to be built with `xelatex` and uses `biber` for bibliography management. A custom style package (`paper_style.sty`) is used to ensure consistent formatting, including syntax highlighting for code blocks.

## Key Files

*   `tfg.tex`: The main source file for the technical report on the Hierarchical Reasoning Model.
*   `mi_paper.tex`: The main source file for the practical report on OpenMP.
*   `TFG.txt`: A plain text draft or notes related to the content of `tfg.tex`.
*   `bibliografia.bib`: The BibTeX database containing all citations used in the documents.
*   `paper_style.sty`: A custom LaTeX style package that defines document structure, colors, and formatting for code listings (C++, Python, shell).
*   `.latexmkrc`: A configuration file for the `latexmk` build tool. It specifies the use of `xelatex` and `biber`.
*   `.vscode/tasks.json`: Defines build and clean tasks for the Visual Studio Code editor, using `latexmk`.
*   `*.pdf`: The final compiled PDF documents generated from the `.tex` source files.

## Building and Usage

The primary workflow for this project is editing the `.tex` files and compiling them to generate PDFs. The `latexmk` tool is configured to automate this process.

### Build Command

To compile a document (e.g., `tfg.tex`), run the following command from the terminal. This command uses `xelatex` as specified in the configuration files.

```sh
latexmk -xelatex tfg.tex
```

Replace `tfg.tex` with `mi_paper.tex` to build the other document.

### Clean Command

To remove the auxiliary files generated during compilation (e.g., `.aux`, `.log`, `.bcf`), you can use the clean command:

```sh
latexmk -c
```
