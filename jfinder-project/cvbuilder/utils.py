from cvbuilder.forms import *

class SingletonMeta(type):

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]
            
class CVBuilderEntityFormFactory(metaclass=SingletonMeta):

    _forms = {
        "header": HeaderForm,
        "education": EducationForm,
        "experience": ExperienceForm,
        "soft_skills": SkillForm,
        "hard_skills": SkillForm,
        "projects": ProjectForm,
        "languages": LanguageForm,
        "custom_sections": None,
    }

    def get_form(self, entity_type):
        if entity_type in self._forms:
            return self._forms[entity_type]
        else:
            return None
        
