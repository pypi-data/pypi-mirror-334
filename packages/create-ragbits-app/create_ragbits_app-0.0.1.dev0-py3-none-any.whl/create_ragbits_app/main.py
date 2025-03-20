import asyncio
import os
import shutil
import pathlib
import textwrap
from typing import Dict, List, Optional

from inquirer.shortcuts import list_input, text, confirm
import aiohttp
import jinja2
from jinja2.filters import FILTERS
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

from create_ragbits_app.helpers import AsciiArtCombiner

TEMPLATES_DIR = pathlib.Path(__file__).parent.parent.parent / "templates"

FILTERS['python_safe'] = lambda value: value.replace('-', '_')

console = Console()

def display_logo(version: str) -> None:
    """Display the ragbits logo with a rabbit face in ASCII art."""
    rabbit_face = textwrap.dedent("""
    [magenta bold]  __     __   
    [magenta bold] /_/|   |\_\  
    [magenta bold]  |U|___|U|   
    [magenta bold]  |       |   
    [magenta bold]  | ,   , |   
    [magenta bold] (  = Y =  )  
    [magenta bold]  |   `   |   
    [magenta bold] /|       |\\ 
    [magenta bold] \| |   | |/
    [magenta bold](_|_|___|_|_)
    [magenta bold]  '"'   '"'
    """)

    ragbits_title = textwrap.dedent(f"""
[cyan bold]▗▄▄▖  ▗▄▖  ▗▄▄▖▗▄▄▖ ▗▄▄▄▖▗▄▄▄▖▗▄▄▖
[cyan bold]▐▌ ▐▌▐▌ ▐▌▐▌   ▐▌ ▐▌  █    █ ▐▌   
[cyan bold]▐▛▀▚▖▐▛▀▜▌▐▌▝▜▌▐▛▀▚▖  █    █  ▝▀▚▖
[cyan bold]▐▌ ▐▌▐▌ ▐▌▝▚▄▞▘▐▙▄▞▘▗▄█▄▖  █ ▗▄▄▞▘

[cyan bold]Current version: [magenta bold]{version}[/magenta bold]
[cyan bold]Docs: [magenta bold underline]https://ragbits.deepsense.ai[/magenta bold underline]
    """)


    combined = AsciiArtCombiner.combine(rabbit_face, ragbits_title, AsciiArtCombiner.Config(vertical_offset=2))

    logo_panel = Panel.fit(
        combined,
        border_style="cyan",
        padding=(0, 1),
    )

    console.print(logo_panel)

async def get_latest_ragbits_version():
    url = 'https://pypi.org/pypi/ragbits/json'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            response = await response.json()
            return response['info']['version']

def get_available_templates() -> List[str]:
    """Get list of available templates from templates directory."""
    if not TEMPLATES_DIR.exists():
        return []
    
    return [d.name for d in TEMPLATES_DIR.iterdir() if d.is_dir()]

def get_template_config(template_name: str) -> Dict:
    """Get template configuration if available."""
    config_path = TEMPLATES_DIR / template_name / "template_config.py"
    if not config_path.exists():
        return {}
    
    # Simple approach to load config - in a real app you might want to use importlib
    config = {}
    with open(config_path, "r") as f:
        exec(f.read(), config)
    
    return config

def prompt_template_questions(template_config: Dict) -> Dict:
    """Prompt user for template-specific questions."""
    answers = {}
    questions = template_config.get("questions", [])
    
    for question in questions:
        q_type = question.get("type", "text")
        q_name = question.get("name")
        q_message = question.get("message", q_name)
        q_choices = question.get("choices", [])
        q_default = question.get("default")
        
        if q_type == "list" and q_choices:
            answers[q_name] = list_input(q_message, choices=q_choices, default=q_default)
        elif q_type == "confirm":
            answers[q_name] = confirm(q_message, default=q_default)
        else:  # Default to text input
            answers[q_name] = text(q_message, default=q_default)
    
    return answers

def create_project(template_name: str, project_path: str, context: Dict) -> None:
    """Create a new project from the selected template."""
    template_path = TEMPLATES_DIR / template_name
    
    # Create project directory if it doesn't exist
    os.makedirs(project_path, exist_ok=True)
    
    # Process all template files and directories
    for item in template_path.glob("**/*"):
        if item.name == "template_config.py":
            continue  # Skip template config file
            
        # Get relative path from template root
        rel_path = str(item.relative_to(template_path))
        
        # Process path parts for Jinja templating (for directory names)
        path_parts = []
        for part in pathlib.Path(rel_path).parts:
            if "{{" in part and "}}" in part:
                # Render the directory name as a template
                name_template = jinja2.Template(part)
                rendered_part = name_template.render(**context)
                path_parts.append(rendered_part)
            else:
                path_parts.append(part)
        
        # Construct the target path with processed directory names
        target_rel_path = os.path.join(*path_parts) if path_parts else ""
        target_path = pathlib.Path(project_path) / target_rel_path
        
        if item.is_dir():
            os.makedirs(target_path, exist_ok=True)
        elif item.is_file():
            # Process as template if it's a .j2 file
            if item.suffix == ".j2":
                with open(item, "r") as f:
                    template_content = f.read()
                
                # Render template with context
                template = jinja2.Template(template_content)
                rendered_content = template.render(**context)
                
                # Save to target path without .j2 extension
                target_path = target_path.with_suffix("")
                with open(target_path, "w") as f:
                    f.write(rendered_content)
            else:
                # Create parent directories if they don't exist
                os.makedirs(target_path.parent, exist_ok=True)
                # Simple file copy
                shutil.copy2(item, target_path)
    
    print(f"Project created successfully at {project_path}")

async def run():
    version = await get_latest_ragbits_version()
    display_logo(version)

    # Get available templates
    templates = get_available_templates()
    if not templates:
        print("No templates found. Please create templates in the 'templates' directory.")
        return
    
    # Let user select a template
    selected_template = list_input(
        "Select a template to use",
        choices=templates
    )
    
    # Get project name
    project_name = text("Project name:", default=f"ragbits-{selected_template}")
    project_path = os.path.abspath(project_name)
    
    # Check if directory exists and is not empty
    if os.path.exists(project_path) and os.listdir(project_path):
            print(f"Directory '{project_name}' already exists and is not empty. Project creation aborted.")
            return
    
    # Get template config and prompt for questions
    template_config = get_template_config(selected_template)
    answers = prompt_template_questions(template_config)
    
    # Create context for template rendering
    context = {
        "project_name": project_name,
        "ragbits_version": version,
        **answers
    }
    
    # Create project from template
    create_project(selected_template, project_path, context)

def entrypoint():
    # asyncio.run(run())
    print("This is a placeholder for the entrypoint function. Please update the create-ragbits-app package.")