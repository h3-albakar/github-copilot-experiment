# Technical Context: GitHub Copilot Experiment

## Technologies Used

### Primary Technologies

1. **Python**
   - Version: 3.8+
   - Primary language for data science tasks and analysis scripts
   - Used for metrics processing and visualization

2. **YAML**
   - Used for structured metrics collection
   - Chosen for human readability and easy parsing

3. **Markdown**
   - Used for all documentation
   - Provides consistent formatting across the repository

4. **Git/GitHub**
   - Version control system
   - Pull request workflow for submissions
   - Collaboration platform for the experiment

### AI Tools Being Compared

1. **Edge Copilot**
   - Browser-based AI assistant
   - Accessible to all graduates
   - Character limitations for inputs
   - Requires context switching between browser and IDE

2. **GitHub Copilot**
   - IDE-integrated AI assistant
   - Currently limited to Grade D+ employees
   - Provides contextual code suggestions
   - Direct integration with development environment

### Supporting Libraries

1. **Data Analysis**
   - pandas: Data manipulation and analysis
   - numpy: Numerical computing
   - matplotlib/seaborn: Data visualization

2. **RS Copilot Library**
   - Lloyds Banking Group's Risk Science standardization library
   - Provides patterns and standards for data science code
   - Important for testing integration capabilities of AI tools

## Development Setup

### Participant Environment

Participants will need:

1. **Python Development Environment**
   - Python 3.8+
   - Preferred IDE (VS Code, PyCharm, etc.)
   - Git client

2. **Edge Copilot Access**
   - Microsoft Edge browser
   - Lloyds Banking Group Microsoft account

3. **GitHub Copilot Access**
   - Temporary access provided for Week 2
   - GitHub Copilot extension installed in their IDE

### Repository Setup

The repository is structured to be:

1. **Self-contained**
   - All necessary resources included
   - No external dependencies beyond standard libraries
   - Clear documentation for setup

2. **Lightweight**
   - Minimal setup requirements
   - Quick to clone and get started
   - Focused on the experiment tasks

3. **Standardized**
   - Consistent structure across task categories
   - Standardized templates for submissions
   - Clear guidelines for participation

## Technical Constraints

### Tool Limitations

1. **Edge Copilot Constraints**
   - Character limit for inputs (~4000 characters)
   - No direct access to full codebase context
   - Browser-based interface only
   - Potential network/firewall limitations

2. **GitHub Copilot Constraints**
   - Requires IDE extension
   - May have varying performance across different IDEs
   - Learning curve for first-time users
   - Potential licensing/access issues

### Experiment Constraints

1. **Time Constraints**
   - 2-hour maximum per graduate
   - Tasks designed to be completable in 20-30 minutes
   - Limited time for familiarization with tools

2. **Skill Variability**
   - Varying levels of Python experience among graduates
   - Varying familiarity with RS Copilot library
   - Different comfort levels with AI tools

3. **Task Complexity Balance**
   - Tasks must be complex enough to test tool capabilities
   - Tasks must be simple enough to complete in time limit
   - Week 1 and Week 2 tasks must be comparable but not identical

## Dependencies

### External Dependencies

1. **Python Ecosystem**
   - Python 3.8+
   - Standard data science libraries (pandas, numpy, matplotlib)
   - No specialized or difficult-to-install packages

2. **AI Tools**
   - Edge Copilot (browser-based)
   - GitHub Copilot (IDE extension)

3. **Version Control**
   - Git
   - GitHub account with repository access

### Internal Dependencies

1. **Metrics Templates**
   - YAML templates for standardized data collection
   - Required for consistent analysis

2. **Analysis Scripts**
   - Python scripts for processing metrics
   - Dependent on specific YAML structure

3. **RS Copilot Examples**
   - Example code following RS Copilot patterns
   - Required for testing integration capabilities

## Technical Risks and Mitigations

### Risks

1. **Tool Access Issues**
   - Risk: Difficulties with GitHub Copilot access for Week 2
   - Mitigation: Pre-arranged access with IT, backup plan for extension

2. **Data Collection Consistency**
   - Risk: Inconsistent metrics recording across participants
   - Mitigation: Standardized templates, clear instructions, validation checks

3. **Task Comparability**
   - Risk: Week 1 and Week 2 tasks not being truly comparable
   - Mitigation: Careful task design, pilot testing, balanced difficulty

4. **Analysis Accuracy**
   - Risk: Metrics not accurately capturing performance differences
   - Mitigation: Multiple metrics types, qualitative feedback, cross-validation

### Technical Debt Considerations

1. **Repository Maintenance**
   - Short-term experiment, designed for 2-week use
   - Limited need for long-term maintenance
   - Documentation focused on immediate experiment needs

2. **Analysis Scripts**
   - Designed for one-time analysis of experiment results
   - May require updates if experiment is extended or repeated
   - Prioritizes clarity and specific purpose over generalizability

## Integration Points

1. **RS Copilot Library Integration**
   - Testing how well each AI tool understands and works with RS Copilot patterns
   - Examples provided in repository for reference

2. **Metrics → Analysis Pipeline**
   - YAML metrics files processed by Python analysis scripts
   - Standardized format ensures consistent processing

3. **Analysis → Visualization**
   - Analysis results fed into visualization functions
   - Generates charts and graphs for the final report
