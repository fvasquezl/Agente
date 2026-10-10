from langchain.tools import tool
from langchain.agents import create_agent


class AgenteCalendario:
    def __init__(self, model):
        self.agent = create_agent(
            model=model,
            tools=[self.revisar_disponibilidad],
            system_prompt=(
                "Eres un agente especialista en calendario, agendar eventos y disponibilidad de fechas y horarios"
                "Si necesitas conocer disponibilidad, usa la herramienta revisar_disponibilidad"
                "Respone en español de manera bereve y concisa"
            ),
        )

    @tool
    def revisar_disponibilidad(dia: str):
        """Revisa la disponibilidad de calendario para una fecha o dia"""
        print(f"herramienta revisar_disponibilidad revisando: {dia}")

        return "Se cuenta con disponibilidad de 11:00am a 12:00pm"

    def procesar(self, input):
        res = self.agent.invoke(
            {"messages": [{"role": "user", "content": input}]},
            config={"recursion_limit": 6},
        )
        return res["message"][-1].content
