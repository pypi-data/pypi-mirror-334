import optionvisualizer_wrapper as ovw
import plotly.graph_objects as go
import numpy as np
from typing import Literal

def plot_greek_vol_strike_surface(
    greek: str,
    S: float = 100,
    T: float = 0.5,
    r: float = 0.01,
    strike_range: tuple[float, float] = (80, 120),
    vol_range: tuple[float, float] = (0.1, 0.5),
    num_strikes: int = 100,
    num_vols: int = 100,
    option_type: Literal["call", "put"] = "call",
    colorscale: str = "viridis",
) -> go.Figure:
    """
    Plots a 3D surface of a specified Greek vs. Strike Price and Volatility.

    Args:
        greek: The Greek to plot (e.g., "delta", "gamma", "vega", "theta", "rho", "vomma", "vanna").
        S: Fixed underlying price.
        T: Fixed time to expiration.
        r: Fixed interest rate.
        strike_range: Tuple (min_strike, max_strike) defining the strike price range.
        vol_range: Tuple (min_vol, max_vol) defining the volatility range.
        num_strikes: Number of strike price points.
        num_vols: Number of volatility points.
        option_type: 'call' or 'put'.  Only relevant for Greeks that differ between calls and puts.
        colorscale: Plotly colorscale (e.g., 'viridis', 'plasma', 'magma').

    Returns:
        go.Figure: The Plotly figure object.
    """
    wrapper = ovw.OptionVisualizerWrapper()

    strikes = np.linspace(strike_range[0], strike_range[1], num_strikes)
    vols = np.linspace(vol_range[0], vol_range[1], num_vols)
    strike_grid, vol_grid = np.meshgrid(strikes, vols)
    greek_values = np.zeros_like(strike_grid)

    for i in range(strike_grid.shape[0]):
        for j in range(strike_grid.shape[1]):
            greek_values[i, j] = wrapper.sensitivities(
                greek=greek,
                S=S,
                K=strike_grid[i, j],
                T=T,
                r=r,
                sigma=vol_grid[i, j],
                option=option_type,
            )

    fig = go.Figure(
        data=[
            go.Surface(
                z=greek_values, x=strike_grid, y=vol_grid, colorscale=colorscale
            )
        ]
    )

    fig.update_layout(
        title=f"{greek.title()} vs. Strike Price and Volatility",
        scene={
            "xaxis_title": "Strike Price",
            "yaxis_title": "Volatility",
            "zaxis_title": greek.title(),
            'xaxis': {
                    'backgroundcolor': "rgb(230, 230, 200)",
                    'gridcolor': "white",
                    'showbackground': True,
                    'zerolinecolor': "white"
                    },
                'yaxis': {
                    'backgroundcolor': "rgb(200, 200, 230)",
                    'gridcolor': "white",
                    'showbackground': True,
                    'zerolinecolor': "white"
                    },
                'zaxis': {
                    'backgroundcolor': "rgb(230, 200, 230)",
                    'gridcolor': "white",
                    'showbackground': True,
                    'zerolinecolor': "white"
                    }
        },
    )
    return fig


def plot_greek_price_time_surface(
    greek: str,
    K: float = 100,
    r: float = 0.01,
    sigma: float = 0.2,
    price_range: tuple[float, float] = (50, 150),
    time_range: tuple[float, float] = (0.01, 1),
    num_prices: int = 100,
    num_times: int = 100,
    option_type: Literal["call", "put"] = "call",
    colorscale: str = "viridis",
) -> go.Figure:
    """
    Plots a 3D surface of a specified Greek vs. Underlying Price and Time to Expiration.

    Args:
        greek: The Greek to plot (e.g., "delta", "gamma", "vega", "theta", "rho").
        K: Fixed strike price.
        r: Fixed interest rate.
        sigma: Fixed volatility.
        price_range: Tuple (min_price, max_price) for the underlying price range.
        time_range: Tuple (min_time, max_time) for the time to expiration range.
        num_prices:  Number of price points.
        num_times:   Number of time points.
        option_type: 'call' or 'put'.  Only relevant for Greeks that differ.
        colorscale: Plotly colorscale (e.g., 'viridis', 'plasma', 'magma').

    Returns:
        go.Figure: The Plotly figure object.
    """
    wrapper = ovw.OptionVisualizerWrapper()

    prices = np.linspace(price_range[0], price_range[1], num_prices)
    times = np.linspace(time_range[0], time_range[1], num_times)
    price_grid, time_grid = np.meshgrid(prices, times)
    greek_values = np.zeros_like(price_grid)

    for i in range(price_grid.shape[0]):
        for j in range(price_grid.shape[1]):
            greek_values[i, j] = wrapper.sensitivities(
                greek=greek,
                S=price_grid[i, j],
                K=K,
                T=time_grid[i, j],
                r=r,
                sigma=sigma,
                option=option_type,
            )

    fig = go.Figure(
        data=[
            go.Surface(
                z=greek_values, x=price_grid, y=time_grid * 365, colorscale=colorscale
            )
        ]
    )

    fig.update_layout(
        title=f"{greek.title()} vs. Price and Time to Expiration",
        scene={
            "xaxis_title": "Underlying Price",
            "yaxis_title": "Time to Expiration (Days)",
            "zaxis_title": greek.title(),
            'xaxis': {
                'backgroundcolor': "rgb(230, 230, 200)",
                'gridcolor': "white",
                'showbackground': True,
                'zerolinecolor': "white"
            },
            'yaxis': {
                'backgroundcolor': "rgb(200, 200, 230)",
                'gridcolor': "white",
                'showbackground': True,
                'zerolinecolor': "white"
            },
            'zaxis': {
                'backgroundcolor': "rgb(230, 200, 230)",
                'gridcolor': "white",
                'showbackground': True,
                'zerolinecolor': "white"
            }
        },

    )
    fig.update_scenes(yaxis_autorange="reversed")
    return fig



if __name__ == '__main__':
    # Example Usage
    fig_vanna = plot_greek_vol_strike_surface(greek="vanna", S=100, T=0.25)
    fig_vanna.show()

    fig_gamma = plot_greek_price_time_surface(greek="gamma", K=100, sigma=0.3, r=0.02)
    fig_gamma.show()

    fig_delta = plot_greek_price_time_surface(greek='delta', option_type='put', K=110, price_range=(80,130))
    fig_delta.show()

    fig_vega = plot_greek_vol_strike_surface(greek='vega', T=1, strike_range=(90, 110), vol_range=(0.1, 0.4), num_vols=50)
    fig_vega.show()