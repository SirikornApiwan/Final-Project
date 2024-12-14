import turtle
import random
import time

class Atom:
    def __init__(self, element, x, y, vx, vy, color):
        self.element = element
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.color = color
        self.turtle = turtle.Turtle()
        self.turtle.shape("circle")
        self.turtle.shapesize(2) 
        self.turtle.color(color)
        self.turtle.penup()
        self.turtle.goto(x, y)

    def move(self, boundary_width, boundary_height):
        self.x += self.vx
        self.y += self.vy

        if self.x + 10 > boundary_width or self.x - 10 < -boundary_width:
            self.vx *= -1
        if self.y + 10 > boundary_height or self.y - 10 < -boundary_height:
            self.vy *= -1

        self.turtle.goto(self.x, self.y)

    def distance(self, other):
        return ((self.x - other.x)**2 + (self.y - other.y)**2)**0.5


class WaterMolecule:
    def __init__(self, x, y, vx, vy):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.turtle = turtle.Turtle()
        self.turtle.shape("circle")
        self.turtle.shapesize(4)
        self.turtle.color("blue")
        self.turtle.penup()
        self.turtle.goto(x, y)

    def move(self, boundary_width, boundary_height):
        self.x += self.vx
        self.y += self.vy

        if self.x + 20 > boundary_width or self.x - 20 < -boundary_width:
            self.vx *= -1
        if self.y + 20 > boundary_height or self.y - 20 < -boundary_height:
            self.vy *= -1

        self.turtle.goto(self.x, self.y)


class Simulation:
    def __init__(self):
        self.screen = turtle.Screen()
        self.screen.tracer(0)
        self.screen.setup(width=800, height=600)
        self.screen.bgcolor("white")
        self.atoms = []
        self.water_molecules = []
        self.boundary_width = 380
        self.boundary_height = 280

        self.draw_boundary()

    def draw_boundary(self):
        border_turtle = turtle.Turtle()
        border_turtle.hideturtle()
        border_turtle.speed(0)
        border_turtle.penup()
        border_turtle.goto(-self.boundary_width, -self.boundary_height)
        border_turtle.pendown()
        border_turtle.pensize(3)
        border_turtle.color("black")
        for _ in range(2):
            border_turtle.forward(self.boundary_width * 2)
            border_turtle.left(90)
            border_turtle.forward(self.boundary_height * 2)
            border_turtle.left(90)

    def add_atom(self, atom):
        self.atoms.append(atom)

    def run(self):
        while True:
            for atom in self.atoms:
                atom.move(self.boundary_width, self.boundary_height)

            for water in self.water_molecules:
                water.move(self.boundary_width, self.boundary_height)

            self.check_combinations()

            self.screen.update()
            time.sleep(0.002)

    def check_combinations(self):
        oxygen_atoms = [atom for atom in self.atoms if atom.element == "O"]
        hydrogen_atoms = [atom for atom in self.atoms if atom.element == "H"]

        for oxygen in oxygen_atoms:
            close_hydrogens = [
                hydrogen for hydrogen in hydrogen_atoms
                if oxygen.distance(hydrogen) < 50
            ]
            if len(close_hydrogens) >= 2:
                self.form_water(oxygen, close_hydrogens[:2])
                break

    def form_water(self, oxygen, hydrogens):
        self.atoms.remove(oxygen)
        for hydrogen in hydrogens:
            self.atoms.remove(hydrogen)
            hydrogen.turtle.hideturtle()
        oxygen.turtle.hideturtle()

        water = WaterMolecule(
            x=oxygen.x,
            y=oxygen.y,
            vx=random.uniform(-2, 2),
            vy=random.uniform(-2, 2)
        )
        self.water_molecules.append(water)

sim = Simulation()

for _ in range(6):
    sim.add_atom(Atom("H", random.randint(-300, 300), random.randint(-200, 200),
                      random.uniform(-2, 2), random.uniform(-2, 2), "orange"))

for _ in range(3):
    sim.add_atom(Atom("O", random.randint(-300, 300), random.randint(-200, 200),
                      random.uniform(-2, 2), random.uniform(-2, 2), "purple"))

sim.run()
