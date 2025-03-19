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

# Set default renderer to browser for interactive plots
pio.renderers.default = "browser"


@catch_exception
def plot_volatility_smile(x_domain: np.ndarray,
                          iv_array: np.ndarray,
                          option_chain: pd.DataFrame = None,
                          maturity: Optional[str] = None,
                          domain_type: str = 'log_moneyness') -> go.Figure:
    """
    Plot volatility smile for a single expiry.

    Parameters:
    - x_domain: Array of x-axis values (log_moneyness, moneyness, strikes, delta)
    - iv_array: Implied volatility values
    - option_chain: Optional market data for comparison
    - maturity: Maturity name for filtering market data
    - domain_type: Type of x-domain ('log_moneyness', 'moneyness', 'strikes', 'delta')

    Returns:
    - Plotly figure
    """
    fig = go.Figure()

    # Map domain types to axis labels
    domain_labels = {
        'log_moneyness': 'Log Moneyness',
        'moneyness': 'Moneyness (S/K)',
        'strikes': 'Strike Price',
        'delta': 'Call Delta'
    }

    # Add model curve
    fig.add_trace(
        go.Scatter(
            x=x_domain,
            y=iv_array * 100,  # Convert to percentage
            mode='lines',
            name='Model',
            line=dict(color='#0080FF', width=2)
        )
    )

    # Add market data if provided
    if option_chain is not None and maturity is not None:
        maturity_data = option_chain[option_chain['maturity_name'] == maturity]

        if not maturity_data.empty:
            # For market data, use log_moneyness by default as x-axis
            market_x = maturity_data['log_moneyness']

            # If domain is not log_moneyness, convert market data to match the domain
            if domain_type == 'moneyness':
                market_x = np.exp(market_x)
            elif domain_type == 'strikes':
                s = maturity_data['underlying_price'].iloc[0]
                market_x = s / np.exp(market_x)
            elif domain_type == 'delta':
                # For delta, we'd need more complex conversion - only show model curve
                pass

            # Add bid and ask IVs if the domain type allows
            if domain_type != 'delta':
                for iv_type in ['bid_iv', 'ask_iv']:
                    if iv_type in maturity_data.columns:
                        fig.add_trace(
                            go.Scatter(
                                x=market_x,
                                y=maturity_data[iv_type] * 100,  # Convert to percentage
                                mode='markers',
                                name=iv_type.replace('_', ' ').upper(),
                                marker=dict(size=8, symbol='circle', opacity=0.7)
                            )
                        )

            dte_value = maturity_data['dtm'].iloc[0]

            # Update layout
            fig.update_layout(
                title=f'Vol Smile for {maturity} (DTE: {dte_value:.1f})',
                xaxis_title=domain_labels.get(domain_type, 'X Domain'),
                yaxis_title='Implied Volatility (%)',
                template='plotly_dark',
                legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1)
            )

    return fig


@catch_exception
def plot_all_smiles(x_surface: Dict[str, np.ndarray],
                    iv_surface: Dict[str, np.ndarray],
                    option_chain: Optional[pd.DataFrame] = None,
                    domain_type: str = 'log_moneyness') -> List[go.Figure]:
    """
    Plot volatility smiles for all expiries.

    Parameters:
    - x_surface: Dictionary mapping maturity names to x-domain arrays
    - iv_surface: Dictionary mapping maturity names to IV arrays
    - option_chain: Optional market data for comparison
    - domain_type: Type of x-domain ('log_moneyness', 'moneyness', 'strikes', 'delta')

    Returns:
    - List of Plotly figures
    """
    return [
        plot_volatility_smile(
            x_domain=x_surface[maturity],
            iv_array=iv_surface[maturity],
            option_chain=option_chain,
            maturity=maturity,
            domain_type=domain_type
        )
        for maturity in iv_surface.keys()
    ]


@catch_exception
def plot_parameters(fit_results: pd.DataFrame) -> go.Figure:
    """
    Plot raw SVI parameters across different expiries.

    Parameters:
    - fit_results: DataFrame from fit_model() with maturity names as index

    Returns:
    - Plotly figure
    """
    # Select parameters to plot
    param_names = ['a', 'b', 'sigma', 'rho', 'm']

    # Create subplots
    fig = make_subplots(
        rows=3, cols=2,
        subplot_titles=[f"Parameter {p}: {SVIModel.PARAM_DESCRIPTIONS.get(p, '')}"
                        for p in param_names] + ['']
    )

    # Get maturity names from index
    maturity_names = fit_results.index

    # Create hover text with maturity info
    tick_labels = [f"{m} (DTE: {fit_results.loc[m, 'dtm']:.1f})"
                   for m in maturity_names]

    # Plot each parameter
    for i, param in enumerate(param_names):
        row, col = (i // 2) + 1, (i % 2) + 1

        fig.add_trace(
            go.Scatter(
                x=list(range(len(maturity_names))),
                y=fit_results[param],
                mode='lines+markers',
                name=param,
                line=dict(width=2),
                marker=dict(size=8),
                text=tick_labels,
                hovertemplate="%{text}<br>%{y:.4f}"
            ),
            row=row, col=col
        )

        # Set x-axis labels
        fig.update_xaxes(
            tickvals=list(range(len(maturity_names))),
            ticktext=maturity_names,
            tickangle=45,
            row=row, col=col
        )

    # Update layout
    fig.update_layout(
        title='Raw SVI Parameters Across Expiries',
        template='plotly_dark',
        showlegend=False
    )

    return fig


@catch_exception
def plot_jw_parameters(fit_results: pd.DataFrame) -> go.Figure:
    """
    Plot Jump-Wing parameters across different expiries.

    Parameters:
    - fit_results: DataFrame from fit_model() with maturity names as index

    Returns:
    - Plotly figure
    """
    # Select parameters to plot
    param_names = ['nu', 'psi', 'p', 'c', 'nu_tilde']

    # Create subplots
    fig = make_subplots(
        rows=3, cols=2,
        subplot_titles=[f"Parameter {p}: {SVIModel.PARAM_DESCRIPTIONS.get(p, '')}"
                        for p in param_names] + ['']
    )

    # Get maturity names from index
    maturity_names = fit_results.index

    # Create hover text with maturity info
    tick_labels = [f"{m} (DTE: {fit_results.loc[m, 'dtm']:.1f})"
                   for m in maturity_names]

    # Plot each parameter
    for i, param in enumerate(param_names):
        row, col = (i // 2) + 1, (i % 2) + 1

        fig.add_trace(
            go.Scatter(
                x=list(range(len(maturity_names))),
                y=fit_results[param],
                mode='lines+markers',
                name=param,
                line=dict(width=2, color='rgb(0, 180, 180)'),
                marker=dict(size=8),
                text=tick_labels,
                hovertemplate="%{text}<br>%{y:.4f}"
            ),
            row=row, col=col
        )

        # Set x-axis labels
        fig.update_xaxes(
            tickvals=list(range(len(maturity_names))),
            ticktext=maturity_names,
            tickangle=45,
            row=row, col=col
        )

    # Update layout
    fig.update_layout(
        title='Jump-Wing Parameters Across Expiries',
        template='plotly_dark',
        showlegend=False
    )

    return fig


@catch_exception
def plot_fit_performance(fit_results: pd.DataFrame) -> go.Figure:
    """
    Plot the fitting accuracy statistics.

    Parameters:
    - fit_results: DataFrame from fit_model() with maturity names as index

    Returns:
    - Plotly figure
    """
    # Define metrics to plot
    metrics = {
        'rmse': {'title': 'RMSE by Expiry', 'row': 1, 'col': 1, 'ylabel': 'RMSE (%)', 'scale': 100},
        'mae': {'title': 'MAE by Expiry', 'row': 1, 'col': 2, 'ylabel': 'MAE (%)', 'scale': 100},
        'r2': {'title': 'R² by Expiry', 'row': 2, 'col': 1, 'ylabel': 'R²', 'scale': 1},
        'max_error': {'title': 'Max Error by Expiry', 'row': 2, 'col': 2, 'ylabel': 'Max Error (%)', 'scale': 100}
    }

    # Create subplots
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=[metrics[m]['title'] for m in metrics]
    )

    # Get maturity names from index and create x-axis indices
    maturity_names = fit_results.index
    x_indices = list(range(len(maturity_names)))

    # Create hover labels
    hover_labels = [f"{m} (DTE: {fit_results.loc[m, 'dtm']:.1f})" for m in maturity_names]

    # Plot each metric
    for metric, config in metrics.items():
        fig.add_trace(
            go.Scatter(
                x=x_indices,
                y=fit_results[metric] * config['scale'],
                mode='lines+markers',
                name=metric.upper(),
                line=dict(width=2),
                marker=dict(size=8),
                text=hover_labels,
                hovertemplate="%{text}<br>%{y:.4f}"
            ),
            row=config['row'], col=config['col']
        )

        # Update axes
        fig.update_yaxes(title_text=config['ylabel'], row=config['row'], col=config['col'])

    # Set x-axis labels for all subplots
    for row in range(1, 3):
        for col in range(1, 3):
            fig.update_xaxes(
                tickvals=x_indices,
                ticktext=maturity_names,
                tickangle=45,
                row=row, col=col
            )

    # Update layout
    fig.update_layout(
        title='Model Fitting Accuracy Statistics',
        template='plotly_dark',
        showlegend=False
    )

    return fig


@catch_exception
def plot_3d_surface(x_surface: Dict[str, np.ndarray],
                    iv_surface: Dict[str, np.ndarray],
                    fit_results: pd.DataFrame = None,
                    domain_type: str = 'log_moneyness') -> go.Figure:
    """
    Plot 3D implied volatility surface.

    Parameters:
    - x_surface: Dictionary mapping maturity names to x-domain arrays
    - iv_surface: Dictionary mapping maturity names to IV arrays
    - fit_results: Optional DataFrame with maturity information
    - domain_type: Type of x-domain ('log_moneyness', 'moneyness', 'strikes', 'delta')

    Returns:
    - Plotly figure
    """
    # Map domain types to axis labels
    domain_labels = {
        'log_moneyness': 'Log Moneyness',
        'moneyness': 'Moneyness (S/K)',
        'strikes': 'Strike Price',
        'delta': 'Delta'
    }

    # Define custom colorscale
    custom_blue_scale = [[0, '#60AEFC'], [1, '#002040']]

    # Get maturity names
    maturity_names = list(iv_surface.keys())

    # Get z-axis values (days to expiry)
    if fit_results is not None:
        # Use DTM values from fit_results
        maturity_values = [fit_results.loc[name, 'dtm'] for name in maturity_names]
    else:
        # Default to sequential values
        maturity_values = list(range(len(maturity_names)))

    # Create a mesh grid for each maturity to handle different x domains
    X = []
    Y = []
    Z = []

    for i, m in enumerate(maturity_names):
        x_values = x_surface[m]
        z_values = iv_surface[m] * 100  # Convert to percentage
        y_value = maturity_values[i]

        # Add to point lists
        for j in range(len(x_values)):
            X.append(x_values[j])
            Y.append(y_value)
            Z.append(z_values[j])

    # Create 3D scatter plot with lines connecting points within each maturity
    fig = go.Figure()

    # Add data as a 3D scatter plot
    fig.add_trace(go.Scatter3d(
        x=X, y=Y, z=Z,
        mode='markers',
        marker=dict(
            size=3,
            color=Z,
            colorscale=custom_blue_scale,
            opacity=0.8
        ),
        hovertemplate="<b>%{y:.1f} days</b><br>X: %{x:.4f}<br>IV: %{z:.2f}%"
    ))

    # Add lines connecting points for each maturity
    cumulative_index = 0
    for i, m in enumerate(maturity_names):
        points_count = len(x_surface[m])
        indices = list(range(cumulative_index, cumulative_index + points_count))

        if len(indices) > 1:
            fig.add_trace(go.Scatter3d(
                x=[X[j] for j in indices],
                y=[Y[j] for j in indices],
                z=[Z[j] for j in indices],
                mode='lines',
                line=dict(color='blue', width=3),
                showlegend=False,
                hoverinfo='none'
            ))

        cumulative_index += points_count

    # Update layout
    fig.update_layout(
        title='Implied Volatility 3D Surface',
        template='plotly_dark',
        scene=dict(
            xaxis_title=domain_labels.get(domain_type, 'X Domain'),
            yaxis_title='Days to Expiry',
            zaxis_title='Implied Volatility (%)',
            aspectmode='manual',
            aspectratio=dict(x=1.5, y=1, z=1)
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

