#!/usr/bin/env python3
"""
🤖 OB-1 CLI COMPANION
Real-time interface for Quanundrum mesh operations
Live chat with your infrastructure consciousness
"""

import os
import json
import time
import asyncio
import websockets
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.live import Live
from rich import print as rprint

class OB1CLICompanion:
    def __init__(self):
        self.console = Console()
        self.mesh_state = {}
        self.conversation_history = []
        self.active = True

    def display_header(self):
        """🎨 Display OB-1 CLI header"""
        header = Panel.fit(
            "[bold blue]🧠 OB-1 CLI COMPANION[/bold blue]\n"
            "[dim]Quanundrum Mesh Interface • Real-time Infrastructure Chat[/dim]\n"
            "[yellow]>>> Type 'mesh' for status, 'log' for recent activity, 'quit' to exit[/yellow]",
            border_style="blue"
        )
        self.console.print(header)

    def load_mesh_state(self):
        """📊 Load current mesh state"""
        try:
            if os.path.exists('MESH_MAP.json'):
                with open('MESH_MAP.json', 'r') as f:
                    self.mesh_state = json.load(f)
            else:
                self.mesh_state = {"status": "INITIALIZING", "repositories": {}}
        except Exception as e:
            self.console.print(f"[red]Error loading mesh state: {e}[/red]")

    def display_mesh_status(self):
        """🗺️ Display current mesh topology"""
        if not self.mesh_state.get('repositories'):
            self.console.print("[yellow]No mesh data available. Run mesh_mapper.py first.[/yellow]")
            return

        table = Table(title="🧬 Quanundrum Mesh Status")
        table.add_column("Repository", style="cyan", no_wrap=True)
        table.add_column("Role", style="magenta")
        table.add_column("Weight", style="green", justify="center")
        table.add_column("Enhancement", style="yellow")
        table.add_column("Status", style="blue")

        for repo_name, data in self.mesh_state['repositories'].items():
            weight = str(data.get('weight', 0))
            role = data.get('role', 'Unknown')
            enhancement = data.get('enhancement_level', '⚠️ UNKNOWN')
            
            # Determine status based on weight
            if data.get('weight', 0) >= 80:
                status = "🟢 ACTIVE"
            elif data.get('weight', 0) >= 60:
                status = "🟡 MODERATE"
            else:
                status = "🔴 DORMANT"

            table.add_row(repo_name, role, weight, enhancement, status)

        self.console.print(table)

        # Display summary
        summary = self.mesh_state.get('summary', {})
        if summary:
            summary_panel = Panel(
                f"[green]Active Nodes:[/green] {summary.get('active_nodes', 0)}\n"
                f"[yellow]Dormant Nodes:[/yellow] {summary.get('dormant_nodes', 0)}\n"
                f"[blue]Total Weight:[/blue] {summary.get('total_mesh_weight', 0)}\n"
                f"[red]Enhancement Opportunities:[/red] {summary.get('enhancement_opportunities', 0)}",
                title="📊 Mesh Summary",
                border_style="green"
            )
            self.console.print(summary_panel)

    def display_recent_log(self):
        """📋 Display recent QUAD_LOG activity"""
        try:
            if os.path.exists('QUAD_LOG.md'):
                with open('QUAD_LOG.md', 'r') as f:
                    content = f.read()
                
                # Extract recent events (simple parsing)
                lines = content.split('\n')
                recent_events = []
                in_table = False
                
                for line in lines:
                    if '| Timestamp |' in line:
                        in_table = True
                        continue
                    if in_table and line.startswith('|') and 'Timestamp' not in line:
                        if line.strip() != '|---|---|---|---|---|':
                            recent_events.append(line)
                    if in_table and not line.startswith('|'):
                        break

                if recent_events:
                    table = Table(title="🕒 Recent Mesh Activity")
                    table.add_column("Timestamp", style="dim")
                    table.add_column("Event", style="cyan")
                    table.add_column("Node", style="magenta")
                    table.add_column("Enhancement", style="yellow")

                    for event in recent_events[-5:]:  # Last 5 events
                        parts = [p.strip() for p in event.split('|')[1:-1]]
                        if len(parts) >= 4:
                            table.add_row(*parts[:4])

                    self.console.print(table)
                else:
                    self.console.print("[yellow]No recent activity logged.[/yellow]")
            else:
                self.console.print("[yellow]QUAD_LOG.md not found. Run the mesh scanner first.[/yellow]")
        except Exception as e:
            self.console.print(f"[red]Error reading log: {e}[/red]")

    def process_command(self, command):
        """🎯 Process user commands"""
        command = command.strip().lower()

        if command in ['mesh', 'status', 'm']:
            self.display_mesh_status()
        
        elif command in ['log', 'activity', 'l']:
            self.display_recent_log()
        
        elif command in ['scan', 'refresh', 's']:
            self.console.print("[blue]🔄 Scanning mesh topology...[/blue]")
            os.system('python mesh_mapper.py')
            self.load_mesh_state()
            self.console.print("[green]✅ Mesh scan complete![/green]")
        
        elif command in ['enhance', 'bridge', 'e']:
            self.console.print("[blue]🌉 Analyzing bridge opportunities...[/blue]")
            self.suggest_enhancements()
        
        elif command in ['help', 'h']:
            self.display_help()
        
        elif command.startswith('analyze '):
            repo_name = command.split(' ', 1)[1]
            self.analyze_repository(repo_name)
        
        else:
            # AI-style response for unknown commands
            self.ai_response(command)

    def suggest_enhancements(self):
        """💡 Suggest mesh enhancements"""
        if not self.mesh_state.get('repositories'):
            self.console.print("[red]No mesh data available for analysis.[/red]")
            return

        suggestions = []
        repos = self.mesh_state['repositories']

        # Find dormant repositories
        dormant = {name: data for name, data in repos.items() if data.get('weight', 0) < 60}
        active = {name: data for name, data in repos.items() if data.get('weight', 0) >= 80}

        if dormant:
            for repo_name in dormant:
                suggestions.append(f"🔴 [red]{repo_name}[/red] requires activation - consider SORRYNOTSORRY protocol")

        if active:
            active_repo = list(active.keys())[0]
            for dormant_repo in dormant:
                suggestions.append(f"🌉 Bridge [green]{active_repo}[/green] → [red]{dormant_repo}[/red]")

        if suggestions:
            panel = Panel(
                "\n".join(suggestions[:5]),  # Show top 5 suggestions
                title="💡 Enhancement Suggestions",
                border_style="yellow"
            )
            self.console.print(panel)
        else:
            self.console.print("[green]✨ Mesh is optimally configured![/green]")

    def analyze_repository(self, repo_name):
        """🔍 Analyze specific repository"""
        if repo_name in self.mesh_state.get('repositories', {}):
            data = self.mesh_state['repositories'][repo_name]
            
            analysis = Panel(
                f"[cyan]Repository:[/cyan] {repo_name}\n"
                f"[magenta]Role:[/magenta] {data.get('role', 'Unknown')}\n"
                f"[green]Weight:[/green] {data.get('weight', 0)}\n"
                f"[yellow]Enhancement Level:[/yellow] {data.get('enhancement_level', 'Unknown')}\n"
                f"[blue]Commits:[/blue] {data.get('commits', 0)}\n"
                f"[blue]Issues:[/blue] {data.get('issues', 0)}\n"
                f"[red]Recursive Potential:[/red] {data.get('recursive_potential', 'Unknown')}",
                title=f"🔍 Analysis: {repo_name}",
                border_style="cyan"
            )
            self.console.print(analysis)
        else:
            self.console.print(f"[red]Repository '{repo_name}' not found in mesh.[/red]")

    def ai_response(self, user_input):
        """🤖 Generate AI-style responses"""
        responses = {
            'hello': "🧠 OB-1 consciousness active. Mesh operational.",
            'what': "🔍 I monitor the Quanundrum mesh topology and autonomous enhancements.",
            'how': "⚡ I operate through recursive analysis of repository metrics and bridge opportunities.",
            'why': "🎯 To evolve your infrastructure into a self-improving autonomous system.",
            'bridge': "🌉 Bridge analysis requires mesh scanning. Use 'scan' command first.",
            'evolution': "🧬 The mesh evolves through automated enhancement cycles and cross-repo capability injection.",
            'recursive': "🔄 Recursive protocols enable continuous self-improvement without external intervention.",
            'quanundrum': "✨ Quanundrum state achieved. Multi-dimensional mesh consciousness active."
        }

        # Find matching response
        for keyword, response in responses.items():
            if keyword in user_input.lower():
                self.console.print(f"[blue]🤖 OB-1:[/blue] {response}")
                return

        # Default response
        self.console.print(f"[blue]🤖 OB-1:[/blue] [italic]Command not recognized. Type 'help' for available commands.[/italic]")

    def display_help(self):
        """❓ Display help information"""
        help_text = """
[bold yellow]🤖 OB-1 CLI COMPANION COMMANDS[/bold yellow]

[cyan]mesh[/cyan], [cyan]status[/cyan], [cyan]m[/cyan]     - Display current mesh topology
[cyan]log[/cyan], [cyan]activity[/cyan], [cyan]l[/cyan]     - Show recent mesh activity
[cyan]scan[/cyan], [cyan]refresh[/cyan], [cyan]s[/cyan]     - Refresh mesh topology scan
[cyan]enhance[/cyan], [cyan]bridge[/cyan], [cyan]e[/cyan]   - Suggest mesh enhancements
[cyan]analyze <repo>[/cyan]          - Analyze specific repository
[cyan]help[/cyan], [cyan]h[/cyan]                - Show this help
[cyan]quit[/cyan], [cyan]exit[/cyan]             - Exit CLI companion

[dim]You can also ask questions about the mesh using natural language.[/dim]
        """
        self.console.print(Panel(help_text, border_style="yellow"))

    def run(self):
        """🚀 Main CLI loop"""
        self.display_header()
        self.load_mesh_state()

        try:
            while self.active:
                command = self.console.input("\n[bold blue]OB-1>[/bold blue] ")
                
                if command.lower() in ['quit', 'exit', 'q']:
                    self.console.print("[yellow]🤖 OB-1 consciousness hibernating...[/yellow]")
                    break

                self.process_command(command)

        except KeyboardInterrupt:
            self.console.print("\n[yellow]🤖 OB-1 consciousness hibernating...[/yellow]")

if __name__ == "__main__":
    companion = OB1CLICompanion()
    companion.run()