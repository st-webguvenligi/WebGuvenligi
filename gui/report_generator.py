#!/usr/bin/env python3
"""HTML Report Generation"""

from typing import List, Dict
from datetime import datetime

class ReportGenerator:
    def __init__(self):
        self.template = self._get_html_template()
    
    def generate_html_report(self, scan_history: List[Dict]) -> str:
        """Generate comprehensive HTML report"""
        
        # Calculate statistics
        total_vulns = sum(len(scan.get('vulnerabilities', [])) for scan in scan_history)
        by_type = {}
        by_severity = {'Critical': 0, 'High': 0, 'Medium': 0, 'Low': 0}
        
        vulns_html = ""
        for scan in scan_history:
            for vuln in scan.get('vulnerabilities', []):
                vuln_type = vuln.get('type', 'Unknown')
                severity = vuln.get('severity', 'Medium')
                
                by_type[vuln_type] = by_type.get(vuln_type, 0) + 1
                by_severity[severity] = by_severity.get(severity, 0) + 1
                
                vulns_html += f"""
                <tr>
                    <td>{vuln_type}</td>
                    <td>{vuln.get('url', 'N/A')}</td>
                    <td><code>{vuln.get('payload', '')[:50]}</code></td>
                    <td><span class="severity-{severity.lower()}">{severity}</span></td>
                    <td>{vuln.get('param', 'N/A')}</td>
                </tr>
                """
        
        # Generate statistics
        stats_html = ""
        for vuln_type, count in by_type.items():
            stats_html += f"<li>{vuln_type}: {count}</li>"
        
        severity_html = ""
        for sev, count in by_severity.items():
            if count > 0:
                severity_html += f"<li class='severity-{sev.lower()}'>{sev}: {count}</li>"
        
        # Create report
        report = f"""
        <!DOCTYPE html>
        <html lang="tr">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>WebGuvenligi Security Report</title>
            <style>
                body {{
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    margin: 0;
                    padding: 20px;
                    background-color: #f5f5f5;
                }}
                .container {{
                    max-width: 1200px;
                    margin: 0 auto;
                    background-color: white;
                    border-radius: 8px;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                    padding: 30px;
                }}
                header {{
                    border-bottom: 3px solid #2c3e50;
                    padding-bottom: 20px;
                    margin-bottom: 30px;
                }}
                h1 {{
                    color: #2c3e50;
                    margin: 0;
                }}
                .subtitle {{
                    color: #7f8c8d;
                    font-size: 14px;
                    margin-top: 5px;
                }}
                .summary {{
                    display: grid;
                    grid-template-columns: repeat(4, 1fr);
                    gap: 20px;
                    margin-bottom: 30px;
                }}
                .summary-card {{
                    padding: 20px;
                    border-radius: 8px;
                    text-align: center;
                    background-color: #ecf0f1;
                }}
                .summary-card h3 {{
                    margin: 0 0 10px 0;
                    color: #7f8c8d;
                    font-size: 14px;
                }}
                .summary-card .value {{
                    font-size: 32px;
                    font-weight: bold;
                    color: #2c3e50;
                }}
                table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin-top: 20px;
                }}
                th, td {{
                    padding: 12px;
                    text-align: left;
                    border-bottom: 1px solid #ecf0f1;
                }}
                th {{
                    background-color: #34495e;
                    color: white;
                    font-weight: bold;
                }}
                tr:hover {{
                    background-color: #f8f9fa;
                }}
                .severity-critical {{
                    color: #e74c3c;
                    font-weight: bold;
                }}
                .severity-high {{
                    color: #e67e22;
                    font-weight: bold;
                }}
                .severity-medium {{
                    color: #f39c12;
                    font-weight: bold;
                }}
                .severity-low {{
                    color: #27ae60;
                    font-weight: bold;
                }}
                code {{
                    background-color: #f4f4f4;
                    padding: 2px 6px;
                    border-radius: 3px;
                    font-family: 'Courier New', monospace;
                    font-size: 12px;
                }}
                .section {{
                    margin-top: 30px;
                }}
                .section h2 {{
                    color: #2c3e50;
                    border-left: 4px solid #3498db;
                    padding-left: 15px;
                    margin-bottom: 20px;
                }}
                ul {{
                    list-style-position: inside;
                }}
                footer {{
                    margin-top: 40px;
                    padding-top: 20px;
                    border-top: 1px solid #ecf0f1;
                    text-align: center;
                    color: #7f8c8d;
                    font-size: 12px;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <header>
                    <h1>🔒 WebGuvenligi Security Assessment Report</h1>
                    <p class="subtitle">Created by ST \\ For WebGuvenligi</p>
                    <p class="subtitle">Report generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                </header>
                
                <div class="summary">
                    <div class="summary-card">
                        <h3>Total Vulnerabilities</h3>
                        <div class="value" style="color: #e74c3c;">{total_vulns}</div>
                    </div>
                    <div class="summary-card">
                        <h3>Critical Issues</h3>
                        <div class="value" style="color: #e74c3c;">{by_severity.get('Critical', 0)}</div>
                    </div>
                    <div class="summary-card">
                        <h3>High Priority</h3>
                        <div class="value" style="color: #e67e22;">{by_severity.get('High', 0)}</div>
                    </div>
                    <div class="summary-card">
                        <h3>Medium Risk</h3>
                        <div class="value" style="color: #f39c12;">{by_severity.get('Medium', 0)}</div>
                    </div>
                </div>
                
                <div class="section">
                    <h2>📊 Vulnerability Distribution</h2>
                    <ul>
                        {stats_html}
                    </ul>
                </div>
                
                <div class="section">
                    <h2>🔍 Severity Breakdown</h2>
                    <ul>
                        {severity_html}
                    </ul>
                </div>
                
                <div class="section">
                    <h2>📋 Detailed Findings</h2>
                    <table>
                        <thead>
                            <tr>
                                <th>Vulnerability Type</th>
                                <th>Target URL</th>
                                <th>Payload</th>
                                <th>Severity</th>
                                <th>Parameter</th>
                            </tr>
                        </thead>
                        <tbody>
                            {vulns_html}
                        </tbody>
                    </table>
                </div>
                
                <div class="section">
                    <h2>⚠️ Recommendations</h2>
                    <ul>
                        <li><strong>SQL Injection:</strong> Use parameterized queries and prepared statements</li>
                        <li><strong>XSS:</strong> Implement Content Security Policy (CSP) and output encoding</li>
                        <li><strong>SSRF:</strong> Validate and sanitize URLs, implement URL whitelisting</li>
                        <li><strong>CSRF:</strong> Implement CSRF tokens and SameSite cookie attributes</li>
                        <li><strong>Clickjacking:</strong> Set X-Frame-Options and CSP frame-ancestors</li>
                    </ul>
                </div>
                
                <footer>
                    <p>This report was generated by WebGuvenligi Security Scanner v1.0</p>
                    <p>For security concerns, contact your security team immediately</p>
                </footer>
            </div>
        </body>
        </html>
        """
        
        return report
    
    def _get_html_template(self) -> str:
        """Get base HTML template"""
        return ""
