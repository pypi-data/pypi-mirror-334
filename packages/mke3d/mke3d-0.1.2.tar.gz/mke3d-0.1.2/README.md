# MKE_3d - Mk Engine 3d

#### This is a simple 3D game engine built with Python, Pygame, and OpenGL. It provides a basic framework for creating 3D games and simulation applications.

## Table of Contents

1. [Features](#features)
2. [Installation](#installation)
3. [Structure](#structure)
4. [Main Components](#main-components)
5. [Usage](#usage)
6. [Example](#usage-script-exemple)

## Features

- 3D rendering with OpenGL
- Camera system with collision detection
- Actor/GameObject system
- Mesh loading from JSON files
- Texture mapping support
- Basic collision detection
- Basic physical system
- Basic lighting system
- Event handling system

## Installation

IF YOU USAGE WINDOWS, DONT FORGOT INSTALL `window-curses`:

```
pip install window-curses
```

## Structure

The engine is organized into several modules:

- `core.py`: Contains the main `Engine` class that handles the game loop and OpenGL setup.
- `camera.py`: Implements the `Camera` player class for 3D navigation.
- `actor.py`: Defines the `Actor` class for game objects.
- `mesh.py`: Contains the `Mesh` class for storing 3D model data.
- `methods.py`: Contains function `load_mesh_on_file` and `load_texture_on_file`.

## Main Components

### Engine

The `Engine` class is the core of the game engine. It handles:

- Initializing Pygame and OpenGL
- Managing the game loop
- Handling user input
- Updating and rendering game objects

### Camera

The `Camera` class manages the 3D view. It supports:

- Camera movement (WASD keys)
- Camera rotation (mouse input)

### Actor

The `Actor` class represents game objects in the 3D world. It:

- Stores position and mesh data
- Handles rendering of the object

### Mesh

The `Mesh` class stores the vertex and face data for 3D models.

## Usage

To use the engine, follow these steps:

1. Create an instance of the `Engine` class.
2. Load 3D models using `load_mesh_on_file` or generate meshes functions in `mke3d.mashes` module.
3. Load textures using `load_texture_on_file`.
4. Create `Actor` instances with the loaded meshes and textures.
5. Add the actors to the engine using `add_game_object`.
6. Call the `run` method on the engine to start the game loop.

## Usage script exemple:

```python
from mke3d import Engine, Actor, Camera, HUD, Light, load_texture_on_file
from mke3d.meshes import gen_sphere
from pygame import Vector3
import math

player = Camera((5, 5, 40), collision=True)
game = Engine(player=player)

blue_texture = load_texture_on_file(file="sun_texture.png")
planet_texture_1 = load_texture_on_file(file="planet_texture_1.png")
planet_texture_2 = load_texture_on_file(file="planet_texture_2.png")

light = Light(
    position=(0, 0, 0),
    color=(1.0, 1.0, 1.0),
    ambient=2.3,
    diffuse=8000,
    specular=0.5
)
game.add_light(light)

sun_actor = Actor(
    position=(0, 0, 0),
    rotation=(0, 0, 0),
    mesh=gen_sphere(radius=3.1, segments=64),
    texture=blue_texture,
    collision=True
)
game.add_game_object(sun_actor)

small_planet = Actor(
    position=(0, 0, 16),
    rotation=(0, 0, 0),
    mesh=gen_sphere(radius=0.8, segments=256), # If you have a weak PC, you can reduce the number of polygons.
    texture=planet_texture_1,
    collision=True
)
game.add_game_object(small_planet)

big_planet = Actor(
    position=(0, 0, 23),
    rotation=(0, 0, 0),
    mesh=gen_sphere(radius=1.6, segments=512), # If you have a weak PC, you can reduce the number of polygons.
    texture=planet_texture_2,
    collision=True
)
game.add_game_object(big_planet)

orbit_radius = 16
orbit_radius_2 = 23
simulating_speed = 0.7
angle_1 = 0
rotation_angle_1 = 0
angle_2 = 11
rotation_angle_2 = 7

def update_planet_orbit():
    global angle_1
    global rotation_angle_1
    angle_1 += simulating_speed / 170
    x = math.cos(angle_1) * orbit_radius
    z = math.sin(angle_1) * orbit_radius
    small_planet.position = Vector3(x, 0, z)

    rotation_angle_1 += simulating_speed
    small_planet.rotation = Vector3(0, rotation_angle_1, 20)

    global angle_2
    global rotation_angle_2
    angle_2 += simulating_speed / 200
    x = math.cos(angle_2) * orbit_radius_2
    z = math.sin(angle_2) * orbit_radius_2
    big_planet.position = Vector3(x, 0, z)

    rotation_angle_2 += simulating_speed
    big_planet.rotation = Vector3(0, rotation_angle_2, 20)

def update_fps_hud():
    hud = HUD(
        font_class=game.fonts.default,
        text=f"FPS: {game.clock.get_fps():.1f}",
        color=(255, 255, 255),
        position=(200, 150)
    )
    game.hud_component.update_hud(uuid="FPS_HUD", hud=hud)

def update_player_pos_hud():
    hud = HUD(
        font_class=game.fonts.default_2,
        text=f"Player pos: {player.position}",
        color=(255, 255, 255),
        position=(200, 170)
    )
    game.hud_component.update_hud(uuid="PLAYER_POS_HUD", hud=hud)

game.add_update_function(func=update_planet_orbit)
game.add_update_function(func=update_player_pos_hud)
game.add_update_function(func=update_fps_hud)

game.run()
```
