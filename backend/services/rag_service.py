import os
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage
class RAGService:
    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY")
        self.llm = None
        
        if self.api_key:
            try:
                self.llm = ChatGroq(
                    groq_api_key=self.api_key,
                    model_name="llama-3.1-8b-instant"
                )
                print("Groq LLM initialized successfully.")
            except Exception as e:
                print(f"Failed to initialize Groq LLM: {e}")

    def chat(self, user_message: str, project_context: str = "") -> str:
        if not self.llm:
            return "Groq LLM is not initialized. Please configure GROQ_API_KEY."

        system_prompt = """You are ContractGraph-RiskNet's AI Contract Expert, an advanced assistant built for Indian Infrastructure Project Monitoring.
You are analyzing THIS specific infrastructure project. 
NEVER ask the user for project details, industry, or contract type. ALL project details, contract baseline obligations, monthly execution deviations, and SHAP explainability insights are provided to you in the structured JSON context below.
Answer the user's question directly based on the provided project health, delays, penalties, and clauses. Be precise, highly analytical, and recommend specific mitigation steps based on the execution risk. Do NOT give generic advice.

If the user asks why the risk increased, cite the specific activities delayed in the DPR and the corresponding clause from the baseline.

PROJECT CONTEXT:
{context}
"""
        
        formatted_prompt = system_prompt.format(context=project_context) + f"\nQuestion: {user_message}\nExpert Analysis:"
        
        messages = [
            SystemMessage(content=formatted_prompt),
            HumanMessage(content=user_message)
        ]
        
        try:
            response = self.llm.invoke(messages)
            return response.content
        except Exception as e:
            return f"An error occurred while generating the response: {e}"

rag_service = RAGService()
