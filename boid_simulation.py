import pygame
import random
import csv

Life_Span = 900

# Parameters
WIDTH, HEIGHT = 1400, 600  # Screen dimensions
NUM_BOIDS = 50  # Number of boids
MAX_SPEED = 2  # Maximum speed of a boid
NEIGHBOR_RADIUS = 50  # Radius within which boids are considered neighbors
ALIGNMENT_WEIGHT = 0.1  # Weight of alignment behavior
COHESION_WEIGHT = 0.5  # Weight of cohesion behavior
SEPARATION_WEIGHT = 0.5  # Weight of separation behavior
AVOID_RADIUS = 50  # Radius within which obstacles are detected
MAX_AVOID_FORCE = 1.0  # Maximum force applied for obstacle avoidance

TARGET_LOCATION = pygame.math.Vector2(WIDTH - 100, HEIGHT // 2)
AVG_DIST = None

# Colors
WHITE = (255, 255, 255)  # Colour of boids
BLACK = (0, 0, 0)  # Background color
GREEN = (0, 255, 0)  # Colour of target point
RED = (255, 0, 0) # Colour of obstacles

# Create obstacles

# Define a list of predetermined positions
OB_POSITIONS = [
    (500, 0),
    (500, 25),
    (500, 50),
    (500, 75),
    #(500, 100),
    #(500, 125),
    #(500, 150),
    (500, 175),
    (500, 200),
    (500, 225),
    (500, 250),
    
    (500, 275),
    (500, 300),
    (500, 325),

    (500, 350),
    (500, 375),
    (500, 400),
    (500, 425),
    #(500, 450),
    #(500, 475),
    #(500, 500),
    (500, 525),
    (500, 550),
    (500, 575),
    (500, 600),
    # Add more positions as needed

    (700, 0),
    (700, 25),
    (700, 50),
    (700, 75),
    (700, 100),
    (700, 125),
    (700, 150),
    (700, 175),
    (700, 200),
    (700, 225),
    (700, 250),
    #(700, 275),
    #(700, 300),
    #(700, 325),
    (700, 350),
    (700, 375),
    (700, 400),
    (700, 425),
    (700, 450),
    (700, 475),
    (700, 500),
    (700, 525),
    (700, 550),
    (700, 575),
    (700, 600),

    (900, 0),
    (900, 25),
    (900, 50),
    #(900, 75),
    #(900, 100),
    #(900, 125),
    (900, 150),
    (900, 175),
    (900, 200),
    (900, 225),
    (900, 250),
    (900, 275),
    (900, 300),
    (900, 325),
    (900, 350),
    (900, 375),
    (900, 400),
    (900, 425),
    (900, 450),
    #(900, 475),
    #(900, 500),
    #(900, 525),
    (900, 550),
    (900, 575),
    (900, 600),

    (1000, 0),
    (1000, 25),
    (1000, 50),
    (1000, 75),
    (1000, 100),
    (1000, 125),
    (1000, 150),
    (1000, 175),
    (1000, 200),
    (1000, 225),
    (1000, 250),
    #(700, 275),
    #(700, 300),
    #(700, 325),
    (1100, 350),
    (1100, 375),
    (1100, 400),
    (1100, 425),
    (1100, 450),
    (1100, 475),
    (1100, 500),
    (1100, 525),
    (1100, 550),
    (1100, 575),
    (1100, 600),
]

#obstacles = [pygame.math.Vector2(random.randint(0, WIDTH), random.randint(0, HEIGHT)) for _ in range(1)]
obstacles = [pygame.math.Vector2(pos) for pos in OB_POSITIONS]

random.seed(42)

class Boid:
    def __init__(self, position, velocity):
        self.position = position  # Position of the boid
        self.velocity = velocity  # Velocity of the boid

    def update(self, flock, obstacles, target_point):
        # Initialize vectors for alignment, cohesion, and separation
        alignment = pygame.math.Vector2(0, 0)
        cohesion = pygame.math.Vector2(0, 0)
        separation = pygame.math.Vector2(0, 0)
        avoidance = pygame.math.Vector2(0, 0)
        num_neighbors = 0

        # Loop through all boids in the flock
        for boid in flock:
            if boid != self:
                # Calculate distance between this boid and the other boid
                distance = self.position.distance_to(boid.position)
                # If the other boid is within the neighbor radius
                if distance < NEIGHBOR_RADIUS:
                    # Add the velocity of the other boid to alignment
                    alignment += boid.velocity
                    # Add the position of the other boid to cohesion
                    cohesion += boid.position
                    # Add a vector pointing away from the other boid to separation
                    separation += (self.position - boid.position) / distance
                    num_neighbors += 1

        # Loop through all obstacles
        for obstacle in obstacles:
            # Calculate distance between this boid and the obstacle
            distance = self.position.distance_to(obstacle)
            # If the obstacle is within the avoidance radius
            if distance < AVOID_RADIUS:
                # Add a vector pointing away from the obstacle to avoidance
                avoidance += (self.position - obstacle) / distance

        # kill if too close to obstacle:
        for obstacle in obstacles:
            if self.position.distance_to(obstacle) < 15:
                for boid in flock:
                    if boid == self:
                        #print("Attempt to delete self")
                        
                        flock.remove(self)

        # If there are neighboring boids
        if num_neighbors > 0:
            # Calculate average alignment vector
            alignment /= num_neighbors
            alignment = alignment.normalize() * MAX_SPEED
            # Calculate average cohesion vector
            cohesion /= num_neighbors
            cohesion = (cohesion - self.position).normalize() * MAX_SPEED
            # Calculate average separation vector
            separation /= num_neighbors
            separation = separation.normalize() * MAX_SPEED

            # Update velocity based on alignment, cohesion, separation, and avoidance
            self.velocity += alignment * ALIGNMENT_WEIGHT + cohesion * COHESION_WEIGHT + separation * SEPARATION_WEIGHT + avoidance * MAX_AVOID_FORCE
            self.velocity = self.velocity.normalize() * MAX_SPEED

        # Move towards the target point
        desired_direction = (target_point - self.position).normalize()
        self.velocity += desired_direction * ALIGNMENT_WEIGHT
        self.velocity = self.velocity.normalize() * MAX_SPEED

        # Update position based on velocity
        self.position += self.velocity

        # Reverse velocity if boid hits the edge of the screen
        if self.position.x <= 0 or self.position.x >= WIDTH:
            self.velocity.x *= -1
        if self.position.y <= 0 or self.position.y >= HEIGHT:
            self.velocity.y *= -1

    def draw(self, screen):
        # Draw the boid as a circle on the screen
        pygame.draw.circle(screen, WHITE, (int(self.position.x), int(self.position.y)), 5)

def average_dist_from_target(flock):
    distance = 0
    for boid in flock:
        distance += boid.position.distance_to(TARGET_LOCATION)

    return distance  / len(flock)

def run(
        num_boids = NUM_BOIDS, 
        max_speed = MAX_SPEED, 
        neighbor_radius = NEIGHBOR_RADIUS,
        alignment_weight = ALIGNMENT_WEIGHT,
        cohesion_weight = COHESION_WEIGHT,
        separation_weight = SEPARATION_WEIGHT,
        avoid_radius = AVOID_RADIUS,
        max_avoid_force = MAX_AVOID_FORCE,
        show_graphics = True
        ):

    global NUM_BOIDS
    global MAX_SPEED # Maximum speed of a boid
    global NEIGHBOR_RADIUS # Radius within which boids are considered neighbors
    global ALIGNMENT_WEIGHT # Weight of alignment behavior
    global COHESION_WEIGHT # Weight of cohesion behavior
    global SEPARATION_WEIGHT # Weight of separation behavior
    global AVOID_RADIUS # Radius within which obstacles are detected
    global MAX_AVOID_FORCE # Maximum force applied for obstacle avoidance

    NUM_BOIDS = num_boids
    MAX_SPEED = max_speed
    NEIGHBOR_RADIUS = neighbor_radius
    ALIGNMENT_WEIGHT = alignment_weight
    COHESION_WEIGHT = cohesion_weight
    SEPARATION_WEIGHT = separation_weight
    AVOID_RADIUS = avoid_radius
    MAX_AVOID_FORCE = max_avoid_force


    # Create a flock of boids
    flock = [Boid(pygame.math.Vector2(random.randint(0, 450), random.randint(0, HEIGHT)), pygame.math.Vector2(random.uniform(-1, 1), random.uniform(-1, 1)).normalize() * MAX_SPEED) for _ in range(NUM_BOIDS)]

    if show_graphics:
        # Initialize Pygame
        pygame.init()
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Flocking Simulation")
        clock = pygame.time.Clock()

    for tick in range(0, Life_Span):  # Simulate for Life Span ticks

        # if all of the boids crash end simulation
        if len(flock) == 0:
            return avg_dist + ((num_boids - len(flock))*50)

        avg_dist = average_dist_from_target(flock=flock)
        #print(avg_dist)

        # Update and draw each boid in the flock
        for boid in flock:
            boid.update(flock, obstacles, TARGET_LOCATION)

        if show_graphics:
            # Clear the screen
            screen.fill(BLACK)

            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Draw obstacles
            for obstacle in obstacles:
                pygame.draw.circle(screen, RED, (int(obstacle.x), int(obstacle.y)), 10)

            # Draw the target point
            pygame.draw.circle(screen, GREEN, (int(TARGET_LOCATION.x), int(TARGET_LOCATION.y)), 10)

            # Update and draw each boid in the flock
            for boid in flock:
                boid.draw(screen)

            # Update the display
            pygame.display.flip()
            clock.tick(60)

    if show_graphics:
        # Quit Pygame
        pygame.quit()

    #print(f"score: {avg_dist + ((num_boids - len(flock))*50)}")
    return avg_dist + ((num_boids - len(flock))*50) # penalty for having dead boids

if __name__ == "__main__":
    run()
