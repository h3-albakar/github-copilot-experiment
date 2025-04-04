# System Patterns: GitHub Copilot Experiment

## Repository Architecture

The GitHub Copilot Experiment repository follows a modular architecture designed for clarity, ease of use, and effective data collection. The system is organized into the following key components:

```
github-copilot-experiment/
├── README.md                      # Experiment overview and setup instructions
├── .github/                       # GitHub-specific configurations
│   └── PULL_REQUEST_TEMPLATE.md   # Standardized PR template for submissions
├── tasks/                         # Task definitions for participants
│   ├── unit-tests/                # Unit testing tasks
│   ├── functions/                 # Function creation tasks
│   ├── code-review/               # Code review tasks
│   └── documentation/             # Documentation tasks
├── metrics/                       # Metrics collection components
│   ├── templates/                 # YAML templates for metrics recording
│   └── submissions/               # Where participants submit completed metrics
├── rs-copilot-examples/           # RS Copilot library examples
├── analysis/                      # Analysis tools and results
│   ├── metrics_aggregator.py      # Script to extract and analyze metrics
│   ├── visualizations.py          # Code for visualizing results
│   └── roi_calculator.py          # ROI calculation based on time savings
├── resources/                     # Supporting resources
│   ├── setup_guide.md             # Tool setup instructions
│   ├── evaluation_criteria.md     # Evaluation guidelines
│   └── final_report_template.md   # Template for final recommendations
└── memory-bank/                   # Documentation for Cline AI assistant
```

## Key Technical Decisions

### 1. YAML for Metrics Collection

The experiment uses YAML for metrics collection due to its:
- Human readability and editability
- Structured format that's easy to parse
- Support for comments and documentation
- Familiarity among data scientists

### 2. Python for Analysis

Python was chosen for analysis scripts because:
- It's the primary language used by the data science teams
- It has excellent libraries for data analysis (pandas, numpy)
- It provides powerful visualization capabilities (matplotlib, seaborn)
- It's familiar to all participants

### 3. Markdown for Documentation

Markdown is used for all documentation because:
- It's lightweight and easy to read/write
- It's rendered nicely on GitHub
- It supports code blocks, tables, and other formatting
- It's version-control friendly

### 4. Task Categorization

Tasks are categorized into four main types:
- Unit Tests: Testing code functionality
- Functions: Creating data processing functions
- Code Review: Reviewing and improving existing code
- Documentation: Writing clear documentation

This categorization allows for:
- Targeted evaluation of different coding activities
- Comparison of tool performance across different task types
- Alignment with common graduate data scientist responsibilities

## Design Patterns

### 1. Template Pattern

The experiment uses templates for:
- Metrics collection (YAML templates)
- Pull requests (PR template)
- Final report (report template)

This ensures consistency in data collection and reporting, making analysis more reliable.

### 2. Observer Pattern

The experiment implements a form of the observer pattern through:
- Standardized metrics collection for each task
- Consistent evaluation criteria across participants
- Centralized analysis of results

This allows for objective comparison between the two tools.

### 3. Factory Pattern

The task structure follows a factory-like pattern where:
- Each task category has a consistent structure
- Tasks are created with similar complexity levels
- From-scratch and context-based variants are provided

This ensures fair comparison between Week 1 and Week 2 performance.

## Data Flow

The data flow in the experiment follows this pattern:

1. **Task Assignment**: Participants select tasks from their assigned category
2. **Task Completion**: Tasks are completed using the assigned tool (Edge or GitHub Copilot)
3. **Metrics Recording**: Participants record metrics using the provided templates
4. **Submission**: Completed tasks and metrics are submitted via pull requests
5. **Analysis**: Scripts process the submitted metrics to generate insights
6. **Reporting**: Results are compiled into a final recommendation document

## Technical Constraints

The experiment operates within these constraints:

1. **Time Limitation**: Maximum 2 hours per graduate
2. **Tool Limitations**:
   - Edge Copilot: Browser-based with character limitations
   - GitHub Copilot: IDE-integrated with context awareness
3. **Task Complexity**: Tasks must be completable within 20-30 minutes
4. **Participant Skill Levels**: Varying experience levels among graduates
5. **RS Copilot Knowledge**: Varying familiarity with the RS Copilot library

## Integration Points

The key integration points in the system are:

1. **Metrics Templates → Submissions**: Standardized format for data collection
2. **Submissions → Analysis Scripts**: Data processing pipeline
3. **Analysis Results → Visualization**: Conversion of data to visual insights
4. **Analysis Results → ROI Calculator**: Business value calculation
5. **All Components → Final Report**: Comprehensive findings compilation
