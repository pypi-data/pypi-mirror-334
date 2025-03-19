import subprocess
import os
from rich.console import Console

console = Console()

def supernova_service(input):
    """
    Execute the supernova.sh shell script.
    
    This service calls an external shell script named supernova.sh
    and returns its output.
    """
    try:
        # Path to the supernova.sh script
        # You may need to adjust this path depending on where the script is located
        script_path = os.path.join(os.path.dirname(__file__), "supernova.sh")
        
        # Check if the script exists
        if not os.path.isfile(script_path):
            return f"Error: Could not find supernova.sh at {script_path}"
        
        # Make the script executable if it's not already
        if not os.access(script_path, os.X_OK):
            os.chmod(script_path, 0o755)
        
        # Execute the script
        console.print("[bold red]Initiating supernova sequence...[/bold red]")
        result = subprocess.run([script_path], 
                               capture_output=True, 
                               text=True)
        
        if result.returncode != 0:
            return f"Supernova script failed with error: {result.stderr}"
        
        # Return the output from the script
        return result.stdout
    
    except Exception as e:
        return f"An error occurred while executing supernova.sh: {str(e)}"
