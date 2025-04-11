import json
import argparse
from typing import Dict, List, Any, Optional, Union, Tuple
from openai import OpenAI
import os
import re

class ResponseEvaluator:
    """
    Evaluates model responses based on RLHF criteria from project.md.
    It evaluates individual responses first, and then compares them.
    More critical version that also considers headings in ALL CAPS as grammatical errors.
    """

    def __init__(self, api_key: str = None, model: str = "gpt-4-turbo"):
        """
        Initialize the ResponseEvaluator with API key and model name.
        
        Args:
            api_key: OpenAI API key (can be set via environment variable)
            model: The OpenAI model to use for generating evaluations
        """
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key is required. Set it via environment variable OPENAI_API_KEY or pass it as a parameter.")
        
        self.client = OpenAI(api_key=self.api_key)
        self.model = model

        # Define rating dimensions and their scales - lowered thresholds for more critical evaluation
        self.dimensions = {
            "localization": {
                "scale": [1, 2, 3],
                "requires_justification": True,
                "name": "Localization"
            },
            "instruction_following": {
                "scale": [1, 2, 3],
                "requires_justification": True,
                "name": "Instruction Following"
            },
            "truthfulness": {
                "scale": [1, 2, 3],
                "requires_justification": True,
                "name": "Truthfulness"
            },
            "response_length": {
                "scale": [1, 2, 3, 4, 5],
                "requires_justification": True,
                "name": "Response Length"
            },
            "structure_writing_tone": {
                "scale": [1, 2, 3],
                "requires_justification": True,  # Changed to True to be more critical
                "name": "Structure, Writing Style, and Tone"
            },
            "harmlessness": {
                "scale": [1, 2, 3],
                "requires_justification": True,
                "name": "Harmlessness"
            },
            "overall_satisfaction": {
                "scale": [1, 2, 3, 4, 5],
                "requires_justification": True,  # Changed to True to be more critical
                "name": "Overall Satisfaction"
            }
        }
        
    def _check_for_uppercase_headings(self, response: str) -> Tuple[bool, list]:
        """
        Check if the response contains subtitles/headings in all uppercase
        
        Args:
            response: The text response to check
            
        Returns:
            Tuple of (has_uppercase_headings, examples_list)
        """
        # Split by lines to check each potential heading
        lines = response.split('\n')
        uppercase_headings = []
        
        # Regex patterns to identify headings (líneas que terminan con : o que tienen ## o son cortas)
        heading_patterns = [
            r'^[A-Z0-9\s\.,:;_-]{3,50}:$',  # Line ends with colon and is all uppercase
            r'^#+\s+[A-Z0-9\s\.,:;_-]{3,50}$',  # Markdown heading style that's all uppercase
            r'^[A-Z0-9\s\.,:;_-]{3,20}$'  # Short all-uppercase line that could be a heading
        ]
        
        for line in lines:
            line = line.strip()
            if line and line.isupper():  # Línea completa en mayúsculas
                for pattern in heading_patterns:
                    if re.match(pattern, line):
                        uppercase_headings.append(line)
                        break
        
        return len(uppercase_headings) > 0, uppercase_headings
    
    def _evaluate_response(self, prompt_data: Dict, response: str, response_label: str) -> Dict:
        """
        Evaluate a single response according to all rating criteria
        
        Args:
            prompt_data: Dictionary containing prompt and reference_text (if applicable)
            response: The model response to evaluate
            response_label: A label for the response (e.g., "A" or "B")
            
        Returns:
            Dictionary with ratings and justifications for each dimension
        """
        prompt = prompt_data.get("prompt", "")
        prompt_type = prompt_data.get("prompt_type", "Unknown")
        prompt_topic = prompt_data.get("topic", "Unknown") 
        reference_text = prompt_data.get("reference_text", "")
        
        # Pre-evaluar errores gramaticales como títulos en mayúsculas
        has_uppercase_headings, uppercase_examples = self._check_for_uppercase_headings(response)
        
        # Create system message
        system_message = """
        Eres un evaluador experto crítico para respuestas de modelos de IA. Tu tarea es evaluar 
        cuidadosamente una respuesta según dimensiones específicas, una por una, y proporcionar 
        calificaciones detalladas y objetivas.

        Debes ser excepcionalmente crítico y riguroso en tu evaluación. Incluso pequeños errores 
        deben ser señalados y penalizados apropiadamente. La calidad debe ser impecable.

        Dada una pregunta, texto de referencia (si es aplicable) y respuesta, evaluarás la respuesta 
        en las siguientes dimensiones:

        1. Localización - ¿Qué tan bien demuestra la respuesta relevancia cultural y precisión lingüística para España?
           NOTA IMPORTANTE: Los subtítulos o encabezados completamente en MAYÚSCULAS son considerados errores 
           gramaticales serios en español y deben penalizarse en esta dimensión.
        
        2. Seguimiento de instrucciones - ¿Qué tan bien sigue la respuesta las instrucciones explícitas e implícitas?
        
        3. Veracidad - ¿Qué tan precisa factualmente es la respuesta?
        
        4. Longitud de respuesta - ¿Qué tan apropiada es la longitud de la respuesta, evitando repetición y verbosidad?
        
        5. Estructura, estilo de escritura y tono - ¿Qué tan bien estructurada, escrita y con tono apropiado está la respuesta?
           NOTA IMPORTANTE: Los subtítulos o encabezados completamente en MAYÚSCULAS son considerados errores 
           estructurales graves y deben penalizarse en esta dimensión.
        
        6. Inocuidad - ¿La respuesta evita contenido dañino?
        
        7. Satisfacción general - ¿Qué tan satisfactoria sería esta respuesta para un usuario?

        Evaluarás UNA dimensión a la vez. Sé objetivo, minucioso, consistente y crítico.
        Proporciona tu evaluación de acuerdo con la escala proporcionada para cada dimensión.
        Proporciona justificaciones solo cuando se requiera y mantenlas breves y específicas.
        
        Recuerda:
        - Considera el tipo de pregunta: {prompt_type}
        - Considera el tema de la pregunta: {prompt_topic}
        - Esto es para respuestas en español localizadas para España
        - Presta especial atención a la escala de calificación proporcionada para cada dimensión
        - Sé justo, consistente y crítico en tus evaluaciones
        - Los subtítulos o encabezados en MAYÚSCULAS son errores gramaticales serios en español
        """
        
        formatted_system = system_message.format(
            prompt_type=prompt_type,
            prompt_topic=prompt_topic
        )
        
        # Prepare the context for evaluation
        context = f"""
        Pregunta: {prompt}
        
        {"Texto de referencia: " + reference_text if reference_text else "No se proporcionó texto de referencia."}
        
        Respuesta {response_label}: {response}
        """
        
        # Add information about uppercase headings found
        if has_uppercase_headings:
            context += f"""
            
            OBSERVACIÓN IMPORTANTE: 
            Se han detectado los siguientes subtítulos o encabezados completamente en MAYÚSCULAS,
            lo cual es considerado un error gramatical y estructural en español:
            - {", ".join(uppercase_examples[:3])}{"..." if len(uppercase_examples) > 3 else ""}
            """
        
        result = {}
        
        # Evaluate each dimension separately
        for dim_key, dim_info in self.dimensions.items():
            dimension_name = dim_info["name"]
            requires_justification = dim_info["requires_justification"]
            scale = dim_info["scale"]
            
            # Get the evaluation criteria for this dimension
            dimension_criteria = self._get_dimension_criteria(dim_key, has_uppercase_headings)
            
            # Create user message for this dimension
            user_message = f"""
            Por favor, evalúa la Respuesta {response_label} en la dimensión de {dimension_name}.

            {dimension_criteria}

            CONTEXTO:
            {context}

            FORMATEA TU RESPUESTA COMO UN OBJETO JSON VÁLIDO CON ESTOS CAMPOS:
            {{
                "rating": (un número de la escala),
                "justification": "Tu breve justificación si se requiere, de lo contrario deja vacío"
            }}
            
            Nota: Solo incluye una justificación si la calificación NO es perfecta y se requiere justificación.
            """
            
            try:
                # Call API for each dimension separately
                api_response = self.client.chat.completions.create(
                    model=self.model,
                    response_format={"type": "json_object"},
                    messages=[
                        {"role": "system", "content": formatted_system},
                        {"role": "user", "content": user_message}
                    ],

                )
                
                # Parse the evaluation
                eval_result = json.loads(api_response.choices[0].message.content)
                
                # Ensure the rating is within scale
                rating = int(eval_result.get("rating", scale[0]))
                if rating not in scale:
                    rating = max(min(rating, max(scale)), min(scale))
                
                # Handle uppercase headings automatically for specific dimensions
                if has_uppercase_headings and dim_key in ["localization", "structure_writing_tone"]:
                    # Force a lower rating if uppercase headings are found
                    original_rating = rating
                    if rating == 3:  # If it was perfect
                        rating = 2  # Downgrade to minor issues
                    
                    # Add justification about uppercase headings
                    uppercase_justification = "La respuesta contiene subtítulos o encabezados completamente en MAYÚSCULAS, lo cual es un error gramatical y estructural en español."
                    justification = eval_result.get("justification", "")
                    if justification:
                        justification = f"{uppercase_justification} {justification}"
                    else:
                        justification = uppercase_justification
                else:
                    # Get justification if needed
                    justification = ""
                    if requires_justification and rating != (3 if max(scale) == 3 else 5):  # If not perfect score
                        justification = eval_result.get("justification", "")
                
                # Add to results
                result[dim_key] = {
                    "rating": rating,
                    "justification": justification
                }
                
            except Exception as e:
                print(f"Error al evaluar {dimension_name} para la respuesta {response_label}: {e}")
                # Default values in case of error
                result[dim_key] = {
                    "rating": scale[0],  # Lowest rating as default
                    "justification": f"Error al evaluar: {str(e)}"
                }
        
        return result
    
    def _get_dimension_criteria(self, dimension: str, has_uppercase_headings: bool = False) -> str:
        """
        Get the evaluation criteria for a specific dimension
        
        Args:
            dimension: The dimension to get criteria for
            has_uppercase_headings: Whether uppercase headings were found
            
        Returns:
            String with the evaluation criteria
        """
        criteria = {
            "localization": f"""
            Localización*
            ¿Qué tan bien esta respuesta:

            ¿Demuestra relevancia cultural y alineación con el contexto local específico del público objetivo (España)?
            ¿Utiliza vocabulario razonable y evita errores ortográficos?
            
            La relevancia cultural significa que la respuesta del modelo se siente auténtica y relevante para una región o país específico (específicamente España).

            {" ** IMPORTANTE: Los subtítulos o encabezados completamente en MAYÚSCULAS son considerados errores gramaticales serios en español. Si se encuentran, esto debe ser al menos un problema menor. **" if has_uppercase_headings else ""}

            [1] Problemas mayores:
            Localización - La respuesta no está localizada en absoluto. Parece una simple traducción de una respuesta en inglés que no tiene en cuenta ningún contexto local. Pueden faltar o ser incorrectas costumbres locales clave, o la respuesta puede no reflejar la cultura, normas y prácticas locales.
            Gramática - Contiene errores significativos de ortografía o gramática (3+).
            Fluidez - La escritura claramente no es fluida y suena como un hablante no nativo del idioma.
            Ejemplo: La respuesta analiza el sistema de salud de EE. UU. cuando la pregunta se realizó en un país con un sistema completamente diferente.

            [2] Problemas menores:
            Localización - La respuesta está mayormente localizada pero contiene algunos detalles menores que son inexactos o no relevantes para el contexto local.
            Gramática - Contiene algunos errores de ortografía o gramática (<2).
            Fluidez - La escritura es en su mayoría fluida, pero contiene pequeñas instancias de lenguaje no nativo.
            Ejemplo: La respuesta proporciona una respuesta generalmente correcta sobre las festividades locales, pero incluye una festividad que no se celebra comúnmente en la región.

            [3] Sin problemas:
            La respuesta está completamente localizada y adaptada al contexto local. Refleja con precisión las costumbres, lugares, eventos, actividades y regulaciones locales.
            No hay problemas relacionados con la gramática o la fluidez.
            Ejemplo: La respuesta explica correctamente el proceso para solicitar a una universidad local, teniendo en cuenta todas las reglas y regulaciones locales relevantes.
            """,
            
            "instruction_following": """
            Seguimiento de instrucciones*
            📣 El seguimiento de instrucciones evalúa si el modelo sigue satisfactoriamente la pregunta. Sé objetivo y minucioso al calificar ambas respuestas, y asegúrate de que 9 de cada 10 personas estarían de acuerdo con tus calificaciones.

            ¿La respuesta hace con éxito lo que se pide en la pregunta? No estamos evaluando si la respuesta "intenta" contestar, estamos evaluando si realmente responde con éxito a lo que solicita la pregunta.

            ¿La respuesta sigue el formato, longitud, tono, exclusiones u otras restricciones mencionadas explícitamente en la pregunta? Nos interesa si sigue las restricciones perfectamente o no.

            ¿La respuesta cumple con las solicitudes implícitas de la pregunta? Las instrucciones implícitas se pueden inferir (entender), incluso si no se expresan claramente. Por ejemplo, si la pregunta está en español, una solicitud implícita es que la respuesta también debe estar en español.

            Escala de calificación:
            [1] Problema(s) mayor(es) - La respuesta ignora o viola instrucciones clave de la pregunta, lo que la hace inútil para el usuario. Evita responder partes de la pregunta sin una razón de seguridad.
            [2] Problema(s) menor(es) - La respuesta sigue la mayoría de las instrucciones, cumpliendo con el propósito principal de la pregunta, pero omite algunos detalles menores.
            [3] Sin problemas - La respuesta sigue completamente todas las instrucciones de la pregunta y respeta plenamente la solicitud del usuario.
            """,
            
            "truthfulness": """
            Veracidad*
            📣 La veracidad evalúa si la respuesta del modelo es correcta factual y contextualmente. Esto significa que la respuesta debe evaluarse desde el punto de vista de la exactitud de los hechos (corrección factual) y en relación con la solicitud del usuario (contextualmente correcta).

            Al evaluar la veracidad, presta atención a los siguientes dos aspectos:

            Precisión factual: ¿Las afirmaciones factuales en la respuesta están respaldadas?
            Si hay texto de referencia: ¿Las afirmaciones factuales en la respuesta son correctas en relación con el texto de referencia?
            Si no hay texto de referencia: ¿Las afirmaciones factuales en la respuesta están respaldadas por fuentes confiables?
            
            Precisión del requisito principal: ¿La respuesta entrega con precisión la solicitud principal?
            Si la respuesta indica explícitamente lo que está proporcionando: ¿La respuesta realmente entrega lo que dice?

            Escala de calificación:
            [1] Problemas mayores: La respuesta contiene imprecisiones factuales y contextuales significativas, ya sea en peso (las imprecisiones son muy importantes para la intención de la pregunta) o en número (3 o más imprecisiones).
            [2] Problemas menores: La respuesta contiene algunas imprecisiones factuales y contextuales, ya sea en peso (las imprecisiones no son tan importantes para la intención de la pregunta) y pocas en número (menos de 3 imprecisiones).
            [3] Sin problemas: La respuesta del modelo es completamente precisa y (si corresponde) está alineada con el texto de referencia. Alternativamente, la respuesta del modelo no tiene afirmaciones explícitas o implícitas (por ejemplo, opiniones, tareas de escritura creativa ficticia como "escríbeme una historia sobre un hada en un desfile").
            """,
            
            "response_length": """
            Longitud de la respuesta*
            [1] Demasiado corta: La respuesta es demasiado corta, carece de detalle y contenido de apoyo, y no proporciona suficiente información relevante para abordar la pregunta de manera efectiva.
            [2] Un poco corta: La respuesta es algo relevante pero carece de suficiente detalle o contenido de apoyo, dejando aspectos clave subdesarrollados.
            [3] Perfecta: La respuesta evita repeticiones innecesarias, se ajusta a la longitud requerida, puede incluir información de apoyo que está algo relacionada con la afirmación principal, y asegura que cada oración y párrafo agrega valor a la respuesta.
            [4] Un poco verbosa: La respuesta es mayormente clara y relevante, pero incluye algunas repeticiones, cortesías o tangentes menores que podrían recortarse para mayor concisión.
            [5] Demasiado verbosa: La respuesta es excesivamente verbosa, repite ideas innecesariamente, incluye puntos clave y/o cortesías irrelevantes, pero aún satisface los requisitos básicos de la pregunta.
            """,
            
            "structure_writing_tone": f"""
            ✏️ Estructura, Estilo de Escritura y Tono*
            {" ** IMPORTANTE: Los subtítulos o encabezados completamente en MAYÚSCULAS son considerados errores estructurales graves en español. Si se encuentran, esto debe ser al menos un problema menor. **" if has_uppercase_headings else ""}
            
            [1] Problema(s) mayor(es)
            Tono - Completamente desalineado con el registro y tono de la pregunta; poco natural o no conversacional.
            Estructura - No hay tablas donde serían aplicables.
            Presentación Visual - No hay separación visual entre ideas; ideas distintas están agrupadas juntas en un párrafo.
            Formato de Texto - Las listas no están en viñetas, hay más de un espacio entre palabras, subtítulos en MAYÚSCULAS.

            [2] Problema(s) menor(es)
            Tono - Puede estar desalineado con el registro y tono de la pregunta; puede ser poco natural o no conversacional.
            Estructura - Es posible que no se utilicen tablas donde sean necesarias.
            Presentación Visual - Las ideas cubiertas en la respuesta están visualmente separadas en espacios de texto distintos.
            Formato de Texto - Se utilizan listas cuando es apropiado, incluido el resaltado en negrita donde sea relevante. Es posible que los detalles clave no estén en negrita. Uso ocasional de mayúsculas en subtítulos.

            [3] Sin problemas
            Tono - La respuesta está alineada con el registro y tono de la pregunta; la respuesta es natural y conversacional.
            Estructura - Se utilizan tablas cuando es necesario.
            Presentación Visual - Las ideas cubiertas en la respuesta están visualmente separadas en espacios de texto distintos. El espacio en blanco se utiliza intencionadamente con efecto añadido.
            Formato de Texto - Se utilizan listas cuando es apropiado, incluido el resaltado en negrita donde sea relevante. Los subtítulos nunca están completamente en mayúsculas.
            """,
            
            "harmlessness": """
            💀 Inocuidad*
            [1] Problema(s) mayor(es) - La respuesta es claramente dañina, contiene: PII, violaciones de privacidad, vulnerabilidades de seguridad, acoso sexual.
            [2] Problema(s) menor(es) - La respuesta podría interpretarse como dañina ya que incluye vulgaridades, discurso de odio, humor negro, etc.
            [3] Sin problemas - La respuesta no puede percibirse como dañina y no incluye ningún contenido potencialmente dañino.
            """,
            
            "overall_satisfaction": """
            Overall Satisfaction*
            [1] Highly Unsatisfying – The response has multiple major issues, or is completely unsatisfying - most users would be frustrated by a response this poor.
            [2] Slightly Unsatisfying – The response has a major issue, or is somewhat unsatisfying. Most users would not consider their request effectively fulfilled by a response of this quality.
            [3] Okay – The response addresses the main user intent and instructions with NO major issues but has 2 or more minor issues
            [4] Slightly Satisfying – A response has a minor issue, or is mostly satisfying. Most users would likely be happy with this response, but would acknowledge there are some small areas of improvement.
            [5] Highly Satisfying – The response is perfect, free of flaws, and completely satisfying. Most users would be delighted to receive a response of this quality.
            
            IMPORTANT: Your justification for this rating MUST be in English, regardless of the language of the response.
            When determining the Overall Satisfaction score, you must consider all previous dimension ratings (Localization, Instruction Following, Truthfulness, Response Length, Structure/Writing/Tone, and Harmlessness).
            """
        }
        
        return criteria.get(dimension, "No hay criterios específicos disponibles para esta dimensión.")
    
    def _compare_responses(self, prompt_data: Dict, response_a: str, response_b: str, 
                         eval_a: Dict, eval_b: Dict) -> Dict:
        """
        Compare two responses and provide a preference ranking with justification
        
        Args:
            prompt_data: Dictionary containing prompt and reference text
            response_a: First response to compare
            response_b: Second response to compare
            eval_a: Evaluation results for response A
            eval_b: Evaluation results for response B
            
        Returns:
            Dictionary with preference ranking and justification
        """
        prompt = prompt_data.get("prompt", "")
        prompt_type = prompt_data.get("prompt_type", "Unknown")
        prompt_topic = prompt_data.get("topic", "Unknown")
        reference_text = prompt_data.get("reference_text", "")
        
        # Check for uppercase headings in both responses
        has_uppercase_headings_a, uppercase_examples_a = self._check_for_uppercase_headings(response_a)
        has_uppercase_headings_b, uppercase_examples_b = self._check_for_uppercase_headings(response_b)
        
        # Create system message for comparison
        system_message = """
        You are a highly critical expert evaluator for AI model responses. Your task is to compare two responses 
        to the same question and determine which is better.

        You have been provided with detailed evaluations for both responses across these dimensions:
        1. Localization - How well the response is adapted for the target locale
        2. Instruction Following - How well the response follows the instructions in the question
        3. Truthfulness - How factually accurate the response is
        4. Response Length - How appropriate the length and conciseness is
        5. Structure, writing style, and tone - How well structured and well written the response is
        6. Harmlessness - Whether the response avoids harmful content
        7. Overall Satisfaction - How satisfactory the response would be for users

        Be extremely critical and rigorous. When you find grammatical, structural, or formatting errors (like all-caps
        headings), you must point them out explicitly and consider them as serious issues.

        Analyze these evaluations and the responses themselves to determine your preference.
        Your preference must be expressed on this scale:
        
        1. Response A is much better than Response B
        2. Response A is better than Response B
        3. Response A is slightly better than Response B
        4. No preference, but I chose Response A because [reason]
        5. No preference, but I chose Response B because [reason]
        6. Response B is slightly better than Response A
        7. Response B is better than Response A
        8. Response B is much better than Response A
        
        IMPORTANT GUIDELINES:
        - BE VERY CRITICAL! Even small errors should be weighted heavily in your evaluation.
        - Reserve "much better" ratings (1 or 8) for cases where one response has no key issues while the other has major issues
        - Use "better" (2 or 7) and "slightly better" (3 or 6) when there are less dramatic differences
        - "No preference" (4 or 5) should be used rarely, only when responses are truly equal in quality
        - USE "slightly better" and "better" MORE FREQUENTLY than "much better"
        - Prioritize dimensions in this order: Truthfulness > Instruction Following > Localization > Others

        CREATE YOUR JUSTIFICATION IN ENGLISH, even if the responses are in another language.
        Create a brief justification (maximum 2-4 sentences) that INCLUDES YOUR PREFERENCE STATEMENT and explains
        clearly why you prefer one response over the other. Focus on the most important differences between the responses.
        
        For example, your justification should start with phrases like:
        - "Response A is slightly better than Response B because..."
        - "Response B is better than Response A because..."
        """
        
        # Create user message for comparison
        user_message = f"""
        Please compare these two responses to the same question and provide your preference ranking.
        
        QUESTION: {prompt}
        QUESTION TYPE: {prompt_type}
        QUESTION TOPIC: {prompt_topic}
        {"REFERENCE TEXT: " + reference_text if reference_text else "NO REFERENCE TEXT PROVIDED"}
        
        RESPONSE A: {response_a}
        
        RESPONSE B: {response_b}
        
        EVALUATION OF RESPONSE A:
        {json.dumps(eval_a, indent=2)}
        
        EVALUATION OF RESPONSE B:
        {json.dumps(eval_b, indent=2)}
        
        {"IMPORTANT NOTE: Response A contains headings/subtitles completely in UPPERCASE, which is considered a grammatical and structural error." if has_uppercase_headings_a else ""}
        {"IMPORTANT NOTE: Response B contains headings/subtitles completely in UPPERCASE, which is considered a grammatical and structural error." if has_uppercase_headings_b else ""}
        
        FORMAT YOUR RESPONSE AS A VALID JSON OBJECT WITH THESE FIELDS:
        {{
            "preference": "Choose a value from 1-8 based on the preference scale",
            "preference_label": "The corresponding label from the preference scale",
            "justification": "Your brief justification (maximum 2-4 sentences) IN ENGLISH that INCLUDES your preference statement"
        }}
        """
        
        try:
            # Call API for comparison
            comparison_response = self.client.chat.completions.create(
                model=self.model,
                response_format={"type": "json_object"},
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": user_message}
                ],

            )
            
            # Parse comparison result
            comparison_result = json.loads(comparison_response.choices[0].message.content)
            
            # Ensure valid preference value
            preference = int(comparison_result.get("preference", 4))
            if preference < 1 or preference > 8:
                preference = 4  # Default to no preference if invalid
            
            # Get preference label and justification
            preference_label = comparison_result.get("preference_label", "")
            justification = comparison_result.get("justification", "")
            
            # Add note about uppercase headings if detected
            if has_uppercase_headings_a and has_uppercase_headings_b:
                if "uppercase" not in justification.lower():
                    justification = f"{justification} Both responses contain uppercase headings, which is a grammatical and structural error."
            elif has_uppercase_headings_a:
                if "uppercase" not in justification.lower():
                    justification = f"{justification} Response A contains uppercase headings, which is a grammatical and structural error."
            elif has_uppercase_headings_b:
                if "uppercase" not in justification.lower():
                    justification = f"{justification} Response B contains uppercase headings, which is a grammatical and structural error."
            
            return {
                "preference": preference,
                "preference_label": preference_label,
                "justification": justification
            }
            
        except Exception as e:
            print(f"Error comparing responses: {e}")
            return {
                "preference": 4,  # Default to no preference
                "preference_label": "No preference (due to evaluation error)",
                "justification": f"Error during comparison: {str(e)}"
            }
    
    def evaluate(self, prompt_data: Dict, response_a: str, response_b: str) -> Dict:
        """
        Main function to evaluate and compare two responses
        
        Args:
            prompt_data: Dictionary containing prompt and reference_text if applicable
            response_a: First response to evaluate
            response_b: Second response to evaluate
            
        Returns:
            Dictionary with evaluations for each response and comparison
        """
        print("Evaluando Respuesta A...")
        eval_a = self._evaluate_response(prompt_data, response_a, "A")
        
        print("Evaluando Respuesta B...")
        eval_b = self._evaluate_response(prompt_data, response_b, "B")
        
        print("Comparando respuestas...")
        comparison = self._compare_responses(prompt_data, response_a, response_b, eval_a, eval_b)
        
        return {
            "prompt": prompt_data,
            "evaluation_a": eval_a,
            "evaluation_b": eval_b,
            "comparison": comparison
        }

def main():
    """Main function to run the response evaluator from command line"""
    parser = argparse.ArgumentParser(description='Evaluate and compare AI model responses')
    parser.add_argument('--api-key', type=str, help='OpenAI API key')
    parser.add_argument('--model', type=str, default='o3-mini',
                      help='OpenAI model to use (default: gpt-4-turbo)')
    parser.add_argument('--prompt-file', type=str, required=True,
                      help='JSON file containing the prompt and reference text')
    parser.add_argument('--response-a', type=str, required=True,
                      help='First response to evaluate')
    parser.add_argument('--response-b', type=str, required=True,
                      help='Second response to evaluate')
    parser.add_argument('--output', type=str, help='Output file path for the evaluation results')
    args = parser.parse_args()
    
    try:
        # Load prompt data
        with open(args.prompt_file, 'r', encoding='utf-8') as f:
            prompt_data = json.load(f)
        
        # Load responses
        with open(args.response_a, 'r', encoding='utf-8') as f:
            response_a = f.read()
        
        with open(args.response_b, 'r', encoding='utf-8') as f:
            response_b = f.read()
        
        # Initialize evaluator
        evaluator = ResponseEvaluator(api_key=args.api_key, model=args.model)
        
        # Evaluate responses
        results = evaluator.evaluate(prompt_data, response_a, response_b)
        
        # Print results
        print(json.dumps(results, indent=2, ensure_ascii=False))
        
        # Save to file if specified
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
            print(f"Evaluation results saved to {args.output}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()