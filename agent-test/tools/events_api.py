from langchain.agents import tool

@tool
def show_available_events() -> str:
    """Esta herramienta sirve para listar los eventos disponibles"""
    # HTTP call to my Events API using the requests library
    events = requests.get('https://my-events-api.com/events')
    
    return events.json()

@tool
def show_event_details(event_id: int) -> str:
    """Esta herramienta sirve para mostrar los detalles de un evento como el nombre, 
    la fecha, la descripción y los precios"""
    # HTTP call to my Events API using the requests library
    event = requests.get(f'https://my-events-api.com/events/{event_id}')
    
    return event.json()

