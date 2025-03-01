from ollama import chat
import webbrowser

class CommandExecutor():

    def execute(self, text: str):
        pass

class OpenUrlCommandExecutor(CommandExecutor):
    
    def execute(self, text: str):
        # Construct the prompt to generate a URL from the given command text
        prompt = f"""Given the following command, generate the corresponding URL:

        '{text}'

        Respond with only the URL, and nothing else. No explanations or additional information. For example, if the command is 'open google', the output should be 'https://www.google.com/'. Do not add anything else."""
        
        response = chat(model='llama3.2', messages=[{'role': 'user', 'content': prompt}])

        url = response.message.content.strip()

        if url:
            webbrowser.open(url)
        else:
            raise Exception("Aucune URL trouvée dans la réponse. Veuillez réessayer.")

command_map = {
    "open url": OpenUrlCommandExecutor()
}
