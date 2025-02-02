import tkinter as tk
import random
import math
import time

# Define the window size and other constants
WINDOW_SIZE = (800, 650)  # Adjusted height to fit all particles vertically with spacing
NUM_PARTICLES = 32  # Double the number of particles
MIN_DISTANCE = 15  # 15 millimeters
PARTICLE_SIZE = 30
G = 1  # Gravitational constant for the simulation
UPDATE_INTERVAL = 16  # Milliseconds (~60fps)
MAX_SPEED = 20  # Maximum speed for the triangles

# Define colors for the triangles
COLORS = ["red", "blue", "yellow", "green", "purple", "orange", "pink", "cyan", "magenta", "lime", "turquoise", "gold", "silver", "navy", "teal", "violet"]

# Initialize particles with positions in a vertical line formation and random velocities
particles = []

center_x = WINDOW_SIZE[0] // 2  # Center X position
spacing_y = MIN_DISTANCE + PARTICLE_SIZE  # Vertical spacing between particles

for i in range(NUM_PARTICLES):
    x = center_x
    y = MIN_DISTANCE + i * spacing_y
    vx, vy = random.uniform(-2, 2), random.uniform(-2, 2)
    particles.append([x, y, vx, vy, 1, str(i + 1), PARTICLE_SIZE, COLORS[i % len(COLORS)]])

def update_positions():
    global particles
    for i, particle in enumerate(particles):
        fx, fy = 0, 0
        for j, other_particle in enumerate(particles):
            if i != j:
                dx, dy = other_particle[0] - particle[0], other_particle[1] - particle[1]
                distance_sq = dx * dx + dy * dy
                if distance_sq > 0:
                    force = G * particle[4] * other_particle[4] / distance_sq
                    fx += force * dx / math.sqrt(distance_sq)
                    fy += force * dy / math.sqrt(distance_sq)

                # Simple AI to aim for each other
                if math.sqrt(distance_sq) > MIN_DISTANCE:
                    direction_x, direction_y = dx / math.sqrt(distance_sq), dy / math.sqrt(distance_sq)
                    fx += direction_x * 0.1
                    fy += direction_y * 0.1

        particle[2] += fx / particle[4]
        particle[3] += fy / particle[4]

        # Limit the speed of the particles
        speed = math.hypot(particle[2], particle[3])
        if speed > MAX_SPEED:
            particle[2] = (particle[2] / speed) * MAX_SPEED
            particle[3] = (particle[3] / speed) * MAX_SPEED

    # Check for collisions between particles
    for i, particle in enumerate(particles):
        for j in range(i + 1, len(particles)):
            dx, dy = particles[j][0] - particle[0], particles[j][1] - particle[1]
            distance = math.hypot(dx, dy)
            if distance < particle[6] + particles[j][6]:
                nx, ny = dx / distance, dy / distance
                p = 2 * (particle[2] * nx + particle[3] * ny - particles[j][2] * nx - particles[j][3] * ny) / (particle[4] + particles[j][4])
                particle[2] -= p * particles[j][4] * nx
                particle[3] -= p * particles[j][4] * ny
                particles[j][2] += p * particle[4] * nx
                particles[j][3] += p * particle[4] * ny

    # Update positions
    for particle in particles:
        particle[0] += particle[2]
        particle[1] += particle[3]
        if particle[0] - particle[6] <= 0 or particle[0] + particle[6] >= WINDOW_SIZE[0]:
            particle[2] *= -1
        if particle[1] - particle[6] <= 0 or particle[1] + particle[6] >= WINDOW_SIZE[1]:
            particle[3] *= -1

def draw_particles(canvas):
    global particles
    canvas.delete("all")

    for particle in particles:
        x, y, size, color, label = particle[0], particle[1], particle[6], particle[7], particle[5]
        angle = math.atan2(particle[3], particle[2])
        points = [
            (x + size * math.cos(angle), y + size * math.sin(angle)),
            (x + size * math.cos(angle + 2 * math.pi / 3), y + size * math.sin(angle + 2 * math.pi / 3)),
            (x + size * math.cos(angle - 2 * math.pi / 3), y + size * math.sin(angle - 2 * math.pi / 3)),
        ]
        canvas.create_polygon(points, fill=color)
        canvas.create_text(x, y, text=label, fill="white")
        arrow_x, arrow_y = x + 25 * 1.25 * particle[2] / math.hypot(particle[2], particle[3]), y + 25 * 1.25 * particle[3] / math.hypot(particle[2], particle[3])
        canvas.create_line(x, y, arrow_x, arrow_y, fill="white", arrow=tk.LAST)

    canvas.after(UPDATE_INTERVAL, main_loop, canvas)

def main_loop(canvas):
    update_positions()
    draw_particles(canvas)

def show_loading_screen(root, main_frame, canvas):
    loading_frame = tk.Frame(root, bg="black")
    loading_frame.place(relwidth=1, relheight=1)
    tk.Label(loading_frame, text="s44b's phys", font=("Helvetica", 24), fg="white", bg="black").pack(expand=True)
    root.update()

    def simulate_loading():
        time.sleep(3)
        loading_frame.destroy()
        main_frame.pack(fill=tk.BOTH, expand=True)
        main_loop(canvas)

    root.after(100, simulate_loading)

def main():
    root = tk.Tk()
    root.title("Physics Simulation")
    root.attributes('-fullscreen', True)

    main_frame = tk.Frame(root, bg="darkgreen")
    canvas = tk.Canvas(main_frame, bg="darkgreen")
    canvas.pack(fill=tk.BOTH, expand=True)

    show_loading_screen(root, main_frame, canvas)
    root.mainloop()

if __name__ == "__main__":
    main()
