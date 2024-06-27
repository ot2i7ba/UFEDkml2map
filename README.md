# UFEDkml2map

UFEDkml2map is a Python script that processes KML files exported from Cellebrite UFED to generate interactive maps using Plotly. This script supports various map types and ensures efficient processing even for large KML files. It has been successfully tested with Cellebrite Reader 7.61.0.12 and higher.

## Features

- Parse and process KML files exported from Cellebrite UFED.
- Generate interactive maps with Plotly.
- Supports multiple plot types: Scatter Plot, Density Plot, and Lines Plot.
- Parallel processing for efficient handling of large datasets.
- Logs important events and errors to a log file.
- Provides visual progress indication during processing.

## Requirements

- Python 3.6 or higher
- The following Python packages:
  - pandas
  - plotly
  - lxml
  - tqdm

# Installation

## Usage
1. **Clone the repository**:

	```bash
	git clone https://github.com/ot2i7ba/UFEDkml2map.git
	cd UFEDkml2map
	```

2. **Install the required packages**:

    ```bash
    pip install -r requirements.txt
    ```

3. **Run the script**:

	```bash
	python UFEDkml2map.py
	```

4. **Follow the prompts**:
- **Input KML filename**: Enter the name of the KML file you want to process. Press Enter to use the default Locations.kml.
- **Choose a plot type**: Select the type of plot you want to generate (Scatter Plot, Density Plot, Lines Plot, or All).
- **Output HTML filename**: Enter the name for the output HTML file. Press Enter to use the default name with a timestamp.

## Compiled Version
A compiled and 7zip-packed version of UFEDkml2map for Windows is available as a release. You can download it from the **[Releases](https://github.com/ot2i7ba/UFEDkml2map/releases)** section on GitHub. This version includes all necessary dependencies and can be run without requiring Python to be installed on your system.

## Example
```
Input KML filename (enter for 'Locations.kml'):
Choose a plot type:
1. Scatter Plot
2. Density Plot
3. Lines Plot
A. All

Enter the number of the plot type (default is 1):
Output HTML filename (enter for 'YYMMDDHHMMSS_scatter_plot.html'):
```

## License
This project is licensed under the **[MIT license](https://github.com/ot2i7ba/UFEDkml2map/blob/main/LICENSE)**, providing users with flexibility and freedom to use and modify the software according to their needs.

## Disclaimer
This project is provided without warranties. Users are advised to review the accompanying license for more information on the terms of use and limitations of liability.
