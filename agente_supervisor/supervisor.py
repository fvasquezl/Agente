from unittest import result

from langchain.tools import tool
from langchain.agents import create_agent


class Supervisor:
    def __init__(self, model, agente_clima, agente_calendario):
        self.agente_clima = agente_clima
        self.agente_calendario = agente_calendario

        @tool
        def delegar_a_agente_clima(input):
            """Consulta al especialista en clima cuando la solicitud hable de clima o temperatura"""
            print(f"Supervisor-> Agente del clima:{input}")
            return self.agente_clima.procesar(input)

        @tool
        def delegar_a_agente_calendario(input):
            """Consulta al especialista en calendario cuando la solicitud hable de fechas o eventos"""
            print(f"Supervisor-> Agente del calendario:{input}")
            return self.agente_calendario.procesar(input)

        self.supervisor = create_agent(
            model=model,
            tools=[delegar_a_agente_clima, delegar_a_agente_calendario],
            system_prompt=(
                "Eres un coordinador de agentes especializados."
                "Tu trabajo es decudir a qué especialista delegar las tareas."
                "Si la solicitud mezcla temas, puedes usar mas de un especialista."
                "No llames  especialistas que no sean necesarios"
                "Responde al usuario de manera breve y concisa, en español"
            ),
        )

    def chat(self):
        while True:
            user_input = input("\nTú: ").strip()

            if user_input.lower() in {"salir", "exit"}:
                break

            print(f"Usuario -> Supervisor: {user_input}")

            result = self.supervisor.invoke(
                {"messages": [{"role": "user", "content": user_input}]},
                config={"recursion_limit": 8},
            )

            print(f"Supervisor -> Usuario:{result['messages'][-1].content}")


load_dotenv()
