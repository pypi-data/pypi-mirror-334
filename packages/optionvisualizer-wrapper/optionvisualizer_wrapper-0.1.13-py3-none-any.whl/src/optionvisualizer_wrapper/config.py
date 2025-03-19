plotly_global_config = {"displaylogo": False}

#                 full_html=full_html, include_plotlyjs="cdn", config=plotly_global_config
plotly_to_full_html_config = {
    "include_plotlyjs": "cdn",
    "config": plotly_global_config,
    "full_html": True,
}

greeks = ['delta', 'gamma', 'theta', 'vega', 'rho', 'vomma', 'vanna', 'charm', 'zomma', 'speed', 'color', 'ultima', 'vega bleed']
greeks_greater_effect_near_expiration = ['color', 'speed', 'charm', 'gamma']