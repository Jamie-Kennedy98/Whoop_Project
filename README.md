# Whoop_Project

An analysis of my personal Whoop data. This analysis includes an exploration of the data followed by predictive modelling carried out using AWS Sagemaker.


## Table of Contents

1. [Installation](#installation)
2. [Data Download](#data-download)
3. [Usage](#usage)


## Installation

To use this app, follow the steps below:

1. Clone this repository:

   ```
   git clone https://github.com/Jamie-Kennedy98/Whoop_Project.git
   ```

2. Navigate to the directory of the cloned repository.

3. Install the required Python packages:

   ```
   pip install -r requirements.txt
   ```

## Data Download

For this project I used my own personal whoop date but you can download your whoop data and use it instead. I also sourced external weather data which can be downloaded at https://www.met.ie/climate/available-data/historical-data. After downloading, please place the data files in a folder named `data` at the root of the project.

## Usage

This project contains a script for cleaning, exploration and carrying out the analysis and the files have been named appropriately. If you are not interested in exploring the data yourself then all of the code used to carry out the data cleaning and preparation is wrapped in functions in the functions.py file which are then called during the analysis so it is possible to complete this project by just running the analysis.ipynb file.

