#!/usr/bin/env python3
"""
WebGuvenligi CLI Interface
Command-line security scanner
"""

import argparse
import json
import sys
from pathlib import Path
from datetime import datetime

from core.scanner import SecurityScanner
from gui.report_generator import ReportGenerator

def main():
    parser = argparse.ArgumentParser(
        description="WebGuvenligi - Advanced Web Security Scanner",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Examples:
  python cli.py --url http://target.com --scan-type all
  python cli.py --url http://target.com --scan-type sqli,xss
  python cli.py --batch urls.txt --output report.html
  python cli.py --url http://target.com --method POST --proxy http://127.0.0.1:8080
        """
    )
    
    # Target specification
    target_group = parser.add_mutually_exclusive_group(required=True)
    target_group.add_argument('-u', '--url', help='Single target URL')
    target_group.add_argument('-b', '--batch', help='Batch file with URLs (one per line)')
    
    # Scan options
    parser.add_argument(
        '-t', '--scan-type',
        default='all',
        help='Scan type: sqli,xss,ssrf,csrf,clickjacking or "all" (default: all)'
    )
    parser.add_argument(
        '-m', '--method',
        default='GET',
        choices=['GET', 'POST', 'PUT', 'PATCH', 'DELETE'],
        help='HTTP method (default: GET)'
    )
    parser.add_argument(
        '--timeout',
        type=int,
        default=10,
        help='Request timeout in seconds (default: 10)'
    )
    parser.add_argument(
        '--threads',
        type=int,
        default=5,
        help='Number of threads (default: 5)'
    )
    parser.add_argument(
        '--proxy',
        help='Proxy URL (e.g., http://127.0.0.1:8080)'
    )
    
    # Output options
    parser.add_argument(
        '-o', '--output',
        help='Output file for report (HTML, JSON, PDF)'
    )
    parser.add_argument(
        '-f', '--format',
        default='html',
        choices=['html', 'json', 'pdf'],
        help='Report format (default: html)'
    )
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Verbose output'
    )
    
    args = parser.parse_args()
    
    # Parse scan types
    scan_types = []
    if args.scan_type.lower() == 'all':
        scan_types = ['sqli', 'xss', 'ssrf', 'csrf', 'clickjacking']
    else:
        scan_types = [s.strip().lower() for s in args.scan_type.split(',')]
    
    # Initialize scanner
    proxy_dict = None
    if args.proxy:
        proxy_dict = {'http': args.proxy, 'https': args.proxy}
    
    scanner = SecurityScanner(
        proxy=proxy_dict,
        timeout=args.timeout,
        threads=args.threads
    )
    
    # Prepare URLs
    urls = []
    if args.url:
        urls = [args.url]
    elif args.batch:
        try:
            with open(args.batch, 'r') as f:
                urls = [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            print(f"❌ Batch file not found: {args.batch}")
            sys.exit(1)
    
    print(f"\n🔍 WebGuvenligi Security Scanner v1.0")
    print(f"Created by ST \\ For WebGuvenligi")
    print(f"{'='*50}")
    print(f"📋 Target URLs: {len(urls)}")
    print(f"🧪 Scan Types: {', '.join(scan_types)}")
    print(f"⚙️  HTTP Method: {args.method}")
    print(f"👥 Threads: {args.threads}")
    print(f"{'='*50}\n")
    
    # Perform scan
    try:
        if len(urls) == 1:
            print(f"🔐 Scanning {urls[0]}...\n")
            result = scanner.scan(urls[0], scan_types, args.method)
        else:
            print(f"🔐 Batch scanning {len(urls)} URLs...\n")
            result = scanner.batch_scan(urls, scan_types, args.method)
        
        # Display results
        summary = scanner.get_results_summary()
        print(f"\n{'='*50}")
        print(f"✅ Scan Complete!")
        print(f"{'='*50}")
        print(f"📊 Summary:")
        print(f"   Total Vulnerabilities: {summary['total_vulnerabilities']}")
        for vuln_type, count in summary['by_type'].items():
            if count > 0:
                print(f"   - {vuln_type}: {count}")
        print(f"\n")
        
        # Generate report
        if args.output:
            report_gen = ReportGenerator()
            
            if args.format == 'html':
                report_content = report_gen.generate_html_report(scanner.scan_history)
            elif args.format == 'json':
                report_content = json.dumps(scanner.scan_history, indent=2)
            else:
                print("⚠️  PDF format not yet implemented")
                report_content = report_gen.generate_html_report(scanner.scan_history)
            
            output_file = args.output
            if not output_file.endswith(f'.{args.format}'):
                output_file += f'.{args.format}'
            
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(report_content)
            
            print(f"💾 Report saved: {output_file}")
        
        # Detailed output if verbose
        if args.verbose and scanner.scan_history:
            print(f"\n{'='*50}")
            print("📝 Detailed Results:")
            print(f"{'='*50}\n")
            
            for idx, scan in enumerate(scanner.scan_history, 1):
                print(f"Scan #{idx}: {scan['url']}")
                for vuln in scan.get('vulnerabilities', []):
                    print(f"  ⚠️  {vuln.get('type', 'Unknown')}")
                    print(f"      Payload: {vuln.get('payload', 'N/A')[:60]}")
                    print(f"      Severity: {vuln.get('severity', 'N/A')}")
                    print()
    
    except KeyboardInterrupt:
        print("\n⚠️  Scan interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
