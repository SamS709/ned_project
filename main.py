#!/usr/bin/env python3
"""
Main launcher for the Ned2 Robot Gaming Interface
This file serves as the entry point for the application.
"""

import sys
import os

# Add the GUI directory to the Python path
gui_path = os.path.join(os.path.dirname(__file__), 'GUI')
sys.path.insert(0, gui_path)

# Import and run the graphics application
from graphics import graphicsApp

if __name__ == '__main__':
    app = graphicsApp()
    app.run()
