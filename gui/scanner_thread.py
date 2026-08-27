#!/usr/bin/env python3
"""Scanner Thread for non-blocking UI"""

from PyQt6.QtCore import QThread, pyqtSignal
from typing import List, Dict

class ScannerThread(QThread):
    progress = pyqtSignal(int)
    result = pyqtSignal(list)
    
    def __init__(self, scanner, url: str, batch_urls: List[str],
                 scan_types: List[str], method: str):
        super().__init__()
        self.scanner = scanner
        self.url = url
        self.batch_urls = batch_urls
        self.scan_types = scan_types
        self.method = method
    
    def run(self):
        """Run scan in thread"""
        results = []
        
        urls_to_scan = [self.url] if self.url else self.batch_urls
        total_urls = len(urls_to_scan)
        
        try:
            for idx, url in enumerate(urls_to_scan):
                if self.isInterruptionRequested():
                    break
                
                scan_result = self.scanner.scan(url, self.scan_types, self.method)
                results.extend(scan_result.get('vulnerabilities', []))
                
                # Update progress
                progress = int((idx + 1) / total_urls * 100)
                self.progress.emit(progress)
            
            self.result.emit(results)
        except Exception as e:
            self.result.emit([{'error': str(e)}])
