#!/usr/bin/env python3
"""
BlackShannon CLI
Main entry point for the tool
"""

import click
from rich.console import Console
from rich.panel import Panel
from pathlib import Path
import sys

from src.core.config_manager import init_config, ConfigManager
from src.core.logger import get_logger
from src.core.orchestrator import Orchestrator
from src.reporting.markdown_reporter import MarkdownReporter

console = Console()


def show_banner():
    """Show ASCII banner"""
    banner = """
╔══════════════════════════════════════════════════════════╗
║                  BlackShannon v1.0                       ║
║         AI-Powered Black-Box Security Scanner            ║
║                                                          ║
║  Shannon-Inspired Methodology                            ║
║  Hybrid LLM Strategy (DeepSeek + Claude)                 ║
╚══════════════════════════════════════════════════════════╝
    """
    console.print(banner, style="cyan bold")
    console.print()


@click.command()
@click.option(
    '--target', '-t',
    required=True,
    help='Target URL to scan (e.g., https://example.com)'
)
@click.option(
    '--config', '-c',
    default='config/default_config.yaml',
    help='Configuration file path'
)
@click.option(
    '--output', '-o',
    help='Output directory for reports (default: workspace/reports/)'
)
@click.option(
    '--verbose', '-v',
    is_flag=True,
    help='Enable verbose output'
)
def main(target: str, config: str, output: str, verbose: bool):
    """
    BlackShannon - AI-Powered Black-Box Web Security Scanner
    
    Example:
        python cli.py --target https://mysite.com
    """
    
    show_banner()
    
    try:
        # Initialize configuration
        console.print("[cyan]Loading configuration...[/cyan]")
        app_config = init_config(config)
        
        # Override output if specified
        if output:
            app_config.set('output.workspace_dir', output)
        
        # Initialize logger
        logger = get_logger()
        
        # Validate target URL
        if not target.startswith(('http://', 'https://')):
            logger.error("Target URL must start with http:// or https://")
            sys.exit(1)
        
        # Warning for non-localhost targets
        from urllib.parse import urlparse
        domain = urlparse(target).netloc
        
        if 'localhost' not in domain and '127.0.0.1' not in domain:
            console.print()
            console.print(Panel(
                "[yellow]⚠️  You are about to scan a remote target!\n\n"
                f"Target: {domain}\n\n"
                "Make sure you have EXPLICIT PERMISSION to test this target.\n"
                "Unauthorized testing is ILLEGAL.[/yellow]",
                title="[red]Legal Warning[/red]",
                border_style="red"
            ))
            console.print()
            
            confirm = click.confirm('Do you have authorization to test this target?', default=False)
            if not confirm:
                logger.info("Scan cancelled by user")
                sys.exit(0)
        
        # Create orchestrator
        logger.info("Initializing BlackShannon...")
        orchestrator = Orchestrator(
            target_url=target,
            config=app_config
        )
        
        # Run scan
        results = orchestrator.run()
        
        # Check for errors
        if 'error' in results:
            logger.error(f"Scan failed: {results['error']}")
            sys.exit(1)
        
        # Generate report
        logger.phase("GENERATING REPORT")
        
        workspace = app_config.get_workspace_dir()
        reports_dir = workspace / 'reports'
        reports_dir.mkdir(parents=True, exist_ok=True)
        
        reporter = MarkdownReporter(output_dir=reports_dir)
        report_path = reporter.generate(results)
        
        logger.success(f"Report saved: {report_path}")
        
        # Final summary
        console.print()
        console.print(Panel(
            f"[green]✓ Scan Complete[/green]\n\n"
            f"Target: {target}\n"
            f"Findings: {results['total_findings']}\n"
            f"  • Exploited: {results['exploited']}\n"
            f"  • Potential: {results['potential']}\n"
            f"Report: {report_path}",
            title="[green]Summary[/green]",
            border_style="green"
        ))
        
        # Exit code based on findings
        if results['exploited'] > 0:
            sys.exit(1)  # Critical findings found
        else:
            sys.exit(0)  # No critical findings
        
    except KeyboardInterrupt:
        console.print("\n[yellow]Scan interrupted by user[/yellow]")
        sys.exit(130)
    
    except Exception as e:
        console.print(f"\n[red]Fatal error: {e}[/red]")
        if verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
