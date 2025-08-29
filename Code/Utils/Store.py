import pickle
import logging
import os
from datetime import datetime
class Store():
    def __init__(self, log_name="log.txt"):
        # Ruta al directorio donde está este archivo (Utils)
        current_dir = os.path.dirname(os.path.abspath(__file__))

        # Subir un nivel (a la raíz del proyecto) y luego entrar a Logs
        logs_root = os.path.join(current_dir, "..", "Logs")

        # Crear carpeta con la fecha actual
        today = datetime.now().strftime("%Y-%m-%d")
        dated_folder = os.path.join(logs_root, today)
        os.makedirs(dated_folder, exist_ok=True)

        # Ruta completa del archivo de log
        log_path = os.path.join(dated_folder, log_name)

        # Configurar el logger
        logging.basicConfig(
            filename=log_path,
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )

        self.logger = logging.getLogger(__name__)
    def save_vars(self,action_values,reward_episode,filepath_vars):
        with open(filepath_vars, "wb") as f:
            pickle.dump({
                'q_table': action_values,
                'rewards': reward_episode,
            }, f)
    def load_vars(self,filepath_vars):
        with open(filepath_vars, "rb") as f:
            data = pickle.load(f)
        return data['q_table'], data['rewards']
    def log(self,message):
        self.logger.info(message)
    


