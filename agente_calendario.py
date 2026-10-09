from langchain.tools import tool
from langchain.agents import create_agent


class AgenteCalendario:
    def __init__(self, model):
        self.agent = create_agent(
            model=model,
            tools=[self.revisar_disponibilidad],
            system_prompt=(
                "Eres un agente especialista en calendario, agendar eventos y disponibilidad de fechas y horarios"
                "Solo debes responder preguntas relacionadas con el clima"
                "Si necesiatas conocer el clima de una ciudad, usa la herramienta revisar_disponibilidad"
                "Respone en español de manera bereve y concisa"
            ),
        )

    @tool
    def revisar_disponibilidad(ciudad: str):
        """Obtiene el clima actual de una ciudad"""
        print(f"herramienta obtener_clima revisando: {ciudad}")

        data = {
            "monterrey": "31 C, seco, con probabilidad de lluvia",
            "guadalajara": "24 C, parcialmente nublado, viento ligero",
            "ciudad de mexico": "21 C, nublado, baja probabilidad de lluvia",
        }

        return data.get(ciudad.lower(), f"No tengo informacion del clima para {ciudad}")

    def procesar(self, input):
        res = self.agent.invoke(
            {"messages": [{"role": "user", "content": input}]},
            config={"recursion_limit": 6},
        )
        return res["message"][-1].content
