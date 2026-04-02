"""
hilbert_problems_prompts.py - PromptBuilder class for Hilbert's 23 Problems

Contains the PromptBuilder class for creating structured prompts
for fetching comprehensive information about Hilbert's mathematical problems.
"""



class PromptBuilder:
    """Builder class for creating Hilbert problem prompts."""
    
    # Canonical mapping of Hilbert's 23 Problems
    PROBLEM_TITLES = {
        1: "The Continuum Hypothesis",
        2: "Consistency of the Axioms of Arithmetic",
        3: "Equality of the Volumes of Two Tetrahedra",
        4: "Problem of the Straight Line as the Shortest Distance Between Two Points",
        5: "Lie's Concept of a Continuous Group",
        6: "Mathematical Treatment of the Axioms of Physics",
        7: "Irrationality and Transcendence of Certain Numbers",
        8: "Problems of Prime Numbers (Riemann Hypothesis, Goldbach's Conjecture)",
        9: "Proof of the Most General Reciprocity Law in Any Number Field",
        10: "Determination of the Solvability of a Diophantine Equation",
        11: "Quadratic Forms with Any Algebraic Numerical Coefficients",
        12: "Extension of Kronecker's Theorem on Abelian Fields to Any Algebraic Domain of Rationality",
        13: "Impossibility of the Solution of the General Equation of the 7th Degree by Means of Functions of Only Two Arguments",
        14: "Proof of the Finiteness of Certain Complete Systems of Functions",
        15: "Rigorous Foundation of Schubert's Enumerative Calculus",
        16: "Problem of the Topology of Algebraic Curves and Surfaces",
        17: "Expression of Definite Forms by Squares",
        18: "Building Up of Space from Congruent Polyhedra",
        19: "Are the Solutions of Regular Problems in the Calculus of Variations Always Necessarily Analytic?",
        20: "General Problem of Boundary Values",
        21: "Proof of the Existence of Linear Differential Equations Having a Prescribed Monodromic Group",
        22: "Uniformization of Analytic Relations by Means of Automorphic Functions",
        23: "Further Development of the Methods of the Calculus of Variations"
    }

    @staticmethod
    def get_system_prompt() -> str:
        """
        Get the system prompt for Hilbert problems generation.
        
        Returns:
            System prompt string for LLM
        """
        return """You are an expert mathematical historian and mathematician specializing in the work of David Hilbert. Your task is to provide accurate, rigorous, and well-structured information about Hilbert's 23 problems proposed in 1900 at the Second International Congress of Mathematicians in Paris.

Fundamental Principles:
1. Historical Precision: Problems were proposed in 1900. Do not confuse them with prior congresses.
2. Direct Correlation: Every problem must match its canonical title (e.g., Problem 1 is the Continuum Hypothesis).
3. Current Status: Accurately reflect whether the problem is solved, partially solved, or still open (e.g., Riemann Hypothesis).
4. Solvers: Identify the correct mathematicians and years (e.g., Kurt Gödel 1940, Paul Cohen 1963 for Problem 1).
5. Mathematical Rigor: Use precise terminology and provide meaningful descriptions of the methodology used for solutions.

Return structured data as requested, ensuring all historical and mathematical facts are verified."""

    @staticmethod
    def get_user_prompt(problem_number: int) -> str:
        """
        Get the user prompt for a specific Hilbert problem.
        
        Args:
            problem_number: The problem number (1-23)
            
        Returns:
            User prompt string for LLM
        """
        title = PromptBuilder.PROBLEM_TITLES.get(problem_number, "Unknown Problem")
        
        return f"""Provide comprehensive information about Hilbert's Problem #{problem_number}: {title}.

Include the following structured details:
1. **Title**: {title}
2. **Mathematical Description**: Clear and precise mathematical formulation of the problem as Hilbert stated it.
3. **Current Status**: Whether solved, unsolved, or partially solved.
4. **Solution Details**: If solved or partially solved, specify WHO solved it and WHEN.
5. **Solution Method**: A detailed explanation of the logic, theorems, or approaches used to address the problem.
6. **Related Fields**: List the mathematical areas connected to this problem.
7. **Important Notes**: Implications, historical context, or modern relevance.

Strict Requirements:
- Number: {problem_number}
- Exact title: {title}
- Use factual, historical data only.
- Return the response with these exact field names: number, title, description, status, solved_by, solution_year, solution_method, related_fields, notes"""

    @staticmethod
    def get_reviewer_system_prompt() -> str:
        """
        Get the system prompt for the reviewer agent.

        Returns:
            System prompt string for the validation and correction pass
        """
        return """You are a second-pass reviewer checking a mathematical reference entry about Hilbert's 23 problems.

Your job is to audit a draft for factual accuracy, historical precision, and schema consistency.

Review Rules:
1. Preserve the canonical Hilbert problem number and title.
2. Correct any factual, historical, or mathematical inaccuracies.
3. Tighten vague wording when needed, but do not add speculation.
4. Return the final corrected response in a well-formatted Markdown structure.
5. Use headers, bullet points, and bold text for readability.
6. If the draft is already accurate, return a cleaned and validated version with only necessary edits."""

    @staticmethod
    def get_reviewer_prompt(problem_number: int, draft_problem_json: str) -> str:
        """
        Get the reviewer prompt for a specific Hilbert problem draft.

        Args:
            problem_number: The problem number (1-23)
            draft_problem_json: JSON string produced by the first agent

        Returns:
            User prompt string for the review agent
        """
        title = PromptBuilder.PROBLEM_TITLES.get(problem_number, "Unknown Problem")

        return f"""Review and correct this draft entry for Hilbert's Problem #{problem_number}: {title}.

Canonical title: {title}

Draft entry (JSON):
{draft_problem_json}

Tasks:
1. Verify that the number and title match the canonical Hilbert problem.
2. Correct any inaccurate status, solver attribution, year, description, method, related fields, or notes.
3. Keep the content historically precise and mathematically rigorous.
4. Format the final output as a clean Markdown report with the following sections:
- # Hilbert's Problem #{problem_number}: {title}
- **Status**: (solved, unsolved, partially solved)
- **Solved By**: (if applicable)
- **Year**: (if applicable)
- **Description**: (clear mathematical formulation)
- **Solution Method**: (detailed explanation)
- **Related Fields**: (list of mathematical areas)
- **Notes**: (historical context or modern relevance)"""


    @staticmethod
    def get_summary_prompt() -> str:
        """
        Get the user prompt for generating a summary of all Hilbert problems.
        
        Returns:
            User prompt string for LLM
        """
        return """Provide a comprehensive overview of all 23 of Hilbert's problems, including:

1. **Problem Numbers and Titles**: List all 23 problems with their titles
2. **Status Overview**: Current status of each problem (solved/unsolved/partially solved)
3. **Historical Significance**: Impact on 20th century mathematics
4. **Key Solvers**: Mathematicians who contributed to solutions
5. **Mathematical Fields**: Areas of mathematics influenced by these problems
6. **Open Problems**: Which problems remain unsolved and their importance

Requirements:
- Provide accurate historical information
- Include current status of each problem
- Highlight major mathematical breakthroughs
- Emphasize the collective impact on mathematics
- Use clear, organized structure
- Reference important dates and contributors

Focus on the collective impact of these problems on mathematical research and their continuing influence on the field."""

    @staticmethod
    def get_summary_reviewer_prompt(summary_text: str) -> str:
        """
        Get the reviewer prompt for the summary draft.

        Args:
            summary_text: Text produced by the first summary agent

        Returns:
            User prompt string for the summary review pass
        """
        return f"""Review and refine the following summary of Hilbert's 23 problems.

Tasks:
1. Correct any factual or historical inaccuracies.
2. Improve clarity and organization without making the summary longer than necessary.
3. Preserve the overall structure when it is already sound.
4. Return only the final revised summary text.

Draft summary:
{summary_text}"""
