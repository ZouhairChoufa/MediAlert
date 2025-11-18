import os
import json
from dotenv import load_dotenv
load_dotenv()  # charge le .env à la racine

from crewai import LLM
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task






@CrewBase
class SystemeUrgencesMedicalesCrew:
    """SystemeUrgencesMedicales crew"""

    
    @agent
    def agentpatient(self) -> Agent:
        
        return Agent(
            config=self.agents_config["agentpatient"],
            
            
            tools=[],
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=5,
            max_rpm=None,
            
            max_execution_time=None,
            llm=LLM(
                model="groq/llama-3.1-8b-instant",
                temperature=0.7,
                max_tokens=256,
            ),
        )
    
    @agent
    def agentmedecinurgence(self) -> Agent:
        
        return Agent(
            config=self.agents_config["agentmedecinurgence"],
            
            
            tools=[],
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=5,
            max_rpm=None,
            
            max_execution_time=None,
            llm=LLM(
                model="groq/llama-3.1-8b-instant",
                temperature=0.7,
                max_tokens=256,
            ),
            
        )
    
    @agent
    def agentcordonnateur(self) -> Agent:
        
        return Agent(
            config=self.agents_config["agentcordonnateur"],
            
            
            tools=[],
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=5,
            max_rpm=None,
            
            max_execution_time=None,
            llm=LLM(
                model="groq/llama-3.1-8b-instant",
                temperature=0.7,
                max_tokens=256,
            ),
            
        )
    
    @agent
    def agenthopital(self) -> Agent:
        
        return Agent(
            config=self.agents_config["agenthopital"],
            
            
            tools=[],
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=5,
            max_rpm=None,
            
            max_execution_time=None,
            llm=LLM(
                model="groq/llama-3.1-8b-instant",
                temperature=0.7,
                max_tokens=256,
            ),
            
        )
    
    @agent
    def agentmedecinspecialiste(self) -> Agent:
        
        return Agent(
            config=self.agents_config["agentmedecinspecialiste"],
            
            
            tools=[],
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=5,
            max_rpm=None,
            
            max_execution_time=None,
            llm=LLM(
                model="groq/llama-3.1-8b-instant",
                temperature=0.7,
                max_tokens=256,
            ),
            
        )
    
    @agent
    def agentambulence(self) -> Agent:
        
        return Agent(
            config=self.agents_config["agentambulence"],
            
            
            tools=[],
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=5,
            max_rpm=None,
            
            max_execution_time=None,
            llm=LLM(
                model="groq/llama-3.1-8b-instant",
                temperature=0.7,
                max_tokens=256,
            ),
            
        )
    

    
    @task
    def creer_l_alerte(self) -> Task:
        return Task(
            config=self.tasks_config["creer_l_alerte"],
            markdown=False,
            
            
        )
    
    @task
    def triage_patients_et_selection_ambulance(self) -> Task:
        return Task(
            config=self.tasks_config["triage_patients_et_selection_ambulance"],
            markdown=False,
            
            
        )
    
    @task
    def valider_la_demande_du_coordonnateur(self) -> Task:
        return Task(
            config=self.tasks_config["valider_la_demande_du_coordonnateur"],
            markdown=False,
            
            
        )
    
    @task
    def recevoir_les_patients(self) -> Task:
        return Task(
            config=self.tasks_config["recevoir_les_patients"],
            markdown=False,
            
            
        )
    
    @task
    def analyse_medicale_d_urgence(self) -> Task:
        return Task(
            config=self.tasks_config["analyse_medicale_d_urgence"],
            markdown=False,
            
            
        )
    
    @task
    def traitement_du_specialiste(self) -> Task:
        return Task(
            config=self.tasks_config["traitement_du_specialiste"],
            markdown=False,
            
            
        )
    

    @crew
    def crew(self) -> Crew:
        """Creates the SystemeUrgencesMedicales crew"""
        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
        )

   # def _load_response_format(self, name):
       # with open(os.path.join(self.base_directory, "config", f"{name}.json")) as f:
          #  json_schema = json.loads(f.read())

       # return SchemaConverter.build(json_schema)
