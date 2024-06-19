# Copyright (c) 2023 ot2i7ba
# https://github.com/ot2i7ba/
# This code is licensed under the MIT License (see LICENSE for details).

"""
Processes a KML file to generate an interactive map using Plotly.
"""

import os
import pandas as pd
import plotly.express as px
from lxml import etree
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from tqdm import tqdm
import logging

# Configure logging
log_file = 'UFEDkml2map.log'

def configure_logging():
    """Configure logging to log to both console and file."""
    if not os.path.exists(log_file):
        try:
            with open(log_file, 'w') as f:
                f.write("")
            print(f"Log file created: {log_file}")
        except IOError as e:
            print(f"Failed to create log file: {e}")
    
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s',
                        handlers=[
                            logging.FileHandler(log_file),
                            logging.StreamHandler()
                        ])
    logging.info("Logging configured successfully")

def clear_screen():
    """Clear the screen depending on the operating system."""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    """Print the header for the script."""
    print(" UFEDkml2map v0.1.0 by ot2i7ba ")
    print("===============================")
    print("")

def get_kml_filename():
    """Prompt the user to input the KML filename."""
    print()
    kml_file = input("Input KML filename (enter for 'Locations.kml'): ")
    
    if not kml_file:
        kml_file = 'Locations.kml'
    elif not kml_file.endswith('.kml'):
        kml_file += '.kml'
    
    logging.info(f"KML file chosen: {kml_file}")
    return kml_file

def validate_kml_file(kml_file):
    """Validate if the file exists and is a KML file."""
    if not os.path.isfile(kml_file):
        logging.error(f"Error: The file '{kml_file}' could not be found.")
        raise FileNotFoundError(f"Error: The file '{kml_file}' could not be found.")
    if not kml_file.endswith('.kml'):
        logging.error(f"Error: The file '{kml_file}' is not a KML file.")
        raise ValueError(f"Error: The file '{kml_file}' is not a KML file.")
    logging.info(f"Validated KML file: {kml_file}")
    return kml_file

def parse_kml(file_path):
    """Parse the KML file and extract relevant data."""
    try:
        context = etree.iterparse(file_path, events=('end',), tag='{http://www.opengis.net/kml/2.2}Placemark')
        data = []
        placemark_count = 0
        for event, elem in tqdm(context, desc="Parsing KML file", unit=" placemarks"):
            name = elem.find('.//{http://www.opengis.net/kml/2.2}name').text
            coordinates = elem.find('.//{http://www.opengis.net/kml/2.2}coordinates').text.strip()
            coord_parts = coordinates.split(',')
            if len(coord_parts) == 3:
                lon, lat, _ = coord_parts
            else:
                lon, lat = coord_parts
            data.append({
                'name': name,
                'longitude': float(lon),
                'latitude': float(lat)
            })
            elem.clear()
            while elem.getprevious() is not None:
                del elem.getparent()[0]
            placemark_count += 1
        logging.info(f"KML file parsed successfully with {placemark_count} placemarks")
        return pd.DataFrame(data)
    except (etree.XMLSyntaxError, AttributeError) as e:
        logging.error(f"Error parsing KML file: {e}")
        raise ValueError(f"Error parsing KML file: {e}")

def choose_plot_type():
    """Prompt the user to choose a plot type."""
    print()
    print("Choose a plot type:")
    plot_types = {
        "1": "Scatter Plot",
        "2": "Density Plot",
        "3": "Lines Plot",
        "A": "All"
    }
    for key, value in plot_types.items():
        print(f"{key}. {value}")
    
    print()
    choice = input("Enter the number of the plot type (default is 1): ")
    plot_type = plot_types.get(choice, "Scatter Plot")
    logging.info(f"Plot type chosen: {plot_type}")
    return plot_type

def create_map(df, plot_type):
    """Create the appropriate plot based on the plot type selected."""
    if plot_type == "Scatter Plot":
        fig = px.scatter_mapbox(df, lat="latitude", lon="longitude", hover_name="name",
                                zoom=3)
    elif plot_type == "Density Plot":
        fig = px.density_mapbox(df, lat="latitude", lon="longitude", hover_name="name",
                                zoom=3)
    elif plot_type == "Lines Plot":
        fig = px.line_geo(df, lat="latitude", lon="longitude", hover_name="name",
                          projection="orthographic")
    else:
        raise ValueError(f"Unknown plot type: {plot_type}")

    fig.update_layout(mapbox_style="open-street-map", height=1080, width=1920)
    logging.info(f"Map created: {plot_type}")
    return fig

def export_plot(fig, plot_name):
    """Export the plot to an HTML file."""
    timestamp = datetime.now().strftime("%y%m%d%H%M%S")
    html_file = f"{timestamp}_{plot_name}.html"
    fig.write_html(html_file)
    logging.info(f"Plot saved as {html_file}")
    print(f"Plot saved as {html_file}")

def get_html_filename(default_name):
    """Prompt the user to input the output HTML filename."""
    print()
    timestamp = datetime.now().strftime("%y%m%d%H%M%S")
    html_file = input(f"Output html filename (enter for '{timestamp}_{default_name}'): ")
    
    if not html_file:
        html_file = f"{timestamp}_{default_name}"
    elif not html_file.endswith('.html'):
        html_file += '.html'
    logging.info(f"HTML filename chosen: {html_file}")
    return html_file

def export_all_plots(df):
    """Export all plot types using parallel processing."""
    plot_types = ["Scatter Plot", "Density Plot", "Lines Plot"]
    with ThreadPoolExecutor() as executor:
        futures = {executor.submit(create_map, df, plot_type): plot_type.lower().replace(" ", "_") for plot_type in plot_types}
        for future in tqdm(as_completed(futures), total=len(futures), desc="Exporting plots", unit=" plot"):
            plot_name = futures[future]
            try:
                fig = future.result()
                export_plot(fig, plot_name)
            except Exception as e:
                logging.error(f"Error creating plot {plot_name}: {e}")

def get_output_filename(kml_file):
    """Generate the output filename based on the KML filename."""
    base_name = os.path.splitext(os.path.basename(kml_file))[0]
    timestamp = datetime.now().strftime("%y%m%d%H%M%S")
    output_file = f"{timestamp}_{base_name}.csv"
    logging.info(f"Output CSV filename: {output_file}")
    return output_file

def save_dataframe(df, output_file):
    """Save the DataFrame to a CSV file."""
    df.to_csv(output_file, index=False)
    logging.info(f"Data saved as {output_file}")
    print(f"Data saved as {output_file}")

def main():
    """Main function to execute the script workflow."""
    configure_logging()
    clear_screen()
    print_header()

    try:
        kml_file = get_kml_filename()
        validate_kml_file(kml_file)
        
        df = parse_kml(kml_file)
        
        output_file = get_output_filename(kml_file)
        save_dataframe(df, output_file)
        
        plot_type = choose_plot_type()
        
        if plot_type == "All":
            export_all_plots(df)
        else:
            fig = create_map(df, plot_type)
            plot_name = plot_type.lower().replace(" ", "_")
            html_file = get_html_filename(f"{plot_name}.html")
            
            fig.show()
            fig.write_html(html_file)
            logging.info(f"Plot saved as {html_file}")
    except (FileNotFoundError, ValueError) as e:
        logging.error(e)
        print(e)

if __name__ == "__main__":
    main()
