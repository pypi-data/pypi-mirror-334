# Starship Agentic

**License Notice:** All source code in this repository is protected under the GNU Affero General Public License (AGPL) v3 or later. For full details, please refer to the LICENSE.md file. To help maintain legal clarity, consider adding the header from LICENSE_HEADER.txt to your source code files.

A command-line toolkit for AI-assisted software development using a sci-fi -inspired interface.

## Why Starship Agentic?

Starship Agentic transforms the software development process into an engaging, sci-fi inspired journey. It combines:

- **AI-powered development** - Leverage LLMs to generate, test, and fix code automatically
- **Guided workflow** - Follow a structured process from project initialization to deployment
- **Intuitive interface** - Use familiar Star Trek terminology for development tasks
- **Automated testing** - Run BDD and unit tests with AI-assisted error correction
- **Project management** - Track progress and maintain code quality throughout development

Whether you're building a new application or maintaining existing code, Starship Agentic helps you navigate the development universe more efficiently.

## Installation

```bash
pip install starshipagentic
```

## Requirements

- Python 3.8 or higher
- Git
- Internet connection (for AI-assisted features)
- API keys for specific LLM services (optional)

## Command Overview

Starship Agentic provides a suite of commands for managing your development workflow, organized into themed command groups.

### Main Command Structure

```
starshipagentic <command-group> <command> [options]
```

Each command is also available as a direct alias:

```
<command-alias> [options]
```

You can also simply run:

```
starshipagentic
```

Without any arguments to start the guided process from the beginning, which will help you navigate through the available commands.

## Command Groups

# Command Reference

## Fleet_commander Commands

Initialize and select project templates

| Command | Alias | Description |
|---------|-------|-------------|
| `fleet_commander tour-ship` | `tour` | Browse available ship templates/frameworks |
| `fleet_commander commission-ship` | `commission` | Clone template and run initialization |
| `fleet_commander visualize-ship` | `` | Launch a Pygame visualization of the specified ship |

## Number_two Commands

Define and expand project requirements

| Command | Alias | Description |
|---------|-------|-------------|
| `number_two mission-brief` | `mission` | Define project mission and requirements |
| `number_two expand-mission` | `expand` | Expand existing requirements |

## Engineering_officer Commands

Review and configure system architecture

| Command | Alias | Description |
|---------|-------|-------------|
| `engineering_officer review-schematics` | `schematics` | Review system architecture diagrams (MD documents for state diagram and DDD) |
| `engineering_officer calibrate-technology` | `calibrate` | Configure technology stack |

## Navigation_officer Commands

Plan feature implementation

| Command | Alias | Description |
|---------|-------|-------------|
| `navigation_officer plot-navigation` | `navigation` | Generate and review BDD gherkin feature files |
| `navigation_officer set-waypoints` | `waypoints` | Create order for working on features (project plan checklist) |

## Communications_officer Commands

Manage external data and API connections

| Command | Alias | Description |
|---------|-------|-------------|
| `communications_officer authorize-codes` | `authorize` | Configure API credentials needed for features |
| `communications_officer scan-sector` | `scan` | Search for topic to find URLs for scraping |
| `communications_officer receive-transmission` | `transmission` | Scrape or directly input information from a known URL |

## Insterstellar_officer Commands

Generate initial code tracks and connect the top down BDD step coverage

| Command | Alias | Description |
|---------|-------|-------------|
| `insterstellar_officer map-planet` | `map` | Lightweight: create initial folder, and file names scaffolding, not the BDD steps yet |
| `insterstellar_officer build-landing-zone` | `buildlz` | Create initial code tracks within the files that map-planet created |
| `insterstellar_officer fabricate-infrastructure` | `fabricate` | Generate BDD steps to connect the code laid down in the landing zone |

## Captains_orders Commands

Execute and test your implementation

| Command | Alias | Description |
|---------|-------|-------------|
| `captains_orders warp-speed` | `warp` | Top-down BDD behave driven loop (get behave errors and feed to AI to fix) |
| `captains_orders trycoder` | `trycoder` | Bottom-up unit test driven loop (get errors and feed to AI to fix) |
| `captains_orders engage` | `engage` | Run warp cycle and trycoder to repeat full set of waypoints N times |

## Tactical_officer Commands

Remove problematic code and tests

| Command | Alias | Description |
|---------|-------|-------------|
| `tactical_officer fire-photons` | `photons` | Remove specified steps that are causing trouble |
| `tactical_officer aim-lasers` | `lasers` | Remove specified code that is causing trouble |
| `tactical_officer shields-up` | `shields` | Protect code from changes (placeholder) |

## Maintenance_officer Commands

Manage project state and analyze code quality

| Command | Alias | Description |
|---------|-------|-------------|
| `maintenance_officer create-checkpoint` | `checkpoint` | Create a copy of entire folder and/or git tags |
| `maintenance_officer restore-checkpoint` | `restore` | Roll code back to checkpoint (git or folder copy) |
| `maintenance_officer inspect-vessel` | `inspect` | Run framework-specific checks to report on integrity |
| `maintenance_officer complexity-report` | `complexity` | Run radon mi and radon cc to report on code complexity issues |

## Red_buttons Commands

Special operations

| Command | Alias | Description |
|---------|-------|-------------|
| `red_buttons supernova` | `supernova` | Remove all git stuff (searches through all sub-folders) |

## Gitmaster Commands

Git-related operations

| Command | Alias | Description |
|---------|-------|-------------|
| `gitmaster teleport` | `teleport` | Take pieces of code and make a new git repo almost automatically |

## Mcars Commands

Code repository and search system

| Command | Alias | Description |
|---------|-------|-------------|
| `mcars search` | `search` | Search for code in the MCARS database |
| `mcars transport` | `transport` | Store pointers/copies of code with AI-generated summaries in tinydb |

## Droids Commands

Explanation and assistance commands

| Command | Alias | Description |
|---------|-------|-------------|
| `droids droid-splain` | `droid` | Get explanation from droid assistant |
| `droids man-splain` | `splain` | Get manual page for a topic |


## Examples

```bash
# Start the guided process
starshipagentic

# Browse available project templates
starshipagentic vessel tour-ship
# or simply
tour

# Initialize a new project (three equivalent ways)
commission django-galaxy
# or with named parameters
commission --template django-galaxy --name myproject
# or interactively (will prompt for missing information)
commission

# Generate BDD features
navigation
# or with parameters
navigation gherkin

# Run tests with AI fixing
warp 3  # shorthand for 3 iterations
# or with named parameters
warp --iterations 3

# Create a project checkpoint
checkpoint "Completed user authentication"
# or with named parameters
checkpoint --message "Completed user authentication"
# or interactively
checkpoint

# Generate code complexity report
complexity
# or with threshold parameter
complexity 15
```

## Development

To contribute to Starship Agentic:

```bash
git clone https://github.com/yourusername/starshipagentic.git
cd starshipagentic
pip install -e .
```

## Roadmap

Future features planned for Starship Agentic:

- **Universal Translator** - Convert code between different programming languages
- **Holodeck** - Interactive visualization of project architecture and dependencies
- **Prime Directive** - Automated code quality enforcement and best practices
- **Replicator** - Generate boilerplate code for common patterns
- **Away Team** - Collaborative development features for team projects
- **Temporal Mechanics** - Advanced project versioning and branching strategies
- **Federation Integration** - Connect with additional AI services and development tools

## License

The source code in this repository is licensed under the GNU Affero General Public License (AGPL) v3 or later.
Note that the CODE OUTPUT generated by this program is licensed under the MIT License.

## License Header Usage Example

To clearly communicate licensing information, include the following header snippet at the top of your source files:

```python
# Starship Agentic License Header
#
# Copyright (c) 2025 Travis Somerville and David Samson
#
# This file is part of Starship Agentic.
#
# It is licensed under the GNU Affero General Public License (AGPL) v3 or later.
# For full details, see the LICENSE.md file in the project root.
```
