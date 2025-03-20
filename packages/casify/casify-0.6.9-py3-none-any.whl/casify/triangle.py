def _draw_angle_arc(
    vertex,
    *other_points,
    radius=0.4,
    show_angle=False,
    vertex_label=None,
    fontsize=20,
):
    """
    Draw an arc to show the angle between two points relative to a vertex.
    For right angles (90 degrees), draws a small square instead.

    Parameters:
    -----------
    ax : matplotlib.axes.Axes
        The axes to draw on
    vertex : tuple
        The vertex point (x, y)
    p1, p2 : tuple
        The two points forming the angle with the vertex
    radius : float
        Radius of the arc or size of the square for right angles
    """
    import numpy as np
    import plotmath

    ax = plotmath.gca()

    # Convert points to numpy arrays with float values
    vertex = np.array(vertex, dtype=float)
    p1, p2 = other_points
    p1 = np.array(p1, dtype=float)
    p2 = np.array(p2, dtype=float)

    # Calculate vectors from vertex to points
    v1 = p1 - vertex
    v2 = p2 - vertex

    # Calculate angles
    angle1 = np.arctan2(v1[1], v1[0])
    angle2 = np.arctan2(v2[1], v2[0])

    # Calculate the angle between vectors
    dot_product = np.dot(v1, v2)
    norms = np.linalg.norm(v1) * np.linalg.norm(v2)
    angle = np.arccos(np.clip(dot_product / norms, -1.0, 1.0))

    # Check if it's approximately a right angle (90 degrees = π/2 radians)
    if np.abs(angle - np.pi / 2) < 1e-10:
        # Draw a square for right angle
        # Get unit vectors

        katet_len = radius / np.sqrt(2)

        u1 = v1 / np.linalg.norm(v1)
        u2 = v2 / np.linalg.norm(v2)

        u1 = u1 * katet_len
        u2 = u2 * katet_len

        # Calculate square corners
        square_points = [
            vertex + u1,
            vertex + (u1 + u2),
            vertex + u2,
            vertex,
        ]

        # Convert to separate x and y arrays
        x = [p[0] for p in square_points]
        y = [p[1] for p in square_points]

        # Plot the square
        ax.plot(x, y, "k-", linewidth=1)

        unit_vector = np.array(
            [
                2 * radius * 0.5 * (np.cos(angle1) + np.cos(angle2)),
                2 * radius * 0.5 * (np.sin(angle1) + np.sin(angle2)),
            ]
        )

        if vertex_label:
            ax.text(
                x=vertex[0] - 0.5 * unit_vector[0],
                y=vertex[1] - 0.5 * unit_vector[1],
                s=f"${vertex_label}$",
                fontsize=fontsize,
                ha="center",
                va="center",
            )

    else:
        # Ensure proper angle range for drawing the smaller angle
        if abs(angle2 - angle1) > np.pi:
            if angle2 > angle1:
                angle2 -= 2 * np.pi
            else:
                angle1 -= 2 * np.pi

        # Create arc points
        if np.degrees(angle) > 90:
            theta = np.linspace(angle1, angle2, 100)
            x = vertex[0] + 0.5 * radius * np.cos(theta)
            y = vertex[1] + 0.5 * radius * np.sin(theta)
        else:
            theta = np.linspace(angle1, angle2, 100)
            x = vertex[0] + radius * np.cos(theta)
            y = vertex[1] + radius * np.sin(theta)

        # Draw the arc
        if show_angle:
            ax.plot(x, y, "k-", linewidth=1)

        # Calculate text position
        unit_vector = np.array(
            [
                1.5 * radius * 0.5 * (np.cos(angle1) + np.cos(angle2)),
                1.5 * radius * 0.5 * (np.sin(angle1) + np.sin(angle2)),
            ]
        )
        x = vertex[0] + unit_vector[0]
        y = vertex[1] + unit_vector[1]

        angle_deg = np.degrees(angle)
        if np.abs(angle_deg - round(angle_deg)) < 1e-8:
            angle_str = f"${int(round(angle_deg))}^\\circ$"
        else:
            angle_str = f"${angle_deg:.2f}^\\circ$"

        # Plot the angle value
        # Determine text alignment based on position relative to vertex
        dx = x - vertex[0]
        dy = y - vertex[1]

        # Set horizontal alignment
        if abs(dx) < 0.1:  # Near vertical
            ha = "center"
        elif dx > 0:
            ha = "left"
        else:
            ha = "right"

        # Set vertical alignment
        if abs(dy) < 0.1:  # Near horizontal
            va = "center"
        elif dy > 0:
            va = "bottom"
        else:
            va = "top"

        if show_angle:
            if show_angle is True:
                ax.text(x, y, angle_str, fontsize=fontsize, ha="center", va="center")
            else:
                ax.text(
                    x=x,
                    y=y,
                    s=f"${show_angle}$",
                    fontsize=fontsize,
                    ha="center",
                    va="center",
                )

        if vertex_label:
            ax.text(
                x=vertex[0] - 0.5 * unit_vector[0],
                y=vertex[1] - 0.5 * unit_vector[1],
                s=f"${vertex_label}$",
                fontsize=fontsize,
                ha=ha,
                va=va,
            )


def draw_triangle(
    *points,
    sss=None,
    asa=None,
    sas=None,
    show_vertices=True,
    radius=0.4,
    alpha=0.1,
    show=True,
    color=(0, 100 / 255, 140 / 255),
    fontsize=20,
    label_angles=(True, True, True),
    vertex_labels=("A", "B", "C"),
    label_sides=(True, True, True),
    numerical_len=False,
    axis_off=True,
):
    import sympy
    import plotmath
    import numpy as np

    if sss:
        triangle = sympy.Triangle(sss=sss)
    elif asa:
        triangle = sympy.Triangle(asa=asa)
    elif sas:
        triangle = sympy.Triangle(sas=sas)
    else:
        triangle = sympy.Triangle(*points)

    side_lengths = [side.length for side in triangle.sides]

    points = [(point.x.evalf(), point.y.evalf()) for point in triangle.vertices]

    plotmath.plot_polygon(
        *points,
        show_vertices=show_vertices,
        alpha=alpha,
        color=color,
    )

    for vertex, label_angle, vertex_label, label_side in zip(
        points, label_angles, vertex_labels, label_sides
    ):
        other_points = [point for point in points if point != vertex]

        _draw_angle_arc(
            vertex,
            *other_points,
            radius=radius,
            show_angle=label_angle,
            fontsize=fontsize,
            vertex_label=vertex_label,
        )

    segments = triangle.sides

    ax = plotmath.gca()
    for segment, label in zip(segments, label_sides):
        if label:
            x, y = tuple(segment.midpoint)
            x = x.evalf()
            y = y.evalf()

            points = segment.points
            dx = float(points[1].x.evalf() - points[0].x.evalf())
            dy = float(points[1].y.evalf() - points[0].y.evalf())

            unit_vector = np.array([dy, -dx]) / np.linalg.norm([dx, dy])

            if dx == 0:
                ha = "center"
                va = "bottom"

            elif dy == 0:  # Should be adjust to account for the angle of the side
                ha = "left"
                va = "center"

            elif dy / dx > 0:
                ha = "right"
                va = "top"

            elif dy / dx < 0:
                ha = "left"
                va = "bottom"

            else:
                ha = "center"
                va = "center"

            if numerical_len:
                if isinstance(label, str):
                    ax.text(
                        x=x + 0.5 * radius * unit_vector[0],
                        y=y + 0.5 * radius * unit_vector[1],
                        s=f"${label}$",
                        fontsize=fontsize,
                        ha=ha,
                        va=va,
                    )

                elif abs(segment.length - round(segment.length)) < 1e-8:
                    ax.text(
                        x=x + 0.5 * radius * unit_vector[0],
                        y=y + 0.5 * radius * unit_vector[1],
                        s=f"${segment.length.evalf() :.0f}$",
                        fontsize=fontsize,
                        ha=ha,
                        va=va,
                    )
                else:
                    ax.text(
                        x=x + 0.5 * radius * unit_vector[0],
                        y=y + 0.5 * radius * unit_vector[1],
                        s=f"${segment.length.evalf() :.2f}$",
                        fontsize=fontsize,
                        ha=ha,
                        va=va,
                    )
            else:
                ax.text(
                    x=x + 0.5 * radius * unit_vector[0],
                    y=y + 0.5 * radius * unit_vector[1],
                    s=(
                        f"${sympy.latex(segment.length)}$"
                        if label is True
                        else f"${label}$"
                    ),
                    fontsize=fontsize,
                    ha=ha,
                    va=va,
                )

    ax.axis("equal")
    if axis_off:
        ax.axis("off")

    if show:
        plotmath.show()
    else:
        return plotmath.gca()
