# Modelling Lessons Repository

This repository contains structured materials for a modelling course. Each lesson focuses on a specific modelling paradigm and includes simulations, visualizations, and supporting theory. Materials are organized for easy navigation and use in both teaching and self-study.

## Repository Structure

### Top-Level Folders

- **`data/`** – Input datasets used across lessons (e.g., demographic and correlation data).
- **`references.bib`** – Central bibliography file used across LaTeX documents.
- **`styles/`** – Custom LaTeX style definitions.
- **`supplementary_files/`** – Miscellaneous materials (notes, reusable LaTeX elements).
- **`other_documents/`** – Grading criteria, example paper drafts.

---

### Lesson Folders (`lesson_1/` to `lesson_6/`)

Each `lesson_X/` folder typically includes the following subfolders and files:

- **`code/`** – MATLAB or Python scripts implementing models or simulations relevant to the lesson.
- **`images/`** – Figures and illustrations used in lecture notes or slides (e.g., model diagrams, simulation outputs).
- **`sections/`** – LaTeX source files for individual sections of the lesson. Modular format to support collaborative editing and reuse.
- **`lesson_X_<topic>.tex` / `.pdf`** – Compiled lesson content in LaTeX and PDF formats, combining all sections.
- **`simulink/`** – Simulink `.slx` models for visual simulation of systems.
- **`literature/`** *(if present)* – Relevant research papers or supporting readings.
- **`other_resources/`** *(if present)* – Additional resources such as spreadsheets or datasets specific to the lesson topic.

---

### Lesson Topics

- **Lesson 1:** Fibonacci sequences, exponential and logistic population models
- **Lesson 2:** Predator-prey systems, ecological feedbacks, pesticide paradox
- **Lesson 3:** Epidemic modelling, SIR models, agent-based approaches
- **Lesson 4:** Cellular automata: Game of Life, fire spread, elementary rules
- **Lesson 5:** Chaos theory, bifurcations, fractals, complex system behavior
- **Lesson 6:** (Reserved for future topics)

---

## Requirements

- **MATLAB / Simulink** – Core simulation platform
- **Python (optional)** – Some models and visualizations
- **LaTeX** – For compiling documents and slides

## Notes

This repository is meant for educational use. All lessons are modular and self-contained. Code is organized for readability and can be used for in-class demonstrations, assignments, or extended projects.
