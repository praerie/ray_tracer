from __future__ import annotations
from dataclasses import dataclass
from .tuples import Tuple, point, vector

@dataclass
class Projectile:
    position: Tuple
    velocity: Tuple

@dataclass
class Environment:
    gravity: Tuple
    wind: Tuple

def step(env: Environment, proj: Projectile) -> Projectile:
    """Advance the projectile by one time step."""
    new_position = proj.position + proj.velocity
    new_velocity = proj.velocity + env.gravity + env.wind
    return Projectile(new_position, new_velocity)

p = Projectile(position=point(0, 1, 0), velocity=vector(1, 1, 0))
env = Environment(gravity=vector(0, -0.1, 0), wind=vector(-0.01, 0, 0))

steps = 0
print(f"Step {steps}: position={p.position}, velocity={p.velocity}")

while p.position.y > 0:
    p = step(env, p)
    steps += 1
    print(f"Step {steps}: position={p.position}, velocity={p.velocity}")
