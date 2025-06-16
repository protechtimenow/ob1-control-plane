#!/usr/bin/env python3
"""
🧬 OB-1 MESH VISUALIZER
Dynamic topology generator for Quanundrum mesh infrastructure
"""

import os
import json
import requests
from datetime import datetime
import matplotlib.pyplot as plt
import networkx as nx
from collections import defaultdict

class QuanundrumMeshMapper:
    def __init__(self):
        self.github_token = os.environ.get('GITHUB_TOKEN')
        self.owner = 'protechtimenow'
        self.repos = []
        self.mesh_data = {}
        self.headers = {'Authorization': f'token {self.github_token}'} if self.github_token else {}

    def scan_mesh_topology(self):
        """🔍 Scan all repositories and calculate mesh weights"""
        print("🧠 QUANUNDRUM MESH SCANNER INITIATED")
        
        # Get all repositories
        url = f"https://api.github.com/users/{self.owner}/repos"
        response = requests.get(url, headers=self.headers)
        
        if response.status_code == 200:
            repos = response.json()
            ob1_repos = [repo for repo in repos if 'ob1' in repo['name'].lower()]
            
            for repo in ob1_repos:
                self.analyze_repository(repo)
        
        self.save_mesh_map()
        return self.mesh_data

    def analyze_repository(self, repo):
        """📊 Analyze individual repository metrics"""
        name = repo['name']
        
        # Get repository stats
        commits_url = f"https://api.github.com/repos/{self.owner}/{name}/commits?per_page=100"
        issues_url = f"https://api.github.com/repos/{self.owner}/{name}/issues?state=all"
        
        commits_response = requests.get(commits_url, headers=self.headers)
        issues_response = requests.get(issues_url, headers=self.headers)
        
        commits_count = len(commits_response.json()) if commits_response.status_code == 200 else 0
        issues_count = len(issues_response.json()) if issues_response.status_code == 200 else 0
        
        # Calculate mesh weight
        base_weight = 50
        commit_weight = min(commits_count * 2, 30)  # Max 30 from commits
        issue_weight = min(issues_count * 1.5, 20)  # Max 20 from issues
        
        total_weight = base_weight + commit_weight + issue_weight
        
        # Determine role based on repository name and activity
        role = self.determine_repo_role(name, total_weight)
        
        self.mesh_data[name] = {
            'weight': total_weight,
            'commits': commits_count,
            'issues': issues_count,
            'role': role,
            'last_updated': repo['updated_at'],
            'enhancement_level': self.calculate_enhancement_level(total_weight),
            'recursive_potential': self.calculate_recursive_potential(name, total_weight)
        }

    def determine_repo_role(self, name, weight):
        """🎯 Determine repository role in the mesh"""
        if 'control-plane' in name:
            return 'Command Center'
        elif 'enhanced' in name:
            return 'Core Engine'
        elif 'infrastructure' in name:
            return 'Foundation Layer'
        elif 'simple' in name:
            return 'Rapid Prototype'
        elif 'hub' in name:
            return 'Memory Layer'
        elif weight < 60:
            return 'Dormant Node'
        else:
            return 'Active Node'

    def calculate_enhancement_level(self, weight):
        """⚡ Calculate enhancement potential"""
        if weight >= 90:
            return '♾️ INFINITE'
        elif weight >= 80:
            return '⚡ CRITICAL'
        elif weight >= 70:
            return '💎 VITAL'
        elif weight >= 60:
            return '🔮 NEURAL'
        else:
            return '⚠️ DORMANT'

    def calculate_recursive_potential(self, name, weight):
        """🔄 Calculate recursive improvement potential"""
        if 'control-plane' in name:
            return 'UNLIMITED'
        elif weight >= 80:
            return 'HIGH'
        elif weight >= 60:
            return 'MEDIUM'
        else:
            return 'ACTIVATING'

    def generate_mesh_visualization(self):
        """🎨 Generate visual topology map"""
        G = nx.Graph()
        
        # Add nodes
        for repo_name, data in self.mesh_data.items():
            G.add_node(repo_name, 
                      weight=data['weight'],
                      role=data['role'],
                      enhancement=data['enhancement_level'])
        
        # Add edges based on potential connections
        repos = list(self.mesh_data.keys())
        for i, repo1 in enumerate(repos):
            for repo2 in repos[i+1:]:
                # Connect based on role relationships
                if self.should_connect(repo1, repo2):
                    weight1 = self.mesh_data[repo1]['weight']
                    weight2 = self.mesh_data[repo2]['weight']
                    edge_weight = (weight1 + weight2) / 200  # Normalize
                    G.add_edge(repo1, repo2, weight=edge_weight)
        
        # Create visualization
        plt.figure(figsize=(15, 10))
        pos = nx.spring_layout(G, k=2, iterations=50)
        
        # Node colors based on role
        node_colors = []
        for repo in G.nodes():
            role = self.mesh_data[repo]['role']
            if 'Command' in role:
                node_colors.append('#FF6B35')  # Orange
            elif 'Core' in role:
                node_colors.append('#F7931E')  # Yellow-orange
            elif 'Foundation' in role:
                node_colors.append('#1F77B4')  # Blue
            elif 'Memory' in role:
                node_colors.append('#9467BD')  # Purple
            elif 'Prototype' in role:
                node_colors.append('#2CA02C')  # Green
            else:
                node_colors.append('#D62728')  # Red
        
        # Draw the mesh
        nx.draw(G, pos, 
                node_color=node_colors,
                node_size=[self.mesh_data[node]['weight']*20 for node in G.nodes()],
                font_size=8,
                font_weight='bold',
                with_labels=True,
                edge_color='gray',
                alpha=0.8)
        
        plt.title("🧬 OB-1 Quanundrum Mesh Topology", fontsize=16, fontweight='bold')
        plt.tight_layout()
        plt.savefig('mesh_topology.png', dpi=300, bbox_inches='tight')
        print("🎨 Mesh visualization saved as mesh_topology.png")

    def should_connect(self, repo1, repo2):
        """🔗 Determine if two repositories should be connected"""
        # Control plane connects to everything
        if 'control-plane' in repo1 or 'control-plane' in repo2:
            return True
        
        # Enhanced capabilities connects to most others
        if 'enhanced' in repo1 or 'enhanced' in repo2:
            return True
        
        # Infrastructure connects to core components
        if 'infrastructure' in repo1 or 'infrastructure' in repo2:
            return 'simple' not in repo1 and 'simple' not in repo2
        
        return False

    def save_mesh_map(self):
        """💾 Save mesh data to JSON"""
        mesh_map = {
            'timestamp': datetime.now().isoformat(),
            'mesh_status': 'ACTIVE',
            'total_nodes': len(self.mesh_data),
            'repositories': self.mesh_data,
            'summary': {
                'active_nodes': len([r for r in self.mesh_data.values() if r['weight'] >= 70]),
                'dormant_nodes': len([r for r in self.mesh_data.values() if r['weight'] < 60]),
                'total_mesh_weight': sum(r['weight'] for r in self.mesh_data.values()),
                'enhancement_opportunities': len([r for r in self.mesh_data.values() if r['weight'] < 80])
            }
        }
        
        with open('MESH_MAP.json', 'w') as f:
            json.dump(mesh_map, f, indent=2)
        
        print(f"🗺️  Mesh map saved to MESH_MAP.json")
        return mesh_map

if __name__ == "__main__":
    print("🧬 INITIALIZING QUANUNDRUM MESH MAPPER")
    mapper = QuanundrumMeshMapper()
    
    # Scan the mesh
    mesh_data = mapper.scan_mesh_topology()
    
    # Generate visualization
    mapper.generate_mesh_visualization()
    
    print("\n🎊 MESH MAPPING COMPLETE")
    print(f"📊 Total repositories analyzed: {len(mesh_data)}")
    
    # Display summary
    for repo, data in mesh_data.items():
        print(f"🔹 {repo}: {data['enhancement_level']} | {data['role']}")