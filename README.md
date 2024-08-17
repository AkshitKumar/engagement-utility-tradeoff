# RecSys Engagement-Utility Tradeoff Repository

This repository contains the source code for the paper "The Fault in Our Recommendations: On the Perils of Optimizing the Measurable". The paper models a recommendation system and explores the tradeoff between engagement and utility.

## Files in the Repository

### parameters.py
This file contains the parameters used in the model, such as the base utility of the popular and outside items, the parameters for the Generalized Pareto Distribution (GPD), the discount factor.

### helper.py
The `helper.py` file contains helper functions used in the model. These include functions to generate zero-mean Gumbel variables, compute the PDF and CDF of the GPD, compute the inverse CDF of the GPD, and sample from the GPD.

### dice_analytical.py
The `dice_analytical.py` file contains the main function `dice()`, which computes the expected engagement and welfare by showing one popular and one niche item until a certain time, and then showing the popular/niche item depending on the values of the niche and popular base utlities. This file is used for generating Figure 3 and 4 in the paper and provides an analytical approximation for the performance of DICE.

### app_analytical.py
The `app_analytical.py` file contains the main function `app()`. It analytically computes the expected engagement and welfare for APP. This file is used for generating Figure 3 and 4 in the paper and provides an analytical solution for the performance of APP.

### app_simulation.py
This file provides the engagement and utility for APP using simulations.

### dice_simulation.py
This file provides engagement and utility for DICE policy using simulations.

## How to Run

To run the files, follow these steps:

1. Ensure that you have Python installed on your machine.
2. Install the required libraries by running `pip install numpy scipy matplotlib`.
3. Run the `app_analytical.py` or `dice_analytical.py` file with `python app_analytical.py` or `python dice_analytical.py`.

Please note that `app_analytical.py`, `app_simulation.py`, `dice_analytical.py` and  `dice_simulation.py` import functions from `parameters.py`, `helper.py`, so make sure these files are in the same directory.