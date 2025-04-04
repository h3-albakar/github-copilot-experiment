# GitHub Copilot Experiment

## Overview

This repository supports a 2-week experiment to demonstrate the value of GitHub Copilot for graduate data scientists at Lloyds Banking Group. The experiment compares GitHub Copilot against Edge Copilot (browser-based) to build a compelling business case for providing GitHub Copilot licenses to graduates.

### Experiment Structure

**Participants:** 8 graduate data scientists in 3 project-based teams:
- Logistic Regression Project (2 grads): Hamza (lead) + Tao
- Pre-processing Project (4 grads): Luke, CJ, Maria, Josh
- ACG Project (2 grads): Rindra, David

**Timeline:**
- Week 1: Complete tasks using Edge Copilot
- Week 2: Complete comparable tasks using GitHub Copilot
- Total time requirement: Maximum 2 hours per graduate

**Task Categories:**
- Writing unit tests
- Creating simple functions
- Reviewing code
- Writing documentation/MDocs

**Key Differentiators Being Tested:**
- Integration with RS Copilot library (Risk Science standardization library)
- Code context understanding capabilities
- Character limitations in Edge Copilot
- Development environment integration vs browser context switching

## Getting Started

### Setup Instructions

1. **Edge Copilot Setup (Week 1)**
   - Access Edge Copilot through Microsoft Edge browser
   - Refer to the [Edge Copilot setup guide](resources/setup_guide.md) for detailed instructions

2. **GitHub Copilot Setup (Week 2)**
   - Install GitHub Copilot extension in your IDE
   - Configure according to the [GitHub Copilot setup guide](resources/setup_guide.md)

### Participation Workflow

1. **Select Tasks**
   - Choose tasks from your assigned category in the `tasks/` directory
   - Each task should take approximately 20-30 minutes

2. **Week 1: Edge Copilot**
   - Complete tasks using Edge Copilot
   - Record metrics using the templates in `metrics/templates/`
   - Submit your results via PR using the standardized template

3. **Week 2: GitHub Copilot**
   - Complete comparable tasks using GitHub Copilot
   - Record metrics using the same templates
   - Submit results via PR

4. **Provide Feedback**
   - Include screenshots of notable interactions
   - Complete the qualitative feedback template

## Repository Structure

```
github-copilot-experiment/
├── README.md                      # Experiment overview and setup instructions
├── .github/
│   └── PULL_REQUEST_TEMPLATE.md   # Standardized PR template
├── tasks/
│   ├── unit-tests/                # Unit testing tasks
│   ├── functions/                 # Function creation tasks
│   ├── code-review/               # Code review tasks
│   └── documentation/             # Documentation tasks
├── metrics/
│   ├── templates/                 # JSON/YAML metrics templates
│   └── submissions/               # Where grads submit completed metrics
├── rs-copilot-examples/           # RS Copilot library integration examples
├── analysis/
│   ├── metrics_aggregator.py      # Script to extract and analyze metrics
│   ├── visualizations.py          # Code for visualizing results
│   └── roi_calculator.py          # ROI calculation based on time savings
└── resources/
    ├── setup_guide.md             # Tool setup instructions
    ├── evaluation_criteria.md     # Clear evaluation guidelines for tasks
    └── final_report_template.md   # Template for final recommendations
```

## Metrics Collection

- Use the provided YAML templates to record:
  - Task completion time
  - Number of iterations required
  - Self-assessed quality score
  - Tool satisfaction rating
  - Any notable observations

## Analysis & Results

The collected metrics will be used to:
1. Calculate time savings between tools
2. Compare code quality based on evaluation criteria
3. Determine ROI based on graduate hourly costs vs license cost
4. Create visualizations for presenting results
5. Generate a recommendation document for leadership

## Questions & Support

If you have any questions or need support during the experiment, please contact Hamza (experiment lead).
