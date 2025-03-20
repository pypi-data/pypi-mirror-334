import subprocess
from colorama import Fore, Style

class GitHandler:
    """Gère les interactions avec Git"""

    @staticmethod
    def extract_commit_message(file_path):
        """Cherche une ligne contenant commit_name="message" et retourne le message."""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                for line in f:
                    if "commit_name=" in line:
                        parts = line.split("commit_name=", 1)
                        if len(parts) > 1:
                            message = parts[1].strip().replace('"', '')
                            return message if message else None
        except Exception as e:
            print(f"{Fore.RED}❌ Erreur lors de la lecture du fichier : {e}{Style.RESET_ALL}")
        return None

    @staticmethod
    def git_commit_push(commit_message):
        """Ajoute, commit et pousse les modifications sur Git."""
        try:
            status_output = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True).stdout.strip()
            
            if not status_output:
                print(f"{Fore.YELLOW}⚠️ Aucun changement détecté, rien à commit.{Style.RESET_ALL}")
                return  

            subprocess.run(["git", "add", "."], check=True)
            subprocess.run(["git", "commit", "-m", commit_message], check=True)
            subprocess.run(["git", "push"], check=True)


            print(f"{Fore.GREEN}✅ Commit et push réussi : {commit_message}{Style.RESET_ALL}")
        except subprocess.CalledProcessError as e:
            print(f"{Fore.RED}❌ Erreur Git : {e}{Style.RESET_ALL}")
