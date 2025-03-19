import time

class CooldownManager:
    def __init__(self):
        self.cooldowns = {}

    def check_cooldown(self, user_id, command_name):
        """Verifica si un usuario está en cooldown para un comando específico."""
        if user_id in self.cooldowns and command_name in self.cooldowns[user_id]:
            last_used = self.cooldowns[user_id][command_name]
            cooldown_time = 10  # Tiempo de cooldown en segundos
            if time.time() - last_used < cooldown_time:
                return True
        return False

    def set_cooldown(self, user_id, command_name, cooldown_time):
        """Establece el cooldown para un usuario en un comando específico."""
        if user_id not in self.cooldowns:
            self.cooldowns[user_id] = {}
        self.cooldowns[user_id][command_name] = time.time()

    def get_cooldown(self, user_id, command_name):
        """Obtiene el tiempo restante del cooldown de un comando para un usuario."""
        if user_id in self.cooldowns and command_name in self.cooldowns[user_id]:
            last_used = self.cooldowns[user_id][command_name]
            cooldown_time = 10  # Tiempo de cooldown por defecto
            remaining_time = max(0, cooldown_time - (time.time() - last_used))
            return remaining_time
        return 0
