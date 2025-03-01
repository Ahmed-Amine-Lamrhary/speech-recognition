from executors.command_executor import command_map
from ollama import chat

COMMANDS = list(command_map.keys())

def recognize_command(text):
    prompt = f"""Si aucune correspondance n'est trouvée, réponds simplement par une chaîne vide. Voici une liste de commandes disponibles : {', '.join(COMMANDS)}.
    Détermine quelle commande correspond le mieux à ce texte : '{text}'.
    Si aucune correspondance n'est trouvée, réponds simplement par une chaîne vide."""

    response = chat(model='llama3.2', messages=[{'role': 'user','content': prompt}])

    command_text = response.message.content.strip().lower()

    print(f"Command text: {command_text}")

    matched_command = next((cmd for cmd in COMMANDS if cmd in command_text), "")

    if not matched_command:
        raise Exception(f"Aucune commande correspondante trouvée pour l'entrée: '{text}'")

    return matched_command
