# Dynamic Systems Identification (Polynomial Models)

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)

## Description
Dynamic Systems Identification (Polynomial Models) :
The provided script “dsi_tookit” leverages a package designed for identifying polynomial models. This is accomplished through a structured pipeline that includes generating candidate terms, detecting the model structure, estimating parameters, and validating both dynamic and static models. The core functionality focuses on analyzing flow plant systems with inherent noise and errors, specifically modeled as a quadratic polynomial corrupted by white noise.
The package supports the following features:
•	Dynamic Data Analysis: Processing and validating input and output time-series data using identification and validation datasets.
•	Structure Detection: Removing unsuitable clusters and applying optimization algorithms (such as AIC and ERR) to refine the model structure.
•	Parameter Estimation: Utilizing methods like Extended Least Squares (ELS) and Restricted Extended Least Squares (RELS) to compute model parameters.
•	Model Validation: Evaluating performance through residual analysis and correlation coefficients.
•	Static Model Simulation: Generating static responses and simulating system behavior under various input conditions.
Usage Instructions:
To use this class/package, follow these steps:
1.	Prepare and Load Data: Load dynamic data (flow_dataset and static_dataset) representing the system's input and output.
2.	Visualize Input/Output: Create visual plots to inspect and compare identification and validation datasets.
3.	Generate Candidate Model Terms: Use dsi_tookit.generateCandidateTerms to build a matrix of potential terms for system characterization.
4.	Detect Model Structure:
	    Use dsi_tookit.removeClusters to filter out invalid clusters and refine the model structure.
	    Run dsi_tookit.detectStructure to apply algorithms like AIC and ERR for precise structural identification.
5.	Estimate Model Parameters:
            Extract dynamic information using dsi_tookit.getInfo.
            Apply dsi_tookit.estimateParametersELS or  dsi_tookit.estimateParametersRELS to calculate the model parameters.
6.	Validate the Model:
            Use dsi_tookit.validateModel to verify the dynamic model's accuracy and analyze residual behavior.
            Simulate the static model using functions like dsi_tookit.buildStaticResponse and dsi_tookit.displayStaticModel to derive and simulate the system's static behavior.
7.	Analyze Results: Evaluate the root mean square error (RMSE), residual correlations, and validate the alignment between real and simulated data.
For more information please see the examples files: exampleELS and exampleRELS

Cite As:
Barroso, M. F. S, Mendes, E. M. A. M. and Marciano, J. J. S. (2025). Dynamic Systems Identification (Polynomial Models) (https://pypi.org/project/dsi-toolkit/), pypi.org. Retrieved March 16, 2025.
## Installation
To install the package, use:
```sh
pip install dsi_toolkit
