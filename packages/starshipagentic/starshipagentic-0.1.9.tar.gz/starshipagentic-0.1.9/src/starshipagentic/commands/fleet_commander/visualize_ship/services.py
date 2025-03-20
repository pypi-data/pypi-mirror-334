from starshipagentic.visualization.pygame_display import display_ship_visualization

def visualize_ship_service(input):
    """
    Service function for visualize-ship command.
    Launches a Pygame visualization of the specified ship.
    
    Args:
        input (str): Name of the ship to visualize. If None, defaults to 'enterprise'.
    
    Returns:
        str: Confirmation message
    """
    ship_name = input or 'scout'
    
    # Launch the pygame visualization
    display_ship_visualization(ship_name)
    
    return f"Visualization of {ship_name} completed."
