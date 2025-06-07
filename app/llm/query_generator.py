from langchain_community.chat_models import ChatOllama 
from langchain_core.output_parsers import StrOutputParser
from app.core.config import settings
from . import prompt_templates

class BilingualQueryProcessor:
    def __init__(self):
        self.llm = ChatOllama(
            model="phi",  
            temperature=0 
        )
    
    def generate_sql(self, user_request: str) -> str:
        chain = (
            prompt_templates.request_to_sql_prompt
            | self.llm
            | StrOutputParser()
        )
        return chain.invoke({"user_request": user_request})
    
    def generate_response(self, database_result: str) -> str:
        chain = (
            prompt_templates.sql_to_response_prompt
            | self.llm
            | StrOutputParser()
        )
        return chain.invoke({"database_result": database_result})