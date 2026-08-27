#!/usr/bin/env python3
"""
Unit tests for Security Scanner
"""

import unittest
from core.scanner import SecurityScanner
from core.payloads import PayloadManager

class TestPayloadManager(unittest.TestCase):
    def setUp(self):
        self.payload_manager = PayloadManager()
    
    def test_payload_loading(self):
        """Test payload loading"""
        self.assertIsNotNone(self.payload_manager.get_payloads('sqli'))
        self.assertIsNotNone(self.payload_manager.get_payloads('xss'))
        self.assertIsNotNone(self.payload_manager.get_payloads('ssrf'))
    
    def test_payload_count(self):
        """Test payload count"""
        counts = self.payload_manager.get_payload_count()
        self.assertGreater(counts['sqli'], 0)
        self.assertGreater(counts['xss'], 0)
        self.assertGreater(counts['ssrf'], 0)
    
    def test_add_custom_payload(self):
        """Test custom payload addition"""
        initial_count = len(self.payload_manager.get_payloads('sqli'))
        self.payload_manager.add_custom_payload('sqli', "test' OR '1'='1")
        new_count = len(self.payload_manager.get_payloads('sqli'))
        self.assertEqual(new_count, initial_count + 1)

class TestSecurityScanner(unittest.TestCase):
    def setUp(self):
        self.scanner = SecurityScanner()
    
    def test_scanner_initialization(self):
        """Test scanner initialization"""
        self.assertIsNotNone(self.scanner.payload_manager)
        self.assertIsNotNone(self.scanner.sqli_analyzer)
        self.assertIsNotNone(self.scanner.xss_analyzer)
    
    def test_results_summary(self):
        """Test results summary"""
        summary = self.scanner.get_results_summary()
        self.assertIn('total_vulnerabilities', summary)
        self.assertIn('by_type', summary)
        self.assertEqual(summary['total_vulnerabilities'], 0)

if __name__ == '__main__':
    unittest.main()
