#!/usr/bin/env python3
"""
Main GUI Window - WebGuvenligi Security Scanner
Created by ST \\ For WebGuvenligi
"""

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTabWidget, QPushButton, QLineEdit, QLabel,
    QListWidget, QListWidgetItem, QTextEdit, QComboBox,
    QCheckBox, QSpinBox, QFileDialog, QProgressBar,
    QTableWidget, QTableWidgetItem, QSplitter, QMessageBox,
    QGroupBox, QFormLayout
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QColor, QIcon, QFont
from PyQt6.QtCore import QTimer
import json
from datetime import datetime
from pathlib import Path

from core.scanner import SecurityScanner
from .scanner_thread import ScannerThread
from .report_generator import ReportGenerator

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("WebGuvenligi - Advanced Security Scanner")
        self.setGeometry(100, 100, 1400, 900)
        
        self.scanner = SecurityScanner()
        self.scanner_thread = None
        self.report_generator = ReportGenerator()
        
        self._setup_ui()
        self._connect_signals()
    
    def _setup_ui(self):
        """Setup UI components"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Create tabs
        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs)
        
        # Tab 1: Scan Configuration
        self.tabs.addTab(self._create_scan_tab(), "Scan Configuration")
        
        # Tab 2: Results
        self.tabs.addTab(self._create_results_tab(), "Results")
        
        # Tab 3: Reports
        self.tabs.addTab(self._create_reports_tab(), "Reports")
        
        # Tab 4: Payloads
        self.tabs.addTab(self._create_payloads_tab(), "Payloads")
        
        # Status bar
        self.statusBar().showMessage("Ready")
    
    def _create_scan_tab(self) -> QWidget:
        """Create scan configuration tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # URL Input
        url_layout = QHBoxLayout()
        url_layout.addWidget(QLabel("Target URL:"))
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("http://example.com")
        url_layout.addWidget(self.url_input)
        layout.addLayout(url_layout)
        
        # Batch URLs
        batch_layout = QHBoxLayout()
        batch_layout.addWidget(QLabel("Batch URLs (one per line):"))
        self.batch_input = QTextEdit()
        self.batch_input.setMaximumHeight(100)
        batch_layout.addWidget(self.batch_input)
        layout.addLayout(batch_layout)
        
        # Scan Options Group
        options_group = QGroupBox("Scan Options")
        options_layout = QFormLayout()
        
        # HTTP Method
        self.method_combo = QComboBox()
        self.method_combo.addItems(["GET", "POST", "PUT", "PATCH", "DELETE"])
        options_layout.addRow("HTTP Method:", self.method_combo)
        
        # Threads
        self.threads_spin = QSpinBox()
        self.threads_spin.setValue(5)
        self.threads_spin.setMinimum(1)
        self.threads_spin.setMaximum(20)
        options_layout.addRow("Threads:", self.threads_spin)
        
        # Timeout
        self.timeout_spin = QSpinBox()
        self.timeout_spin.setValue(10)
        self.timeout_spin.setMinimum(1)
        self.timeout_spin.setMaximum(60)
        options_layout.addRow("Timeout (s):", self.timeout_spin)
        
        options_group.setLayout(options_layout)
        layout.addWidget(options_group)
        
        # Scan Types
        types_group = QGroupBox("Scan Types")
        types_layout = QVBoxLayout()
        
        self.sqli_check = QCheckBox("SQL Injection (500+ payloads)")
        self.sqli_check.setChecked(True)
        types_layout.addWidget(self.sqli_check)
        
        self.xss_check = QCheckBox("Cross-Site Scripting (300+ payloads)")
        self.xss_check.setChecked(True)
        types_layout.addWidget(self.xss_check)
        
        self.ssrf_check = QCheckBox("SSRF (200+ payloads)")
        self.ssrf_check.setChecked(True)
        types_layout.addWidget(self.ssrf_check)
        
        self.csrf_check = QCheckBox("CSRF Protection Check")
        self.csrf_check.setChecked(True)
        types_layout.addWidget(self.csrf_check)
        
        self.clickjacking_check = QCheckBox("Clickjacking Detection")
        self.clickjacking_check.setChecked(True)
        types_layout.addWidget(self.clickjacking_check)
        
        types_group.setLayout(types_layout)
        layout.addWidget(types_group)
        
        # Proxy
        proxy_layout = QHBoxLayout()
        proxy_layout.addWidget(QLabel("Proxy (optional):"))
        self.proxy_input = QLineEdit()
        self.proxy_input.setPlaceholderText("http://127.0.0.1:8080")
        proxy_layout.addWidget(self.proxy_input)
        layout.addLayout(proxy_layout)
        
        # Progress
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        self.start_btn = QPushButton("▶ Start Scan")
        self.start_btn.setStyleSheet("""
            background-color: #2ecc71;
            color: white;
            padding: 10px;
            border-radius: 5px;
            font-weight: bold;
        """)
        button_layout.addWidget(self.start_btn)
        
        self.stop_btn = QPushButton("⏹ Stop Scan")
        self.stop_btn.setStyleSheet("""
            background-color: #e74c3c;
            color: white;
            padding: 10px;
            border-radius: 5px;
            font-weight: bold;
        """)
        self.stop_btn.setEnabled(False)
        button_layout.addWidget(self.stop_btn)
        
        self.clear_btn = QPushButton("🗑 Clear")
        button_layout.addWidget(self.clear_btn)
        
        layout.addLayout(button_layout)
        layout.addStretch()
        
        return widget
    
    def _create_results_tab(self) -> QWidget:
        """Create results tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Summary
        summary_layout = QHBoxLayout()
        summary_layout.addWidget(QLabel("Total Vulnerabilities:"))
        self.total_label = QLabel("0")
        self.total_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        summary_layout.addWidget(self.total_label)
        
        summary_layout.addWidget(QLabel("  SQLi:"))
        self.sqli_label = QLabel("0")
        summary_layout.addWidget(self.sqli_label)
        
        summary_layout.addWidget(QLabel("  XSS:"))
        self.xss_label = QLabel("0")
        summary_layout.addWidget(self.xss_label)
        
        summary_layout.addStretch()
        layout.addLayout(summary_layout)
        
        # Results Table
        self.results_table = QTableWidget()
        self.results_table.setColumnCount(6)
        self.results_table.setHorizontalHeaderLabels([
            "Type", "URL", "Payload", "Severity", "Parameter", "Timestamp"
        ])
        self.results_table.setColumnWidth(0, 120)
        self.results_table.setColumnWidth(1, 250)
        self.results_table.setColumnWidth(2, 250)
        layout.addWidget(self.results_table)
        
        return widget
    
    def _create_reports_tab(self) -> QWidget:
        """Create reports tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Report options
        options_layout = QHBoxLayout()
        
        self.report_format = QComboBox()
        self.report_format.addItems(["HTML", "JSON", "PDF"])
        options_layout.addWidget(QLabel("Format:"))
        options_layout.addWidget(self.report_format)
        
        self.generate_report_btn = QPushButton("📄 Generate Report")
        options_layout.addWidget(self.generate_report_btn)
        
        self.export_btn = QPushButton("💾 Export Results")
        options_layout.addWidget(self.export_btn)
        
        options_layout.addStretch()
        layout.addLayout(options_layout)
        
        # Report preview
        self.report_text = QTextEdit()
        self.report_text.setReadOnly(True)
        layout.addWidget(QLabel("Report Preview:"))
        layout.addWidget(self.report_text)
        
        return widget
    
    def _create_payloads_tab(self) -> QWidget:
        """Create payloads tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Payload type selector
        type_layout = QHBoxLayout()
        type_layout.addWidget(QLabel("Payload Type:"))
        self.payload_type = QComboBox()
        self.payload_type.addItems(["sqli", "xss", "ssrf", "csrf", "clickjacking"])
        type_layout.addWidget(self.payload_type)
        type_layout.addStretch()
        layout.addLayout(type_layout)
        
        # Payloads list
        self.payloads_list = QListWidget()
        layout.addWidget(QLabel("Available Payloads:"))
        layout.addWidget(self.payloads_list)
        
        # Payload details
        layout.addWidget(QLabel("Payload Details:"))
        self.payload_details = QTextEdit()
        self.payload_details.setMaximumHeight(150)
        layout.addWidget(self.payload_details)
        
        # Custom payload
        self.custom_payload_input = QTextEdit()
        self.custom_payload_input.setMaximumHeight(100)
        layout.addWidget(QLabel("Add Custom Payload:"))
        layout.addWidget(self.custom_payload_input)
        
        self.add_custom_btn = QPushButton("➕ Add Payload")
        layout.addWidget(self.add_custom_btn)
        
        return widget
    
    def _connect_signals(self):
        """Connect UI signals"""
        self.start_btn.clicked.connect(self._start_scan)
        self.stop_btn.clicked.connect(self._stop_scan)
        self.clear_btn.clicked.connect(self._clear_scan)
        self.generate_report_btn.clicked.connect(self._generate_report)
        self.export_btn.clicked.connect(self._export_results)
        self.payload_type.currentTextChanged.connect(self._load_payloads)
        self.add_custom_btn.clicked.connect(self._add_custom_payload)
        self.payloads_list.itemClicked.connect(self._show_payload_details)
    
    def _start_scan(self):
        """Start security scan"""
        url = self.url_input.text().strip()
        batch_urls = [u.strip() for u in self.batch_input.toPlainText().split('\n') if u.strip()]
        
        if not url and not batch_urls:
            QMessageBox.warning(self, "Error", "Please enter a URL or batch URLs")
            return
        
        # Prepare scan parameters
        scan_types = []
        if self.sqli_check.isChecked():
            scan_types.append('sqli')
        if self.xss_check.isChecked():
            scan_types.append('xss')
        if self.ssrf_check.isChecked():
            scan_types.append('ssrf')
        if self.csrf_check.isChecked():
            scan_types.append('csrf')
        if self.clickjacking_check.isChecked():
            scan_types.append('clickjacking')
        
        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.statusBar().showMessage("Scanning...")
        
        # Run scan in thread
        self.scanner_thread = ScannerThread(
            self.scanner, url, batch_urls, scan_types,
            self.method_combo.currentText()
        )
        self.scanner_thread.progress.connect(self._update_progress)
        self.scanner_thread.result.connect(self._on_scan_complete)
        self.scanner_thread.start()
    
    def _stop_scan(self):
        """Stop current scan"""
        if self.scanner_thread and self.scanner_thread.isRunning():
            self.scanner_thread.requestInterruption()
            self.scanner_thread.wait()
        
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.progress_bar.setVisible(False)
        self.statusBar().showMessage("Scan stopped")
    
    def _clear_scan(self):
        """Clear all inputs and results"""
        self.url_input.clear()
        self.batch_input.clear()
        self.results_table.setRowCount(0)
        self.scanner.results = {'sqli': [], 'xss': [], 'ssrf': [], 'csrf': [], 'clickjacking': []}
        self._update_summary()
    
    def _update_progress(self, value: int):
        """Update progress bar"""
        self.progress_bar.setValue(value)
    
    def _on_scan_complete(self, results: list):
        """Handle scan completion"""
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.progress_bar.setVisible(False)
        
        # Display results
        self._display_results(results)
        self._update_summary()
        self.statusBar().showMessage(f"Scan complete: Found {len(results)} vulnerabilities")
    
    def _display_results(self, results: list):
        """Display scan results in table"""
        self.results_table.setRowCount(0)
        
        for result in results:
            row_position = self.results_table.rowCount()
            self.results_table.insertRow(row_position)
            
            self.results_table.setItem(row_position, 0, QTableWidgetItem(result.get('type', '')))
            self.results_table.setItem(row_position, 1, QTableWidgetItem(result.get('url', '')))
            self.results_table.setItem(row_position, 2, QTableWidgetItem(result.get('payload', '')[:50]))
            self.results_table.setItem(row_position, 3, QTableWidgetItem(result.get('severity', '')))
            self.results_table.setItem(row_position, 4, QTableWidgetItem(result.get('param', '')))
            self.results_table.setItem(row_position, 5, QTableWidgetItem(
                datetime.now().strftime('%H:%M:%S')
            ))
    
    def _update_summary(self):
        """Update summary statistics"""
        total = sum(len(v) for v in self.scanner.results.values())
        self.total_label.setText(str(total))
        self.sqli_label.setText(str(len(self.scanner.results['sqli'])))
        self.xss_label.setText(str(len(self.scanner.results['xss'])))
    
    def _generate_report(self):
        """Generate HTML report"""
        if not self.scanner.scan_history:
            QMessageBox.warning(self, "Error", "No scan results to generate report")
            return
        
        report_html = self.report_generator.generate_html_report(self.scanner.scan_history)
        self.report_text.setText(report_html)
        
        # Save report
        filename, _ = QFileDialog.getSaveFileName(self, "Save Report", "", "HTML Files (*.html)")
        if filename:
            with open(filename, 'w') as f:
                f.write(report_html)
            QMessageBox.information(self, "Success", f"Report saved to {filename}")
    
    def _export_results(self):
        """Export results as JSON"""
        filename, _ = QFileDialog.getSaveFileName(self, "Export Results", "", "JSON Files (*.json)")
        if filename:
            with open(filename, 'w') as f:
                json.dump(self.scanner.scan_history, f, indent=2)
            QMessageBox.information(self, "Success", f"Results exported to {filename}")
    
    def _load_payloads(self):
        """Load payloads for selected type"""
        payload_type = self.payload_type.currentText()
        payloads = self.scanner.payload_manager.get_payloads(payload_type)
        
        self.payloads_list.clear()
        for payload in payloads[:20]:  # Show first 20
            self.payloads_list.addItem(payload)
    
    def _show_payload_details(self, item):
        """Show payload details"""
        self.payload_details.setText(f"Selected Payload:\n\n{item.text()}")
    
    def _add_custom_payload(self):
        """Add custom payload"""
        payload = self.custom_payload_input.toPlainText().strip()
        if payload:
            payload_type = self.payload_type.currentText()
            self.scanner.payload_manager.add_custom_payload(payload_type, payload)
            self.custom_payload_input.clear()
            self._load_payloads()
            QMessageBox.information(self, "Success", "Custom payload added!")
