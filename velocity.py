import pygame
import sys
import random
import math

# Initialize Pygame
pygame.init()

FPS = 30

# Set the dimensions of the window
WIDTH, HEIGHT = 800, 600
WINDOW_SIZE = (WIDTH, HEIGHT)
POPULATION = 100
NEIGHBOR_RADIUS = 75
COHESION = 10
ALIGNMENT = 10

MAX_SPEED = 5

SEPARATION = 5

def distance(point1, point2):
    # Unpack coordinates
    x1, y1 = point1
    x2, y2 = point2
    # Calculate Euclidean distance
    dist = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    return dist

class Circle:
    def __init__(self, 
                colour=(255, 0, 0),
                radius=5,
                vector=None,
                speed=3,
                pos=[WIDTH // 2, HEIGHT // 2]
                ):
        
        self.colour = colour
        self.radius = radius
        self.vector = vector
        self.pos = pos

        self.alignment = ALIGNMENT
        self.cohesion = COHESION
        self.separation = SEPARATION

        self.num_neighbors = 0
        self.neighbour_radius = NEIGHBOR_RADIUS


    def normalized_vector(self):
        # Calculate the magnitude of the vector
        magnitude = math.sqrt(self.vector[0]**2 + self.vector[1]**2)

        # Normalize the vector
        normalized_vector = (self.vector[0] / magnitude, self.vector[1] / magnitude)

        return normalized_vector
    
    def findNeighbours(self, list_of_agents):
        self.num_neighbors = 0

        for agent in list_of_agents:
            if distance(self.pos, agent.pos) < NEIGHBOR_RADIUS:
                self.num_neighbors += 1

        self.num_neighbors -= 1


    def wiggle(self, buzz = 0.1):
        self.vector = [self.vector[0]+random.uniform(-buzz, buzz), self.vector[1]+random.uniform(-buzz, buzz)]

        # keep vector within bounds of -1, 1
        for i in range(0,2):
            if self.vector[i] < -1:
                self.vector[i] = -1
            elif self.vector[i] > 1:
                self.vector[i] = 1

    def __str__(self):
        return f"Circle: Color={self.colour}, Position={self.pos}, Vector={self.vector}"


flock = []

# generate flock agents
for i in range(0,POPULATION):
    flock.append(
        Circle(
            colour = (random.uniform(0, 255),random.uniform(0, 255),random.uniform(0, 255)),
            radius = 10,
            vector = pygame.Vector2(random.uniform(-1, 1), random.uniform(-1, 1)).normalize() * MAX_SPEED,
            pos = pygame.Vector2(random.uniform(1, 799), random.uniform(1, 599))
        )
    )

# Set up the window
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Moving Circle")

# Colors
WHITE = (255, 255, 255)
BLACK = (0,0,0)

# Clock for controlling the frame rate
clock = pygame.time.Clock()

# Font
font = pygame.font.Font(None, 36)

# Clock
clock = pygame.time.Clock()



# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear the screen
    screen.fill(WHITE)

    # Draw Text
    fps_text = font.render(f"FPS: {round(clock.get_fps(), 2)}", True, BLACK)
    screen.blit(fps_text, (WIDTH - fps_text.get_width() - 10, 10))

    flock[0].findNeighbours(flock)
    neighbour_txt = font.render(f"N: {flock[0].num_neighbors}", True, BLACK)
    screen.blit(neighbour_txt, (WIDTH - neighbour_txt.get_width() - 10, 30))

    for agent in flock:

        agent.wiggle()
        # Update circle position based on vector
        nv = agent.normalized_vector()
        agent.pos[0] += nv[0] * agent.speed
        agent.pos[1] += nv[1] * agent.speed
        
        # Bounce off the edges of the screen
        if agent.pos[0] < 0 or agent.pos[0] > WIDTH:
            agent.vector[0] *= -1
        if agent.pos[1] < 0 or agent.pos[1] > HEIGHT:
            agent.vector[1] *= -1
    
    
    pygame.draw.circle(screen, (200,200,255), (int(flock[0].pos[0]), int(flock[0].pos[1])), NEIGHBOR_RADIUS)
    

    for agent in flock:
        # Draw the circle
        pygame.draw.circle(screen, agent.colour, (int(agent.pos[0]), int(agent.pos[1])), agent.radius)

        nv = agent.normalized_vector()
        end_point = (agent.pos[0] + (nv[0]*(agent.speed*3)), agent.pos[1] + (nv[1]*(agent.speed*3)))
        pygame.draw.line(screen, BLACK, agent.pos, end_point, 2)
    

    

    # Update the display
    pygame.display.flip()
    
    # Control frame rate
    clock.tick(FPS)

# Quit Pygame
pygame.quit()
sys.exit()