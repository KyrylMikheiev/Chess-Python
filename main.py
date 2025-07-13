from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import pygame
pygame.init()

from core.app import app

def main():
    app()

if __name__ == "__main__":
    main()
