#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File              : plt_utils.py
# Author            : Chi Han, Jiayuan Mao
# Email             : haanchi@gmail.com, maojiayuan@gmail.com
# Date              : 02.07.2024
# Last Modified Date: 02.07.2024
# Last Modified By  : Jimmy Yao
#
# This file is part of the VCML codebase
# Distributed under MIT license
#
# printing / visualization

import numpy as np
import plotly.graph_objects as go

def plot_histogram(data, use_probability=False):
    """
    Plot a histogram using a Plotly scatter plot with lines.

    Parameters:
    - data: array-like, the dataset for the histogram.
    - use_probability: bool, if True, the y-axis will show probabilities instead of counts.
    """
    # Calculate the histogram data using np.histogram, with density based on use_probability
    counts, bin_edges = np.histogram(data, bins='auto', density=use_probability)
    
    # Calculate the x values as the average of the bin edges
    x_values = 0.5 * (bin_edges[:-1] + bin_edges[1:])
    
    # Determine the y-axis title based on the use_probability flag
    yaxis_title = 'Probability' if use_probability else 'Count'
    
    # Create a scatter plot with lines using Plotly
    fig = go.Figure(data=go.Scatter(x=x_values, y=counts, mode='lines+markers', name='Histogram'))
    
    # Update the layout for a better view
    fig.update_layout(title='Histogram with Scatter Plot',
                      xaxis_title='Data',
                      yaxis_title=yaxis_title,
                      template='plotly_dark')
    
    # Show the figure
    fig.show()

# # Example data
# data = np.random.randn(1000)

# # Plot the histogram with counts
# plot_histogram(data)

# # Plot the histogram with probability
# plot_histogram(data, use_probability=True)