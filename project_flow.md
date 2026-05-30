# Project Architecture & Flow

This diagram illustrates the high-level architecture and data flow of the 5edma Management System.

```mermaid
graph TD
    %% Styling
    Style[assets/styles/main.qss] -->|Loaded by| SM[utils.StyleManager]
    SM -->|Applies styles to| App

    %% Entry Point
    Entry[main.py] -->|Initializes| App[QApplication]
    Entry -->|Creates| MW[ui.MainWindow]
    
    %% Main Window & Tabs
    subgraph "UI Layer (PyQt5)"
        MW -->|Contains| Tabs[QTabWidget]
        
        Tabs -->|Tab 1| RegTab[RegistrationTab]
        Tabs -->|Tab 2| AbsTab[AbsenceTab]
        Tabs -->|Tab 3| DashTab[DashboardTab]
        Tabs -->|Tab 4| DataTab[DataManagementTab]
        Tabs -->|Tab 5| EarlyTab[EarlyArrivalTab]
        Tabs -->|Tab 6| AttRepTab[AttendanceReportTab]
        Tabs -->|Tab 7| CompTab[ComparisonReportTab]
        
        %% Inter-Tab Communication
        RegTab -->|Signal: registration_finished| MW
        MW -->|Updates| AbsTab
        MW -->|Updates| EarlyTab
        
        %% Dialogs
        CompTab -.->|Opens| DateDialog[DateRangeDialog]
        AbsTab -.->|Opens| ServerDialog[ServerAssignmentDialog]
        RegTab -.->|Opens| ChildDialog[ChildDetailsDialog]
    end

    %% Data Layer
    subgraph "Data Layer"
        DB[utils.DatabaseManager]
        Excel[utils.ExcelHandler]
        
        %% Database Connections
        RegTab <--> DB
        AbsTab <--> DB
        DashTab <--> DB
        DataTab <--> DB
        EarlyTab <--> DB
        AttRepTab <--> DB
        CompTab <--> DB
        ChildDialog <--> DB
        
        %% Excel Internal Logic
        DataTab --> Excel
        AttRepTab --> Excel
        CompTab --> Excel
    end

    %% Storage
    DB <-->|Reads/Writes| JSON[data/database.json]
    Excel -->|Exports| XLSX[Excel Files]
    
    %% Styling Application
    classDef main fill:#2c3e50,stroke:#2c3e50,color:white;
    classDef tab fill:#3498db,stroke:#2980b9,color:white;
    classDef util fill:#27ae60,stroke:#2ecc71,color:white;
    classDef file fill:#f39c12,stroke:#d35400,color:white;
    
    class Entry,MW main;
    class RegTab,AbsTab,DashTab,DataTab,EarlyTab,AttRepTab,CompTab tab;
    class DB,Excel,SM util;
    class Style,JSON,XLSX file;
```

## Flow Description

1.  **Initialization**: `main.py` starts the application and uses `StyleManager` to load `assets/styles/main.qss`.
2.  **Main Interface**: `MainWindow` serves as the shell, hosting multiple functional tabs.
3.  **Registration**: The `RegistrationTab` handles daily attendance. When registration is finished, it emits a signal to update other tabs like `AbsenceTab` and `EarlyArrivalTab`.
4.  **Dashboard**: `DashboardTab` provides visual analytics and time-series trends using Matplotlib.
5.  **Data Management**: All tabs interact with `DatabaseManager` to read/write from `data/database.json`.
6.  **Reporting**: `AttendanceReportTab` and `ComparisonReportTab` aggregate data and use `ExcelHandler` (or internal logic) to export reports.
