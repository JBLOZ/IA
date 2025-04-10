import os
import json
import argparse
from typing import Dict, Any, Optional, List, Union
from datetime import datetime
from promptGenerator import PromptGenerator
from responseEvaluator import ResponseEvaluator

#####################################################################
#                 CONFIGURACIÓN FÁCIL DEL SERVICIO                   #
#####################################################################

# Tu clave de API de OpenAI (si está vacía, se buscará en variables de entorno)
API_KEY = "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"

# Modo del servicio: "generate" para generar prompts o "evaluate" para evaluar respuestas
SERVICE_MODE = "evaluate"  # Opciones: "generate" o "evaluate"

# ------ Configuración para modo "generate" ------
# Categoría del prompt a generar (dejar en blanco para aleatorio)
PROMPT_CATEGORY = "Open QA"  # Opciones: "Rewrite", "Classification", "Summarization", "Extraction", 
                             # "Closed QA", "Brainstorming", "Chatbot", "Creative Writing", "Open QA"

# Tema del prompt (dejar en blanco para aleatorio)
PROMPT_TOPIC = ""  # Opciones: "Business & Management", "Computer Science & Technology",
                                        # "Education", "Fitness/Sports", "Health/Medical", "Life Sciences & Biology",
                                        # "Physics Sciences & Engineering", "Social Sciences & Law", 
                                        # "Travel & Transportation", "Mathematics", "Other"

# ------ Configuración para modo "evaluate" ------
# Ruta al archivo JSON con el prompt generado (sólo para modo "evaluate")
PROMPT_FILE = "results\open_qa_education_20250410_132634.json"

# Respuesta A a evaluar (texto completo)
RESPONSE_A = """
La enseñanza de la lengua española en las escuelas ha evolucionado notablemente en las últimas décadas, adaptándose a nuevos enfoques pedagógicos y a las necesidades de los estudiantes. A continuación, te presento algunos cambios clave en metodologías y sus efectos en la percepción del idioma entre los jóvenes:

1. **Enfoque comunicativo**: A partir de los años 80 y 90, se comenzó a privilegiar un enfoque más comunicativo, en lugar de la enseñanza centrada en la gramática. Esto significa que se busca que los estudiantes utilicen el español en contextos auténticos y cotidianos, lo que mejora su fluidez y confianza al hablar.

2. **Aprendizaje basado en proyectos**: Esta metodología permite a los alumnos trabajar en proyectos que integre el uso del idioma en distintas áreas, fomentando un aprendizaje más significativo y contextual. Por ejemplo, pueden investigar sobre la cultura hispana, realizar presentaciones o crear contenidos multimedia en español.

3. **Tecnología educativa**: La incorporación de herramientas digitales y recursos en línea ha cambiado la forma en que los estudiantes interactúan con la lengua. Plataformas de aprendizaje, aplicaciones de idiomas y foros en línea les ofrecen oportunidades de practicar el español de manera interactiva y colaborativa.

4. **Diversidad e inclusión**: Se ha hecho un esfuerzo por incluir una variedad de dialectos y variantes del español en el currículo, reconociendo que es una lengua diversa y rica. Esto no solo beneficia a estudiantes de diferentes orígenes, sino que también enriquece la experiencia de aprendizaje.

5. **Fomento de la creatividad**: Se alienta a los estudiantes a utilizar su creatividad, por ejemplo, a través de la escritura de relatos, poesía o la creación de videos. Esto no solo mejora su habilidad lingüística, sino también su interés y conexión emocional con el idioma.

En cuanto a la percepción del español entre los jóvenes, estos cambios han tendido a generar una relación más positiva y activa con la lengua. Muchos estudiantes sienten que el español no solo es una materia escolar, sino una herramienta valiosa para la comunicación y la identidad cultural. Además, el acceso a contenidos en español a través de redes sociales, música y cine ha fortalecido su interés y motivación por aprender.

Sin embargo, es importante considerar que todavía existen retos, como la falta de recursos en algunas instituciones y la necesidad de formación continua para los docentes en nuevas metodologías. En resumen, la enseñanza del español ha avanzado para ser más dinámica y relevante, afectando la manera en que los jóvenes perciben y utilizan la lengua en su vida diaria.
"""

# Respuesta B a evaluar (texto completo)
RESPONSE_B = """
La enseñanza de la lengua española en las escuelas ha experimentado una serie de cambios significativos a lo largo de las últimas décadas, adaptándose a las necesidades cambiantes de la sociedad y a los avances en la investigación lingüística y educativa. Aquí te explico algunos de los cambios más destacados en las metodologías y su impacto en la percepción del idioma entre los jóvenes:

1. **Enfoque comunicativo**: Anteriormente, la enseñanza del español se centraba mucho en la gramática y la literatura, a menudo de manera descontextualizada. Hoy, sin embargo, las metodologías se inclinan más hacia un enfoque comunicativo, donde se da prioridad a la habilidad de comunicarse eficazmente en situaciones reales. Esto incluye actividades de conversación, debates y proyectos que fomentan el uso práctico del idioma.

2. **Diversificación de materiales**: Actualmente, se utilizan una variedad mucho más amplia de materiales didácticos, incluidos recursos multimedia como videos, música, podcasts y juegos interactivos. Estos recursos no solo hacen la clase más dinámica, sino que también ayudan a los estudiantes a percibir el idioma como relevante y útil en contextos modernos.

3. **Aprendizaje basado en tareas**: Esta metodología se centra en que los estudiantes adquieran el idioma al realizar tareas significativas que reflejen situaciones de la vida real. Este enfoque busca mejorar la fluidez y la competencia comunicativa de los alumnos, haciéndoles ver el idioma como una herramienta valiosa para lograr objetivos específicos.

4. **Educación bilingüe y plurilingüismo**: En algunas regiones, la enseñanza del español se imparte junto con otras lenguas, promoviendo el plurilingüismo. Esta tendencia ayuda a los estudiantes a valorar el español como parte de su identidad cultural y lingüística, pero también los prepara para interactuar en un mundo globalizado.

5. **Fomento de la creatividad y la crítica**: Las clases de español hoy en día suelen integrar actividades que fomentan la creatividad, como la escritura de blogs, guiones o producción de medios. Además, se promueve el análisis crítico de textos, lo cual ayuda a desarrollar una percepción más profunda y crítica del idioma y su uso.

6. **Uso de tecnologías digitales**: Las plataformas digitales y las aplicaciones de aprendizaje de idiomas han transformado la enseñanza del español al ofrecer herramientas personalizadas y accesibles para el aprendizaje fuera del aula. Estas tecnologías permiten a los estudiantes interactuar con el idioma de formas innovadoras, lo que puede aumentar su motivación y cambiar su percepción, haciéndoles ver el español como un idioma moderno y accesible.

En conjunto, estas metodologías han ayudado a transformar la manera en que los jóvenes perciben el idioma español, haciéndolo más relevante, accesible y útil para sus vidas cotidianas. Además, estos cambios han contribuido a generar un entorno de aprendizaje más inclusivo y participativo, donde los estudiantes se sienten más motivados y comprometidos.
"""

# Directorio donde se guardarán los resultados
OUTPUT_DIR = "results"

#####################################################################
#                   FIN DE LA CONFIGURACIÓN                          #
#####################################################################

class CypherRLHFService:
    """
    Servicio unificado para la generación de prompts y evaluación de respuestas de modelos AI
    siguiendo los criterios del proyecto RLHF de Cypher.
    """

    def __init__(self, api_key: str = None, 
                 generator_model: str = "gpt-4o-mini", 
                 evaluator_model: str = "o3-mini",
                 output_dir: str = "results"):
        """
        Inicializa el servicio con los parámetros necesarios.
        
        Args:
            api_key: Clave de API para OpenAI (puede estar como variable de entorno)
            generator_model: Modelo de OpenAI para generar prompts
            evaluator_model: Modelo de OpenAI para evaluar respuestas
            output_dir: Directorio donde se guardarán los resultados
        """
        # Primero intentamos obtener la clave API del parámetro
        self.api_key = api_key 
        
        # Si no se proporcionó, intentamos obtenerla de la variable de entorno
        if not self.api_key:
            self.api_key = os.environ.get("OPENAI_API_KEY")
            
        # Si aún no tenemos una clave API, lanzamos una excepción
        if not self.api_key:
            raise ValueError("Se requiere una clave API de OpenAI. Configure la variable de entorno OPENAI_API_KEY o pásela como parámetro.")
        
        self.generator_model = generator_model
        self.evaluator_model = evaluator_model
        self.output_dir = output_dir
        
        # Crear el directorio de salida si no existe
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Inicializar los servicios individuales
        self.prompt_generator = PromptGenerator(api_key=self.api_key, model=self.generator_model)
        self.response_evaluator = ResponseEvaluator(api_key=self.api_key, model=self.evaluator_model)
        
        # Lista de categorías de prompts disponibles
        self.prompt_categories = list(self.prompt_generator.prompt_categories.keys())
        
        # Lista de categorías temáticas disponibles
        self.topic_categories = self.prompt_generator.topic_categories
    
    def generate_prompt(self, category: str = None, topic: str = None) -> Dict:
        """
        Genera un prompt de una categoría y tema específicos o aleatorios.
        
        Args:
            category: Categoría del prompt a generar (opcional)
            topic: Tema del prompt a generar (opcional)
            
        Returns:
            Un diccionario con los detalles del prompt generado
        """
        if category and category not in self.prompt_categories:
            categories_str = ", ".join(self.prompt_categories)
            raise ValueError(f"Categoría '{category}' no válida. Categorías disponibles: {categories_str}")
        
        if topic and topic not in self.topic_categories:
            topics_str = ", ".join(self.topic_categories)
            raise ValueError(f"Tema '{topic}' no válida. Temas disponibles: {topics_str}")
        
        # Generar el prompt
        generated_prompt = self.prompt_generator.generate_prompt(category=category, topic=topic)
        
        # Guardar el prompt generado
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        prompt_type = generated_prompt.get("prompt_type", "unknown").replace(" ", "_").lower()
        topic_name = generated_prompt.get("topic", "unknown").replace(" ", "_").replace("&", "and").lower()
        filename = f"{prompt_type}_{topic_name}_{timestamp}.json"
        filepath = os.path.join(self.output_dir, filename)
        
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(generated_prompt, f, ensure_ascii=False, indent=2)
        
        print(f"✅ Prompt generado y guardado en: {filepath}")
        return {
            "prompt_data": generated_prompt,
            "filepath": filepath
        }
    
    def evaluate_responses(self, prompt_data: Dict = None, 
                         prompt_file: str = None,
                         response_a: str = None, 
                         response_b: str = None,
                         response_a_file: str = None,
                         response_b_file: str = None) -> Dict:
        """
        Evalúa dos respuestas a un mismo prompt.
        
        Args:
            prompt_data: Diccionario con los datos del prompt (opcional)
            prompt_file: Ruta al archivo JSON del prompt (opcional)
            response_a: Texto de la primera respuesta (opcional)
            response_b: Texto de la segunda respuesta (opcional)
            response_a_file: Ruta al archivo con la primera respuesta (opcional)
            response_b_file: Ruta al archivo con la segunda respuesta (opcional)
            
        Returns:
            Un diccionario con los resultados de la evaluación
        """
        # Verificar que tengamos un prompt, ya sea como datos o como archivo
        if not prompt_data and not prompt_file:
            raise ValueError("Se requiere o bien prompt_data o prompt_file")
        
        # Si se proporciona un archivo de prompt, cargarlo
        if prompt_file and not prompt_data:
            with open(prompt_file, "r", encoding="utf-8") as f:
                prompt_data = json.load(f)
        
        # Verificar que tengamos ambas respuestas, ya sea como texto o como archivos
        if not response_a and not response_a_file:
            raise ValueError("Se requiere o bien response_a o response_a_file")
        if not response_b and not response_b_file:
            raise ValueError("Se requiere o bien response_b o response_b_file")
        
        # Si se proporcionan archivos de respuesta, cargarlos
        if response_a_file and not response_a:
            with open(response_a_file, "r", encoding="utf-8") as f:
                response_a = f.read()
        if response_b_file and not response_b:
            with open(response_b_file, "r", encoding="utf-8") as f:
                response_b = f.read()
        
        # Evaluar las respuestas
        evaluation_results = self.response_evaluator.evaluate(prompt_data, response_a, response_b)
        
        # Guardar los resultados
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        prompt_type = prompt_data.get("prompt_type", "unknown").replace(" ", "_").lower()
        topic_name = prompt_data.get("topic", "unknown").replace(" ", "_").replace("&", "and").lower()
        filename = f"eval_{prompt_type}_{topic_name}_{timestamp}.json"
        filepath = os.path.join(self.output_dir, filename)
        
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(evaluation_results, f, ensure_ascii=False, indent=2)
        
        print(f"✅ Evaluación completada y guardada en: {filepath}")
        return {
            "evaluation_results": evaluation_results,
            "filepath": filepath
        }
    
    def run_complete_workflow(self, category: str = None, topic: str = None, model_a: str = None, model_b: str = None) -> Dict:
        """
        Ejecuta el flujo completo: genera un prompt, obtiene respuestas de uno o dos modelos y las evalúa.
        Esta funcionalidad está pensada para implementarse más adelante, cuando tengas acceso
        a los modelos para generar respuestas.
        
        Args:
            category: Categoría del prompt a generar
            topic: Tema del prompt a generar
            model_a: Identificador del primer modelo para generar respuestas
            model_b: Identificador del segundo modelo para generar respuestas
            
        Returns:
            Un diccionario con los resultados del flujo completo
        """
        # Esta es una función de placeholder para el flujo completo
        # que podrías implementar más adelante
        raise NotImplementedError("Esta funcionalidad será implementada próximamente")

def main():
    """Función principal para ejecutar el servicio desde la línea de comandos"""
    # Si se proporcionan argumentos por línea de comandos, se usa el parser
    if len(os.sys.argv) > 1:
        parser = argparse.ArgumentParser(description='Servicio integrado de RLHF para Cypher')
        parser.add_argument('--api-key', type=str, help='Clave de API de OpenAI')
        parser.add_argument('--mode', choices=['generate', 'evaluate'], required=True,
                          help='Modo de operación: generar prompts o evaluar respuestas')
        parser.add_argument('--category', type=str, help='Categoría del prompt a generar (solo para modo "generate")')
        parser.add_argument('--topic', type=str, help='Tema del prompt a generar (solo para modo "generate")')
        parser.add_argument('--prompt-file', type=str, 
                          help='Archivo JSON con el prompt (solo para modo "evaluate")')
        parser.add_argument('--response-a', type=str,
                          help='Ruta al archivo con la primera respuesta (solo para modo "evaluate")')
        parser.add_argument('--response-b', type=str,
                          help='Ruta al archivo con la segunda respuesta (solo para modo "evaluate")')
        parser.add_argument('--output-dir', type=str, default='results',
                          help='Directorio donde se guardarán los resultados')
        parser.add_argument('--list-categories', action='store_true',
                          help='Mostrar las categorías de prompts disponibles')
        parser.add_argument('--list-topics', action='store_true',
                          help='Mostrar los temas de prompts disponibles')
        
        args = parser.parse_args()
        
        try:
            # Inicializar el servicio
            service = CypherRLHFService(
                api_key=args.api_key,
                output_dir=args.output_dir
            )
            
            # Mostrar listas si se solicita
            if args.list_categories:
                print("Categorías de prompts disponibles:")
                for category in service.prompt_categories:
                    print(f"- {category}")
                return
                
            if args.list_topics:
                print("Temas de prompts disponibles:")
                for topic in service.topic_categories:
                    print(f"- {topic}")
                return
            
            # Ejecutar el modo seleccionado
            if args.mode == 'generate':
                result = service.generate_prompt(category=args.category, topic=args.topic)
                print(f"Prompt generado:\n{json.dumps(result['prompt_data'], ensure_ascii=False, indent=2)}")
                
            elif args.mode == 'evaluate':
                if not args.prompt_file:
                    raise ValueError("Se requiere --prompt-file en modo 'evaluate'")
                if not args.response_a:
                    raise ValueError("Se requiere --response-a en modo 'evaluate'")
                if not args.response_b:
                    raise ValueError("Se requiere --response-b en modo 'evaluate'")
                    
                result = service.evaluate_responses(
                    prompt_file=args.prompt_file,
                    response_a_file=args.response_a,
                    response_b_file=args.response_b
                )
                
                print(f"Preferencia: {result['evaluation_results']['comparison']['preference_label']}")
                print(f"Justificación: {result['evaluation_results']['comparison']['justification']}")
                
        except Exception as e:
            print(f"Error: {e}")
    
    # Si no hay argumentos, se usan las variables globales definidas al inicio del archivo
    else:
        try:
            # Inicializar el servicio con la configuración global
            service = CypherRLHFService(
                api_key=API_KEY,
                output_dir=OUTPUT_DIR
            )
            
            # Ejecutar el modo seleccionado según la configuración global
            if SERVICE_MODE == 'generate':
                print(f"🚀 Generando prompt de categoría '{PROMPT_CATEGORY}' y tema '{PROMPT_TOPIC}'...")
                result = service.generate_prompt(category=PROMPT_CATEGORY, topic=PROMPT_TOPIC)
                print(f"Prompt generado:\n{json.dumps(result['prompt_data'], ensure_ascii=False, indent=2)}")
                
            elif SERVICE_MODE == 'evaluate':
                if not PROMPT_FILE:
                    raise ValueError("Se requiere definir PROMPT_FILE en la configuración para el modo 'evaluate'")
                if not RESPONSE_A:
                    raise ValueError("Se requiere definir RESPONSE_A en la configuración para el modo 'evaluate'")
                if not RESPONSE_B:
                    raise ValueError("Se requiere definir RESPONSE_B en la configuración para el modo 'evaluate'")
                
                print(f"🔍 Evaluando respuestas para el prompt en '{PROMPT_FILE}'...")
                
                # Crear archivos temporales para las respuestas
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                response_a_file = f"{OUTPUT_DIR}/temp_response_a_{timestamp}.txt"
                response_b_file = f"{OUTPUT_DIR}/temp_response_b_{timestamp}.txt"
                
                # Guardar las respuestas en archivos temporales
                with open(response_a_file, "w", encoding="utf-8") as f:
                    f.write(RESPONSE_A)
                
                with open(response_b_file, "w", encoding="utf-8") as f:
                    f.write(RESPONSE_B)
                
                # Evaluar las respuestas
                result = service.evaluate_responses(
                    prompt_file=PROMPT_FILE,
                    response_a=RESPONSE_A,
                    response_b=RESPONSE_B
                )
                
                print(f"\n✅ Evaluación completada")
                print(f"Preferencia: {result['evaluation_results']['comparison']['preference_label']}")
                print(f"Justificación: {result['evaluation_results']['comparison']['justification']}")
                
                # Mostrar un resumen de las evaluaciones individuales
                print("\n📊 Resumen de Evaluación de Respuesta A:")
                for dim, data in result['evaluation_results']['evaluation_a'].items():
                    rating = data['rating']
                    justification = data['justification'] if data['justification'] else "Sin problemas"
                    print(f"  - {dim}: {rating}/{'3' if dim not in ['response_length', 'overall_satisfaction'] else '5'} - {justification}")
                    
                print("\n📊 Resumen de Evaluación de Respuesta B:")
                for dim, data in result['evaluation_results']['evaluation_b'].items():
                    rating = data['rating']
                    justification = data['justification'] if data['justification'] else "Sin problemas"
                    print(f"  - {dim}: {rating}/{'3' if dim not in ['response_length', 'overall_satisfaction'] else '5'} - {justification}")
                
                # Limpiar los archivos temporales
                try:
                    os.remove(response_a_file)
                    os.remove(response_b_file)
                except:
                    pass
                
            else:
                raise ValueError(f"Modo de servicio no válido: {SERVICE_MODE}. Debe ser 'generate' o 'evaluate'")
                
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()