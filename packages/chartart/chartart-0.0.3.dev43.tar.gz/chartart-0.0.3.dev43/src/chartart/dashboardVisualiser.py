import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import re
import json
import numpy as np
import matplotlib.ticker as mticker
import textwrap


def create_grid_from_structure(structure, debug=False):
    """
    Creates a matplotlib grid based on the nested structure.
    Layout is determined intelligently based on the element type and child ID patterns.

    IMPORTANT:
    - Rows in the output are plotted horizontally (side by side)
    - Columns in the output are plotted vertically (stacked)
    """
    if debug:
        print("Creating grid from structure...")

    # Create the figure with explicit figsize to control proportions
    # Using a taller figure helps separate the charts vertically
    fig = plt.figure(figsize=(16, 14))  # Made taller to provide more vertical space
    
    # Set a clean, modern style
    plt.style.use('ggplot')
    
    # Override some style elements for a cleaner look
    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['font.sans-serif'] = ['Arial', 'Helvetica', 'DejaVu Sans']
    plt.rcParams['axes.facecolor'] = '#f9f9f9'
    plt.rcParams['figure.facecolor'] = 'white'
    plt.rcParams['grid.color'] = '#dddddd'
    plt.rcParams['axes.grid'] = True
    plt.rcParams['axes.edgecolor'] = '#cccccc'
    plt.rcParams['axes.linewidth'] = 1.5
    plt.rcParams['xtick.color'] = '#555555'
    plt.rcParams['ytick.color'] = '#555555'
    plt.rcParams['grid.linestyle'] = '--'
    plt.rcParams['grid.linewidth'] = 0.8
    plt.rcParams['axes.spines.top'] = False
    plt.rcParams['axes.spines.right'] = False

    # Calculate the number of rows and columns in the main grid
    has_rows = 'rows' in structure and 'children' in structure['rows']
    has_columns = 'columns' in structure and 'children' in structure['columns']

    if debug:
        print(f"Has rows: {has_rows}, Has columns: {has_columns}")

    # Initialize the axes dictionary
    axes_dict = {}

    # Get the main ratio for splitting the figure
    main_ratios = structure.get('main', {}).get('ratio', [1, 1])
    
    # Create the gridspec with proper spacing
    # Using a larger wspace value to separate adjacent plots horizontally
    fig.subplots_adjust(wspace=0.4, hspace=0.4)

    # For a grid layout, split the figure into top/bottom and left/right based on main ratio
    if has_rows and has_columns:
        # Create a 2x1 grid for the main split (rows on top, columns on bottom)
        # Add very large space between main sections to prevent overlap
        main_gs = gridspec.GridSpec(2, 1, height_ratios=[0.45, 0.55], figure=fig, hspace=0.4)

        # Process rows in the top section
        if debug:
            print(f"Processing rows with ratios: {structure['rows']['ratio']}")

        row_ratios = structure['rows']['ratio']
        # MODIFIED: Main level rows are horizontal (side by side)
        rows_gs = gridspec.GridSpecFromSubplotSpec(1, len(row_ratios),
                                                subplot_spec=main_gs[0, 0],
                                                width_ratios=row_ratios,
                                                wspace=0.25)  # Added wspace

        # Process each row child - now horizontally
        for i, child in enumerate(structure['rows']['children']):
            process_element(fig, child, rows_gs[0, i], axes_dict, debug=debug)

        # Process columns in the bottom section
        if debug:
            print(f"Processing columns with ratios: {structure['columns']['ratio']}")

        col_ratios = structure['columns']['ratio']
        # MODIFIED: Main level columns are vertical (stacked)
        cols_gs = gridspec.GridSpecFromSubplotSpec(len(col_ratios), 1,
                                                subplot_spec=main_gs[1, 0],
                                                height_ratios=col_ratios,
                                                hspace=0.4)  # Added hspace

        # Process each column child - now vertically
        for i, child in enumerate(structure['columns']['children']):
            process_element(fig, child, cols_gs[i, 0], axes_dict, debug=debug)

    # Handle rows-only layout
    elif has_rows:
        if debug:
            print(f"Processing rows-only layout with ratios: {structure['rows']['ratio']}")

        # Process row children recursively
        ratios = structure['rows']['ratio']
        # MODIFIED: Main level rows are horizontal (side by side)
        gs = gridspec.GridSpec(1, len(ratios), width_ratios=ratios, figure=fig, wspace=0.25)

        for i, child in enumerate(structure['rows']['children']):
            process_element(fig, child, gs[0, i], axes_dict, debug=debug)

    # Handle columns-only layout
    elif has_columns:
        if debug:
            print(f"Processing columns-only layout with ratios: {structure['columns']['ratio']}")

        # Process column children recursively
        ratios = structure['columns']['ratio']
        # MODIFIED: Main level columns are vertical (stacked)
        gs = gridspec.GridSpec(len(ratios), 1, height_ratios=ratios, figure=fig, hspace=0.4)

        for i, child in enumerate(structure['columns']['children']):
            process_element(fig, child, gs[i, 0], axes_dict, debug=debug)

    # Add a default axis if no charts were found
    if not axes_dict:
        ax = fig.add_subplot(111)
        ax.text(0.5, 0.5, "No charts found in structure", ha='center', va='center', fontsize=14)
        ax.axis('off')

    # Don't use tight_layout as requested
    # Apply targeted axis adjustments based on the chart structure
    for ax in fig.get_axes():
        # Get the position of the axes in figure coordinates
        pos = ax.get_position()
        
        # Check chart ID and type for specific adjustments
        chart_id = ax.get_title()
        
        # Check if this is a parent chart at the top
        if 'row_0' == str(chart_id) or 'row_0 ' in str(chart_id):
            # For parent charts, make them slightly shorter to create space below
            # but not too extreme to avoid excessive spacing
            ax.set_position([pos.x0, pos.y0, pos.width, pos.height * 0.85])
            
            # For parent chart, we can also modify tick parameters
            ax.tick_params(axis='x', labelsize=7, pad=2)
            
        # For row charts that are children of the parent
        elif '_row' in str(chart_id):
            row_number = 0
            try:
                # Extract row number from ID (e.g., "row_0_row1" → 1)
                parts = str(chart_id).split('_row')
                if len(parts) > 1 and parts[1].isdigit():
                    row_number = int(parts[1])
            except:
                pass
                
            if row_number == 0:
                # First row under parent - subtle adjustment
                ax.set_position([pos.x0, pos.y0 + 0.01, pos.width, pos.height])
            elif row_number == 1:
                # Middle row - no special adjustment needed
                pass
            elif row_number == 2:
                # Last row - normal position
                pass

    return fig, axes_dict

def determine_layout_orientation(element, children, debug=False):
    """
    Determine the layout orientation based on element type and children IDs.
    IMPORTANT: For this specific application:
    - Rows in the output should be plotted as columns in matplotlib (stacked vertically)
    - Columns in the output should be plotted as rows in matplotlib (side by side horizontally)

    Returns:
        str: Either "horizontal" or "vertical"
    """
    element_id = element.get('id', '')
    element_type = element.get('type', '')

    # Check if we have child IDs that can give us a hint
    row_pattern = re.compile(r'_row\d+$')
    col_pattern = re.compile(r'_col\d+$')

    row_children = [c for c in children if row_pattern.search(c.get('id', ''))]
    col_children = [c for c in children if col_pattern.search(c.get('id', ''))]

    if debug:
        print(f"  Element {element_id} has {len(row_children)} row children and {len(col_children)} col children")

    # Look at the container name for hints
    container_is_row = "row" in element_id.lower() and "col" not in element_id.lower()
    container_is_col = "col" in element_id.lower() and "row" not in element_id.lower()

    # CHANGED LOGIC: If children have row in their IDs, they should be horizontal (side by side)
    # but if the parent is a "row" type, we want to stack them vertically
    if row_children and not col_children:
        if debug:
            print(f"  Children have row IDs, using horizontal layout")
        return "horizontal"

    # If children have col in their IDs, they should be vertical (stacked)
    elif col_children and not row_children:
        if debug:
            print(f"  Children have col IDs, using vertical layout")
        return "vertical"

    # MODIFIED: If it's explicitly a row container, use vertical layout for children
    # This is the key change - rows in output should be plotted as columns in matplotlib
    elif element_type == 'row':
        if debug:
            print(f"  Element is row type, using vertical layout instead of horizontal")
        return "vertical"  # Changed from "horizontal" to "vertical"

    # If it's explicitly a column container, use horizontal layout for children
    elif element_type == 'col':
        if debug:
            print(f"  Element is col type, using horizontal layout")
        return "horizontal"  # Changed from "vertical" to "horizontal"

    # Last resort: look at container name
    elif container_is_row:
        if debug:
            print(f"  Container name suggests row, using vertical layout")
        return "vertical"  # Changed from "horizontal" to "vertical"

    elif container_is_col:
        if debug:
            print(f"  Container name suggests column, using horizontal layout")
        return "horizontal"  # Changed from "vertical" to "horizontal"

    # Default fallback
    if debug:
        print(f"  No clear pattern, defaulting to horizontal layout")
    return "horizontal"

def process_element(fig, element, subplot_spec, axes_dict, level=0, debug=False):
    """
    Process an element in the structure (row, column, or chart).

    Parameters:
    fig: Matplotlib figure
    element: The element to process
    subplot_spec: Subplot specification for this element
    axes_dict: Dictionary to store chart axes
    level: Current nesting level
    debug: Whether to show debug information
    """
    if not element or 'type' not in element:
        return

    indent = "  " * level
    element_id = element.get('id', f"unknown_{level}")
    element_type = element.get('type')

    if debug:
        print(f"{indent}Processing {element_type}: {element_id} at level {level}")
        
    # Detect whether this is the specific row_0 chart (parent chart with nested children)
    is_parent_chart = element_id == 'row_0' and element_type == 'chart' and 'children' in element
    has_row_children = 'children' in element and any('_row' in child.get('id', '') for child in element['children'])

    # Check if this is a chart without children (leaf chart)
    if element_type == 'chart' and ('children' not in element or not element['children']):
        # For charts without children, create an axis in the specified subplot position
        if debug:
            print(f"{indent}Creating chart axis for: {element_id}")

        ax = fig.add_subplot(subplot_spec)
        axes_dict[element_id] = ax

        # Add debug info if needed
        if debug:
            ax.set_title(f"{element_id}\n{element_type}")
            ax.grid(True)

        return

    # For chart containers (charts with children), handle differently
    if element_type == 'chart' and 'children' in element and element['children']:
        if debug:
            print(f"{indent}Processing chart container: {element_id} with {len(element['children'])} children")

        # Create a composite layout that includes the parent chart at the top
        # Parent gets 30% height, children get 70% height
        # Use moderate spacing between parent and children charts
        parent_height_ratio = 0.3  # Back to standard ratio
        children_height_ratio = 0.7
        composite_gs = gridspec.GridSpecFromSubplotSpec(2, 1,
                                                        subplot_spec=subplot_spec,
                                                        height_ratios=[parent_height_ratio, children_height_ratio],
                                                        hspace=0.35)  # Moderate hspace

        # Create an axis for the parent chart at the top
        parent_ax = fig.add_subplot(composite_gs[0, 0])
        axes_dict[element_id] = parent_ax

        if debug:
            print(f"{indent}Created parent chart axis: {element_id}")

        # Check for the presence of both rowRatio and colRatio
        has_row_ratio = 'rowRatio' in element
        has_col_ratio = 'colRatio' in element

        # Create a grid in the lower section for all the children
        children_gs = composite_gs[1, 0]

        if has_row_ratio and has_col_ratio:
            # This chart container has both row and column children
            if debug:
                print(f"{indent}Chart container has both row and column children")
                print(f"{indent}Row ratios: {element['rowRatio']}")
                print(f"{indent}Column ratios: {element['colRatio']}")

            # Sort children by their ID to ensure proper ordering
            sorted_children = sorted(element['children'], key=lambda x: x['id'])

            # Group children by type (row or col prefix in ID)
            row_children = [child for child in sorted_children if '_row' in child['id']]
            col_children = [child for child in sorted_children if '_col' in child['id']]

            if debug:
                print(f"{indent}Found {len(row_children)} row children and {len(col_children)} column children")

            # Create a complex grid with both rows and columns
            # First, create a 2-row grid to separate rows and columns
            children_composite_gs = gridspec.GridSpecFromSubplotSpec(2, 1,
                                                                    subplot_spec=children_gs,
                                                                    height_ratios=[0.7, 0.3],
                                                                    hspace=0.3)  # Added hspace

            # Create row grid in the top section
            if row_children:
                row_ratios = element['rowRatio']
                row_orientation = determine_layout_orientation(element, row_children, debug)

                if row_orientation == "horizontal":
                    # Row children side by side - increased spacing
                    row_gs = gridspec.GridSpecFromSubplotSpec(1, len(row_ratios),
                                                            subplot_spec=children_composite_gs[0, 0],
                                                            width_ratios=row_ratios,
                                                            wspace=0.4)  # Increased spacing

                    # Process row children horizontally
                    for i, child in enumerate(row_children):
                        if i < len(row_ratios):
                            process_element(fig, child, row_gs[0, i], axes_dict, level+1, debug)
                else:
                    # Row children stacked
                    row_gs = gridspec.GridSpecFromSubplotSpec(len(row_ratios), 1,
                                                            subplot_spec=children_composite_gs[0, 0],
                                                            height_ratios=row_ratios,
                                                            hspace=0.4)  # Added hspace

                    # Process row children vertically
                    for i, child in enumerate(row_children):
                        if i < len(row_ratios):
                            process_element(fig, child, row_gs[i, 0], axes_dict, level+1, debug)

            # Create column grid in the bottom section
            if col_children:
                col_ratios = element['colRatio']
                col_orientation = determine_layout_orientation(element, col_children, debug)

                if col_orientation == "horizontal":
                    # Column children side by side - increased spacing
                    col_gs = gridspec.GridSpecFromSubplotSpec(1, len(col_ratios),
                                                            subplot_spec=children_composite_gs[1, 0],
                                                            width_ratios=col_ratios,
                                                            wspace=0.4)  # Increased spacing

                    # Process column children horizontally
                    for i, child in enumerate(col_children):
                        if i < len(col_ratios):
                            process_element(fig, child, col_gs[0, i], axes_dict, level+1, debug)
                else:
                    # Column children stacked
                    col_gs = gridspec.GridSpecFromSubplotSpec(len(col_ratios), 1,
                                                            subplot_spec=children_composite_gs[1, 0],
                                                            height_ratios=col_ratios,
                                                            hspace=0.4)  # Added hspace

                    # Process column children vertically
                    for i, child in enumerate(col_children):
                        if i < len(col_ratios):
                            process_element(fig, child, col_gs[i, 0], axes_dict, level+1, debug)

        # Handle row children only
        elif has_row_ratio:
            ratios = element['rowRatio']
            # Sort row children by ID for proper ordering
            row_children = sorted(
                [child for child in element['children'] if '_row' in child['id']],
                key=lambda x: x['id']
            )

            # Determine orientation based on child IDs and container type
            orientation = determine_layout_orientation(element, row_children, debug)

            if debug:
                print(f"{indent}Using {orientation} layout for row children with ratios: {ratios}")

            if orientation == "horizontal":
                # Row children side by side - increased spacing
                gs = gridspec.GridSpecFromSubplotSpec(1, len(ratios),
                                                    subplot_spec=children_gs,
                                                    width_ratios=ratios,
                                                    wspace=0.4)  # Increased spacing

                # Process children horizontally
                for i, child in enumerate(row_children):
                    if i < len(ratios):
                        process_element(fig, child, gs[0, i], axes_dict, level+1, debug)
            else:
                # Row children stacked
                gs = gridspec.GridSpecFromSubplotSpec(len(ratios), 1,
                                                    subplot_spec=children_gs,
                                                    height_ratios=ratios,
                                                    hspace=0.4)  # Added hspace

                # Process children vertically
                for i, child in enumerate(row_children):
                    if i < len(ratios):
                        process_element(fig, child, gs[i, 0], axes_dict, level+1, debug)

        # Handle column children only
        elif has_col_ratio:
            ratios = element['colRatio']
            # Sort column children by ID for proper ordering
            col_children = sorted(
                [child for child in element['children'] if '_col' in child['id']],
                key=lambda x: x['id']
            )

            # Determine orientation based on child IDs and container type
            orientation = determine_layout_orientation(element, col_children, debug)

            if debug:
                print(f"{indent}Using {orientation} layout for column children with ratios: {ratios}")

            if orientation == "horizontal":
                # Column children side by side - increased spacing
                gs = gridspec.GridSpecFromSubplotSpec(1, len(ratios),
                                                    subplot_spec=children_gs,
                                                    width_ratios=ratios,
                                                    wspace=0.4)  # Increased spacing

                # Process children horizontally
                for i, child in enumerate(col_children):
                    if i < len(ratios):
                        process_element(fig, child, gs[0, i], axes_dict, level+1, debug)
            else:
                # Column children stacked
                gs = gridspec.GridSpecFromSubplotSpec(len(ratios), 1,
                                                    subplot_spec=children_gs,
                                                    height_ratios=ratios,
                                                    hspace=0.4)  # Added hspace

                # Process children vertically
                for i, child in enumerate(col_children):
                    if i < len(ratios):
                        process_element(fig, child, gs[i, 0], axes_dict, level+1, debug)

        # If no ratios available, use a grid layout
        else:
            # Sort all children by ID for proper ordering
            sorted_children = sorted(element['children'], key=lambda x: x['id'])
            num_children = len(sorted_children)

            # Determine a reasonable grid shape
            n_cols = int(np.ceil(np.sqrt(num_children)))
            n_rows = int(np.ceil(num_children / n_cols))

            if debug:
                print(f"{indent}Using grid layout {n_rows}x{n_cols} for chart container")

            gs = gridspec.GridSpecFromSubplotSpec(n_rows, n_cols, 
                                                subplot_spec=children_gs,
                                                wspace=0.4, hspace=0.4)  # Increased spacing

            # Process children in grid layout
            for i, child in enumerate(sorted_children):
                if i < n_rows * n_cols:
                    row = i // n_cols
                    col = i % n_cols
                    process_element(fig, child, gs[row, col], axes_dict, level+1, debug)

        return

    # For other containers (row/col), create nested grid
    if 'children' not in element or not element['children']:
        if debug:
            print(f"{indent}Element {element_id} has no children, skipping")
        return

    # Get ratios for this level (default to equal if not specified)
    ratios = element.get('ratio', [1] * len(element['children']))

    if debug:
        print(f"{indent}Creating grid for {element_type} with ratios: {ratios}")

    # Sort children by ID for proper ordering
    sorted_children = sorted(element['children'], key=lambda x: x['id'])

    # Determine orientation based on child IDs and container type
    orientation = determine_layout_orientation(element, sorted_children, debug)

    if debug:
        print(f"{indent}Using {orientation} layout for children")

    # For horizontal layouts (side-by-side charts), add extra wspace
    if orientation == "horizontal":
        # Children side by side
        n_cols = len(ratios)
        n_rows = 1
        gs = gridspec.GridSpecFromSubplotSpec(n_rows, n_cols,
                                            subplot_spec=subplot_spec,
                                            width_ratios=ratios,
                                            wspace=0.4)  # Increased wspace for side-by-side plots

        # Process children
        for i, child in enumerate(sorted_children):
            if i < len(ratios):
                # Place children horizontally
                process_element(fig, child, gs[0, i], axes_dict, level+1, debug)

    else:  # vertical
        # Children stacked
        n_rows = len(ratios)
        n_cols = 1
        gs = gridspec.GridSpecFromSubplotSpec(n_rows, n_cols,
                                            subplot_spec=subplot_spec,
                                            height_ratios=ratios,
                                            hspace=0.4)  # Added hspace

        # Process children
        for i, child in enumerate(sorted_children):
            if i < len(ratios):
                # Place children vertically
                process_element(fig, child, gs[i, 0], axes_dict, level+1, debug)

def populate_chart(ax, chart_data, debug=False):
    """
    Populate a chart with data, using matplotlib's built-in text wrapping
    and layout capabilities for better alignment.

    Parameters:
    ax: Matplotlib axis
    chart_data: Chart data from the structure
    debug: Whether to show debug information
    """
    import numpy as np
    import matplotlib.pyplot as plt
    import matplotlib.ticker as mticker
    
    if debug:
        print(f"Populating chart: {chart_data.get('id')}")

    # Extract chart data
    chart_type = chart_data.get('charts')
    chart_props = chart_data.get('chartData', {})
    
    # Check chart position/type
    chart_id = chart_data.get('id', '')
    
    # Analyze chart placement:
    # 1. Is this a parent chart?
    is_parent = 'children' in chart_data and chart_data['children']
    
    # 2. Is this a top row chart? 
    is_top_row = 'row_0' == chart_id or chart_id.startswith('row_0_') 
    
    # 3. Is this a child chart?
    is_child = '_row' in chart_id or '_col' in chart_id
    
    # Set chart title and labels with position-specific adjustments
    title = chart_props.get('title', 'Chart')
    
    # Make titles shorter to avoid overlap between adjacent plots
    # Create a wrapped title that won't extend too far horizontally
    if len(title) > 25:
        # Limit title length and split into multiple lines using textwrap
        import textwrap
        wrapped_title = '\n'.join(textwrap.wrap(title, width=25))
        title = wrapped_title
    
    # Balanced title padding with bold font and custom color
    if is_parent:
        ax.set_title(title, fontsize=11, fontweight='bold', wrap=True, pad=6, color='#2F4F4F')  # Dark slate gray
    else:
        ax.set_title(title, fontsize=11, fontweight='bold', wrap=True, pad=8, color='#2F4F4F')  # Dark slate gray

    # Handle x-label placement - balanced approach
    x_label = chart_props.get('xAxisLabel')
    if x_label:
        if is_parent:
            # For parent charts, slightly reduce padding but keep readable
            ax.set_xlabel(x_label, fontsize=10, fontweight='bold', labelpad=3, color='#2F4F4F')  # Dark slate gray
        else:
            # For child charts, standard settings
            ax.set_xlabel(x_label, fontsize=10, fontweight='bold', labelpad=5, color='#2F4F4F')  # Dark slate gray

    y_label = chart_props.get('yAxisLabel')
    if y_label:
        ax.set_ylabel(y_label, fontsize=10, fontweight='bold', labelpad=5, color='#2F4F4F')  # Dark slate gray
    
    # Ensure the grid is active for all charts with consistent appearance
    ax.grid(True, linestyle='--', alpha=0.6, color='#cccccc')
    
    # Make tick labels darker and more readable
    ax.tick_params(axis='both', colors='#555555')
    for tick in ax.get_xticklabels():
        tick.set_fontsize(9)
    for tick in ax.get_yticklabels():
        tick.set_fontsize(9)

    # Adjust margins for better text fitting
    ax.margins(0.1)

    # Custom formatter for the y-axis
    class LargeNumberFormatter(mticker.FuncFormatter):
        def __call__(self, x, pos=None):
            return format_large_number(x)

    # Format function that includes currency for money values
    def format_large_number(value, pos=None):
        if value >= 1e9:
            return f'${value/1e9:.1f}B'  # Billion
        elif value >= 1e6:
            return f'${value/1e6:.1f}M'  # Million
        elif value >= 1e3:
            return f'${value/1e3:.1f}K'  # Thousand
        else:
            return f'${int(value)}'  # Small values show as whole dollars

    # Handle different chart types
    if chart_type == 'bar':
        # Bar chart
        data = chart_props.get('data', [])

        if not data:
            ax.text(0.5, 0.5, "No bar data found", ha='center', va='center')
            return

        # Get x-axis data
        x_data = None
        for series in data:
            if 'xData' in series:
                x_data = series['xData']
                break

        if not x_data:
            ax.text(0.5, 0.5, "No x-axis data found", ha='center', va='center')
            return

        # Plot each series
        x_positions = np.arange(len(x_data))
        bar_width = 0.8 / len(data)

        for i, series in enumerate(data):
            if 'yData' not in series:
                continue

            # Create a beautiful color palette for bars
            color_palette = ['#4E79A7', '#F28E2B', '#E15759', '#76B7B2', '#59A14F', '#EDC948', '#B07AA1', '#FF9DA7', '#9C755F', '#BAB0AC']
            
            # Get series properties with better colors
            offset = (i - len(data)/2 + 0.5) * bar_width
            name = series.get('name', f'Series {i+1}')
            color = series.get('color', color_palette[i % len(color_palette)])  # Use our palette if color not specified
            y_values = series['yData']

            # Plot bars with enhanced styling
            bars = ax.bar(x_positions + offset, y_values, width=bar_width, 
                        label=name, color=color, edgecolor='white', linewidth=0.8,
                        alpha=0.85)

            # Annotate y-values on bars with "6M" format with clean styling
            for bar, y_value in zip(bars, y_values):
                # Only show value if bar is tall enough
                if bar.get_height() > max(y_values) * 0.05:  # Skip very small bars
                    # Use black text for all values as requested
                    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() * 0.95,
                            format_large_number(y_value), ha='center', va='top', 
                            fontsize=9, fontweight='bold', color='black')

        # Set x-ticks and labels with intelligent rotation
        ax.set_xticks(x_positions)

        # Dynamically adjust label rotation for better readability
        max_label_len = max([len(str(x)) for x in x_data])
        n_labels = len(x_data)

        # Dynamic calculation of rotation angle
        rotation_angle = min(90, max(0, max_label_len * 2 + n_labels * 3 - 10))

        if rotation_angle > 0:
            # Adjust rotation and placement based on chart position/type
            chart_id = chart_data.get('id', '')
            is_parent = 'children' in chart_data and chart_data['children']
            is_top_row = 'row_0' == chart_id or chart_id.startswith('row_0_')
            
            # For parent charts or top row charts, optimize tick display without hiding labels
            if is_parent or is_top_row:
                # Reduce the rotation angle for parent charts
                rotation_angle = min(45, rotation_angle)  # Cap rotation at 45 degrees
                
                # Use smaller font but don't hide any labels
                ax.set_xticklabels(x_data, rotation=rotation_angle, 
                                ha='right' if rotation_angle > 0 else 'center',
                                fontsize=7)  # Small but readable font
                
                # Minimize tick padding but not too extreme
                ax.tick_params(axis='x', pad=2)
            else:
                # For other charts, use standard settings
                ax.set_xticklabels(x_data, rotation=rotation_angle, 
                                ha='right' if rotation_angle < 60 else 'center',
                                fontsize=7)  # Same font size
                ax.tick_params(axis='x', pad=4)
        else:
            ax.set_xticklabels(x_data)

        # Add a border around the figure
        for spine in ax.spines.values():
            spine.set_linewidth(1.2)
            spine.set_color('#555555')
            
        # Format y-axis numbers to "M", "K", etc.
        ax.yaxis.set_major_formatter(mticker.FuncFormatter(format_large_number))

        # Add legend with optimal positioning based on data distribution
        y_data_all = [series.get('yData', []) for series in data if 'yData' in series]

        # Determine best legend location based on data distribution
        if y_data_all:
            all_y = []
            for yd in y_data_all:
                all_y.extend(yd)

            if not all_y:
                legend_loc = 'best'
            else:
                # Find where there's the least data (top or bottom)
                max_y = max(all_y) if all_y else 0
                min_y = min(all_y) if all_y else 0
                mid_y = (max_y + min_y) / 2

                # Calculate average values in top and bottom halves
                top_values = [y for y in all_y if y > mid_y]
                bottom_values = [y for y in all_y if y <= mid_y]

                top_density = len(top_values) / len(all_y) if all_y else 0.5

                # Choose location based on data density
                if top_density > 0.6:  # More data in top half
                    legend_loc = 'lower right'
                elif top_density < 0.4:  # More data in bottom half
                    legend_loc = 'upper right'
                else:
                    legend_loc = 'best'
        else:
            legend_loc = 'best'

        # Create a clean, modern legend
        legend = ax.legend(loc=legend_loc, fontsize=9, frameon=True, framealpha=0.9, 
                        edgecolor='#dddddd', facecolor='white', 
                        title_fontsize=10, ncol=min(2, len(y_data_all)))
        
        # Add thin borders to improve legend appearance
        legend.get_frame().set_linewidth(0.8)

    elif chart_type == 'pie' or (chart_type is None and any(d.get('type') == 'pie' for d in chart_props.get('data', []))):
        # Pie chart (may have type=None)
        # Find pie data
        pie_data = None
        for item in chart_props.get('data', []):
            if item.get('type') == 'pie' and 'data' in item:
                pie_data = item['data']
                break

        if pie_data:
            # Extract non-zero wedges
            labels = []
            sizes = []

            for item in pie_data:
                size = item.get('wedgeSize', 0)
                if size > 0:  # Only include non-zero wedges
                    labels.append(item.get('label', ''))
                    sizes.append(size)

            if sizes:
                # Create a modern color palette for pie charts
                pie_palette = ['#4E79A7', '#F28E2B', '#E15759', '#76B7B2', '#59A14F', '#EDC948', '#B07AA1', '#FF9DA7']
                
                # Create pie chart with clean, modern styling
                wedges, texts, autotexts = ax.pie(
                    sizes,
                    labels=labels,
                    autopct='%1.1f%%',
                    startangle=90,
                    colors=pie_palette,
                    textprops={'fontsize': 9, 'fontweight': 'bold', 'color': '#2F4F4F'},
                    wedgeprops={'edgecolor': 'white', 'linewidth': 1.5, 'antialiased': True},
                    shadow=False,  # Cleaner look without shadow
                )

                # Make percentage text bold and white for better visibility
                for autotext in autotexts:
                    autotext.set_fontweight('bold')
                    autotext.set_color('white')
                    autotext.set_fontsize(10)
                
               

                ax.axis('equal')  # Equal aspect ratio ensures circular pie
            else:
                ax.text(0.5, 0.5, "No non-zero values for pie chart",
                        ha='center', va='center')
        else:
            ax.text(0.5, 0.5, "No pie data found", ha='center', va='center')

    else:
        # Unsupported chart type
        ax.text(0.5, 0.5, f"Unsupported chart type: {chart_type}",
                ha='center', va='center')


def find_charts(structure):
    """
    Find all charts in the structure, including those that are also containers.

    Returns:
    list: List of (chart_id, chart_data) tuples
    """
    charts = []

    def traverse(node):
        if not node or not isinstance(node, dict):
            return

        # If this is a chart, add it to the list
        if node.get('type') == 'chart':
            charts.append((node['id'], node))

            # IMPORTANT: Even if it's a chart, also check if it has children
            # This handles the case where a chart is also a container

        # Traverse children (whether or not this node is a chart)
        if 'children' in node and node['children']:
            for child in node['children']:
                traverse(child)

    # Start with rows container
    if 'rows' in structure and 'children' in structure['rows']:
        for row in structure['rows']['children']:
            traverse(row)

    # Also check columns container
    if 'columns' in structure and 'children' in structure['columns']:
        for col in structure['columns']['children']:
            traverse(col)

    # Sort charts by ID to ensure consistent ordering
    return sorted(charts, key=lambda x: x[0])

def visualize_data_structure(structure_json, output_file=None, debug=False):
    """
    Visualize a dashboard structure.

    Parameters:
    structure_json: JSON string or dictionary with structure
    output_file: Optional path to save the visualization
    debug: Whether to show debug information

    Returns:
    tuple: (fig, axes_dict) with the figure and axes dictionary
    """
    # Parse the JSON if it's a string
    if isinstance(structure_json, str):
        try:
            structure = json.loads(structure_json)
        except:
            # Try to load from file
            with open(structure_json, 'r') as f:
                structure = json.load(f)
    else:
        structure = structure_json

    # Create the grid
    fig, axes_dict = create_grid_from_structure(structure, debug)

    if debug:
        print(f"Created grid with {len(axes_dict)} axes")

    # Find and populate chart nodes
    charts = find_charts(structure)

    if debug:
        print(f"Found {len(charts)} charts in structure")
        for chart_id, _ in charts:
            print(f"  - Chart ID: {chart_id}")

    # Populate each chart
    for chart_id, chart_data in charts:
        if chart_id in axes_dict:
            try:
                populate_chart(axes_dict[chart_id], chart_data, debug)
                if debug:
                    print(f"Populated chart: {chart_id}")
            except Exception as e:
                if debug:
                    print(f"Error populating chart {chart_id}: {e}")
                # Add error message to chart
                axes_dict[chart_id].text(0.5, 0.5, f"Error: {e}",
                                    ha='center', va='center')
        elif debug:
            print(f"Chart {chart_id} not found in axes_dict")

    # Don't use tight_layout as requested
    # Instead use explicit subplot adjustments only
    fig.subplots_adjust(hspace=0.6, wspace=0.3)

    # Save the figure if requested
    if output_file:
        plt.savefig(output_file, bbox_inches='tight')
        if debug:
            print(f"Saved visualization to {output_file}")

    return fig, axes_dict