# TimeSleuth

TimeSleuth is a software that detects and stores what a user does on their computer.
This data is stored in a database and is later visualized inside a graphical
user interface with a graph.

Made for a school project.

## Installation

Do any one of the following:
- Download latest release from [releases](https://github.com/dtele/timesleuth/releases)
- Build it yourself:
    1. `pip install -r /path/to/requirements.txt`
    2. `pip install pyinstaller`
    3. `pyinstaller /path/to/gui.py --onefile --windowed`

## Technologies used

1. [WinAPI](https://docs.microsoft.com/en-us/windows/win32/api/): Active process detection
2. [SQLite](https://sqlite.org/index.html/): Database management
3. [Qt Framework](https://doc.qt.io/): Graphical User Interface
4. [Matplotlib](https://matplotlib.org/) and [Seaborn](https://seaborn.pydata.org/): Data visualization
5. [.NET Platform](https://docs.microsoft.com/en-us/dotnet/api/system.drawing?view=net-6.0/): Icon extraction

## Credits

- [dcsp3](https://github.com/dcsp3): Database Management
- [dtele](https://github.com/dtele): Process Detection, Icon Extraction
- [RoutesLOL](https://github.com/RoutesLOL): Graphical User Interface
- [xyltius](https://github.com/xyltius): Data Visualization
