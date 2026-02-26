# PRACTICE_GUIDELINES

Generated: 2026-02-26 16:38 UTC
Repo: `JBLOZ/IA`

## 1) Voice and output style
- Language: Spanish
- Tone: direct, technical, no filler
- Structure for explanations: objective -> plan -> execution -> checks -> next steps
- For academic writeups, keep wording clear and reproducible

## 2) Model routing policy
- Redaction, summaries, explanations, and final narrative text: `main` (`openai-codex/gpt-5.2`) only
- Coding/refactor/debug/terminal changes: `repo-coder` (`openai-codex/gpt-5.3-codex`)
- Validation and release checks: `repo-validator`
- Notebook execution checks: `notebook-runner`

## 3) Practice workflow
1. Study `docs/REPO_CONTEXT.md` before editing
2. Reuse existing structure and naming conventions found in this repo
3. Open branch with `repo_workflow start-task`
4. Implement minimal scoped changes
5. Run `repo_workflow validate --repo-id <repo>`
6. Finish with `repo_workflow finish-task` and PR

## 4) Inferred local patterns
- Notebook count: 71
- Main practice clusters:
  - 3erAnyo/1erCuatri/modelos_computacionales_y_simulacion_de_sistemas: 17
  - 2doAnyo/2doCuatri/razonamiento_bajo_incertidumbre: 9
  - 2doAnyo/2doCuatri/tecnicas_de_algoritmos_de_busqueda: 8
  - 3erAnyo/1erCuatri/infraestructuras_y_servicios_cloud: 6
  - 3erAnyo/2doCuatri/redes_neuronales: 6
  - 3erAnyo/1erCuatri/fundamentos_de_aprendizaje_automatico: 4
  - 3erAnyo/2doCuatri/datos: 4
  - 3erAnyo/2doCuatri/agentes_inteligentes: 4
  - 2doAnyo/1erCuatri/sistemasDistrubuidos: 4
  - 3erAnyo/2doCuatri/aprendizaje_avanzado: 3
  - 2doAnyo/1erCuatri/algoritmia: 2
  - 2doAnyo/2doCuatri/computacion_de_alto_rendimiento: 2
- Frequent imports to keep style-consistent:
  - sklearn (26)
  - numpy (14)
  - matplotlib (14)
  - scipy (9)
  - simpy (4)
  - math (4)
  - pandas (3)
  - os (3)
  - warnings (3)
  - pathlib (1)
  - seaborn (1)
  - ipywidgets (1)

## 5) Reference baseline
- No external reference baseline used

## 6) Hard constraints
- Never push directly to main/master
- Never suggest bypassing GitHub branch protection
- Always use explicit confirmation gate for repo/file actions
