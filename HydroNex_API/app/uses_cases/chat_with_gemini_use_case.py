from services.ai_engine.gemini_connect import model
from commons.utils.utils import clean_and_parse_ai_json
from commons.prompt.prompt import Prompt
from adaptater.assessment.assessment_adaptater import AssessmentAdaptater
from adaptater.module_formation.module_formation_adaptater import ModuleFormationAdaptater


class ChatWithGemini:
    @staticmethod
    def get_questionary(theme: str):
        prompt = Prompt.get_questionary_prompt(theme)
        response = model.generate_content(prompt)
        return clean_and_parse_ai_json(response)
    

    @staticmethod
    def evaluate_user_answers(competition_id: int, submitted_answer):
        assessment = AssessmentAdaptater.get_assessment_by_competition_id(competition_id)
        prompt = Prompt.get_user_answers_prompt(assessment.topic, assessment.questionary, submitted_answer)
        response = model.generate_content(prompt)
        return clean_and_parse_ai_json(response)
    

    @staticmethod
    def get_content_module(titre : str, formation_titre: str):
        prompt = Prompt.get_module_prompt(titre, formation_titre)
        response = model.generate_content(prompt)
        return clean_and_parse_ai_json(response)
     
    
    @staticmethod
    def evaluate_user_answers_module(module_id: int, submitted_answer):
        module = ModuleFormationAdaptater.get_module_by_id(module_id)
        prompt = Prompt.get_user_answers_module_prompt(module.titre, module.questionnaire, submitted_answer)
        response = model.generate_content(prompt)
        return clean_and_parse_ai_json(response)
    