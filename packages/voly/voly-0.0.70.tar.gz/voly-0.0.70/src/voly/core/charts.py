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
                # For delta, we'd need more complex conversion - skip market data for this domain
                market_x = None

            # Add bid and ask IVs if the domain type allows
            if domain_type != 'delta' and market_x is not None:
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

            # Update layout with DTE
            title = f'Vol Smile for {maturity} (DTE: {dte_value:.1f})'
        else:
            title = f'Vol Smile for {maturity}'
    else:
        title = 'Volatility Smile'

    # Update layout
    fig.update_layout(
        title=title,
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
    tick_labels = [f"{m} (DTE: {fit_results.loc[m, 'dtm']:.1f}, YTE: {fit_results.loc[m, 'ytm']:.4f})"
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
        showlegend=False,
        height=800
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
    tick_labels = [f"{m} (DTE: {fit_results.loc[m, 'dtm']:.1f}, YTE: {fit_results.loc[m, 'ytm']:.4f})"
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
        showlegend=False,
        height=800
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
        showlegend=False,
        height=700
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
        'delta': 'Call Delta'
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

    # For domains with uniform x values across maturities (like log_moneyness, moneyness)
    # we can use standard surface plot
    if domain_type in ['log_moneyness', 'moneyness']:
        # Create mesh grid
        X, Y = np.meshgrid(list(x_surface.values())[0], maturity_values)
        Z = np.array([iv_surface[m] * 100 for m in maturity_names])  # Convert to percentage

        # Create figure
        fig = go.Figure(data=[
            go.Surface(
                z=Z,
                x=X,
                y=Y,
                colorscale=custom_blue_scale,
                contours_z=dict(
                    show=True,
                    usecolormap=True,
                    highlightcolor="#0080FF",
                    project_z=True
                )
            )
        ])

    # For domains that might have different x values per maturity (like strikes, delta)
    # we need to use a different approach
    else:
        # Create a 3D scatter plot with lines
        fig = go.Figure()

        # For each maturity, create a curve
        for i, maturity in enumerate(maturity_names):
            x_values = x_surface[maturity]
            z_values = iv_surface[maturity] * 100  # Convert to percentage
            y_values = np.full_like(x_values, maturity_values[i])

            # Add a line for this maturity
            fig.add_trace(go.Scatter3d(
                x=x_values,
                y=y_values,
                z=z_values,
                mode='lines',
                line=dict(
                    color=f'rgb({30 + 225 * (i / len(maturity_names))}, {30 + 150 * (i / len(maturity_names))}, {200 - 170 * (i / len(maturity_names))})',
                    width=5
                ),
                name=maturity
            ))

    # Update layout
    fig.update_layout(
        title='Implied Volatility 3D Surface',
        template='plotly_dark',
        scene=dict(
            xaxis_title=domain_labels.get(domain_type, 'X Domain'),
            yaxis_title='Days to Expiry',
            zaxis_title='Implied Volatility (%)',
            aspectmode='manual',
            aspectratio=dict(x=1.5, y=1, z=1),
            camera=dict(
                eye=dict(x=1.5, y=-1.5, z=1)
            )
        ),
        margin=dict(l=65, r=50, b=65, t=90)
    )

    return fig


@catch_exception
def plot_rnd(x_domain: np.ndarray,
             rnd_values: np.ndarray,
             spot_price: float = 1.0,
             title: str = 'Risk-Neutral Density') -> go.Figure:
    """
    Plot risk-neutral density (RND).

    Parameters:
    - x_domain: Grid of domain values
    - rnd_values: RND values
    - spot_price: Spot price for reference
    - title: Plot title

    Returns:
    - Plotly figure
    """
    # Create figure
    fig = go.Figure()

    # Convert x_domain to prices (assuming it's in log_moneyness)
    # This may need adjustment if the domain is not log_moneyness
    prices = spot_price * np.exp(x_domain)

    # Normalize the RND to integrate to 1
    dx = x_domain[1] - x_domain[0]
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
        title=title,
        xaxis_title='Price',
        yaxis_title='Density',
        template='plotly_dark',
        showlegend=False
    )

    return fig
