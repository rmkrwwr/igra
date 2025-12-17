# game/sound.py
import pygame
import os


class SoundManager:
    def __init__(self):
        pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
        self.sounds = {}
        self.muted = False

    def load_sound(self, name, filepath):
        """Загрузить звук из файла"""
        if os.path.exists(filepath):
            try:
                self.sounds[name] = pygame.mixer.Sound(filepath)
                print(f" Звук загружен: {name}")
                return True
            except Exception as e:
                print(f" Ошибка загрузки {name}: {e}")
        else:
            print(f" Файл не найден: {filepath}")

        self.sounds[name] = None
        return False

    def play(self, name):
        """Воспроизвести звук"""
        if not self.muted and name in self.sounds and self.sounds[name]:
            self.sounds[name].play()

    def set_volume(self, volume):
        """Громкость от 0.0 до 1.0"""
        for sound in self.sounds.values():
            if sound:
                sound.set_volume(volume)

    def toggle_mute(self):
        """Включить/выключить звук"""
        self.muted = not self.muted
        return self.muted


sound_manager = SoundManager()