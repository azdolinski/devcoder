#!/usr/bin/env python3
"""
GitHub Actions Workflow Analyzer and Mermaid Diagram Generator - Simplified
"""

import sys
import re
from pathlib import Path
from typing import Dict, List, Set, Optional
from dataclasses import dataclass, field
from collections import defaultdict

try:
    import ruamel.yaml
    yaml_loader = ruamel.yaml.YAML(typ='safe', pure=True)
    yaml_loader.preserve_quotes = True
except ImportError:
    yaml_loader = None


@dataclass
class Trigger:
    type: str
    details: Dict[str, any] = field(default_factory=lambda: {})


@dataclass
class Job:
    name: str
    needs: List[str] = field(default_factory=lambda: [])
    runs_on: str = "ubuntu-latest"
    environment: Optional[str] = None
    outputs: Dict[str, str] = field(default_factory=lambda: {})


@dataclass
class Workflow:
    filename: str
    name: str
    triggers: List[Trigger] = field(default_factory=lambda: [])
    jobs: Dict[str, Job] = field(default_factory=lambda: {})
    env_vars: Dict[str, str] = field(default_factory=lambda: {})


class WorkflowAnalyzer:
    def __init__(self, workflows_dir: str):
        self.workflows_dir = Path(workflows_dir)
        self.workflows: Dict[str, Workflow] = {}
        self.workflow_graph: Dict[str, Set[str]] = defaultdict(set)

    def _parse_yaml_with_on(self, filepath: Path) -> Dict:
        """Fallback YAML parser that handles 'on:' key correctly"""
        with open(filepath, 'r') as f:
            content = f.read()

        # Replace 'on:' with 'triggers:' to avoid YAML boolean parsing
        content = re.sub(r'^\s*on\s*:', 'triggers:', content, flags=re.MULTILINE)
        return yaml.safe_load(content)

    def parse_workflow_file(self, filepath: Path) -> Optional[Workflow]:
        try:
            with open(filepath, 'r') as f:
                if yaml_loader:
                    parsed = yaml_loader.load(f)
                    # Convert CommentedMap to dict
                    if hasattr(parsed, 'items'):
                        parsed = dict(parsed)
                else:
                    parsed = yaml.safe_load(f)

            if not parsed:
                return None

            # Get 'on' config
            on_config = parsed.get('on')

            if on_config is None:
                on_config = {}

            # Parse triggers
            triggers = []
            if isinstance(on_config, str):
                triggers.append(Trigger(type=on_config))
            elif isinstance(on_config, dict):
                for trigger_type, trigger_config in on_config.items():
                    details = trigger_config if trigger_config else {}
                    triggers.append(Trigger(type=trigger_type, details=details))

            # Parse jobs
            jobs = {}
            jobs_config = parsed.get('jobs', {})

            for job_name, job_config in jobs_config.items():
                # Handle needs
                needs_config = job_config.get('needs', [])
                if isinstance(needs_config, str):
                    needs_list = [needs_config]
                elif needs_config is None:
                    needs_list = []
                else:
                    needs_list = list(needs_config) if needs_config else []

                # Handle runs-on
                runs_on_config = job_config.get('runs-on', 'ubuntu-latest')
                if isinstance(runs_on_config, list):
                    runs_on_str = ', '.join(runs_on_config)
                else:
                    runs_on_str = str(runs_on_config)

                # Extract outputs
                outputs = job_config.get('outputs', {})

                job = Job(
                    name=job_name,
                    needs=needs_list,
                    runs_on=runs_on_str,
                    environment=job_config.get('environment'),
                    outputs=outputs
                )
                jobs[job_name] = job

            # Get env vars
            env_vars = parsed.get('env', {})

            workflow = Workflow(
                filename=filepath.name,
                name=parsed.get('name', filepath.stem),
                triggers=triggers,
                jobs=jobs,
                env_vars=env_vars
            )

            return workflow

        except Exception as e:
            print(f"Error parsing {filepath}: {e}")
            return None

    def analyze(self):
        if not self.workflows_dir.exists():
            print(f"Error: Directory {self.workflows_dir} does not exist")
            return

        yaml_files = list(self.workflows_dir.glob("*.yml")) + list(self.workflows_dir.glob("*.yaml"))

        for yaml_file in yaml_files:
            workflow = self.parse_workflow_file(yaml_file)
            if workflow:
                self.workflows[workflow.name] = workflow

        # Build workflow dependency graph
        for workflow_name, workflow in self.workflows.items():
            for trigger in workflow.triggers:
                if trigger.type == "workflow_run":
                    workflows = trigger.details.get("workflows", [])
                    if isinstance(workflows, str):
                        workflows = [workflows]
                    self.workflow_graph[workflow_name].update(workflows)

    def print_analysis(self):
        print("\n" + "=" * 80)
        print("GITHUB ACTIONS WORKFLOW ANALYSIS")
        print("=" * 80 + "\n")

        for workflow_name, workflow in sorted(self.workflows.items()):
            print(f"\n{'─' * 80}")
            print(f"WORKFLOW: {workflow_name}")
            print(f"File: {workflow.filename}")
            print(f"{'─' * 80}")

            print("\n🎯 TRIGGERS:")
            for trigger in workflow.triggers:
                print(f"  • {trigger.type}")
                if trigger.type == "workflow_run":
                    wfs = trigger.details.get("workflows", [])
                    types = trigger.details.get("types", [])
                    print(f"    → workflows: {wfs}")
                    print(f"    → types: {types}")

            print("\n📋 JOBS:")
            for job_name, job in workflow.jobs.items():
                print(f"\n  Job: {job_name}")
                print(f"    Runs on: {job.runs_on}")
                if job.environment:
                    print(f"    Environment: {job.environment}")
                if job.needs:
                    print(f"    Depends on: {', '.join(job.needs)}")
                if job.outputs:
                    print(f"    Outputs: {', '.join(job.outputs.keys())}")

        print("\n" + "=" * 80)
        print("WORKFLOW DEPENDENCY GRAPH")
        print("=" * 80)

        if self.workflow_graph:
            print("\n🔗 Workflow chaining:")
            for workflow, deps in sorted(self.workflow_graph.items()):
                if deps:
                    print(f"  {workflow} → {', '.join(sorted(deps))}")
        else:
            print("\n  No workflow_run triggers found")

    def generate_mermaid_diagram(self) -> str:
        lines = []

        lines.append("```mermaid")
        lines.append("flowchart TD")
        lines.append("    %% GitHub Actions Workflow Dependency Diagram")
        lines.append("")

        # Styles - dark text for better readability
        lines.append("    classDef workflow fill:#e1f5fe,stroke:#01579b,stroke-width:2px,color:#000000")
        lines.append("    classDef trigger fill:#fff3e0,stroke:#e65100,stroke-width:2px,color:#000000")
        lines.append("    classDef job fill:#f3e5f5,stroke:#4a148c,stroke-width:2px,color:#000000")
        lines.append("    classDef dataFlow fill:#e8f5e9,stroke:#1b5e20,stroke-width:2px,stroke-dasharray: 5 5,color:#000000")
        lines.append("")

        # Create subgraphs for each workflow
        for workflow_name, workflow in sorted(self.workflows.items()):
            safe_id = re.sub(r'[^a-zA-Z0-9]', '_', workflow_name)

            lines.append(f"    subgraph {safe_id}[\"{workflow_name}\"]")
            lines.append(f"        direction TB")
            lines.append("")

            # Add trigger node
            if workflow.triggers:
                trigger_list = [f"{t.type}" for t in workflow.triggers]
                trigger_desc = " | ".join(trigger_list[:2])
                lines.append(f"        {safe_id}_trigger[\"🎯 {trigger_desc}\"]:::trigger")

            # Add job nodes
            for job_name, job in workflow.jobs.items():
                job_id = f"{safe_id}_{job_name}"
                label = job_name
                if job.environment:
                    label += f"\\n(env: {job.environment})"
                lines.append(f"        {job_id}[\"📋 {label}\"]:::job")

                # Add dependencies
                for dep in job.needs:
                    dep_id = f"{safe_id}_{dep}"
                    lines.append(f"        {dep_id} --> {job_id}")

                # Add outputs
                for output_name in workflow.jobs[job_name].outputs.keys():
                    # Create safe ID from output name
                    safe_output_id = re.sub(r'[^a-zA-Z0-9]', '_', output_name)[:30]
                    # Use just the output name for the label
                    label = output_name[:20]
                    lines.append(f"        {job_id} -.->|{label}| {job_id}_{safe_output_id}['data']:::dataFlow")

            lines.append("    end")
            lines.append("")

        # Add workflow dependencies
        for workflow_name, deps in sorted(self.workflow_graph.items()):
            safe_id = re.sub(r'[^a-zA-Z0-9]', '_', workflow_name)
            for dep_workflow in deps:
                dep_id = re.sub(r'[^a-zA-Z0-9]', '_', dep_workflow)
                lines.append(f"    {dep_id}_trigger ==> |triggers| {safe_id}_trigger")

        # External triggers
        lines.append("    Push[\"📝 git push\"]:::trigger")
        lines.append("    TagPush[\"🏷️ git tag\"]:::trigger")
        lines.append("    Manual[\"⚡ Manual\"]:::trigger")
        lines.append("")

        # Connect external triggers
        for workflow_name, workflow in sorted(self.workflows.items()):
            safe_id = re.sub(r'[^a-zA-Z0-9]', '_', workflow_name)
            for trigger in workflow.triggers:
                if trigger.type == "push":
                    paths = trigger.details.get("paths", [])
                    tags = trigger.details.get("tags", [])
                    if isinstance(paths, list) and "CHANGELOG.md" in paths:
                        lines.append(f"    Push --> {safe_id}_trigger")
                    if tags:
                        lines.append(f"    TagPush --> {safe_id}_trigger")
                elif trigger.type == "workflow_dispatch":
                    lines.append(f"    Manual --> {safe_id}_trigger")

        lines.append("```")
        return "\n".join(lines)


def main():
    workflows_dir = "/mnt/self/.github/workflows"

    analyzer = WorkflowAnalyzer(workflows_dir)
    analyzer.analyze()
    analyzer.print_analysis()

    print("\n" + "=" * 80)
    print("GENERATING MERMAID DIAGRAM")
    print("=" * 80 + "\n")

    diagram = analyzer.generate_mermaid_diagram()
    print(diagram)

    # Save to file
    output_file = Path(workflows_dir) / "workflows-diagram.md"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# GitHub Actions Workflow Diagrams\n\n")
        f.write(diagram)
        f.write("\n\n## Usage\n\n")
        f.write("Copy the Mermaid code above and paste it into:\n")
        f.write("- [Mermaid Live Editor](https://mermaid.live)\n")
        f.write("- [GitHub Markdown](https://github.com/) (supports Mermaid)\n")
        f.write("- [Notion](https://notion.so/) (with Mermaid block)\n")

    print(f"\n✅ Diagram saved to: {output_file}")


if __name__ == "__main__":
    main()
