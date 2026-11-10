import random

try:
    import pygame  # type: ignore
except ImportError as exc:
    raise SystemExit(
        "Pygame is not installed. Install it with: pip install pygame"
    ) from exc

WIDTH = 400
HEIGHT = 600
BIRD_X = 100
BIRD_SIZE = 30
PIPE_WIDTH = 60
PIPE_GAP = 150
PIPE_SPEED = 3
GROUND_Y = 600

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird Clone")
clock = pygame.time.Clock()

font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 25)

WHITE = (255, 255, 255)
SKY = (135, 206, 235)
GREEN = (40, 160, 70)
DARK_GREEN = (25, 120, 50)
YELLOW = (255, 220, 50)
BLACK = (25, 25, 25)
BROWN = (145, 95, 55)


def update_bird(y, velocity, space_pressed=False):
    # The jump is applied first, then gravity affects the bird.
    if space_pressed:
        velocity = -10
    velocity += 1
    y += velocity
    return y, velocity


def make_pipe():
    gap_top = random.randint(80, 350)
    return {"x": WIDTH, "gap_top": gap_top, "scored": False}


def get_pipe_rects(pipe):
    top_height = pipe["gap_top"]
    bottom_y = pipe["gap_top"] + PIPE_GAP
    top_rect = pygame.Rect(pipe["x"], 0, PIPE_WIDTH, top_height)
    bottom_rect = pygame.Rect(
        pipe["x"], bottom_y, PIPE_WIDTH, HEIGHT - bottom_y
    )
    return top_rect, bottom_rect


def reset_game():
    return {
        "bird_y": 300,
        "velocity": 0,
        "pipes": [make_pipe()],
        "score": 0,
        "game_over": False,
        "last_pipe_time": pygame.time.get_ticks()
    }


def check_collision(bird_rect, pipes):
    for pipe in pipes:
        top_rect, bottom_rect = get_pipe_rects(pipe)
        if bird_rect.colliderect(top_rect) or bird_rect.colliderect(bottom_rect):
            return True
    return False


def draw_game(game):
    screen.fill(SKY)

    bird_rect = pygame.Rect(BIRD_X, int(game["bird_y"]), BIRD_SIZE, BIRD_SIZE)
    pygame.draw.ellipse(screen, YELLOW, bird_rect)
    pygame.draw.circle(screen, BLACK, (BIRD_X + 21, int(game["bird_y"]) + 9), 3)

    for pipe in game["pipes"]:
        top_rect, bottom_rect = get_pipe_rects(pipe)
        pygame.draw.rect(screen, GREEN, top_rect)
        pygame.draw.rect(screen, GREEN, bottom_rect)
        pygame.draw.rect(screen, DARK_GREEN,
                         (pipe["x"], pipe["gap_top"] - 8, PIPE_WIDTH, 8))
        pygame.draw.rect(screen, DARK_GREEN,
                         (pipe["x"], pipe["gap_top"] + PIPE_GAP, PIPE_WIDTH, 8))

    pygame.draw.rect(screen, BROWN, (0, 585, WIDTH, 15))

    score_text = font.render(str(game["score"]), True, WHITE)
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 20))

    if game["game_over"]:
        title = font.render("Game Over", True, WHITE)
        restart = small_font.render("Press R to restart or ESC to quit", True, WHITE)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 250))
        screen.blit(restart, (WIDTH // 2 - restart.get_width() // 2, 290))

    pygame.display.flip()


def main():
    game = reset_game()
    running = True

    while running:
        clock.tick(60)
        space_pressed = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_SPACE and not game["game_over"]:
                    space_pressed = True
                elif event.key == pygame.K_r and game["game_over"]:
                    game = reset_game()

        if not game["game_over"]:
            game["bird_y"], game["velocity"] = update_bird(
                game["bird_y"], game["velocity"], space_pressed
            )

            now = pygame.time.get_ticks()
            if now - game["last_pipe_time"] >= 1500:
                game["pipes"].append(make_pipe())
                game["last_pipe_time"] = now

            for pipe in game["pipes"]:
                pipe["x"] -= PIPE_SPEED
                if not pipe["scored"] and pipe["x"] + PIPE_WIDTH < BIRD_X:
                    pipe["scored"] = True
                    game["score"] += 1

            game["pipes"] = [
                pipe for pipe in game["pipes"]
                if pipe["x"] + PIPE_WIDTH > 0
            ]

            bird_rect = pygame.Rect(
                BIRD_X, int(game["bird_y"]), BIRD_SIZE, BIRD_SIZE
            )

            if check_collision(bird_rect, game["pipes"]):
                game["game_over"] = True
            elif bird_rect.top < 0 or bird_rect.bottom >= GROUND_Y:
                game["game_over"] = True

        draw_game(game)

    pygame.quit()


if __name__ == "__main__":
    main()
