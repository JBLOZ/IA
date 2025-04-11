import os
import json
import random
import argparse
from openai import OpenAI
from typing import Dict, List, Optional, Tuple, Union

class PromptGenerator:
    """
    A class that generates prompts based on specified categories
    with Spanish localization for RLHF evaluation.
    """

    def __init__(self, api_key: str = None, model: str = "gpt-4o-mini"):
        """
        Initialize the PromptGenerator with API key and model name.
        
        Args:
            api_key: OpenAI API key (can be set via environment variable)
            model: The OpenAI model to use for generating prompts
        """
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key is required. Set it via environment variable OPENAI_API_KEY or pass it as a parameter.")
        
        self.client = OpenAI(api_key=self.api_key)
        self.model = model
        
        # Define prompt categories and whether they need reference text
        self.prompt_categories = {
            "Rewrite": {"needs_reference": True},
            "Classification": {"needs_reference": True},
            "Summarization": {"needs_reference": True},
            "Extraction": {"needs_reference": True},
            "Closed QA": {"needs_reference": True},
            "Brainstorming": {"needs_reference": False},
            "Chatbot": {"needs_reference": False},
            "Creative Writing": {"needs_reference": False},
            "Open QA": {"needs_reference": False}
        }
        
        # Define topic categories
        self.topic_categories = [
            "Business & Management",
            "Computer Science & Technology",
            "Education",
            "Fitness/Sports",
            "Health/Medical",
            "Life Sciences & Biology",
            "Physics Sciences & Engineering",
            "Social Sciences & Law",
            "Travel & Transportation",
            "Mathematics",
            "Other"
        ]
        
        # Keep track of used categories to ensure alternation
        self.last_category = None
        self.last_topic = None
    
    def _select_prompt_category(self, specific_category: str = None) -> str:
        """
        Select a prompt category, alternating between different types.
        
        Args:
            specific_category: If provided, use this specific category
            
        Returns:
            A prompt category name
        """
        if specific_category and specific_category in self.prompt_categories:
            self.last_category = specific_category
            return specific_category
            
        # Get categories different from last used
        available_categories = [cat for cat in self.prompt_categories.keys() 
                               if cat != self.last_category]
        
        # If no last category or no available categories, use all
        if not available_categories:
            available_categories = list(self.prompt_categories.keys())
            
        # Select random category from available ones
        selected_category = random.choice(available_categories)
        self.last_category = selected_category
        return selected_category
    
    def _select_topic_category(self, specific_topic: str = None) -> str:
        """
        Select a topic category, alternating between different types.
        
        Args:
            specific_topic: If provided, use this specific topic
            
        Returns:
            A topic category name
        """
        if specific_topic and specific_topic in self.topic_categories:
            self.last_topic = specific_topic
            return specific_topic
            
        # Get topics different from last used
        available_topics = [topic for topic in self.topic_categories 
                           if topic != self.last_topic]
        
        # If no last topic or no available topics, use all
        if not available_topics:
            available_topics = self.topic_categories
            
        # Select random topic from available ones
        selected_topic = random.choice(available_topics)
        self.last_topic = selected_topic
        return selected_topic
    
    def generate_prompt(self, category: str = None, topic: str = None) -> Dict:
        """
        Generate a localized prompt for Spain based on a specified or random category and topic.
        
        Args:
            category: Optional specific category to use
            topic: Optional specific topic to use
            
        Returns:
            A dictionary with prompt details
        """
        selected_category = self._select_prompt_category(category)
        selected_topic = self._select_topic_category(topic)
        needs_reference = self.prompt_categories[selected_category]["needs_reference"]
        
        # Create system message with specific instructions for Spanish localization
        system_message = """
        Eres un generador de prompts para modelos de IA. Tu tarea es crear prompts de alta calidad
        que estén claramente localizados para España. Es imprescindible que los prompts parezcan 
        haber sido escritos por una persona española.

        Para lograr una localización auténtica española, asegúrate de que el prompt incluya:

        1. Referencias a lugares específicos de España: ciudades, regiones, monumentos, calles, barrios.
           Ejemplos: "Estudio en la Universidad de Valencia", "Trabajo cerca de la Plaza de España en Madrid", 
           "Vivo en un pueblo de la Costa Brava", "Necesito ir desde Atocha hasta Nuevos Ministerios".

        2. Instituciones, organizaciones o servicios españoles:
           Ejemplos: "Tengo que renovar mi DNI", "Quiero darme de alta en la Seguridad Social", 
           "¿Cómo funciona el sistema de cita previa en el SEPE?", "¿Qué documentos necesito para la declaración de la Renta?"

        3. Expresiones, modismos o jerga española:
           Ejemplos: "Me ha costado un pastón", "Eso es la leche", "Vamos a tomar unas cañas", "Estoy agobiado con los exámenes"

        4. Referencias a productos, marcas o servicios populares en España:
           Ejemplos: "¿Cómo puedo reclamar a Movistar?", "¿Qué supermercado es más barato, Mercadona o Carrefour?"
           "¿Cómo llego a El Corte Inglés desde aquí?", "¿Cuál es el mejor plan de datos de Vodafone?"

        5. Festividades, tradiciones o costumbres españolas:
           Ejemplos: "¿Qué hacer durante las Fallas?", "Busco recetas tradicionales de torrijas para Semana Santa",
           "¿Dónde puedo ver la mejor Cabalgata de Reyes en Barcelona?"

        6. Sistema educativo español:
           Ejemplos: "¿Cómo funciona la selectividad?", "¿Qué nota necesito para entrar en Medicina?", 
           "Estoy preparándome las oposiciones para profesor"

        Tu prompt debe evitar:
        - Parecer que lo ha escrito un turista o alguien no familiarizado con España
        - Usar referencias culturales que no sean comunes en España
        - Utilizar terminología o conceptos que no se usan en España (como "colegiatura" en lugar de "matrícula")
        - Utilizar expresiones latinoamericanas que no sean comunes en España

        Crea un prompt para la categoría: {category}
        
        El tema del prompt debe ser: {topic}
        
        {reference_requirement}
        
        INSTRUCCIÓN ESPECIAL PARA PROMPTS OPEN QA:
        Si estás creando un prompt de tipo "Open QA", debes hacer preguntas más abiertas y conceptuales 
        que permitan respuestas diversas y diferentes interpretaciones. En lugar de preguntar por información 
        específica y concreta (como requisitos para un trámite o pasos para hacer algo), haz preguntas sobre:
        
        - Fenómenos sociales o culturales en España ("¿Cómo ha cambiado la gastronomía española en las últimas décadas?")
        - Análisis comparativos ("¿Qué diferencias hay entre el sistema educativo español y el británico?")
        - Impactos y tendencias ("¿Qué impacto tiene el turismo de masas en las ciudades costeras españolas?") 
        - Evolución histórica de algo ("¿Cómo ha evolucionado la arquitectura en Barcelona desde la época de Gaudí?")
        - Reflexiones sobre identidad cultural ("¿Qué elementos definen la identidad cultural catalana en el contexto español?")
        
        Estos prompts abiertos generan respuestas más diversas y permiten evaluar mejor las capacidades del modelo.
        
        No crees prompts que requieran conocimiento posterior al 30 de abril de 2024.
        Crea prompts que producirán respuestas claramente diferentes entre modelos.
        El prompt NO debe incluir restricciones o requisitos de formato arbitrarios.

        Devuelve SOLO un objeto JSON con los siguientes campos:
        - "prompt": El texto del prompt generado en español
        - "prompt_type": "{category}"
        - "topic": "{topic}"
        {reference_field}
        """
        
        reference_requirement = ""
        reference_field = ""
        
        if needs_reference:
            reference_requirement = "Incluye un texto de referencia entre 200-400 palabras de una fuente creíble que sea relevante para el prompt. Este texto de referencia DEBE estar localizado para España."
            reference_field = '- "reference_text": Un texto de referencia creíble en español entre 200-400 palabras'
        else:
            reference_requirement = "Esta categoría de prompt no requiere un texto de referencia."
            reference_field = ""
            
        formatted_system = system_message.format(
            category=selected_category,
            topic=selected_topic,
            reference_requirement=reference_requirement,
            reference_field=reference_field
        )
        
        # Examples of Spanish localization for each category type
        examples_by_category = {
            "Rewrite": "Por ejemplo: 'Reescribe este texto sobre la historia del Acueducto de Segovia para que lo entienda mi hijo de 10 años, que estamos planeando visitarlo este fin de semana.'",
            "Classification": "Por ejemplo: 'Clasifica los siguientes platos según su región de origen en España: paella valenciana, gazpacho andaluz, pulpo a feira, pintxos vascos, cocido madrileño y calçots catalanes.'",
            "Summarization": "Por ejemplo: 'Resume en 3 párrafos esta noticia sobre la última etapa de la Vuelta Ciclista a España que pasó por mi ciudad, Cuenca.'",
            "Extraction": "Por ejemplo: 'Extrae todas las fechas importantes y eventos del siguiente texto sobre la historia de la democracia española desde la Transición hasta nuestros días.'",
            "Closed QA": "Por ejemplo: 'Según el siguiente texto, ¿cuáles son los requisitos para solicitar el bono social térmico en mi comunidad autónoma, Andalucía?'",
            "Brainstorming": "Por ejemplo: 'Dame 5 ideas para organizar una fiesta temática para celebrar San Juan en la playa de Alicante con mis compañeros de la oficina.'",
            "Chatbot": "Por ejemplo: 'Actúa como un funcionario del ayuntamiento de Sevilla y responde a mis preguntas sobre cómo tramitar el empadronamiento en mi nuevo piso de Triana.'",
            "Creative Writing": "Por ejemplo: 'Escribe un relato corto ambientado en mi pueblo natal en la Sierra de Gredos durante las fiestas patronales.'",
            "Open QA": "Por ejemplo: '¿Cómo ha influido la cultura árabe en la gastronomía y arquitectura del sur de España? Me interesa especialmente entender qué elementos se mantienen vigentes en la actualidad.'"
        }
        
        # Add category-specific examples
        user_message = f"Crea un prompt de {selected_category} sobre el tema '{selected_topic}' que esté claramente localizado para España y que parezca escrito por un español. {examples_by_category.get(selected_category, '')}"
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                response_format={"type": "json_object"},
                messages=[
                    {"role": "system", "content": formatted_system},
                    {"role": "user", "content": user_message}
                ],
                temperature=0.8
            )
            
            result = json.loads(response.choices[0].message.content)
            
            # Ensure the result has the required fields
            if "prompt" not in result or "prompt_type" not in result:
                raise ValueError("Generated result missing required fields")
                
            # Add reference_text field if needed but missing
            if needs_reference and "reference_text" not in result:
                # Generate a reference text
                reference_text = self._generate_reference_text(result["prompt"])
                result["reference_text"] = reference_text
            
            # Ensure topic field exists
            if "topic" not in result:
                result["topic"] = selected_topic
            
            return result
            
        except Exception as e:
            print(f"Error generating prompt: {e}")
            return {
                "error": str(e),
                "prompt_type": selected_category,
                "topic": selected_topic
            }
    
    def _generate_reference_text(self, prompt: str) -> str:
        """
        Generate a reference text for prompts that require one.
        
        Args:
            prompt: The prompt to generate a reference text for
            
        Returns:
            A reference text string
        """
        system_message = """
        Genera un texto de referencia creíble en español para España entre 200-400 palabras que se relacione 
        con el prompt dado. El texto de referencia debe:
        
        1. Ser factualmente preciso y creíble
        2. Estar claramente localizado para España con referencias españolas, ubicaciones o elementos culturales
        3. Tener entre 200-400 palabras
        4. Ser directamente relevante para el prompt
        5. No requerir imágenes o acceso web para entenderse
        6. Evitar usar URLs como fuentes
        
        Incluye elementos específicamente españoles como:
        - Referencias a lugares reales de España
        - Instituciones, organizaciones o servicios españoles
        - Terminología y vocabulario utilizado en España (no latinoamericano)
        - Costumbres, tradiciones o prácticas específicas españolas
        
        Devuelve SOLO el texto de referencia sin comentarios adicionales.
        """
        
        user_message = f"Genera un texto de referencia en español para este prompt: '{prompt}'"
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": user_message}
                ],
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"Error generating reference text: {e}")
            return "Error generando texto de referencia. Por favor, proporciona un texto manualmente."

def main():
    """Main function to run the prompt generator from command line"""
    parser = argparse.ArgumentParser(description='Generate localized prompts for Spain')
    parser.add_argument('--api-key', type=str, help='OpenAI API key')
    parser.add_argument('--model', type=str, default='gpt-4o-mini',
                      help='OpenAI model to use (default: gpt-4o-mini)')
    parser.add_argument('--category', type=str, help='Specific prompt category to generate')
    parser.add_argument('--topic', type=str, help='Specific topic category for the prompt')
    parser.add_argument('--output', type=str, help='Output file path for the generated prompt')
    args = parser.parse_args()
    
    try:
        generator = PromptGenerator(api_key=args.api_key, model=args.model)
        result = generator.generate_prompt(category=args.category, topic=args.topic)
        
        # Print the result
        print(json.dumps(result, indent=2, ensure_ascii=False))
        
        # Save to file if specified
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            print(f"Prompt saved to {args.output}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()