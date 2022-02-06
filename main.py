import pygame
from sys import exit
from random import randint


def display_score():
    current_time = pygame.time.get_ticks() - start_time
    score_font = pygame.font.SysFont("Verdana", 30)
    score = '{0:.1f}'.format(current_time / 1000)
    score_surface = score_font.render(f"Score: {score} ", False, "Black")
    score_rect = score_surface.get_rect(center=(650, 50))
    pygame.draw.rect(screen, "Pink", score_rect)
    pygame.draw.rect(screen, "Pink", score_rect, 10)
    screen.blit(score_surface, score_rect)
    return score


def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 5
            if obstacle_rect.bottom == 300:
                screen.blit(snail_surface, obstacle_rect)
            else:
                screen.blit(fly_surface, obstacle_rect)
        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]
        return obstacle_list
    else:
        return []


def collisions(player, obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect): return False
    return True

def player_animation():
    global player_surf, player_index

    if player_rect.bottom < 300:
         player_surf = player_jump
    else:
        player_index += 0.1
        if player_index >= len(player_walk): player_index = 0
        player_surf = player_walk[int(player_index)]


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((800, 400))
    pygame.display.set_caption("Wild runner")
    clock = pygame.time.Clock()
    game_active = True
    start_time = 0
    score = '{0:.1f}'.format((pygame.time.get_ticks() - start_time)/1000)

    # background
    sky_surface = pygame.image.load("images/bg_desert.png").convert()
    test_font = pygame.font.SysFont("Verdana", 50)
    text_surface = test_font.render("My game", False, "Black")
    text_rect = text_surface.get_rect(midbottom=(400, 70))
    ground_surface = pygame.image.load("images/ground.png").convert_alpha()

    # score
    #score_font = pygame.font.SysFont("Verdana", 30)
    #score_surface = score_font.render( f"Score: {current_time} s.", "Black")
    #score_rect = score_surface.get_rect(center=(700, 50))

    # obstacles
    snail_surface = pygame.image.load("images/snailWalk1.png").convert_alpha()
    fly_surface = pygame.image.load("images/flyFly1.png").convert_alpha()

    obstacle_rect_list = []

    # player
    player_walk_1 = pygame.image.load("images/p1_walk01.png").convert_alpha()
    player_walk_2 = pygame.image.load("images/p1_stand.png").convert_alpha()
    player_walk = [player_walk_1, player_walk_2]
    player_index = 0
    player_jump = pygame.image.load("images/p1_jump.png").convert_alpha()
    player_surf = player_walk[player_index]
    player_rect = player_surf.get_rect(midbottom=(80, 300))
    player_gravity = 0

    #timer
    obstacle_timer = pygame.USEREVENT + 1
    pygame.time.set_timer(obstacle_timer, 1500)

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
                        player_rect.left = 0
                        start_time = pygame.time.get_ticks()

            if event.type == obstacle_timer and game_active:
                if randint(0, 2):
                    obstacle_rect_list.append(snail_surface.get_rect(midbottom=(randint(900, 1100), 300)))
                else:
                    obstacle_rect_list.append(fly_surface.get_rect(midbottom=(randint(900, 1100), 200)))

        if game_active:
            screen.blit(sky_surface, (0, 0))
            screen.blit(ground_surface, (0, 300))
            pygame.draw.rect(screen, (110, 176, 210), text_rect)
            pygame.draw.rect(screen, (110, 176, 210), text_rect, 8)
            screen.blit(text_surface, text_rect)

            score = display_score()

            obstacle_rect_list = obstacle_movement(obstacle_rect_list)

            screen.blit(player_surf, player_rect)
            player_animation()

            # player loop
            player_gravity += 1
            player_rect.y += player_gravity
            if player_rect.bottom >= 300:
                player_rect.bottom = 300


           # player_rect.left += 5
            #if player_rect.left >= 800:
               #player_rect.left = 0

            #if player_rect.left % 80 > 40:
            #else:
                #screen.blit(player_surface2, player_rect)

            game_active = collisions(player_rect, obstacle_rect_list)
            #Game over message

        else:
            screen.fill((94, 129, 163))
            player_stand = pygame.image.load("images/p1_stand.png").convert_alpha()
            player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
            player_stand_rect = player_stand.get_rect(center=(400, 200))
            Game_Over_font = pygame.font.SysFont("Helvetica", 40)
            Game_Over_surface = Game_Over_font.render(f"Game Over! Your score: {score}", False, "Black")
            Game_Over_rect = Game_Over_surface.get_rect(center=(400, 90))
            message_font = pygame.font.SysFont("Verdana", 20)
            message_surface = message_font.render("to play again press Space", False, "Grey")
            message_rect = message_surface.get_rect(center=(400, 300))

            screen.blit(player_stand, player_stand_rect)
            screen.blit(Game_Over_surface, Game_Over_rect)
            screen.blit(message_surface, message_rect)
            obstacle_rect_list.clear()
            player_rect.midbottom =(80, 300)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_active = True

        # mouse_pos = pygame.mouse.get_pos()

        pygame.display.update()
        clock.tick(60)
