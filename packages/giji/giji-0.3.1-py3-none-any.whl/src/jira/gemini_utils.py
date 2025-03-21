"""Gemini utilities for Jira integration"""

import google.generativeai as genai
from typing import Optional

from src.ai.base import BaseGenerativeModel


def generate_jira_comment(pr_summary: str, jira_description: str, api_key: str) -> str:
    """Generate a Jira comment explaining the implemented changes and how they relate to the ticket"""
    model = BaseGenerativeModel.get_instance().get_model()

    prompt = f"""
    Actúa como un desarrollador técnico explicando en detalle los cambios realizados en un Pull Request y cómo estos resuelven específicamente el problema del ticket de Jira.

    Reglas importantes:
    1. Ser informativo y técnicamente preciso - máximo 3-4 oraciones por sección
    2. Solo mencionar cambios listados en el PR summary
    3. Relacionar DIRECTAMENTE los cambios con el problema descrito en el ticket
    4. Explicar con detalle técnico cómo la implementación resuelve la causa raíz del problema
    5. Equilibrar lenguaje técnico con explicaciones comprensibles
    6. Proporcionar contexto completo sobre el antes y después del cambio

    Formato del comentario:
    ## Solución Implementada
    [3-4 oraciones técnicas sobre los cambios realizados, mencionar archivos modificados, clases/funciones creadas o modificadas, y detalles de implementación]

    ## Relación con el Ticket
    [3-4 oraciones explicando:
    - Cuál era exactamente el problema (referenciando la descripción del ticket)
    - Cómo la solución técnica implementada resuelve ese problema específico
    - Qué aspectos concretos de la implementación abordan cada parte del problema]

    ## Valor para el Usuario
    [2-3 oraciones sobre los beneficios tangibles para usuarios/desarrolladores:
    - Cómo mejora la experiencia del usuario
    - Qué errores o limitaciones se eliminan
    - Qué procesos se optimizan o simplifican]

    PR Summary:
    {pr_summary}

    Descripción del ticket:
    {jira_description}
    """

    generation_config = {
        "temperature": 0.3,
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