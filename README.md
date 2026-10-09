# Agente Supervisor

Sistema multiagente con [LangChain](https://python.langchain.com/) y modelos de [Groq](https://groq.com/). Un agente supervisor recibe la pregunta del usuario y la delega al agente especialista adecuado.

> **Estado:** en desarrollo. Los agentes especialistas están definidos; el supervisor (`supervisor.py`) aún no está implementado.

## Agentes

| Archivo | Clase | Descripción |
|---|---|---|
| `agente_clima.py` | `AgenteClima` | Responde preguntas sobre el clima de una ciudad con la herramienta `obtener_clima`. |
| `agente_calendario.py` | `AgenteCalendario` | Agente de calendario y disponibilidad con la herramienta `revisar_disponibilidad`. |
| `supervisor.py` | — | Orquestador que enrutará las preguntas a cada agente (pendiente). |

Por ahora las herramientas devuelven datos de ejemplo para Monterrey, Guadalajara y Ciudad de México.

## Requisitos

- Python 3.14 o superior
- Una API key de [Groq](https://console.groq.com/keys)

## Instalación

```bash
git clone https://github.com/fvasquezl/agente_supervisor.git
cd agente_supervisor

python -m venv venv
source venv/bin/activate

pip install -r requirements.txt
```

## Configuración

Crea un archivo `.env` en la raíz del proyecto:

```env
GROQ_API_KEY=tu_api_key
```

Opcionalmente, para trazar las ejecuciones con LangSmith:

```env
LANGSMITH_TRACING=true
LANGSMITH_API_KEY=tu_api_key
LANGSMITH_PROJECT=agente_supervisor
```

El archivo `.env` está excluido del repositorio en `.gitignore`.

## Uso

Cada agente recibe un modelo de chat y expone el método `procesar`:

```python
from dotenv import load_dotenv
from langchain_groq import ChatGroq

from agente_clima import AgenteClima

load_dotenv()

model = ChatGroq(model="llama-3.3-70b-versatile")
agente = AgenteClima(model)

print(agente.procesar("¿Cómo está el clima en Monterrey?"))
```
