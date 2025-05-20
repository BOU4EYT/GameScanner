import os
import subprocess
import platform as sys_platform
import psutil
import GPUtil
import time
import math
import ctypes
import sys
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

# OpenGL imports with alias to avoid conflicts
import OpenGL.GL as gl
import OpenGL.GLU as glu
from OpenGL.GLUT import glutInit, glutCreateWindow, glutInitWindowSize, glutInitWindowPosition, glutInitDisplayMode, GLUT_RGBA, GLUT_SINGLE

# For Windows WMI fallback
if sys_platform.system() == "Windows":
    import wmi

def get_gpu_info():
    try:
        gpus = GPUtil.getGPUs()
        if gpus:
            return gpus[0].name
    except Exception as e:
        # GPUtil failed, probably non-NVIDIA GPU or driver issue
        pass

    # Try Windows WMI fallback
    if sys_platform.system() == "Windows":
        try:
            w = wmi.WMI()
            gpus = w.Win32_VideoController()
            if gpus:
                return gpus[0].Name
        except Exception as e:
            pass

    # Fallback generic
    return "Unknown GPU"


# --- System specs function ---
def get_system_specs():
    print("Detecting system specs...")
    cpu = sys_platform.processor() or "Unknown CPU"
    ram_gb = round(psutil.virtual_memory().total / (1024 ** 3), 2)
    gpu = get_gpu_info()
    return {
        "cpu": cpu,
        "ram_gb": ram_gb,
        "gpu": gpu
    }

# --- Game detection (basic) ---
def detect_games():
    games_found = []

    # Check Minecraft by default (common folder)
    mc_path = os.path.expanduser(r"~\AppData\Roaming\.minecraft")
    if os.path.exists(mc_path):
        games_found.append("Minecraft")

    # Check Ubisoft games in default Ubisoft folder (example)
    ubisoft_path = r"C:\Program Files (x86)\Ubisoft\Ubisoft Game Launcher\games"
    if os.path.exists(ubisoft_path):
        for game_folder in os.listdir(ubisoft_path):
            games_found.append(game_folder)

    # Add Steam common games detection example
    steam_path = os.path.expandvars(r"%ProgramFiles(x86)%\Steam\steamapps\common")
    if os.path.exists(steam_path):
        for folder in os.listdir(steam_path):
            games_found.append(folder)

    # Remove duplicates and sort
    games_found = sorted(set(games_found))

    return games_found

# --- OpenGL benchmark function ---
def benchmark_opengl(duration=5):
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -5)

    num_triangles = 10000  # Increase complexity here

    start_time = time.time()
    frames = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glBegin(GL_TRIANGLES)
        for i in range(num_triangles):
            # Just random vertices for demo, could be more complex
            glColor3fv((i % 3 / 3.0, (i * 2) % 3 / 3.0, (i * 3) % 3 / 3.0))
            glVertex3fv((0, 0, 0))
            glVertex3fv((1, 0, 0))
            glVertex3fv((0, 1, 0))
        glEnd()

        pygame.display.flip()
        frames += 1

        elapsed = time.time() - start_time
        if elapsed > duration:
            break

    avg_fps = frames / elapsed
    pygame.quit()
    return avg_fps

# --- Simple settings recommendation based on specs and benchmark ---
def recommend_settings(specs, benchmark_fps, game):
    print(f"\nRecommended settings for {game} based on your system:")

    # Example logic (very simplified)
    if benchmark_fps > 100 and specs["ram_gb"] >= 16:
        return "Ultra"
    elif benchmark_fps > 60 and specs["ram_gb"] >= 8:
        return "High"
    elif benchmark_fps > 30:
        return "Medium"
    else:
        return "Low"

# --- Main menu ---
def main_menu():
    while True:
        print("\n=== Game & System Scan & Benchmark ===")
        print("1. Show system specs")
        print("2. Detect installed games")
        print("3. Run OpenGL benchmark")
        print("4. Show game recommendations")
        print("5. Exit")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            specs = get_system_specs()
            print(f"\nCPU: {specs['cpu']}")
            print(f"RAM: {specs['ram_gb']} GB")
            print(f"GPU: {specs['gpu']}")
        elif choice == "2":
            games = detect_games()
            print("\nDetected games:")
            for g in games:
                print(" -", g)
        elif choice == "3":
            fps = benchmark_opengl()
            print(f"Benchmark FPS: {fps:.2f}")
        elif choice == "4":
            specs = get_system_specs()
            games = detect_games()
            fps = benchmark_opengl()
            print("\nRecommendations:")
            for game in games:
                setting = recommend_settings(specs, fps, game)
                print(f"{game}: Recommended settings -> {setting}")
        elif choice == "5":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main_menu()
