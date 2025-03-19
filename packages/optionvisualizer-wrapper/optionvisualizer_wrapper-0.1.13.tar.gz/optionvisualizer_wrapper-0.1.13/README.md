# OptionVisualizer Wrapper

Wrapper for https://github.com/GBERESEARCH/optionvisualizer - now methods output **plotly** fig objects instead of `None`, giving you the flexibility of further processing the plots and converting them to different formats that can be displayed and interacted with outside of jupyter notebooks.

<!-- Wrapper for https://github.com/GBERESEARCH/optionvisualizer . -->

<!-- If you only want to see the visualizations in jupyter notebooks, just use the original `optionvisualizer` package is fine. -->

<!-- Demo: https://gist.github.com/tddschn/984962bd09eceb5c736cae945eabeea8 -->

This library provides a wrapper around the excellent `optionvisualizer` package, ensuring that all plotting functions consistently return Plotly `Figure` objects. This makes it easier to integrate with other Plotly-based tools, save figures in various formats, and customize plots further.

- [OptionVisualizer Wrapper](#optionvisualizer-wrapper)
  - [Key Features](#key-features)
  - [Installation](#installation)
  - [Usage Examples](#usage-examples)
  - [API Comparison with `optionvisualizer`](#api-comparison-with-optionvisualizer)


## Key Features

*   **Consistent Plotly Output:** All plotting functions (`visualize`, `greeks`, `payoffs`) return `plotly.graph_objects.Figure` instances.
*   **Mirrored API:** The API closely mirrors the original `optionvisualizer`, making it easy to transition. You can use the same function names and parameters.
*   **Simplified Usage:** No need to juggle `interactive`, `notebook`, and `web_graph` flags.  The wrapper handles this internally.
*   **Full Functionality:**  Provides access to all the core features of `optionvisualizer`, including:
    *   Option pricing (Black-Scholes)
    *   Greek calculations (analytical and numerical)
    *   Barrier option pricing
    *   2D and 3D Greek visualizations
    *   Payoff diagrams for various option strategies

## Installation

<!-- ### pipx

This is the recommended installation method.

```
$ pipx install optionvisualizer-wrapper
``` -->

[PyPI](https://pypi.org/project/optionvisualizer-wrapper/)

```
$ pip install optionvisualizer-wrapper
```


## Usage Examples

Output of the code below: https://gist.github.com/tddschn/984962bd09eceb5c736cae945eabeea8

```python
from optionvisualizer_wrapper import OptionVisualizerWrapper

# Create an instance of the wrapper
wrapper = OptionVisualizerWrapper()

# --- Option Pricing and Greeks ---

# Calculate the price of a call option
price = wrapper.option_data(
    option_value="price", S=100, K=105, T=0.5, r=0.01, sigma=0.2, option="call"
)
print(f"Call Option Price: {price}")

# Calculate Delta (using analytical method by default)
delta = wrapper.sensitivities(greek="delta", S=100, K=100, T=0.5, r=0.01, sigma=0.2)
print(f"Delta: {delta}")

# Calculate Delta numerically
delta_num = wrapper.sensitivities(
    greek="delta", S=100, K=100, T=0.5, r=0.01, sigma=0.2, num_sens=True
)
print(f"Numerical Delta: {delta_num}")

# Calculate Barrier Option Price
barrier_price = wrapper.barrier(
    S=100, K=95, H=110, R=0, T=1, r=0.05, q=0, sigma=0.3, option='call', barrier_direction='up', knock='in'
)
print(f"Barrier Option Price: {barrier_price}")


# --- 3D Greek Visualization ---

# Visualize Vega in 3D
fig_3d = wrapper.visualize(
    risk=True,
    graphtype="3D",
    greek="vega",
    S=100,
    T=0.75,
    r=0.02,
    sigma=0.25,
    direction="long",
    colorscheme="Viridis",
)
fig_3d.show()
# Save the figure to an HTML file
fig_3d.write_html("vega_3d.html")


# --- 2D Greek Visualization ---
fig_2d = wrapper.visualize(
    risk=True,
    graphtype="2D",
    x_plot="price",
    y_plot="delta",
    S=100,
    G1=90,
    G2=100,
    G3=110,
    T=0.5,
    r=0.02,
    sigma=0.25,
)
fig_2d.show()

# --- Payoff Diagram ---

# Visualize a straddle payoff
fig_payoff = wrapper.visualize(
    risk=False, combo_payoff="straddle", S=100, K=100, T=0.25, r=0.01, sigma=0.3
)
fig_payoff.show()

# Visualize a call option payoff
fig_call_payoff = wrapper.visualize(
    risk=False, payoff_type="call", S=100, K=100, T=0.25, r=0.01, sigma=0.3, direction='long', value=True
)
fig_call_payoff.show()

# --- Using greeks() method for 3D Greek Graph ---

fig_3d_greek = wrapper.greeks(
    graphtype="3D", greek="gamma", S=100, T=0.75, r=0.02, sigma=0.25, direction="short"
)
fig_3d_greek.show()

# --- Using greeks() method for 2D Greek Graph ---

fig_2d_greek = wrapper.greeks(
    graphtype="2D", x_plot="vol", y_plot="theta", S=100, T=0.75, r=0.02, sigma=0.25, direction="long"
    , G1=90, G2=100, G3=110
)

fig_2d_greek.show()
# --- Using payoffs() method ---

fig_payoff = wrapper.payoffs(
    payoff_type="butterfly", S=100, K1=90, K2=100, K3=110, T=0.75, r=0.02, sigma=0.25, direction="long"
)

fig_payoff.show()
```

## API Comparison with `optionvisualizer`

The `OptionVisualizerWrapper` aims to provide a very similar API to the original `optionvisualizer.visualizer.Visualizer` class.  Here's a breakdown of the similarities and key differences:

**Similarities:**

*   **Method Names:**  The core methods have the same names:
    *   `option_data()`
    *   `sensitivities()`
    *   `barrier()`
    *   `visualize()`
    *   `greeks()`
    *  `payoffs()`
*   **Parameters:**  The methods accept (almost) all the same parameters as the original methods.  You can use the same keyword arguments (e.g., `S`, `K`, `T`, `r`, `sigma`, `option`, `greek`, `direction`, `combo_payoff`, etc.).
*   **Functionality:** The underlying calculations and plotting logic are identical, as the wrapper simply calls the original library's functions.

**Key Differences:**

1.  **Return Values (Plotting):**
    *   **`optionvisualizer`:** The `visualize()`, `greeks()` and `payoffs()` methods in the original library *display* graphs (either using Matplotlib or by opening a browser window for Plotly) and return `None`.  To get the Plotly figure object, you had to use specific combinations of `interactive`, `notebook`, and `web_graph` flags, which could be confusing.  Or, you could use `data_output=True` to get the *data* used to create the plot, but not the figure object itself.
    *   **`OptionVisualizerWrapper`:** The `visualize()`, `greeks()` and `payoffs()` methods in the wrapper *always* return the Plotly `go.Figure` object.  You no longer need to worry about the display flags. The wrapper handles the internal details to ensure you get the figure object.

2.  **Simplified Usage (Plotting):**  The wrapper eliminates the need to manage the `interactive`, `notebook`, and `web_graph` flags for getting Plotly figures. The wrapper handles the internal details.

3.  **No `animated_gif`:** The wrapper does *not* include the `animated_gif` method from the original library.  Creating animated GIFs is a separate concern and can be handled using other libraries if needed (or potentially added as a separate feature to the wrapper).

4. **`graphtype` is restricted to 2D and 3D for `greeks` and `visualize` methods:** `graphtype` argument is now type hinted with `Literal["2D", "3D"]` and raises a `ValueError` if any other value supplied.

In essence, the wrapper provides a *cleaner, more consistent interface* for generating Plotly visualizations from `optionvisualizer`'s powerful calculations, while retaining the familiar API. It's a thin layer that makes the library more convenient to use in a Plotly-centric workflow.
