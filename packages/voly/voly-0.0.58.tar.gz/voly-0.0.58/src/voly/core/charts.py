"""
Visualization module for the Voly package.

This module provides visualization functions for volatility surfaces,
risk-neutral densities, and model fitting results.
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional, Union, Any
from voly.utils.logger import logger, catch_exception
from voly.models import SVIModel
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.io as pio
import plotly.express as px
from plotly.colors import hex_to_rgb, make_colorscale


# Set default renderer to browser for interactive plots
pio.renderers.default = "browser"


@catch_exception
def plot_volatility_smile(moneyness_array: np.ndarray,
                          iv_array: np.ndarray,
                          market_data: pd.DataFrame = None,
                          maturity: Optional[float] = None,
                          ) -> go.Figure:
    """
    Plot volatility smile for a single expiry.

    Parameters:
    - moneyness_array: Moneyness grid
    - iv_array: Implied volatility values
    - market_data: Optional market data for comparison
    - maturity: Maturity name for filtering market data

    Returns:
    - Plotly figure
    """
    fig = go.Figure()

    # Add model curve
    fig.add_trace(
        go.Scatter(
            x=moneyness_array,
            y=iv_array * 100,  # Convert to percentage
            mode='lines',
            name='Model',
            line=dict(color='#0080FF', width=2)
        )
    )

    # Filter market data for the specific expiry
    maturity_data = market_data[market_data['maturity_name'] == maturity]

    if not maturity_data.empty:
        # Add bid IV
        fig.add_trace(
            go.Scatter(
                x=maturity_data['log_moneyness'],
                y=maturity_data['bid_iv'] * 100,  # Convert to percentage
                mode='markers',
                name='Bid IV',
                marker=dict(size=8, symbol='circle', opacity=0.7)
            )
        )

        # Add ask IV
        fig.add_trace(
            go.Scatter(
                x=maturity_data['log_moneyness'],
                y=maturity_data['ask_iv'] * 100,  # Convert to percentage
                mode='markers',
                name='Ask IV',
                marker=dict(size=8, symbol='circle', opacity=0.7)
            )
        )

    dte_value = maturity_data['dte'].iloc[0]

    # Update layout
    fig.update_layout(
        title=f'Vol Smile for {maturity} (DTE: {dte_value:.1f})',
        xaxis_title='Log Moneyness',
        yaxis_title='Implied Volatility (%)',
        template='plotly_dark',
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1)
    )

    return fig


@catch_exception
def plot_all_smiles(moneyness_array: np.ndarray,
                    iv_surface: Dict[float, np.ndarray],
                    market_data: Optional[pd.DataFrame] = None) -> List[go.Figure]:
    """
    Plot volatility smiles for all expiries.

    Parameters:
    - moneyness: Moneyness grid
    - iv_surface: Dictionary mapping expiry times to IV arrays
    - market_data: Optional market data for comparison

    Returns:
    - List of Plotly figures
    """
    figures = []

    # Get maturities
    maturities = list(iv_surface.keys())

    # Create a figure for each expiry
    for maturity in maturities:
        fig = plot_volatility_smile(
            moneyness_array=moneyness_array,
            iv_array=iv_surface[maturity],
            market_data=market_data,
            maturity=maturity
        )
        figures.append(fig)

    return figures


@catch_exception
def plot_parameters(raw_param_matrix: pd.DataFrame,
                    jw_param_matrix: Optional[pd.DataFrame] = None) -> Tuple[go.Figure, Optional[go.Figure]]:
    """
    Plot model parameters across different expiries.

    Parameters:
    - raw_param_matrix: Matrix of raw SVI parameters with maturity names as columns
    - jw_param_matrix: Optional matrix of Jump-Wing parameters

    Returns:
    - Tuple of Plotly figures (raw_params_fig, jw_params_fig)
    """
    # Plot raw SVI parameters
    param_names = raw_param_matrix.index
    raw_fig = make_subplots(rows=3, cols=2, subplot_titles=[f"Parameter {p}: {SVIModel.PARAM_DESCRIPTIONS.get(p, '')}"
                                                            for p in param_names] + [''])

    # Get maturity names (columns) in order
    maturity_names = raw_param_matrix.columns

    # Get YTE and DTE values from attributes
    yte_values = raw_param_matrix.attrs['yte_values']
    dte_values = raw_param_matrix.attrs['dte_values']

    # Create custom x-axis tick labels
    tick_labels = [f"{m} (DTE: {dte_values[m]:.1f}, YTE: {yte_values[m]:.4f})" for m in maturity_names]

    # Plot each parameter
    for i, param in enumerate(param_names):
        row = i // 2 + 1
        col = i % 2 + 1

        raw_fig.add_trace(
            go.Scatter(
                x=list(range(len(maturity_names))),  # Use indices for x-axis positioning
                y=raw_param_matrix.loc[param],
                mode='lines+markers',
                name=param,
                line=dict(width=2),
                marker=dict(size=8),
                text=tick_labels,  # Add hover text
                hovertemplate="%{text}<br>%{y:.4f}"
            ),
            row=row, col=col
        )

        # Update x-axis for this subplot with custom tick labels
        raw_fig.update_xaxes(
            tickvals=list(range(len(maturity_names))),
            ticktext=maturity_names,
            tickangle=45,
            row=row, col=col
        )

    # Update layout for raw parameters
    raw_fig.update_layout(
        title='Raw SVI Parameters Across Expiries',
        template='plotly_dark',
        showlegend=False,
        height=800
    )

    # Plot Jump-Wing parameters if provided
    jw_fig = None
    if jw_param_matrix is not None:
        jw_param_names = jw_param_matrix.index
        jw_fig = make_subplots(rows=3, cols=2,
                               subplot_titles=[f"Parameter {p}: {SVIModel.PARAM_DESCRIPTIONS.get(p, '')}"
                                               for p in jw_param_names] + [''])

        # Plot each JW parameter
        for i, param in enumerate(jw_param_names):
            row = i // 2 + 1
            col = i % 2 + 1

            jw_fig.add_trace(
                go.Scatter(
                    x=list(range(len(maturity_names))),  # Use indices for x-axis positioning
                    y=jw_param_matrix.loc[param],
                    mode='lines+markers',
                    name=param,
                    line=dict(width=2, color='rgb(0, 180, 180)'),
                    marker=dict(size=8),
                    text=tick_labels,  # Add hover text
                    hovertemplate="%{text}<br>%{y:.4f}"
                ),
                row=row, col=col
            )

            # Update x-axis for this subplot with custom tick labels
            jw_fig.update_xaxes(
                tickvals=list(range(len(maturity_names))),
                ticktext=maturity_names,
                tickangle=45,
                row=row, col=col
            )

        # Update layout for JW parameters
        jw_fig.update_layout(
            title='Jump-Wing Parameters Across Expiries',
            template='plotly_dark',
            showlegend=False,
            height=800
        )

    return raw_fig, jw_fig


@catch_exception
def plot_fit_performance(fit_performance: pd.DataFrame) -> go.Figure:
    """
    Plot the fitting accuracy statistics.

    Parameters:
    - stats_df: DataFrame with fitting statistics

    Returns:
    - Plotly figure
    """
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=['RMSE by Expiry', 'MAE by Expiry',
                        'R² by Expiry', 'Max Error by Expiry']
    )

    # Create custom tick labels with maturity name, DTE, and YTE
    tick_labels = [f"{m} (DTE: {d:.1f})" for m, d in
                   zip(fit_performance['Maturity'], fit_performance['DTE'])]

    # Get x-axis values for plotting (use indices for positioning)
    x_indices = list(range(len(fit_performance)))

    # Plot RMSE
    fig.add_trace(
        go.Scatter(
            x=x_indices,
            y=fit_performance['RMSE'] * 100,  # Convert to percentage
            mode='lines+markers',
            name='RMSE',
            line=dict(width=2),
            marker=dict(size=8),
            text=tick_labels  # Add hover text
        ),
        row=1, col=1
    )

    # Plot MAE
    fig.add_trace(
        go.Scatter(
            x=x_indices,
            y=fit_performance['MAE'] * 100,  # Convert to percentage
            mode='lines+markers',
            name='MAE',
            line=dict(width=2),
            marker=dict(size=8),
            text=tick_labels  # Add hover text
        ),
        row=1, col=2
    )

    # Plot R²
    fig.add_trace(
        go.Scatter(
            x=x_indices,
            y=fit_performance['R²'],
            mode='lines+markers',
            name='R²',
            line=dict(width=2),
            marker=dict(size=8),
            text=tick_labels  # Add hover text
        ),
        row=2, col=1
    )

    # Plot Max Error
    fig.add_trace(
        go.Scatter(
            x=x_indices,
            y=fit_performance['Max Error'] * 100,  # Convert to percentage
            mode='lines+markers',
            name='Max Error',
            line=dict(width=2),
            marker=dict(size=8),
            text=tick_labels  # Add hover text
        ),
        row=2, col=2
    )

    # Update x-axis for all subplots with maturity names
    for row in range(1, 3):
        for col in range(1, 3):
            fig.update_xaxes(
                tickvals=x_indices,
                ticktext=fit_performance['Maturity'],
                tickangle=45,
                row=row, col=col
            )

    # Update y-axis titles
    fig.update_yaxes(title_text='RMSE (%)', row=1, col=1)
    fig.update_yaxes(title_text='MAE (%)', row=1, col=2)
    fig.update_yaxes(title_text='R²', row=2, col=1)
    fig.update_yaxes(title_text='Max Error (%)', row=2, col=2)

    # Update layout
    fig.update_layout(
        title='Model Fitting Accuracy Statistics',
        template='plotly_dark',
        showlegend=False
    )

    return fig


@catch_exception
def plot_3d_surface(moneyness_array: np.ndarray,
                    iv_surface: dict[float, np.ndarray]) -> go.Figure:
    """
    Plot 3D implied volatility surface.

    Parameters:
    - moneyness_array: grid of moneyness values
    - iv_surface: Dictionary mapping expiry times to IV arrays

    Returns:
    - Plotly figure
    """
    start_color = '#60AEFC'
    end_color = '#002040'  # Darker blue
    custom_blue_scale = [[0, start_color], [1, end_color]]
    maturities = list(iv_surface.keys())

    # Convert implied volatility surface to array
    z_array = np.array([iv_surface[m] for m in maturities])

    # Create mesh grid
    X, Y = np.meshgrid(moneyness_array, maturities)
    Z = z_array * 100  # Convert to percentage

    # Create 3D surface plot with custom blue colorscale
    fig = go.Figure(data=[go.Surface(z=Z, x=X, y=Y, colorscale=custom_blue_scale)])

    # Add colorbar
    fig.update_traces(contours_z=dict(show=True, usecolormap=True,
                                      highlightcolor="#0080FF", project_z=True))

    # Update layout
    fig.update_layout(
        title='Implied Volatility 3D Surface',
        template='plotly_dark',
        scene=dict(
            xaxis_title='Log Moneyness',
            yaxis_title='Maturities',
            zaxis_title='Implied Volatility (%)'
        ),
        margin=dict(l=65, r=50, b=65, t=90)
    )

    return fig


@catch_exception
def plot_rnd(moneyness_array: np.ndarray,
             rnd_values: np.ndarray,
             spot_price: float = 1.0) -> go.Figure:
    """
    Plot risk-neutral density (RND).

    Parameters:
    - moneyness_array: Grid of log-moneyness values
    - rnd_values: RND values
    - spot_price: Spot price for converting to absolute prices
    - title: Plot title

    Returns:
    - Plotly figure
    """
    # Create figure
    fig = go.Figure()

    # Convert to prices and normalize RND
    prices = spot_price * np.exp(moneyness_array)

    # Normalize the RND to integrate to 1
    dx = moneyness_array[1] - moneyness_array[0]
    total_density = np.sum(rnd_values) * dx
    normalized_rnd = rnd_values / total_density if total_density > 0 else rnd_values

    # Add trace
    fig.add_trace(
        go.Scatter(
            x=prices,
            y=normalized_rnd,
            mode='lines',
            name='RND',
            line=dict(color='#00FFC1', width=2),
            fill='tozeroy',
            fillcolor='rgba(0, 255, 193, 0.2)'
        )
    )

    # Add vertical line at spot price
    fig.add_shape(
        type='line',
        x0=spot_price, y0=0,
        x1=spot_price, y1=max(normalized_rnd) * 1.1,
        line=dict(color='red', width=2, dash='dash')
    )

    # Add annotation for spot price
    fig.add_annotation(
        x=spot_price,
        y=max(normalized_rnd) * 1.15,
        text=f"Spot: {spot_price}",
        showarrow=False,
        font=dict(color='red')
    )

    # Update layout
    fig.update_layout(
        title='Risk-Neutral Density',
        xaxis_title='Price',
        yaxis_title='Density',
        template='plotly_dark',
        showlegend=False
    )

    return fig


@catch_exception
def plot_rnd_all_expiries(moneyness_array: np.ndarray,
                          rnd_surface: Dict[str, np.ndarray],
                          fit_results: Dict[str, Any],
                          spot_price: float = 1.0) -> go.Figure:
    """
    Plot risk-neutral densities for all expiries.

    Parameters:
    - moneyness_array: Grid of log-moneyness values
    - rnd_surface: Dictionary mapping maturity names to RND arrays
    - param_matrix: Matrix containing model parameters with maturity info
    - spot_price: Spot price for converting to absolute prices

    Returns:
    - Plotly figure
    """
    # Get maturity information
    dte_values = fit_results['fit_performance']['DTE']

    # Create figure
    fig = go.Figure()

    # Get maturity names in order by DTE
    maturity_names = sorted(rnd_surface.keys(), key=lambda x: dte_values[x])

    # Create color scale from purple to green
    n_maturities = len(maturity_names)
    colors = [f'rgb({int(255 - i * 255 / n_maturities)}, {int(i * 255 / n_maturities)}, 255)'
              for i in range(n_maturities)]

    # Convert to prices
    prices = spot_price * np.exp(moneyness_array)

    # Add traces for each expiry
    for i, maturity_name in enumerate(maturity_names):
        rnd = rnd_surface[maturity_name]
        dte = dte_values[maturity_name]

        # Normalize the RND
        dx = moneyness_array[1] - moneyness_array[0]
        total_density = np.sum(rnd) * dx
        normalized_rnd = rnd / total_density if total_density > 0 else rnd

        # Add trace
        fig.add_trace(
            go.Scatter(
                x=prices,
                y=normalized_rnd,
                mode='lines',
                name=f"{maturity_name} (DTE: {dte:.1f})",
                line=dict(color=colors[i], width=2),
            )
        )

    # Add vertical line at spot price
    fig.add_shape(
        type='line',
        x0=spot_price, y0=0,
        x1=spot_price, y1=1,  # Will be scaled automatically
        line=dict(color='red', width=2, dash='dash')
    )

    # Update layout
    fig.update_layout(
        title="Risk-Neutral Densities Across Expiries",
        xaxis_title='Price',
        yaxis_title='Density',
        template='plotly_dark',
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01
        )
    )

    return fig


@catch_exception
def plot_rnd_3d(moneyness_array: np.ndarray,
                rnd_surface: Dict[str, np.ndarray],
                param_matrix: pd.DataFrame,
                spot_price: float = 1.0) -> go.Figure:
    """
    Plot 3D surface of risk-neutral densities.

    Parameters:
    - moneyness_array: Grid of log-moneyness values
    - rnd_surface: Dictionary mapping maturity names to RND arrays
    - param_matrix: Matrix containing model parameters with maturity info
    - spot_price: Spot price for converting to absolute prices

    Returns:
    - Plotly figure
    """
    # Get maturity information
    dte_values = param_matrix.attrs['dte_values']

    # Get maturity names in order by DTE
    maturity_names = sorted(rnd_surface.keys(), key=lambda x: dte_values[x])

    # Extract DTE values for z-axis
    dte_list = [dte_values[name] for name in maturity_names]

    # Convert to prices
    prices = spot_price * np.exp(moneyness_array)

    # Create z-data matrix and normalize RNDs
    z_data = np.zeros((len(maturity_names), len(prices)))

    for i, name in enumerate(maturity_names):
        rnd = rnd_surface[name]

        # Normalize the RND
        dx = moneyness_array[1] - moneyness_array[0]
        total_density = np.sum(rnd) * dx
        normalized_rnd = rnd / total_density if total_density > 0 else rnd

        z_data[i] = normalized_rnd

    # Create mesh grid
    X, Y = np.meshgrid(prices, dte_list)

    # Create 3D surface
    fig = go.Figure(data=[
        go.Surface(
            z=z_data,
            x=X,
            y=Y,
            colorscale='Viridis',
            showscale=True
        )
    ])

    # Update layout
    fig.update_layout(
        title="3D Risk-Neutral Density Surface",
        scene=dict(
            xaxis_title="Price",
            yaxis_title="Days to Expiry",
            zaxis_title="Density"
        ),
        margin=dict(l=65, r=50, b=65, t=90),
        template="plotly_dark"
    )

    return fig


@catch_exception
def plot_rnd_statistics(rnd_statistics: pd.DataFrame,
                        rnd_probabilities: pd.DataFrame) -> Tuple[go.Figure, go.Figure]:
    """
    Plot RND statistics and probabilities.

    Parameters:
    - rnd_statistics: DataFrame with RND statistics
    - rnd_probabilities: DataFrame with RND probabilities

    Returns:
    - Tuple of (statistics_fig, probabilities_fig)
    """
    # Create subplot figure for key statistics
    stats_fig = make_subplots(
        rows=1, cols=3,
        subplot_titles=("Standard Deviation (%) vs. DTE",
                        "Skewness vs. DTE",
                        "Excess Kurtosis vs. DTE")
    )

    # Add traces for each statistic
    stats_fig.add_trace(
        go.Scatter(
            x=rnd_statistics["dte"],
            y=rnd_statistics["std_dev_pct"],
            mode="lines+markers",
            name="Standard Deviation (%)",
            hovertemplate="DTE: %{x:.1f}<br>Std Dev: %{y:.2f}%"
        ),
        row=1, col=1
    )

    stats_fig.add_trace(
        go.Scatter(
            x=rnd_statistics["dte"],
            y=rnd_statistics["skewness"],
            mode="lines+markers",
            name="Skewness",
            hovertemplate="DTE: %{x:.1f}<br>Skewness: %{y:.4f}"
        ),
        row=1, col=2
    )

    stats_fig.add_trace(
        go.Scatter(
            x=rnd_statistics["dte"],
            y=rnd_statistics["excess_kurtosis"],
            mode="lines+markers",
            name="Excess Kurtosis",
            hovertemplate="DTE: %{x:.1f}<br>Excess Kurtosis: %{y:.4f}"
        ),
        row=1, col=3
    )

    # Update layout
    stats_fig.update_layout(
        title="Risk-Neutral Density Statistics Across Expiries",
        template="plotly_dark",
        height=500,
        showlegend=False
    )

    # Update axes
    stats_fig.update_xaxes(title_text="Days to Expiry", row=1, col=1)
    stats_fig.update_xaxes(title_text="Days to Expiry", row=1, col=2)
    stats_fig.update_xaxes(title_text="Days to Expiry", row=1, col=3)

    stats_fig.update_yaxes(title_text="Standard Deviation (%)", row=1, col=1)
    stats_fig.update_yaxes(title_text="Skewness", row=1, col=2)
    stats_fig.update_yaxes(title_text="Excess Kurtosis", row=1, col=3)

    # Create a second figure for probability thresholds
    prob_fig = go.Figure()

    # Get probability columns (those starting with "p_")
    prob_cols = [col for col in rnd_probabilities.columns if col.startswith("p_")]

    # Sort the columns to ensure they're in order by threshold value
    prob_cols_above = sorted([col for col in prob_cols if "above" in col],
                             key=lambda x: float(x.split("_")[2]))
    prob_cols_below = sorted([col for col in prob_cols if "below" in col],
                             key=lambda x: float(x.split("_")[2]))

    # Color gradients
    green_colors = [
        'rgba(144, 238, 144, 1)',  # Light green
        'rgba(50, 205, 50, 1)',  # Lime green
        'rgba(34, 139, 34, 1)',  # Forest green
        'rgba(0, 100, 0, 1)'  # Dark green
    ]

    red_colors = [
        'rgba(139, 0, 0, 1)',  # Dark red
        'rgba(220, 20, 60, 1)',  # Crimson
        'rgba(240, 128, 128, 1)',  # Light coral
        'rgba(255, 182, 193, 1)'  # Light pink/red
    ]

    # Add lines for upside probabilities (green)
    for i, col in enumerate(prob_cols_above):
        threshold = float(col.split("_")[2])
        label = f"P(X > {threshold})"

        # Select color based on how far OTM
        color_idx = min(i, len(green_colors) - 1)

        prob_fig.add_trace(
            go.Scatter(
                x=rnd_probabilities["dte"],
                y=rnd_probabilities[col] * 100,  # Convert to percentage
                mode="lines+markers",
                name=label,
                line=dict(color=green_colors[color_idx], width=3),
                marker=dict(size=8, color=green_colors[color_idx]),
                hovertemplate="DTE: %{x:.1f}<br>" + label + ": %{y:.2f}%"
            )
        )

    # Add lines for downside probabilities (red)
    for i, col in enumerate(prob_cols_below):
        threshold = float(col.split("_")[2])
        label = f"P(X < {threshold})"

        # Select color based on how far OTM
        color_idx = min(i, len(red_colors) - 1)

        prob_fig.add_trace(
            go.Scatter(
                x=rnd_probabilities["dte"],
                y=rnd_probabilities[col] * 100,  # Convert to percentage
                mode="lines+markers",
                name=label,
                line=dict(color=red_colors[color_idx], width=3),
                marker=dict(size=8, color=red_colors[color_idx]),
                hovertemplate="DTE: %{x:.1f}<br>" + label + ": %{y:.2f}%"
            )
        )

    # Update layout
    prob_fig.update_layout(
        title="Probability Thresholds Across Expiries",
        xaxis_title="Days to Expiry",
        yaxis_title="Probability (%)",
        template="plotly_dark",
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="right",
            x=0.99
        )
    )

    return stats_fig, prob_fig


@catch_exception
def plot_cdf(moneyness_array: np.ndarray,
             rnd_values: np.ndarray,
             spot_price: float = 1.0,
             title: str = 'Cumulative Distribution Function') -> go.Figure:
    """
    Plot the cumulative distribution function (CDF) from RND values.

    Parameters:
    - moneyness_array: Grid of log-moneyness values
    - rnd_values: RND values
    - spot_price: Spot price for converting to absolute prices
    - title: Plot title

    Returns:
    - Plotly figure
    """
    # Convert to prices and normalize RND
    prices = spot_price * np.exp(moneyness_array)

    # Normalize the RND
    dx = moneyness_array[1] - moneyness_array[0]
    total_density = np.sum(rnd_values) * dx
    normalized_rnd = rnd_values / total_density if total_density > 0 else rnd_values

    # Calculate CDF
    cdf = np.cumsum(normalized_rnd) * dx

    # Create figure
    fig = go.Figure()

    # Add CDF trace
    fig.add_trace(
        go.Scatter(
            x=prices,
            y=cdf,
            mode='lines',
            name='CDF',
            line=dict(color='#00FFC1', width=2)
        )
    )

    # Add vertical line at spot price
    fig.add_shape(
        type='line',
        x0=spot_price, y0=0,
        x1=spot_price, y1=1,
        line=dict(color='red', width=2, dash='dash')
    )

    # Add horizontal line at CDF=0.5 (median)
    fig.add_shape(
        type='line',
        x0=prices[0], y0=0.5,
        x1=prices[-1], y1=0.5,
        line=dict(color='orange', width=2, dash='dash')
    )

    # Add annotation for spot price
    fig.add_annotation(
        x=spot_price,
        y=1.05,
        text=f"Spot: {spot_price}",
        showarrow=False,
        font=dict(color='red')
    )

    # Update layout
    fig.update_layout(
        title=title,
        xaxis_title='Price',
        yaxis_title='Cumulative Probability',
        template='plotly_dark',
        yaxis=dict(range=[0, 1.1]),
        showlegend=False
    )

    return fig


@catch_exception
def plot_pdf(moneyness_array: np.ndarray,
             rnd_values: np.ndarray,
             spot_price: float = 1.0,
             title: str = 'Probability Density Function') -> go.Figure:
    """
    Plot the probability density function (PDF) from RND values.

    Parameters:
    - moneyness_array: Grid of log-moneyness values
    - rnd_values: RND values
    - spot_price: Spot price for converting to absolute prices
    - title: Plot title

    Returns:
    - Plotly figure
    """
    # This is essentially the same as plot_rnd but with a different title
    return plot_rnd(moneyness_array, rnd_values, spot_price, title)


@catch_exception
def plot_interpolated_surface(
        interp_results: Dict[str, Any],
        title: str = 'Interpolated Implied Volatility Surface'
) -> go.Figure:
    """
    Plot interpolated implied volatility surface.

    Parameters:
    - interp_results: Dictionary with interpolation results
    - title: Plot title

    Returns:
    - Plotly figure
    """
    # Extract data from interpolation results
    moneyness_array = interp_results['moneyness_array']
    target_expiries_years = interp_results['target_expiries_years']
    iv_surface = interp_results['iv_surface']

    # Create a 3D surface plot
    fig = plot_3d_surface(
        moneyness=moneyness_array,
        expiries=target_expiries_years,
        iv_surface=iv_surface,
        title=title
    )

    return fig

