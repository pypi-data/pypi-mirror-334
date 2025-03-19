# optionvisualizer_wrapper.py

import optionvisualizer.visualizer as ov
import plotly.graph_objects as go
from typing import Literal

class OptionVisualizerWrapper:
    """
    Wrapper around the optionvisualizer library to consistently return
    Plotly Figure objects.
    """

    def __init__(self, **kwargs):
        """
        Initializes the wrapper, passing any keyword arguments to the
        underlying optionvisualizer.
        """
        self.visualizer = ov.Visualizer(**kwargs)

    def option_data(self, option_value: str, **kwargs) -> float:
        """
        Calculates option prices or Greeks, mirroring the original API.

        Args:
            option_value: The value to return ('price', 'delta', etc.)
            **kwargs: Parameters for option calculation (S, K, T, r, q, sigma, option).

        Returns:
            float: The calculated option value or Greek.
        """
        return self.visualizer.option_data(option_value=option_value, **kwargs)

    def sensitivities(self, **kwargs) -> float:
        """
        Calculates option sensitivities, mirroring the original API.

        Args:
            **kwargs:  Parameters, including 'greek' and optionally 'num_sens'.

        Returns:
            float: The calculated sensitivity.
        """
        return self.visualizer.sensitivities(**kwargs)

    def barrier(self, **kwargs) -> float:
        """
        Calculates barrier option prices, mirroring the original API.

        Args:
            **kwargs: Parameters for barrier option calculation.

        Returns:
            float: The calculated barrier option price.
        """
        return self.visualizer.barrier(**kwargs)


    def visualize(
        self,
        risk: bool = True,
        graphtype: Literal["2D", "3D"] = "2D",
        **kwargs,
    ) -> go.Figure:
        """
        Visualizes option Greeks or payoffs, returning a Plotly Figure object.

        Args:
            risk: True for risk graphs, False for payoff diagrams.
            graphtype: '2D' or '3D' for the type of graph.
            **kwargs:  All other parameters accepted by the original
                `visualize` method (S, K, T, r, q, sigma, option, direction,
                greek, x_plot, y_plot, G1, G2, G3, T1, T2, T3,
                time_shift, interactive, notebook, colorscheme, size2d,
                size3d, axis, spacegrain, azim, elev, combo_payoff, etc.).

        Returns:
            go.Figure: The Plotly Figure object.  Always returns the figure.
        """

        if risk:
            if graphtype == "3D":
                # Use data_output=True to get the intermediate data,
                # then construct the Plotly figure.
                data = self.visualizer.visualize(
                    risk=True, graphtype="3D", interactive=True, data_output=True, **kwargs
                )
                params = data['params']
                graph_params = data['graph_params']
                fig = go.Figure(
                    data=[
                        go.Surface(
                            x=graph_params['x'],
                            y=graph_params['y'],
                            z=graph_params['z'],
                            colorscale=params['colorscheme'],
                            contours={
                                "x": {
                                    "show": True,
                                    "start": graph_params['x_start'],
                                    "end": graph_params['x_stop'],
                                    "size": graph_params['x_size'],
                                    "color": "white",
                                },
                                "y": {
                                    "show": True,
                                    "start": graph_params['y_start'],
                                    "end": graph_params['y_stop'],
                                    "size": graph_params['y_size'],
                                    "color": "white",
                                },
                                "z": {
                                    "show": True,
                                    "start": graph_params['z_start'],
                                    "end": graph_params['z_stop'],
                                    "size": graph_params['z_size'],
                                },
                            },
                        )
                    ]
                )

                fig.update_layout(
                    scene={
                        "xaxis_title": graph_params['axis_label2'],
                        "yaxis_title": graph_params['axis_label1'],
                        "zaxis_title": graph_params['axis_label3'],
                        'xaxis': {
                                    'backgroundcolor': "rgb(200, 200, 230)",
                                    'gridcolor': "white",
                                    'showbackground': True,
                                    'zerolinecolor': "white"
                                    },
                                'yaxis': {
                                    'backgroundcolor': "rgb(230, 200, 230)",
                                    'gridcolor': "white",
                                    'showbackground': True,
                                    'zerolinecolor': "white"
                                    },
                                'zaxis': {
                                    'backgroundcolor': "rgb(230, 230, 200)",
                                    'gridcolor': "white",
                                    'showbackground': True,
                                    'zerolinecolor': "white"
                                    },
                    },
                    title={
                        "text": graph_params['titlename'],
                        "y": 0.9,
                        "x": 0.5,
                        "xanchor": "center",
                        "yanchor": "top",
                        "font": {"size": 20, "color": "black"},
                    },
                )
                return fig

            elif graphtype == "2D":
                data = self.visualizer.visualize(risk=True,
                            graphtype='2D',
                            interactive=True,
                            data_output=True,
                            **kwargs)

                params = data['params']
                vis_params = data['vis_params']
                fig = go.Figure()
                # If plotting against time, show time to maturity reducing left
                # to right
                if vis_params['x_plot'] == 'time':
                    fig.update_xaxes(autorange="reversed")

                # Plot the 1st option
                fig.add_trace(go.Scatter(x=vis_params['xarray'],
                                            y=vis_params['yarray1'],
                                            line={'color': 'blue'},
                                            name=vis_params['label1']))

                # Plot the 2nd option
                fig.add_trace(go.Scatter(x=vis_params['xarray'],
                                            y=vis_params['yarray2'],
                                            line={'color': 'red'},
                                            name=vis_params['label2']))

                # Plot the 3rd option
                fig.add_trace(go.Scatter(x=vis_params['xarray'],
                                            y=vis_params['yarray3'],
                                            line={'color': 'green'},
                                            name=vis_params['label3']))

                # 4th option only used in Rho graphs
                if vis_params['label4'] is not None:
                    fig.add_trace(go.Scatter(x=vis_params['xarray'],
                                                y=vis_params['yarray4'],
                                                line={'color': 'orange'},
                                                name=vis_params['label4']))


                fig.update_layout(
                    title={
                        'text': vis_params['title'],
                        'y':0.95,
                        'x':0.5,
                        'xanchor':'center',
                        'yanchor':'top',
                        'font':{
                            'size': 20,
                            'color': "#f2f5fa"
                        }
                    },
                    xaxis_title={
                        'text': vis_params['xlabel'],
                        'font': {
                            'size': 15,
                            'color': "#f2f5fa"
                        }
                    },
                    yaxis_title={
                        'text': vis_params['ylabel'],
                        'font': {
                            'size': 15,
                            'color': "#f2f5fa"
                        }
                    },
                    font={'color': '#f2f5fa'},
                    paper_bgcolor='black',
                    plot_bgcolor='black',
                    legend={
                        'x': 0.05,
                        'y': 0.95,
                        'traceorder': "normal",
                        'bgcolor': 'rgba(0, 0, 0, 0)',
                        'font': {
                            'family': "sans-serif",
                            'size': 12,
                            'color': "#f2f5fa"
                        },
                    },
                )
                fig.update_xaxes(showline=True,
                                    linewidth=2,
                                    linecolor='#2a3f5f',
                                    mirror=True,
                                    range = [vis_params['xmin'], vis_params['xmax']],
                                    gridwidth=1,
                                    gridcolor='#2a3f5f',
                                    zeroline=False)

                fig.update_yaxes(showline=True,
                                    linewidth=2,
                                    linecolor='#2a3f5f',
                                    mirror=True,
                                    range = [vis_params['ymin'], vis_params['ymax']],
                                    gridwidth=1,
                                    gridcolor='#2a3f5f',
                                    zeroline=False)
                return fig


        else:  # Payoff diagrams
            data = self.visualizer.visualize(
                risk=False, interactive=True, data_output=True, **kwargs
            )
            params = data['params']
            payoff_dict = data['payoff_dict']

            fig = go.Figure()
            fig.add_trace(
                go.Scatter(
                    x=payoff_dict["SA"],
                    y=payoff_dict["payoff"],
                    line={"color": "blue"},
                    name="Payoff",
                )
            )

            # If the value flag is selected, plot the payoff with the
            # current time to maturity
            if payoff_dict['payoff2'] is not None:
                fig.add_trace(go.Scatter(x=payoff_dict['SA'],
                                            y=payoff_dict['payoff2'],
                                            line={'color': 'red'},
                                            name='Value'))

            fig.update_layout(
                title={
                    "text": payoff_dict["title"],
                    "y": 0.95,
                    "x": 0.5,
                    "xanchor": "center",
                    "yanchor": "top",
                    "font": {"size": 20, "color": "#f2f5fa"},
                },
                xaxis_title={
                    "text": "Underlying Price",
                    "font": {"size": 15, "color": "#f2f5fa"},
                },
                yaxis_title={
                    "text": "P&L",
                    "font": {"size": 15, "color": "#f2f5fa"},
                },
                font={"color": "#f2f5fa"},
                paper_bgcolor="black",
                plot_bgcolor="black",
                legend={
                    "x": 0.05,
                    "y": 0.95,
                    "traceorder": "normal",
                    "bgcolor": "rgba(0, 0, 0, 0)",
                    "font": {"family": "sans-serif", "size": 12, "color": "#f2f5fa"},
                },
            )

            fig.add_vline(x=payoff_dict['S'], line_width=0.5, line_color="white")
            fig.add_hline(y=0, line_width=0.5, line_color="white")

            fig.update_xaxes(
                showline=True,
                linewidth=2,
                linecolor="#2a3f5f",
                mirror=True,
                # range = [xmin, xmax],
                gridwidth=1,
                gridcolor="#2a3f5f",
                zeroline=False,
            )

            fig.update_yaxes(
                showline=True,
                linewidth=2,
                linecolor="#2a3f5f",
                mirror=True,
                # range = [ymin, ymax],
                gridwidth=1,
                gridcolor="#2a3f5f",
                zeroline=False,
            )
            return fig


    def greeks(self, graphtype: Literal["2D", "3D"] = "2D", **kwargs) -> go.Figure:
        """
        Wrapper for greeks method, creates 2D or 3D graph.

        Args:
            graphtype: '2D' or '3D'.
            **kwargs: Parameters for the greeks method.

        Returns:
            go.Figure: Plotly figure object.
        """
        if graphtype == "3D":
            data = self.visualizer.greeks(
                graphtype="3D", interactive=True, data_output=True, **kwargs
            )
            params = data['params']
            graph_params = data['graph_params']
            fig = go.Figure(
                data=[
                    go.Surface(
                        x=graph_params['x'],
                        y=graph_params['y'],
                        z=graph_params['z'],
                        colorscale=params['colorscheme'],
                        contours={
                            "x": {
                                "show": True,
                                "start": graph_params['x_start'],
                                "end": graph_params['x_stop'],
                                "size": graph_params['x_size'],
                                "color": "white",
                            },
                            "y": {
                                "show": True,
                                "start": graph_params['y_start'],
                                "end": graph_params['y_stop'],
                                "size": graph_params['y_size'],
                                "color": "white",
                            },
                            "z": {
                                "show": True,
                                "start": graph_params['z_start'],
                                "end": graph_params['z_stop'],
                                "size": graph_params['z_size'],
                            },
                        },
                    )
                ]
            )

            fig.update_layout(
                scene={
                    "xaxis_title": graph_params['axis_label2'],
                    "yaxis_title": graph_params['axis_label1'],
                    "zaxis_title": graph_params['axis_label3'],
                    'xaxis': {
                                'backgroundcolor': "rgb(200, 200, 230)",
                                'gridcolor': "white",
                                'showbackground': True,
                                'zerolinecolor': "white"
                                },
                            'yaxis': {
                                'backgroundcolor': "rgb(230, 200, 230)",
                                'gridcolor': "white",
                                'showbackground': True,
                                'zerolinecolor': "white"
                                },
                            'zaxis': {
                                'backgroundcolor': "rgb(230, 230, 200)",
                                'gridcolor': "white",
                                'showbackground': True,
                                'zerolinecolor': "white"
                                },
                },
                title={
                    "text": graph_params['titlename'],
                    "y": 0.9,
                    "x": 0.5,
                    "xanchor": "center",
                    "yanchor": "top",
                    "font": {"size": 20, "color": "black"},
                },
            )
            return fig
        
        elif graphtype == "2D":
            data = self.visualizer.greeks(
                graphtype="2D",
                interactive=True,
                data_output=True,
                **kwargs)

            params = data['params']
            vis_params = data['vis_params']
            fig = go.Figure()
            # If plotting against time, show time to maturity reducing left
            # to right
            if vis_params['x_plot'] == 'time':
                fig.update_xaxes(autorange="reversed")

            # Plot the 1st option
            fig.add_trace(go.Scatter(x=vis_params['xarray'],
                                        y=vis_params['yarray1'],
                                        line={'color': 'blue'},
                                        name=vis_params['label1']))

            # Plot the 2nd option
            fig.add_trace(go.Scatter(x=vis_params['xarray'],
                                        y=vis_params['yarray2'],
                                        line={'color': 'red'},
                                        name=vis_params['label2']))

            # Plot the 3rd option
            fig.add_trace(go.Scatter(x=vis_params['xarray'],
                                        y=vis_params['yarray3'],
                                        line={'color': 'green'},
                                        name=vis_params['label3']))

            # 4th option only used in Rho graphs
            if vis_params['label4'] is not None:
                fig.add_trace(go.Scatter(x=vis_params['xarray'],
                                            y=vis_params['yarray4'],
                                            line={'color': 'orange'},
                                            name=vis_params['label4']))


            fig.update_layout(
                title={
                    'text': vis_params['title'],
                    'y':0.95,
                    'x':0.5,
                    'xanchor':'center',
                    'yanchor':'top',
                    'font':{
                        'size': 20,
                        'color': "#f2f5fa"
                    }
                },
                xaxis_title={
                    'text': vis_params['xlabel'],
                    'font': {
                        'size': 15,
                        'color': "#f2f5fa"
                    }
                },
                yaxis_title={
                    'text': vis_params['ylabel'],
                    'font': {
                        'size': 15,
                        'color': "#f2f5fa"
                    }
                },
                font={'color': '#f2f5fa'},
                paper_bgcolor='black',
                plot_bgcolor='black',
                legend={
                    'x': 0.05,
                    'y': 0.95,
                    'traceorder': "normal",
                    'bgcolor': 'rgba(0, 0, 0, 0)',
                    'font': {
                        'family': "sans-serif",
                        'size': 12,
                        'color': "#f2f5fa"
                    },
                },
            )
            fig.update_xaxes(showline=True,
                                linewidth=2,
                                linecolor='#2a3f5f',
                                mirror=True,
                                range = [vis_params['xmin'], vis_params['xmax']],
                                gridwidth=1,
                                gridcolor='#2a3f5f',
                                zeroline=False)

            fig.update_yaxes(showline=True,
                                linewidth=2,
                                linecolor='#2a3f5f',
                                mirror=True,
                                range = [vis_params['ymin'], vis_params['ymax']],
                                gridwidth=1,
                                gridcolor='#2a3f5f',
                                zeroline=False)
            return fig
        else:
            raise ValueError("Invalid graphtype. Must be '2D' or '3D'")

    def payoffs(self, payoff_type: str, **kwargs) -> go.Figure:
        """
        Wrapper for payoffs method.  Creates a payoff diagram.

        Args:
            payoff_type: The type of payoff (e.g., 'straddle', 'call', etc.)
            **kwargs: Parameters for the payoff calculation.
        Returns:
            go.Figure: Plotly figure object.
        """
        data = self.visualizer.payoffs(
            payoff_type=payoff_type, interactive=True, data_output=True, **kwargs
        )
        params = data['params']
        payoff_dict = data['payoff_dict']

        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=payoff_dict["SA"],
                y=payoff_dict["payoff"],
                line={"color": "blue"},
                name="Payoff",
            )
        )

        # If the value flag is selected, plot the payoff with the
        # current time to maturity
        if payoff_dict['payoff2'] is not None:
            fig.add_trace(go.Scatter(x=payoff_dict['SA'],
                                      y=payoff_dict['payoff2'],
                                      line={'color': 'red'},
                                      name='Value'))
        fig.update_layout(
            title={
                "text": payoff_dict["title"],
                "y": 0.95,
                "x": 0.5,
                "xanchor": "center",
                "yanchor": "top",
                "font": {"size": 20, "color": "#f2f5fa"},
            },
            xaxis_title={
                "text": "Underlying Price",
                "font": {"size": 15, "color": "#f2f5fa"},
            },
            yaxis_title={
                "text": "P&L",
                "font": {"size": 15, "color": "#f2f5fa"},
            },
            font={"color": "#f2f5fa"},
            paper_bgcolor="black",
            plot_bgcolor="black",
            legend={
                "x": 0.05,
                "y": 0.95,
                "traceorder": "normal",
                "bgcolor": "rgba(0, 0, 0, 0)",
                "font": {"family": "sans-serif", "size": 12, "color": "#f2f5fa"},
            },
        )

        fig.add_vline(x=payoff_dict['S'], line_width=0.5, line_color="white")
        fig.add_hline(y=0, line_width=0.5, line_color="white")

        fig.update_xaxes(
            showline=True,
            linewidth=2,
            linecolor="#2a3f5f",
            mirror=True,
            # range = [xmin, xmax],
            gridwidth=1,
            gridcolor="#2a3f5f",
            zeroline=False,
        )

        fig.update_yaxes(
            showline=True,
            linewidth=2,
            linecolor="#2a3f5f",
            mirror=True,
            # range = [ymin, ymax],
            gridwidth=1,
            gridcolor="#2a3f5f",
            zeroline=False,
        )
        return fig

# Example usage (demonstrates all methods)
if __name__ == "__main__":
    wrapper = OptionVisualizerWrapper()

    # Option Data
    price = wrapper.option_data("price", S=100, K=100, T=0.5, r=0.05, sigma=0.2)
    print(f"Option Price: {price}")

    # Sensitivities
    delta = wrapper.sensitivities(greek="delta", S=100, K=100, T=0.5, r=0.05, sigma=0.2)
    print(f"Delta: {delta}")

    # Barrier
    barrier_price = wrapper.barrier(
        S=100,
        K=100,
        H=110,
        T=0.5,
        r=0.05,
        sigma=0.2,
        barrier_direction="up",
        knock="in",
        option="call",
    )
    print(f"Barrier Price: {barrier_price}")

    # 3D Greek Graph
    fig_3d_greek = wrapper.visualize(
        risk=True, graphtype="3D", greek="vega", S=100, T=0.5, r=0.05, sigma=0.2
    )
    fig_3d_greek.show()  # Show the figure

    # 2D Greek Graph
    fig_2d_greek = wrapper.visualize(
        risk=True,
        graphtype="2D",
        x_plot="price",
        y_plot="delta",
        S=100,
        G1=90,
        G2=100,
        G3=110,
        T=0.5,
        r=0.05,
        sigma=0.2,
        direction='long'
    )
    fig_2d_greek.show()


    # Payoff Diagram
    fig_payoff = wrapper.visualize(
        risk=False, combo_payoff="straddle", S=100, K=100, T=0.5, r=0.05, sigma=0.2
    )
    fig_payoff.show()

     # 3D Greek Graph with greeks()
    fig_3d_greek = wrapper.greeks(
        graphtype="3D", greek="vega", S=100, T=0.5, r=0.05, sigma=0.2
    )
    fig_3d_greek.show()  # Show the figure

    # 2D Greek Graph with greeks()
    fig_2d_greek = wrapper.greeks(
        graphtype="2D",
        x_plot="price",
        y_plot="delta",
        S=100,
        G1=90,
        G2=100,
        G3=110,
        T=0.5,
        r=0.05,
        sigma=0.2,
        direction='long'
    )
    fig_2d_greek.show()


    # Payoff Diagram with payoffs() method
    fig_payoff = wrapper.payoffs(
        payoff_type="straddle", S=100, K=100, T=0.5, r=0.05, sigma=0.2
    )
    fig_payoff.show()

    print("All examples executed successfully!")