import pygame
import random

# Parameters
WIDTH, HEIGHT = 800, 600  # Screen dimensions
NUM_BOIDS = 50  # Number of boids
MAX_SPEED = 5  # Maximum speed of a boid
NEIGHBOR_RADIUS = 50  # Radius within which boids are considered neighbors
ALIGNMENT_WEIGHT = 0.1  # Weight of alignment behavior
COHESION_WEIGHT = 0.5  # Weight of cohesion behavior
SEPARATION_WEIGHT = 0.5  # Weight of separation behavior
AVOID_RADIUS = 50  # Radius within which obstacles are detected
MAX_AVOID_FORCE = 1.0  # Maximum force applied for obstacle avoidance

# Colors
WHITE = (255, 255, 255)  # Color of boids
BLACK = (0, 0, 0)  # Background color
GREEN = (0, 255, 0)  # Color of target point

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

def main():
    # Initialize Pygame
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Flocking Simulation")
    clock = pygame.time.Clock()

    # Create a flock of boids
    flock = [Boid(pygame.math.Vector2(random.randint(0, WIDTH), random.randint(0, HEIGHT)), pygame.math.Vector2(random.uniform(-1, 1), random.uniform(-1, 1)).normalize() * MAX_SPEED) for _ in range(NUM_BOIDS)]

    # Create obstacles
    obstacles = [pygame.math.Vector2(random.randint(0, WIDTH), random.randint(0, HEIGHT)) for _ in range(5)]

    # Set a target point for the flock to move towards
    target_point = pygame.math.Vector2(WIDTH // 2, HEIGHT // 2)

    running = True
    while running:
        # Clear the screen
        screen.fill(BLACK)

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update and draw each boid in the flock
        for boid in flock:
            boid.update(flock, obstacles, target_point)
            boid.draw(screen)

        # Draw obstacles
        for obstacle in obstacles:
            pygame.draw.circle(screen, (255, 0, 0), (int(obstacle.x), int(obstacle.y)), 10)

        # Draw the target point
        pygame.draw.circle(screen, GREEN, (int(target_point.x), int(target_point.y)), 10)

        # Update the display
        pygame.display.flip()
        clock.tick(60)

    # Quit Pygame
    pygame.quit()

if __name__ == "__main__":
    main()
