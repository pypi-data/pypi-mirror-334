
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.colors as mcolors
import numpy as np
import datetime
import matplotlib.dates as mdates
import logging
from dashboardVisualiser import visualize_data_structure
import matplotlib
matplotlib.use('agg')

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


###################################--------Page begins here---------##############################################
class Page:
    def __init__(self, response):
        """
        Initialize with a response dictionary.
        The response is transformed into the structured grid data.
        """
        self.response = response
        logging.info("Initializing Page with response data.")
        self.grid_data = self.transform_input_to_structure(response)

    def extract_chart_data(self, chart_dict):
        """
        Extract chart data from a chart dictionary.
        """
        logging.info(f"Extracting chart data for {chart_dict.get('id', 'unknown')}")

        chart_type = None
        chart_data = {}

        if (
            'chartData' in chart_dict and chart_dict['chartData'] and
            'data' in chart_dict['chartData'] and chart_dict['chartData']['data'] and
            'data' in chart_dict['chartData']['data'] and
            len(chart_dict['chartData']['data']['data']) > 0 and
            'charts' in chart_dict['chartData']['data']['data'][0] and
            chart_dict['chartData']['data']['data'][0]['charts'] and
            len(chart_dict['chartData']['data']['data'][0]['charts']) > 0
        ):
            chart_data = chart_dict['chartData']['data']['data'][0]['charts'][0]
            chart_type = chart_data.get('type')


            if chart_type is None and 'data' in chart_data:
                for data_item in chart_data['data']:
                    if data_item.get('type') == 'pie':
                        chart_type = 'pie'
                        break

            logging.info(f"Found chart of type: {chart_type}")
            return chart_type, chart_data
        else:
            logging.warning(f"No valid chart data found for {chart_dict.get('id', 'unknown')}")
            return None, {}

    def analyze_structure_type(self, response_dict):
        """
        Analyze the structure type of the input data to determine the correct processing approach.

        Returns:
            str: One of "NESTED_ROWS", "NESTED_COLUMNS", "GRID", "CHART_CONTAINER" or "UNKNOWN"
        """
        has_top_level_rows = response_dict.get('rows') and len(response_dict.get('rows', [])) > 0
        has_top_level_columns = response_dict.get('columns') and len(response_dict.get('columns', [])) > 0

        # Special case: Check if top-level row is a chart that contains other charts
        if has_top_level_rows and len(response_dict['rows']) == 1 and response_dict['rows'][0].get('type') == 'chart':
            top_row = response_dict['rows'][0]
            if ((top_row.get('rows') and len(top_row.get('rows', [])) > 0) or
                (top_row.get('columns') and len(top_row.get('columns', [])) > 0)):
                return "CHART_CONTAINER"

        if has_top_level_rows and not has_top_level_columns:
            # Check if rows have nested structure
            if any((r.get('columns') and len(r.get('columns', [])) > 0) or
                   (r.get('rows') and len(r.get('rows', [])) > 0)
                   for r in response_dict['rows']):
                return "NESTED_ROWS"
            else:
                return "SIMPLE_ROWS"

        elif not has_top_level_rows and has_top_level_columns:
            # Check if columns have nested structure
            if any((c.get('columns') and len(c.get('columns', [])) > 0) or
                   (c.get('rows') and len(c.get('rows', [])) > 0)
                   for c in response_dict['columns']):
                return "NESTED_COLUMNS"
            else:
                return "SIMPLE_COLUMNS"

        elif has_top_level_rows and has_top_level_columns:
            # Both rows and columns at the top level
            return "GRID"

        return "UNKNOWN"

    def process_chart(self, chart_dict, id_prefix, idx):
        """
        Process a chart element and return its structured representation.
        """
        result = {
            'id': f"{id_prefix}{idx}",
            'parent_index': idx,
            'type': 'chart'
        }

        chart_type, chart_data = self.extract_chart_data(chart_dict)
        result['charts'] = chart_type
        result['chartData'] = chart_data

        return result

    def process_chart_container(self, chart_container, id_prefix, idx):
        """
        Process a special case where a chart is also a container for other charts.
        """
        logging.info(f"Processing chart container with ID: {id_prefix}{idx}")

        # First process it as a chart to extract chart data
        result = self.process_chart(chart_container, id_prefix, idx)

        # Then add container properties
        has_rows = chart_container.get('rows') and len(chart_container.get('rows', [])) > 0
        has_columns = chart_container.get('columns') and len(chart_container.get('columns', [])) > 0
        has_row_sizes = 'resizedRowSizes' in chart_container
        has_column_sizes = 'resizedColumnSizes' in chart_container

        # Add children array
        result['children'] = []

        # Process rows
        if has_rows:
            if has_row_sizes:
                result['rowRatio'] = [size['ratio'] for size in chart_container['resizedRowSizes']]

            for i, row in enumerate(chart_container['rows']):
                if row.get('type') == 'chart':
                    child = self.process_chart(row, f"{result['id']}_row", i)
                else:
                    child = self.process_complex_element(row, f"{result['id']}_row", i)
                result['children'].append(child)

        # Process columns
        if has_columns:
            if has_column_sizes:
                result['colRatio'] = [size['ratio'] for size in chart_container['resizedColumnSizes']]

            for i, col in enumerate(chart_container['columns']):
                if col.get('type') == 'chart':
                    child = self.process_chart(col, f"{result['id']}_col", i)
                else:
                    child = self.process_complex_element(col, f"{result['id']}_col", i)
                result['children'].append(child)

        return result

    def process_complex_element(self, element, id_prefix, idx):
        """
        Process a complex element (row or column) with possible nested structure.
        """
        element_id = f"{id_prefix}{idx}"
        logging.info(f"Processing complex element: {element_id}, type: {element.get('type', 'unknown')}")

        # Special case: Element is both a chart and a container
        if element.get('type') == 'chart' and (
            (element.get('rows') and len(element.get('rows', [])) > 0) or
            (element.get('columns') and len(element.get('columns', [])) > 0)
        ):
            return self.process_chart_container(element, id_prefix, idx)

        result = {
            'id': element_id,
            'parent_index': idx
        }

        # Determine element type
        if element.get('type') == 'row' or 'resizedRowSizes' in element:
            result['type'] = 'row'
        elif element.get('type') == 'column' or 'resizedColumnSizes' in element:
            result['type'] = 'col'
        else:
            # Default to row if type isn't clear
            result['type'] = 'row'

        # Process internal structure based on available sizing info
        has_rows = element.get('rows') and len(element.get('rows', [])) > 0
        has_columns = element.get('columns') and len(element.get('columns', [])) > 0
        has_row_sizes = 'resizedRowSizes' in element
        has_column_sizes = 'resizedColumnSizes' in element

        # Case 1: Element has both rows and columns with respective sizing
        if has_rows and has_columns and has_row_sizes and has_column_sizes:
            logging.info(f"Complex element {element_id} has both rows and columns with sizing")

            # Use column structure as primary
            result['ratio'] = [size['ratio'] for size in element['resizedColumnSizes']]
            result['children'] = []

            # Container for rows
            row_container = {
                'id': f"{element_id}_container0",
                'parent_index': 0,
                'type': 'row',
                'ratio': [size['ratio'] for size in element['resizedRowSizes']],
                'children': []
            }

            # Process rows into the container
            for i, row in enumerate(element['rows']):
                if row.get('type') == 'chart':
                    child = self.process_chart(row, f"{row_container['id']}_row", i)
                else:
                    child = self.process_complex_element(row, f"{row_container['id']}_row", i)
                row_container['children'].append(child)

            result['children'].append(row_container)

            # Container for columns
            col_container = {
                'id': f"{element_id}_container1",
                'parent_index': 1,
                'type': 'col',
                'children': []
            }

            # Add ratio if multiple columns
            if len(element['columns']) > 1:
                col_container['ratio'] = [1/len(element['columns'])] * len(element['columns'])

            # Process columns into container
            for i, col in enumerate(element['columns']):
                if col.get('type') == 'chart':
                    child = self.process_chart(col, f"{col_container['id']}_col", i)
                else:
                    child = self.process_complex_element(col, f"{col_container['id']}_col", i)
                col_container['children'].append(child)

            result['children'].append(col_container)

        # Case 2: Element has rows with row sizing
        elif has_rows and has_row_sizes:
            logging.info(f"Element {element_id} has rows with sizing")
            result['ratio'] = [size['ratio'] for size in element['resizedRowSizes']]
            result['children'] = []

            for i, row in enumerate(element['rows']):
                if row.get('type') == 'chart':
                    child = self.process_chart(row, f"{element_id}_row", i)
                else:
                    child = self.process_complex_element(row, f"{element_id}_row", i)
                result['children'].append(child)

        # Case 3: Element has columns with column sizing
        elif has_columns and has_column_sizes:
            logging.info(f"Element {element_id} has columns with sizing")
            result['ratio'] = [size['ratio'] for size in element['resizedColumnSizes']]
            result['children'] = []

            for i, col in enumerate(element['columns']):
                if col.get('type') == 'chart':
                    child = self.process_chart(col, f"{element_id}_col", i)
                else:
                    child = self.process_complex_element(col, f"{element_id}_col", i)
                result['children'].append(child)

        # Case 4: Element has rows without explicit sizing
        elif has_rows:
            logging.info(f"Element {element_id} has rows without explicit sizing")
            result['ratio'] = [1/len(element['rows'])] * len(element['rows'])
            result['children'] = []

            for i, row in enumerate(element['rows']):
                if row.get('type') == 'chart':
                    child = self.process_chart(row, f"{element_id}_row", i)
                else:
                    child = self.process_complex_element(row, f"{element_id}_row", i)
                result['children'].append(child)

        # Case 5: Element has columns without explicit sizing
        elif has_columns:
            logging.info(f"Element {element_id} has columns without explicit sizing")
            result['ratio'] = [1/len(element['columns'])] * len(element['columns'])
            result['children'] = []

            for i, col in enumerate(element['columns']):
                if col.get('type') == 'chart':
                    child = self.process_chart(col, f"{element_id}_col", i)
                else:
                    child = self.process_complex_element(col, f"{element_id}_col", i)
                result['children'].append(child)

        else:
            logging.warning(f"Element {element_id} has no children to process")

        return result

    def process_chart_container_structure(self, response_dict):
        """
        Process a structure where the top-level row is a chart that contains other charts.
        """
        result = {}

        # Handle main ratios
        if 'dimensions' in response_dict and 'main' in response_dict['dimensions']:
            main_ratios = [item['ratio'] for item in response_dict['dimensions']['main']]
            result['main'] = {'ratio': main_ratios}

        # Process row dimensions and the chart container
        if 'dimensions' in response_dict and 'row' in response_dict['dimensions'] and response_dict['dimensions']['row']:
            row_ratios = [item['ratio'] for item in response_dict['dimensions']['row']]

            # Process the chart container
            chart_container = response_dict['rows'][0]
            chart_container_child = self.process_chart_container(chart_container, "row_", 0)

            result['rows'] = {
                'ratio': row_ratios,
                'children': [chart_container_child]
            }

        return result

    def process_grid_structure(self, response_dict):
        """
        Process a simple grid structure with both rows and columns at the top level.
        """
        result = {}

        # Handle main ratios
        if 'dimensions' in response_dict and 'main' in response_dict['dimensions']:
            main_ratios = [item['ratio'] for item in response_dict['dimensions']['main']]
            result['main'] = {'ratio': main_ratios}

        # Process rows
        if 'dimensions' in response_dict and 'row' in response_dict['dimensions'] and response_dict['dimensions']['row']:
            row_ratios = [item['ratio'] for item in response_dict['dimensions']['row']]
            row_children = []

            for idx, row in enumerate(response_dict.get('rows', [])):
                if row.get('type') == 'chart':
                    if ((row.get('rows') and len(row.get('rows', [])) > 0) or
                        (row.get('columns') and len(row.get('columns', [])) > 0)):
                        child = self.process_chart_container(row, "row_", idx)
                    else:
                        child = self.process_chart(row, "row_", idx)
                else:
                    child = self.process_complex_element(row, "row_", idx)
                row_children.append(child)

            result['rows'] = {'ratio': row_ratios, 'children': row_children}

        # Process columns
        if 'dimensions' in response_dict and 'column' in response_dict['dimensions'] and response_dict['dimensions']['column']:
            col_ratios = [item['ratio'] for item in response_dict['dimensions']['column']]
            col_children = []

            for idx, col in enumerate(response_dict.get('columns', [])):
                if col.get('type') == 'chart':
                    if ((col.get('rows') and len(col.get('rows', [])) > 0) or
                        (col.get('columns') and len(col.get('columns', [])) > 0)):
                        child = self.process_chart_container(col, "column_col", idx)
                    else:
                        child = self.process_chart(col, "column_col", idx)
                else:
                    child = self.process_complex_element(col, "column_col", idx)
                col_children.append(child)

            result['columns'] = {'ratio': col_ratios, 'children': col_children}

        return result

    def process_nested_rows(self, response_dict):
        """
        Process a structure with nested rows.
        """
        result = {}

        # Handle main ratios
        if 'dimensions' in response_dict and 'main' in response_dict['dimensions']:
            main_ratios = [item['ratio'] for item in response_dict['dimensions']['main']]
            result['main'] = {'ratio': main_ratios}

        # Process row dimensions and children
        if 'dimensions' in response_dict and 'row' in response_dict['dimensions'] and response_dict['dimensions']['row']:
            row_ratios = [item['ratio'] for item in response_dict['dimensions']['row']]
            row_children = []

            for idx, row in enumerate(response_dict.get('rows', [])):
                if row.get('type') == 'chart':
                    if ((row.get('rows') and len(row.get('rows', [])) > 0) or
                        (row.get('columns') and len(row.get('columns', [])) > 0)):
                        child = self.process_chart_container(row, "row_", idx)
                    else:
                        child = self.process_chart(row, "row_", idx)
                else:
                    child = self.process_complex_element(row, "row_", idx)
                row_children.append(child)

            result['rows'] = {'ratio': row_ratios, 'children': row_children}

        return result

    def process_nested_columns(self, response_dict):
        """
        Process a structure with nested columns.
        """
        result = {}

        # Handle main ratios
        if 'dimensions' in response_dict and 'main' in response_dict['dimensions']:
            main_ratios = [item['ratio'] for item in response_dict['dimensions']['main']]
            result['main'] = {'ratio': main_ratios}

        # Process column dimensions and children
        if 'dimensions' in response_dict and 'column' in response_dict['dimensions'] and response_dict['dimensions']['column']:
            col_ratios = [item['ratio'] for item in response_dict['dimensions']['column']]
            col_children = []

            for idx, col in enumerate(response_dict.get('columns', [])):
                if col.get('type') == 'chart':
                    if ((col.get('rows') and len(col.get('rows', [])) > 0) or
                        (col.get('columns') and len(col.get('columns', [])) > 0)):
                        child = self.process_chart_container(col, "column_col", idx)
                    else:
                        child = self.process_chart(col, "column_col", idx)
                else:
                    child = self.process_complex_element(col, "column_col", idx)
                col_children.append(child)

            result['columns'] = {'ratio': col_ratios, 'children': col_children}

        return result

    def transform_input_to_structure(self, response_dict):
        """
        Builds the grid structure from the user response based on the detected structure type.
        """
        logging.info("Transforming input response to structured format.")

        # Analyze the structure type
        structure_type = self.analyze_structure_type(response_dict)
        logging.info(f"Detected structure type: {structure_type}")

        # Process the structure based on its type
        if structure_type == "CHART_CONTAINER":
            result = self.process_chart_container_structure(response_dict)
        elif structure_type == "GRID":
            result = self.process_grid_structure(response_dict)
        elif structure_type in ["NESTED_ROWS", "SIMPLE_ROWS"]:
            result = self.process_nested_rows(response_dict)
        elif structure_type in ["NESTED_COLUMNS", "SIMPLE_COLUMNS"]:
            result = self.process_nested_columns(response_dict)
        else:
            # Fallback to the most flexible approach
            logging.warning("Unknown structure type, attempting general processing")
            result = self.process_grid_structure(response_dict)

        logging.info("Finished transforming input to structured format.")
        return result

    def transform(self):
        """
        Return the processed grid data.
        """
        logging.info("Exporting transformed structure.")
        return self.grid_data

  ###################################---------visualisation--------------##############################


    def export(self, output_file=None, debug=False, show=True):
        """
        Export the page data as a visualization.
        
        Parameters:
        -----------
        output_file : str, optional
            Path to save the visualization
        debug : bool
            Whether to show debug information
        show : bool
            Whether to display the plot
            
        Returns:
        --------
        tuple: (fig, axes) The matplotlib figure and axes dictionary
        """
        # Get the structured data
        structured_output = self.transform()
        
        # Call visualization function from the imported module
        fig, axes = visualize_data_structure(structured_output, output_file, debug)
        
        # Optionally show the plot
        if show:
            plt.show()
            
        return fig, axes


import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import time

class Documents:
    def __init__(self, json_data):
        """
        Initialize a Documents instance with JSON data containing multiple pages.
        
        Parameters:
        -----------
        json_data : dict
            Dictionary containing a "pages" key with an array of page data
        """
        self.json_data = json_data
        # Create Page instances for each page in the input data
        self.pages = [Page(page) for page in json_data.get("pages", [])]
    
    def export(self, output_pdf="final_output.pdf", debug=False):
        """
        Export all pages to a multi-page PDF document.
        
        Parameters:
        -----------
        output_pdf : str
            Path to save the output PDF file
        debug : bool
            Whether to print debug information during processing
        """
        start_time_total = time.time()
        
        print(f"Exporting {len(self.pages)} pages to {output_pdf}...")
        
        with PdfPages(output_pdf) as pdf:
            for i, page in enumerate(self.pages):
                print(f"Processing Page {i+1}...")
                
                # Export the page - note we're capturing both figure and axes now
                try:
                    fig, axes = page.export(output_file=None, debug=debug, show=False)
                    
                    if fig is None:
                        print(f"Warning: No figure generated for Page {i+1}, skipping...")
                        continue
                    
                    # Add page titles and footer
                    fig.suptitle(
                        f"Page {i + 1} - Document Title",
                        fontsize=14, fontweight='bold', color='black', y=1.02
                    )
                    
                    fig.text(
                        0.95, 0.01,
                        "ChartArt",
                        fontsize=10, fontweight='normal', color='gray', ha='right'
                    )
                    
                    # Save to PDF
                    pdf.savefig(fig, dpi=100, bbox_inches='tight')
                    
                    # Close the figure to free memory
                    plt.close(fig)
                    
                except Exception as e:
                    print(f"Error processing Page {i+1}: {e}")
        
        total_time_taken = time.time() - start_time_total
        print(f"\nDocument export completed in {total_time_taken:.2f} seconds.")


__all__ = ["Documents"]