# Starship Agentic License Header
#
# Copyright (c) 2025 Travis Somerville and David Samson
#
# This file is part of Starship Agentic.
#
# It is licensed under the GNU Affero General Public License (AGPL) v3 or later.
# For full details, see the LICENSE.md file in the project root.
"""Command registry for Starship Agentic."""

import yaml
from pathlib import Path

class CommandRegistry:
    _instance = None
    _commands = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(CommandRegistry, cls).__new__(cls)
            cls._instance._load_commands()
        return cls._instance
    
    def _load_commands(self):
        """Load commands from YAML file."""
        commands_path = Path(__file__).parent.parent / "commands-list.yml"
        with open(commands_path, 'r') as f:
            self._commands = yaml.safe_load(f)
    
    def get_all_groups(self):
        """Return all command groups."""
        return self._commands.keys()
    
    def get_group_info(self, group_name):
        """Return info for a specific command group."""
        return self._commands.get(group_name, {})
    
    def get_command_info(self, group_name, command_name):
        """Return info for a specific command."""
        group = self.get_group_info(group_name)
        return group.get('commands', {}).get(command_name, {})
    
    def get_all_commands(self, group_name=None):
        """Return all commands, optionally filtered by group."""
        if group_name:
            group = self.get_group_info(group_name)
            return group.get('commands', {})
        
        all_commands = {}
        for group_name, group_data in self._commands.items():
            for cmd_name, cmd_data in group_data.get('commands', {}).items():
                all_commands[f"{group_name} {cmd_name}"] = cmd_data
        return all_commands
    
    def get_aliases_map(self):
        """Return a mapping of aliases to their full commands.
        
        Uses pyproject.toml as the source of truth for aliases.
        """
        aliases_map = {}
        
        # First try to get aliases from pyproject.toml (source of truth)
        try:
            import tomli
        except ImportError:
            try:
                import tomllib as tomli
            except ImportError:
                # If neither tomli nor tomllib is available, fall back to YAML
                for group_name, group_data in self._commands.items():
                    for cmd_name, cmd_data in group_data.get('commands', {}).items():
                        for alias in cmd_data.get('aliases', []):
                            aliases_map[alias] = (group_name, cmd_name)
                return aliases_map
        
        # Load aliases from pyproject.toml
        pyproject_path = Path(__file__).parent.parent.parent.parent / "pyproject.toml"
        if pyproject_path.exists():
            try:
                with open(pyproject_path, "rb") as f:
                    pyproject = tomli.load(f)
                
                # Extract aliases from project.scripts
                scripts = pyproject.get("project", {}).get("scripts", {})
                for alias, target in scripts.items():
                    # Skip the main command
                    if alias == "starshipagentic":
                        continue
                        
                    # Parse the target to get the group and command
                    # Format is typically: "starshipagentic.commands.group_cmds:command_name_command"
                    try:
                        module_path, func_name = target.split(":")
                        group_name = module_path.split(".")[-1].replace("_cmds", "")
                        
                        # The command function name typically ends with "_command"
                        # and is derived from the actual command name
                        cmd_func_name = func_name.replace("_command", "")
                        
                        # Convert function name to command name (replace underscores with hyphens)
                        cmd_name = cmd_func_name.replace("_", "-")
                        
                        # Find the actual command name in the YAML that matches this function name
                        for command_name in self._commands.get(group_name, {}).get('commands', {}):
                            if command_name.replace("-", "_") == cmd_func_name:
                                aliases_map[alias] = (group_name, command_name)
                                break
                    except (ValueError, KeyError, IndexError):
                        # Skip entries that don't match the expected format
                        continue
            except Exception as e:
                # Log the error but continue with fallback
                print(f"Error reading pyproject.toml: {e}")
                # Fall back to YAML
                for group_name, group_data in self._commands.items():
                    for cmd_name, cmd_data in group_data.get('commands', {}).items():
                        for alias in cmd_data.get('aliases', []):
                            aliases_map[alias] = (group_name, cmd_name)
                return aliases_map
        
        # Fall back to YAML if no aliases were found in pyproject.toml
        if not aliases_map:
            for group_name, group_data in self._commands.items():
                for cmd_name, cmd_data in group_data.get('commands', {}).items():
                    for alias in cmd_data.get('aliases', []):
                        aliases_map[alias] = (group_name, cmd_name)
        
        return aliases_map
    
    def get_example_command(self, group_name):
        """Return an example command for a group."""
        group = self.get_group_info(group_name)
        commands = group.get('commands', {})
        if not commands:
            return f"{group_name}"
        
        # Get first command as example
        cmd_name = next(iter(commands.keys()), "")
        return f"{group_name} {cmd_name}"
    
    def get_aliases_for_command(self, group_name, command_name):
        """Get aliases for a specific command from pyproject.toml."""
        aliases = []
        
        # Try to get aliases from pyproject.toml (source of truth)
        try:
            import tomli
        except ImportError:
            try:
                import tomllib as tomli
            except ImportError:
                # If neither tomli nor tomllib is available, fall back to YAML
                cmd_info = self.get_command_info(group_name, command_name)
                return cmd_info.get("aliases", [])
        
        # Load aliases from pyproject.toml
        pyproject_path = Path(__file__).parent.parent.parent.parent / "pyproject.toml"
        if pyproject_path.exists():
            try:
                with open(pyproject_path, "rb") as f:
                    pyproject = tomli.load(f)
                
                # Convert command name to function name (replace hyphens with underscores)
                cmd_func_name = command_name.replace("-", "_")
                
                # Extract aliases from project.scripts
                scripts = pyproject.get("project", {}).get("scripts", {})
                for alias, target in scripts.items():
                    # Skip the main command
                    if alias == "starshipagentic":
                        continue
                    
                    # Check if this target matches our command
                    target_pattern = f"starshipagentic.commands.{group_name}_cmds:{cmd_func_name}_command"
                    if target_pattern in target:
                        aliases.append(alias)
            except Exception as e:
                # Log the error but continue with fallback
                print(f"Error reading pyproject.toml: {e}")
                # Fall back to YAML
                cmd_info = self.get_command_info(group_name, command_name)
                return cmd_info.get("aliases", [])
        
        # Fall back to YAML if no aliases were found in pyproject.toml
        if not aliases:
            cmd_info = self.get_command_info(group_name, command_name)
            aliases = cmd_info.get("aliases", [])
        
        return aliases
    
    def validate_commands(self):
        """Validate that all commands in YAML have implementations."""
        # This would check that all commands in YAML have corresponding
        # implementations in the codebase. For now, it's a placeholder.
        return True

# Create a singleton instance
command_registry = CommandRegistry()
