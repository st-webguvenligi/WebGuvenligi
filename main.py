#!/usr/bin/env python3
"""
WebGuvenligi - Advanced Web Security Scanner
Created by ST \\ For WebGuvenligi
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from gui.main_window import MainWindow
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
import traceback

def main():
    try:
        app = QApplication(sys.argv)
        app.setApplicationName("WebGuvenligi Security Scanner")
        app.setApplicationVersion("1.0.0")
        app.setStyle('Fusion')
        
        window = MainWindow()
        window.show()
        
        sys.exit(app.exec())
    except Exception as e:
        print(f"Fatal Error: {str(e)}")
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
