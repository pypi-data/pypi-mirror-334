"""Gemini utilities for PR Summary Generator"""

import google.generativeai as genai
from typing import Optional

from src.ai.base import BaseGenerativeModel
from .utils import get_branch_name, extract_ticket_from_branch


def generate_pr_summary(
    diff: str, api_key: str, jira_number: Optional[str] = None
) -> str:
    """Generate a PR summary using Gemini"""
    model = BaseGenerativeModel.get_instance().get_model()

    if not jira_number:
        branch_name = get_branch_name()
        jira_number = extract_ticket_from_branch(branch_name)

    ticket_section = (
        f"- [{jira_number}](https://cometa.atlassian.net/browse/{jira_number})"
        if jira_number
        else "- [JIRA-NUMBER](https://cometa.atlassian.net/browse/[JIRA-NUMBER])"
    )

    prompt = f"""
    Actúa como un experto desarrollador revisando cambios de código. Analiza los siguientes cambios de git y genera un resumen técnico y preciso del Pull Request.
    
    Reglas importantes:
    1. SOLO incluir cambios que realmente estén en el diff proporcionado
    2. Ser específico sobre qué archivos y funciones se modificaron
    3. Explicar el propósito técnico de cada cambio
    4. Mencionar cambios en la estructura del código, refactorizaciones o nuevas funcionalidades
    5. NO inventar cambios que no estén en el diff
    6. Usar lenguaje técnico y preciso
    7. Mantener el resumen conciso pero informativo
    
    El formato DEBE ser:
    
    ## Cambios realizados
    
    • [Archivo/Componente]: [Descripción técnica del cambio y su propósito]
    • [Siguiente cambio significativo...]
    
    ## Ticket
    
    {ticket_section}
    
    Cambios a analizar:
    {diff}
    """

    generation_config = {
        "temperature": 0.3,  # Reducido para mayor precisión
        "top_p": 0.8,
        "top_k": 40,
        "max_output_tokens": 2048,
    }

    safety_settings = [
        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
    ]

    response = model.generate_content(
        prompt, generation_config=generation_config, safety_settings=safety_settings
    )

    return response.text


def generate_commit_message(diff: str, api_key: str) -> str:
    """Generate a commit message using Gemini"""
    model = BaseGenerativeModel.get_instance().get_model()

    prompt = f"""
    Act as an expert developer and generate a commit message following the Conventional Commits format.
    Analyze the provided changes and generate a concise but descriptive message that specifically reflects the changes made.
    
    The format must be:
    type(scope): description
    
    Where:
    - type: feat (new feature), fix (bug fix), docs (documentation), style (formatting), refactor (code refactoring), test (adding tests), chore (maintenance)
    - scope: area of change (optional, e.g., cli, utils, api)
    - description: concise description in present tense that specifically explains what changed
    
    Rules:
    1. The description must reflect the specific changes in the diff
    2. Use verbs in present tense
    3. Do not exceed 72 characters
    4. Do not use a period at the end
    5. Be specific about what was changed
    6. MUST BE IN ENGLISH (not Spanish)
    
    For example, if the diff shows:
    - Changes in authentication functions: "feat(auth): implement JWT token validation"
    - Fix for a bug in the CLI: "fix(cli): resolve error when processing --help arguments"
    - Refactoring utilities: "refactor(utils): simplify file grouping function"
    
    Here are the changes to analyze:
    {diff}
    """

    generation_config = {
        "temperature": 0.3,
        "top_p": 0.8,
        "top_k": 40,
        "max_output_tokens": 100,
    }

    response = model.generate_content(prompt, generation_config=generation_config)
    return response.text.strip()
