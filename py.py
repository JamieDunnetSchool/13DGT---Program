import pygame
import random
import math
from collections import defaultdict

pygame.init()

# ---------------------------
# Config
# ---------------------------
W, H = 1100, 700
FPS = 60
TILE = 24
WORLD_W = 320   # tiles wide
WORLD_H = 140   # tiles high

GRAVITY = 2400.0
MOVE_SPEED = 420.0
JUMP_VEL = 820.0
FRICTION_GROUND = 14.0
FRICTION_AIR = 2.0

MINING_TIME = {
    1: 0.30,  # dirt
    2: 0.55,  # stone
    3: 0.25,  # grass
}

# Block IDs:
# 0 = air
# 1 = dirt
# 2 = stone
# 3 = grass
# 4 = wood (placeable)
# 5 = torch (cosmetic)
BLOCK_NAME = {0:"Air",1:"Dirt",2:"Stone",3:"Grass",4:"Wood",5:"Torch"}

COL = {
    0: (0,0,0,0),
    1: (139, 101, 57),
    2: (120, 120, 120),
    3: (90, 170, 85),
    4: (155, 110, 60),
    5: (255, 200, 80),
}

SOLID = {1,2,3,4}  # torch is not solid

# ---------------------------
# Helpers
# ---------------------------
def clamp(v, a, b):
    return a if v < a else b if v > b else v

def sign(x):
    return -1 if x < 0 else 1 if x > 0 else 0

def tile_at(px, py):
    return int(math.floor(px / TILE)), int(math.floor(py / TILE))

def rect_to_tile_range(r):
    x0 = int(math.floor(r.left / TILE))
    x1 = int(math.floor((r.right - 1) / TILE))
    y0 = int(math.floor(r.top / TILE))
    y1 = int(math.floor((r.bottom - 1) / TILE))
    return x0, x1, y0, y1

# ---------------------------
# World generation
# ---------------------------
def generate_world():
    world = [[0 for _ in range(WORLD_W)] for _ in range(WORLD_H)]

    # height map
    base = WORLD_H // 2
    hmap = [base]
    for x in range(1, WORLD_W):
        hmap.append(clamp(hmap[-1] + random.choice([-1,0,0,1]), base-6, base+10))

    # fill terrain
    for x in range(WORLD_W):
        surface = hmap[x]
        for y in range(surface, WORLD_H):
            if y == surface:
                world[y][x] = 3  # grass
            elif y < surface + 6:
                world[y][x] = 1  # dirt
            else:
                world[y][x] = 2  # stone

    # carve caves with random walkers
    walkers = 18
    for _ in range(walkers):
        x = random.randint(0, WORLD_W-1)
        y = random.randint(base+8, WORLD_H-10)
        steps = random.randint(220, 520)
        for _s in range(steps):
            r = random.randint(1, 2)
            for yy in range(y-r, y+r+1):
                for xx in range(x-r, x+r+1):
                    if 0 <= xx < WORLD_W and 0 <= yy < WORLD_H:
                        if (xx-x)*(xx-x) + (yy-y)*(yy-y) <= r*r:
                            world[yy][xx] = 0
            x += random.choice([-1,0,1])
            y += random.choice([-1,0,1,1])
            x = clamp(x, 0, WORLD_W-1)
            y = clamp(y, base+4, WORLD_H-2)

    # a few trees
    for _ in range(42):
        x = random.randint(3, WORLD_W-4)
        # find surface
        for y in range(0, WORLD_H-1):
            if world[y][x] == 3:
                trunk = random.randint(3, 6)
                for t in range(1, trunk+1):
                    if y-t >= 0:
                        world[y-t][x] = 4
                # simple canopy
                cy = y - trunk
                for yy in range(cy-2, cy+1):
                    for xx in range(x-2, x+3):
                        if 0 <= xx < WORLD_W and 0 <= yy < WORLD_H:
                            if random.random() < 0.65:
                                world[yy][xx] = 4
                break

    return world, hmap

# ---------------------------
# Game objects
# ---------------------------
class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.w = TILE * 0.8
        self.h = TILE * 1.35
        self.vx = 0.0
        self.vy = 0.0
        self.on_ground = False

        self.hp = 100
        self.max_hp = 100

        self.inventory = defaultdict(int)
        # start items
        self.inventory[4] = 80  # wood
        self.inventory[5] = 25  # torch
        self.hotbar = [1,2,4,5,0,0,0,0,0]
        self.selected = 0

    @property
    def rect(self):
        return pygame.Rect(int(self.x), int(self.y), int(self.w), int(self.h))

    def give_block(self, bid, amt=1):
        if bid in (0,):
            return
        # grass gives dirt when mined
        if bid == 3:
            bid = 1
        self.inventory[bid] += amt

    def consume_selected(self):
        bid = self.hotbar[self.selected]
        if bid == 0:
            return False
        if self.inventory[bid] <= 0:
            return False
        self.inventory[bid] -= 1
        return True

# ---------------------------
# Collision
# ---------------------------
def is_solid(world, tx, ty):
    if tx < 0 or ty < 0 or tx >= WORLD_W or ty >= WORLD_H:
        return True  # treat out of bounds as solid walls
    return world[ty][tx] in SOLID

def move_and_collide(player, world, dt):
    # horizontal
    player.x += player.vx * dt
    r = player.rect
    x0, x1, y0, y1 = rect_to_tile_range(r)
    if player.vx != 0:
        dirx = sign(player.vx)
        edge_tx = x1 if dirx > 0 else x0
        for ty in range(y0, y1+1):
            if is_solid(world, edge_tx, ty):
                if dirx > 0:
                    player.x = edge_tx * TILE - player.w
                else:
                    player.x = (edge_tx + 1) * TILE
                player.vx = 0.0
                break

    # vertical
    player.y += player.vy * dt
    r = player.rect
    x0, x1, y0, y1 = rect_to_tile_range(r)
    player.on_ground = False
    if player.vy != 0:
        diry = sign(player.vy)
        edge_ty = y1 if diry > 0 else y0
        for tx in range(x0, x1+1):
            if is_solid(world, tx, edge_ty):
                if diry > 0:
                    player.y = edge_ty * TILE - player.h
                    player.on_ground = True
                else:
                    player.y = (edge_ty + 1) * TILE
                player.vy = 0.0
                break

# ---------------------------
# Rendering
# ---------------------------
def draw_world(screen, world, camx, camy):
    # visible tiles
    tx0 = int(camx // TILE) - 2
    ty0 = int(camy // TILE) - 2
    tx1 = int((camx + W) // TILE) + 2
    ty1 = int((camy + H) // TILE) + 2

    for ty in range(ty0, ty1+1):
        if ty < 0 or ty >= WORLD_H:
            continue
        for tx in range(tx0, tx1+1):
            if tx < 0 or tx >= WORLD_W:
                continue
            bid = world[ty][tx]
            if bid == 0:
                continue
            x = tx * TILE - camx
            y = ty * TILE - camy
            pygame.draw.rect(screen, COL[bid], (x, y, TILE, TILE))

            # quick top highlight for grass
            if bid == 3:
                pygame.draw.rect(screen, (120, 210, 120), (x, y, TILE, 4))

            # tile outline
            pygame.draw.rect(screen, (0,0,0), (x, y, TILE, TILE), 1)

def draw_ui(screen, font, player, mining_prog, mining_target, fps):
    # HP bar
    pygame.draw.rect(screen, (30,30,30), (20, 20, 220, 18))
    hpw = int(220 * (player.hp / player.max_hp))
    pygame.draw.rect(screen, (200,60,60), (20, 20, hpw, 18))
    pygame.draw.rect(screen, (0,0,0), (20, 20, 220, 18), 2)
    screen.blit(font.render(f"HP {player.hp}/{player.max_hp}", True, (240,240,240)), (250, 17))

    # Hotbar
    bar_w = 9 * 54
    startx = (W - bar_w) // 2
    y = H - 70
    for i in range(9):
        x = startx + i*54
        rect = pygame.Rect(x, y, 50, 50)
        pygame.draw.rect(screen, (45,45,45), rect)
        pygame.draw.rect(screen, (220,220,220) if i == player.selected else (0,0,0), rect, 3)

        bid = player.hotbar[i]
        if bid != 0:
            pygame.draw.rect(screen, COL[bid], (x+12, y+12, 26, 26))
            amt = player.inventory[bid]
            screen.blit(font.render(str(amt), True, (255,255,255)), (x+4, y+30))
            screen.blit(font.render(BLOCK_NAME.get(bid,"?"), True, (230,230,230)), (x-2, y+52))

    # mining progress
    if mining_target is not None:
        tx, ty = mining_target
        pct = clamp(mining_prog, 0.0, 1.0)
        pygame.draw.rect(screen, (30,30,30), (20, 48, 220, 10))
        pygame.draw.rect(screen, (120,200,255), (20, 48, int(220*pct), 10))
        pygame.draw.rect(screen, (0,0,0), (20, 48, 220, 10), 2)
        screen.blit(font.render(f"Mining {pct*100:.0f}%", True, (230,230,230)), (250, 41))

    screen.blit(font.render(f"{fps:.0f} FPS", True, (230,230,230)), (W-110, 12))

# ---------------------------
# Main
# ---------------------------
def main():
    screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption("Mini Terraria (Pygame)")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("arial", 16)
    big = pygame.font.SysFont("arial", 22, bold=True)

    world, hmap = generate_world()

    # spawn on surface middle
    sx = WORLD_W // 2
    sy = hmap[sx] - 6
    player = Player(sx*TILE, sy*TILE)

    # camera
    camx = player.x - W/2
    camy = player.y - H/2

    mining_target = None
    mining_timer = 0.0
    mining_needed = 0.5
    mining_progress = 0.0

    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0
        fps = clock.get_fps()

        # ---------------------------
        # Events
        # ---------------------------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if pygame.K_1 <= event.key <= pygame.K_9:
                    player.selected = event.key - pygame.K_1

        keys = pygame.key.get_pressed()

        # ---------------------------
        # Input + Physics
        # ---------------------------
        ax = 0.0
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            ax -= 1.0
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            ax += 1.0

        # accelerate to target speed
        target = ax * MOVE_SPEED
        accel = 2600.0 if player.on_ground else 1500.0
        player.vx += (target - player.vx) * clamp(accel*dt, 0.0, 1.0)

        # friction if no input
        if ax == 0.0:
            fr = FRICTION_GROUND if player.on_ground else FRICTION_AIR
            player.vx -= player.vx * clamp(fr*dt, 0.0, 1.0)

        # jump
        if (keys[pygame.K_SPACE] or keys[pygame.K_w] or keys[pygame.K_UP]) and player.on_ground:
            player.vy = -JUMP_VEL

        # gravity
        player.vy += GRAVITY * dt
        player.vy = clamp(player.vy, -2000, 2600)

        move_and_collide(player, world, dt)

        # ---------------------------
        # Camera follow
        # ---------------------------
        camx += ((player.x + player.w/2) - (camx + W/2)) * clamp(8.0*dt, 0.0, 1.0)
        camy += ((player.y + player.h/2) - (camy + H/2)) * clamp(8.0*dt, 0.0, 1.0)
        camx = clamp(camx, 0, WORLD_W*TILE - W)
        camy = clamp(camy, 0, WORLD_H*TILE - H)

        # ---------------------------
        # Mouse interactions (mine/place)
        # ---------------------------
        mx, my = pygame.mouse.get_pos()
        world_x = mx + camx
        world_y = my + camy
        tx, ty = tile_at(world_x, world_y)

        # limit reach
        reach = 6.0 * TILE
        px = player.x + player.w/2
        py = player.y + player.h/2
        dist = math.hypot(world_x - px, world_y - py)
        in_reach = dist <= reach

        mouse = pygame.mouse.get_pressed()
        left = mouse[0]
        right = mouse[2]

        # Mining
        if left and in_reach and 0 <= tx < WORLD_W and 0 <= ty < WORLD_H:
            bid = world[ty][tx]
            if bid != 0:
                if mining_target != (tx, ty):
                    mining_target = (tx, ty)
                    mining_timer = 0.0
                    mining_needed = MINING_TIME.get(bid, 0.6)
                mining_timer += dt
                mining_progress = mining_timer / mining_needed
                if mining_timer >= mining_needed:
                    world[ty][tx] = 0
                    player.give_block(bid, 1)
                    mining_timer = 0.0
                    mining_progress = 0.0
                    mining_target = None
            else:
                mining_target = None
                mining_timer = 0.0
                mining_progress = 0.0
        else:
            mining_target = None
            mining_timer = 0.0
            mining_progress = 0.0

        # Placing (single-click style)
        if right and in_reach and 0 <= tx < WORLD_W and 0 <= ty < WORLD_H:
            bid = player.hotbar[player.selected]
            # place only into air
            if world[ty][tx] == 0 and bid != 0 and player.inventory[bid] > 0:
                # prevent placing inside player
                place_rect = pygame.Rect(tx*TILE, ty*TILE, TILE, TILE)
                if not place_rect.colliderect(player.rect):
                    # torch is non-solid; others solid
                    world[ty][tx] = bid
                    player.inventory[bid] -= 1
            pygame.time.wait(90)  # crude debounce

        # ---------------------------
        # Render
        # ---------------------------
        screen.fill((120, 190, 255))  # sky
        draw_world(screen, world, camx, camy)

        # highlight target
        if in_reach and 0 <= tx < WORLD_W and 0 <= ty < WORLD_H:
            hx = tx*TILE - camx
            hy = ty*TILE - camy
            pygame.draw.rect(screen, (255, 255, 255), (hx, hy, TILE, TILE), 2)

        # player
        pr = pygame.Rect(int(player.x - camx), int(player.y - camy), int(player.w), int(player.h))
        pygame.draw.rect(screen, (80, 80, 95), pr)             # body
        pygame.draw.rect(screen, (0, 0, 0), pr, 2)             # outline
        pygame.draw.rect(screen, (210, 190, 170), (pr.x+6, pr.y+6, pr.w-12, 14))  # head band

        # UI
        draw_ui(screen, font, player, mining_progress, mining_target, fps)

        # help text
        screen.blit(big.render("A/D move  |  SPACE jump  |  LMB mine  |  RMB place  |  1-9 hotbar", True, (20,20,20)),
                    (20, H-120))

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()