from __future__ import annotations

import math

import pygame

from animations.tween import Tween, ease_out_back
from audio.audio_manager import AudioManager
from config import COLORS, WINDOW_HEIGHT, WINDOW_WIDTH
from ui.button import GlossyButton


class MenuScene:
    def __init__(self, resources, audio: AudioManager) -> None:
        self.resources = resources
        self.audio = audio
        self.time = 0.0
        self.menu_enter = Tween(0.9, 0.7, 1.0, ease_out_back)
        self.title_enter = Tween(0.8, -170, 66, ease_out_back)
        self.islands_enter = Tween(1.0, WINDOW_HEIGHT + 160, 390, ease_out_back)
        self.message_enter = Tween(1.1, WINDOW_WIDTH + 300, 975, ease_out_back)
        self.audio.play_ui("menu_open.wav", 0.8)
        self.audio.play_ui("whoosh.wav", 0.6)

        title_font = pygame.font.Font(None, 98)
        label_font = pygame.font.Font(None, 56)
        small_font = pygame.font.Font(None, 52)

        self.play_button = GlossyButton(
            pygame.Rect(460, 520, 450, 130),
            "ИГРАТЬ",
            title_font,
            (255, 180, 12),
            (170, 85, 15),
            COLORS["text_light"],
        )

        self.bottom_buttons = [
            GlossyButton(pygame.Rect(70, 695, 240, 80), "Обучение", label_font, (73, 176, 60), (46, 118, 38), (245, 255, 245), "📖"),
            GlossyButton(pygame.Rect(330, 695, 290, 80), "Достижения", label_font, (235, 79, 33), (156, 43, 20), (255, 250, 245), "🏆"),
            GlossyButton(pygame.Rect(640, 695, 260, 80), "Настройки", label_font, (242, 155, 15), (161, 94, 12), (255, 252, 242), "⚙"),
        ]

        self.small_font = small_font
        self.label_font = label_font
        self.last_hover = False

    def handle_event(self, event) -> None:
        if self.play_button.handle_event(event):
            self.audio.play_ui("click.wav")

        for button in self.bottom_buttons:
            if button.handle_event(event):
                self.audio.play_ui("click.wav", 0.9)

    def update(self, dt: float) -> None:
        self.time += dt
        mouse_pos = pygame.mouse.get_pos()

        hovered = self.play_button.update(mouse_pos)
        for button in self.bottom_buttons:
            hovered = button.update(mouse_pos) or hovered

        if hovered:
            self.audio.play_ui("hover.wav", 0.75)

        self.menu_enter.update(dt)
        self.title_enter.update(dt)
        self.islands_enter.update(dt)
        self.message_enter.update(dt)

    def draw(self, surface: pygame.Surface) -> None:
        self._draw_sky(surface)
        island_y = self.islands_enter.end if self.islands_enter.done else self.islands_enter.start + (self.islands_enter.end - self.islands_enter.start) * min(1.0, self.islands_enter.elapsed / self.islands_enter.duration)
        island_y += math.sin(self.time * 1.2) * 5
        self._draw_island(surface, island_y)
        self._draw_title(surface)
        self._draw_robot(surface, island_y)

        self.play_button.draw(surface)
        for button in self.bottom_buttons:
            button.draw(surface)

        self._draw_player_badge(surface)

    def _draw_sky(self, surface: pygame.Surface) -> None:
        for y in range(WINDOW_HEIGHT):
            t = y / WINDOW_HEIGHT
            r = int(COLORS["sky_top"][0] + (COLORS["sky_bottom"][0] - COLORS["sky_top"][0]) * t)
            g = int(COLORS["sky_top"][1] + (COLORS["sky_bottom"][1] - COLORS["sky_top"][1]) * t)
            b = int(COLORS["sky_top"][2] + (COLORS["sky_bottom"][2] - COLORS["sky_top"][2]) * t)
            pygame.draw.line(surface, (r, g, b), (0, y), (WINDOW_WIDTH, y))

        for i in range(10):
            x = (i * 170 + int(self.time * 18)) % (WINDOW_WIDTH + 220) - 120
            y = 85 + (i % 4) * 78
            self._draw_cloud(surface, x, y, 1.0 + (i % 3) * 0.3)

    def _draw_cloud(self, surface: pygame.Surface, x: int, y: int, scale: float) -> None:
        base = pygame.Surface((240, 110), pygame.SRCALPHA)
        color = (235, 245, 255, 160)
        pygame.draw.ellipse(base, color, (10, 34, 110, 52))
        pygame.draw.ellipse(base, color, (70, 15, 120, 68))
        pygame.draw.ellipse(base, color, (140, 30, 90, 54))
        cloud = pygame.transform.smoothscale(base, (int(240 * scale), int(110 * scale)))
        surface.blit(cloud, (x, y))

    def _draw_island(self, surface: pygame.Surface, island_y: float) -> None:
        pygame.draw.ellipse(surface, (49, 168, 208), (45, island_y + 170, 1240, 195))
        pygame.draw.ellipse(surface, (134, 205, 89), (145, island_y - 30, 1060, 300))
        pygame.draw.ellipse(surface, (157, 108, 53), (130, island_y + 150, 1080, 175))

        pygame.draw.polygon(surface, (181, 211, 91), [(530, island_y + 30), (780, island_y + 30), (920, island_y + 170), (380, island_y + 170)])

        pygame.draw.rect(surface, (247, 194, 121), (560, island_y - 5, 190, 130), border_radius=12)
        pygame.draw.polygon(surface, (225, 92, 52), [(540, island_y + 5), (770, island_y + 5), (720, island_y - 45), (585, island_y - 45)])
        pygame.draw.rect(surface, (98, 157, 226), (595, island_y + 40, 50, 35), border_radius=5)
        pygame.draw.rect(surface, (98, 157, 226), (665, island_y + 40, 50, 35), border_radius=5)
        pygame.draw.rect(surface, (150, 76, 46), (650, island_y + 77, 40, 48), border_radius=5)

        for idx in range(12):
            tx = 260 + idx * 80
            ty = island_y + 105 + math.sin(idx + self.time * 1.8) * 8
            pygame.draw.polygon(surface, (68, 155, 56), [(tx, ty), (tx + 28, ty - 55), (tx + 58, ty)])

    def _draw_title(self, surface: pygame.Surface) -> None:
        y = self.title_enter.update(0)
        board = pygame.Rect(330, int(y), 710, 210)
        pygame.draw.rect(surface, (116, 73, 45), board, border_radius=25)
        pygame.draw.rect(surface, (152, 98, 62), board.inflate(0, -26), border_radius=20)

        top_font = pygame.font.Font(None, 72)
        bottom_font = pygame.font.Font(None, 108)
        top = top_font.render("Математический", True, (255, 202, 54))
        bot = bottom_font.render("ОСТРОВ", True, (245, 245, 250))

        surface.blit(top, top.get_rect(center=(board.centerx, board.centery - 40)))
        surface.blit(bot, bot.get_rect(center=(board.centerx, board.centery + 40)))

        num_font = pygame.font.Font(None, 95)
        for txt, pos, col in [("5", (300, board.y + 35), (64, 180, 235)), ("2", (260, board.y + 110), (255, 101, 128)), ("8", (1035, board.y + 60), (255, 192, 50)), ("7", (1055, board.y + 145), (103, 93, 255))]:
            surface.blit(num_font.render(txt, True, col), pos)

        bubble_x = self.message_enter.update(0)
        bubble_rect = pygame.Rect(int(bubble_x), 270, 360, 150)
        pygame.draw.rect(surface, (242, 248, 255), bubble_rect, border_radius=30)
        pygame.draw.polygon(surface, (242, 248, 255), [(970, 402), (990, 432), (1020, 402)])
        bubble_text = self.label_font.render("Привет! Готов", True, (44, 95, 173))
        bubble_text2 = self.label_font.render("решать задачки?", True, (44, 95, 173))
        surface.blit(bubble_text, (bubble_rect.x + 28, bubble_rect.y + 35))
        surface.blit(bubble_text2, (bubble_rect.x + 28, bubble_rect.y + 78))

    def _draw_robot(self, surface: pygame.Surface, island_y: float) -> None:
        x = 965
        y = int(island_y + 130 + math.sin(self.time * 2.4) * 6)
        pygame.draw.rect(surface, (235, 245, 255), (x, y + 65, 150, 132), border_radius=36)
        pygame.draw.rect(surface, (15, 114, 231), (x + 18, y + 145, 114, 48), border_radius=20)
        pygame.draw.rect(surface, (217, 233, 252), (x - 24, y + 82, 30, 77), border_radius=14)
        pygame.draw.rect(surface, (217, 233, 252), (x + 145, y + 82, 30, 77), border_radius=14)

        pygame.draw.ellipse(surface, (223, 235, 250), (x - 22, y - 10, 190, 115))
        pygame.draw.ellipse(surface, (17, 34, 72), (x + 8, y + 12, 130, 70))
        pygame.draw.circle(surface, (91, 245, 255), (x + 45, y + 45), 8)
        pygame.draw.circle(surface, (91, 245, 255), (x + 103, y + 45), 8)
        pygame.draw.arc(surface, (255, 120, 80), (x + 55, y + 50, 40, 18), 0.1, 3.0, 4)
        pygame.draw.circle(surface, (40, 162, 255), (x + 148, y - 15), 8)

        pygame.draw.rect(surface, (33, 78, 159), (x + 24, y + 187, 45, 36), border_radius=12)
        pygame.draw.rect(surface, (33, 78, 159), (x + 88, y + 187, 45, 36), border_radius=12)

    def _draw_player_badge(self, surface: pygame.Surface) -> None:
        pygame.draw.circle(surface, (240, 248, 255), (1130, 700), 68)
        pygame.draw.circle(surface, (40, 152, 210), (1130, 700), 63, 6)
        pygame.draw.circle(surface, (252, 214, 170), (1130, 700), 34)
        pygame.draw.arc(surface, (113, 64, 40), (1102, 665, 56, 42), 3.1, 6.2, 7)
        pygame.draw.circle(surface, (34, 20, 16), (1118, 697), 4)
        pygame.draw.circle(surface, (34, 20, 16), (1143, 697), 4)
        pygame.draw.arc(surface, (34, 20, 16), (1116, 707, 30, 14), 0.1, 3.1, 2)

        badge = pygame.Rect(1183, 674, 128, 56)
        pygame.draw.rect(surface, (28, 91, 171), badge, border_radius=18)
        txt = self.small_font.render("Ур. 1", True, (235, 245, 255))
        surface.blit(txt, txt.get_rect(center=badge.center))
