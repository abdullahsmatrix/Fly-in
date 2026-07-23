from visualize import PyGameVisualizer

# Create visualizer and run map selection
viz = PyGameVisualizer(fullscreen=True)
selected_map = viz.run()

if selected_map:
    print(f"You selected: {selected_map}")
else:
    print("No map selected")