from aiogram.types import Message
import asyncio

from config import TIME_WAITING

class ProgressBar:
    def __init__(self, message: Message, total_steps: int = 10, step_size: int = 2):
        """
        Инициализация класса ProgressBar.
        
        :param message: Сообщение, на основе которого будет отправлена шкала прогресса.
        :param total_steps: Общее количество шагов для полного заполнения шкалы.
        :param step_size: Количество символов, на которое увеличивается шкала за шаг.
        """
        self.message = message
        self.total_steps = total_steps
        self.step_size = step_size
        self.progress_message = None
        self.current_step = 0

    async def start(self):
        """Отправляет начальное сообщение с прогрессом."""
        progress = int((self.current_step / self.total_steps) * 100)
        filled_length = min(self.current_step * self.step_size, self.total_steps * self.step_size)
        progress_bar = f"{'█' * filled_length}{'░' * (self.total_steps * self.step_size - filled_length)} {progress}%"

        self.message = await self.message.answer(f"Загрузка: {progress_bar}")

    async def update(self):
        await asyncio.sleep(TIME_WAITING)
        """Обновляет сообщение с прогрессом с шагом."""
        self.current_step += 1
        progress = int((self.current_step / self.total_steps) * 100)
        filled_length = min(self.current_step * self.step_size, self.total_steps * self.step_size)
        progress_bar = f"{'█' * filled_length}{'░' * (self.total_steps * self.step_size - filled_length)} {progress}%"

        await self.message.edit_text(f"Загрузка: {progress_bar}")

    async def finish(self, final_text: str):
        """Отображает финальное сообщение."""
        await self.progress_message.edit_text(final_text)
