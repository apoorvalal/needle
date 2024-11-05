import streamlit as st
import numpy as np
import time
import math

# At the top of the script
st.set_page_config(layout="wide")  # Make the page wider


# Modify the generate_semicircle_svg function parameters
def generate_semicircle_svg(value, width=800, height=400):  # Increased dimensions
    # Center of the semicircle - adjust to show full semicircle
    cx = width // 2
    cy = height - 50  # More space at bottom
    radius = min(width // 2, height - 60)  # Adjusted radius
    # Calculate angles for the value (180 degrees = π radians)
    needle_angle = math.pi - (value / 100) * math.pi  # Convert value to radians

    # Generate color gradients for the arc segments
    def get_color(angle_deg):
        # Interpolate between blue (0) and red (180)
        ratio = angle_deg / 180
        r = int(0 + (255 * ratio))
        b = int(255 * (1 - ratio))
        return f"rgb({r},0,{b})"

    # Generate the SVG path for the semicircle with segments
    segments = []
    for i in range(0, 180, 30):
        start_angle = math.pi - math.radians(i)
        end_angle = math.pi - math.radians(i + 30)
        # Calculate points for arc
        start_x = cx + radius * math.cos(start_angle)
        start_y = cy - radius * math.sin(start_angle)  # Note the minus sign
        end_x = cx + radius * math.cos(end_angle)
        end_y = cy - radius * math.sin(end_angle)  # Note the minus sign
        # For SVG arc: A rx ry x-axis-rotation large-arc-flag sweep-flag x y
        segments.append(
            f'<path d="M {start_x} {start_y} A {radius} {radius} 0 0 0 {end_x} {end_y}"'
            f' stroke="{get_color(i)}" stroke-width="20" fill="none" />'
        )
    # Calculate needle position (adjust for correct orientation)
    needle_angle = math.radians(180 - (value / 100) * 180)
    needle_length = radius - 20
    needle_x = cx + needle_length * math.cos(needle_angle)
    needle_y = cy - needle_length * math.sin(needle_angle)  # Note the minus sign
    # Generate the complete SVG
    svg = f"""
    <svg width="{width}" height="{height}">
        <rect width="{width}" height="{height}" fill="white"/>
        {''.join(segments)}
        <!-- Needle -->
        <line x1="{cx}" y1="{cy}" x2="{needle_x}" y2="{needle_y}"
              stroke="black" stroke-width="3"/>
        <!-- Center point -->
        <circle cx="{cx}" cy="{cy}" r="5" fill="black"/>
        <text x="{cx - radius - 20}" y="{cy}"
              font-family="Arial" font-size="20" fill="blue">K</text>
        <text x="{cx + radius + 20}" y="{cy}"
              font-family="Arial" font-size="20" fill="red">D</text>
    </svg>
    """
    return svg


# Initialize session state for the value if it doesn't exist
if "gauge_value" not in st.session_state:
    st.session_state.gauge_value = 50.0

# Create a placeholder for the gauge
gauge_placeholder = st.empty()

# Update loop
while True:
    jitter = np.random.normal(0, 2)
    new_value = st.session_state.gauge_value + jitter
    new_value = max(0, min(100, new_value))
    st.session_state.gauge_value = 0.95 * new_value + 0.05 * 50

    with gauge_placeholder.container():
        st.components.v1.html(
            generate_semicircle_svg(st.session_state.gauge_value),
            height=1000,
            width=2000,  # Match SVG width
        )

    time.sleep(0.2)
