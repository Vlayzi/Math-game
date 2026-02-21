from __future__ import annotations

import pygame


class GlossyButton:
    def __init__(
        self,
        rect: pygame.Rect,
        text: str,
        font: pygame.font.Font,
        base_color: tuple[int, int, int],
        shadow_color: tuple[int, int, int],
        text_color: tuple[int, int, int],
        icon: str | None = None,
    ) -> None:
        self.rect = rect
        self.text = text
        self.font = font
        self.base_color = base_color
        self.shadow_color = shadow_color
        self.text_color = text_color
        self.icon = icon
        self.hovered = False
        self.pressed = False
        self.scale = 1.0

    def update(self, mouse_pos: tuple[int, int]) -> bool:
        was_hovered = self.hovered
        self.hovered = self.rect.collidepoint(mouse_pos)
        target_scale = 1.05 if self.hovered else 1.0
        self.scale += (target_scale - self.scale) * 0.24
        return self.hovered and not was_hovered

    def handle_event(self, event) -> bool:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.hovered:
            self.pressed = True
            return False
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            clicked = self.hovered and self.pressed
            self.pressed = False
            return clicked
        return False

    def draw(self, surface: pygame.Surface) -> None:
        scaled_w = int(self.rect.width * self.scale)
        scaled_h = int(self.rect.height * self.scale)
        draw_rect = pygame.Rect(0, 0, scaled_w, scaled_h)
        draw_rect.center = self.rect.center

        shadow_rect = draw_rect.move(0, 7)
        pygame.draw.rect(surface, self.shadow_color, shadow_rect, border_radius=scaled_h // 2)

        pygame.draw.rect(surface, self.base_color, draw_rect, border_radius=scaled_h // 2)
        highlight = pygame.Rect(draw_rect.x + 10, draw_rect.y + 8, draw_rect.width - 20, draw_rect.height // 2)
        pygame.draw.rect(surface, (255, 235, 140), highlight, border_radius=scaled_h // 3)

        text = self.font.render(self.text, True, self.text_color)
        text_rect = text.get_rect(center=draw_rect.center)

        if self.icon:
            icon_font = pygame.font.Font(None, int(draw_rect.height * 0.55))
            icon = icon_font.render(self.icon, True, self.text_color)
            icon_rect = icon.get_rect(midleft=(draw_rect.left + 26, draw_rect.centery))
            text_rect.centerx += 18
            surface.blit(icon, icon_rect)

        surface.blit(text, text_rect)
