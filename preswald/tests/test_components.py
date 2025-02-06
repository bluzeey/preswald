import pytest
import matplotlib.pyplot as plt
import numpy as np
from preswald.components import matplotlib_plot

def test_matplotlib_plot_basic():
    """Test basic Matplotlib plot creation"""
    # Create a simple plot
    plt.figure(figsize=(6, 4))
    plt.plot([1, 2, 3, 4], [1, 4, 2, 3])
    plt.title('Test Plot')

    # Render the plot
    component = matplotlib_plot(plt.gcf())

    # Assertions
    assert component['type'] == 'matplotlib_plot'
    assert 'id' in component
    assert 'data' in component
    assert 'image' in component['data']
    assert component['data']['image'].startswith('data:image/png;base64,')

def test_matplotlib_plot_complex():
    """Test a more complex Matplotlib plot"""
    # Create a more complex plot with multiple elements
    plt.figure(figsize=(8, 6))
    x = np.linspace(0, 10, 100)
    plt.plot(x, np.sin(x), label='sin(x)')
    plt.plot(x, np.cos(x), label='cos(x)')
    plt.title('Trigonometric Functions')
    plt.xlabel('X axis')
    plt.ylabel('Y axis')
    plt.legend()

    # Render the plot
    component = matplotlib_plot(plt.gcf())

    # Assertions
    assert component['type'] == 'matplotlib_plot'
    assert 'image' in component['data']

def test_matplotlib_plot_error_handling():
    """Test error handling for invalid input"""
    with pytest.raises(Exception):
        # Pass an invalid object
        matplotlib_plot(None)