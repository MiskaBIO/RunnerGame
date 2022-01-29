import pygame
from sys import exit

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((800, 400))
    pygame.display.set_caption("Wild runner")
    clock = pygame.time.Clock()
    game_active = True

    # background
    sky_surface = pygame.image.load("images/bg_desert.png").convert()
    test_font = pygame.font.SysFont("Verdana", 50)
    text_surface = test_font.render("My game", False, "Black")
    text_rect = text_surface.get_rect(midbottom=(400, 70))

    # score
    score_font = pygame.font.SysFont("Verdana", 30)
    score_surface = score_font.render("Score:", False, "Black")
    score_rect = score_surface.get_rect(center=(700, 50))

    # Game over message
    Game_Over_font = pygame.font.SysFont("Helvetica", 40)
    Game_Over_surface = Game_Over_font.render("Game Over", False, "Black")
    Game_Over_rect = Game_Over_surface.get_rect(center=(400, 200))
    message_font = pygame.font.SysFont("Verdana", 20)
    message_surface = message_font.render("to play again press Space", False, "Grey")
    message_rect = message_surface.get_rect(center=(400, 120))

    # snail
    snail_surface = pygame.image.load("images/snailWalk1.png").convert_alpha()
    snail_rect = snail_surface.get_rect(midbottom=(600, 300))

    # player
    player_surface = pygame.image.load("images/p1_walk01.png").convert_alpha()
    player_rect = player_surface.get_rect(midbottom=(80, 300))
    player_gravity = 0

    play = True
    while play:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if game_active:
                if event.type == pygame.MOUSEBUTTONDOWN and player_rect.bottom == 300:
                    if player_rect.collidepoint(event.pos):
                        player_gravity = -20

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and player_rect.bottom == 300:
                        player_gravity = -20
                else:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            game_active = True
                            snail_rect.left = 800

            # if event.type == pygame.KEYUP:
            #   pass
        if game_active:
            screen.blit(sky_surface, (0, 0))
            pygame.draw.rect(screen, (110, 176, 210), text_rect)
            pygame.draw.rect(screen, (110, 176, 210), text_rect, 8)
            screen.blit(text_surface, text_rect)
            pygame.draw.rect(screen, "Pink", score_rect)
            pygame.draw.rect(screen, "Pink", score_rect, 10)
            screen.blit(score_surface, score_rect)
            pygame.draw.line(screen, "Black", (0, 300), (800, 300), 10)
            # pygame.draw.ellipse(screen, "Brown", pygame.Rect(50, 200, 100, 100))

            snail_rect.left -= 3
            if snail_rect.right <= 0:
                snail_rect.right = 800
            screen.blit(snail_surface, snail_rect)

            # player loop
            player_gravity += 1
            player_rect.y += player_gravity
            if player_rect.bottom >= 300:
                player_rect.bottom = 300

            player_rect.left += 3
            if player_rect.left >= 800:
                player_rect.left = 0
            screen.blit(player_surface, player_rect)

            if player_rect.colliderect(snail_rect):
                game_active = False
                screen.blit(Game_Over_surface, Game_Over_rect)
                screen.blit(message_surface, message_rect)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        game_active = True
                        snail_rect.left = 800

        # mouse_pos = pygame.mouse.get_pos()
        # if player_rect.collidepoint(mouse_pos):
        #  print(pygame.mouse.get_pressed())

        pygame.display.update()
        clock.tick(60)
