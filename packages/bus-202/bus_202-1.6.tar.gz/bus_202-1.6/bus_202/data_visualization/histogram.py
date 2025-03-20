import matplotlib.pyplot as plt
import numpy as np
from .trim import trim

def histogram(series, title=None, bins=30, trim_outliers=100, details=False):
    # Create figure and axis
    fig, ax = plt.subplots()
    
    # Get base title
    if not title:
        title = series.name
        
    # Apply trimming if trim < 100
    if trim_outliers < 100:
        series = trim(series, trim_outliers)
        title = f"{title} (outliers removed at {trim_outliers}% level)"
    
    # Convert to numpy array and handle NaN
    data = np.array(series.dropna()).flatten()
    
    # Create histogram
    ax.hist(data, 
            bins=bins,
            edgecolor='black',
            color='skyblue',
            alpha=0.7)
    
    # Add labels and styling
    ax.set_title(title)
    ax.set_ylabel('Count')
    ax.ticklabel_format(style='plain', axis='x')
    ax.grid(True, linestyle='--', alpha=0.7)
    
    if details:
        # Add mean and median lines
        mean = np.mean(data)
        median = np.median(data)
        ax.axvline(mean, color='red', linestyle='--', label=f'Mean: {mean:.2f}')
        ax.axvline(median, color='green', linestyle='--', label=f'Median: {median:.2f}')
        
        # Calculate standard deviations
        std = np.std(data)
        
        # Calculate percentages within SDs
        within_1sd = np.sum((data >= mean - std) & (data <= mean + std)) / len(data) * 100
        within_2sd = np.sum((data >= mean - 2*std) & (data <= mean + 2*std)) / len(data) * 100
        within_3sd = np.sum((data >= mean - 3*std) & (data <= mean + 3*std)) / len(data) * 100
        
        # Add text box with statistics
        stats_text = (
            f'Skewness: {series.skew():.3f}\n'
            f'Within 1 SD: {within_1sd:.1f}%\n'
            f'Within 2 SD: {within_2sd:.1f}%\n'
            f'Within 3 SD: {within_3sd:.1f}%'
        )
        plt.text(0.95, 0.95, stats_text,
                transform=ax.transAxes,
                verticalalignment='top',
                horizontalalignment='right',
                bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
        
        # Add legend
        plt.legend()
    
    plt.show(block=False)
