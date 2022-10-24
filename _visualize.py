from typing import Literal
import plotly.graph_objects as go
import plotly.express as px
from math import dist, exp, ceil
from statistics import mode
from numpy import arange, linspace


def visualize(self, show=True, html=False, img=False):

    if not self.frames:
        self.add_frame()

    fig = go.Figure(
        layout=go.Layout(
            title="atoms",
            updatemenus=[dict(
                type="buttons",
                buttons=[dict(label="Play",
                              method="animate",
                              args=[None])])]
        ),
        data=self.frames[0].data,
        frames=self.frames[1:],

    )

    axis_range = [ceil(min([min(a.position) for a in self.atoms])-5),
                  ceil(max([max(a.position) for a in self.atoms])+5)]
    nticks = abs(axis_range[0]-axis_range[1])

    fig.update_layout(

        scene=dict(
            xaxis=dict(range=axis_range, autorange=False,
                       nticks=nticks),
            yaxis=dict(range=axis_range, autorange=False,
                       nticks=nticks),
            zaxis=dict(range=axis_range, autorange=False,
                       nticks=nticks),
            aspectmode="cube",
            aspectratio={"x": 1, "y": 1, "z": 1}),
    )

    fig.update_traces(marker_line_width=80)

    if html:
        fig.write_html(html)
    if img:
        fig.write_image(img)
    if show:
        fig.show(equal_axes=True)


def add_frame(self):

    data = []

    for color_group, atoms in self.atoms_colors.items():
        A, B = list(map(float, color_group.split("|")))
        data.append(
            go.Scatter3d(
                x=[atom.position[0]
                   for atom in atoms if not (atom is self.marked_atom)],
                y=[atom.position[1]
                   for atom in atoms if not (atom is self.marked_atom)],
                z=[atom.position[2] for atom in atoms if not (atom is self.marked_atom)] if self.dimensions == 3
                else [0 for _ in range(len(self.atoms))],
                mode="markers",
                marker_color=f'rgb({ ( min(A,B) / max(A,B) ) * 255 },{ ( 1 - min(A,B) / max(A,B) ) * 255 },150)', name=f"Atoms with A={A} and B={B}"
            ))

    if self.marked_atom:
        data.append(go.Scatter3d(
            x=[self.marked_atom.position[0]],
            y=[self.marked_atom.position[1]],
            z=[self.marked_atom.position[2]] if self.dimensions == 3
            else [0],
            mode="markers",
            marker_color='rgb(225,0,0)', name="Atom rdf was counted from"

        ))
    frame = go.Frame(
        data=data
    )
    self.frames.append(frame)


def add_rdf_frame(self):

    data = []

    x, y = self.add_cur_state_to_rdf(xy=True)

    data.append(go.Scatter(
        x=x,
        y=y,
        mode="lines",  # lines, markers,text,none,(lines+markers)
        marker_color='rgb(200,67,34)', name="RDF"))
    frame = go.Frame(data=data)
    self.rdf_frames.append(frame)


def _gaussian(dst, x, width=0.15):
    return exp(-(abs(dst-x) ** 2) / width ** 2)


def add_cur_state_to_rdf(self, target_point=None, title: str = "Untitled", calculation_type: Literal["for all pairs", "from certain atom"] = "for all pairs", xy=False):

    distances_intensities = {}

    if calculation_type == "from certain atom":

        for a in self.atoms:

            d = dist(a.position, target_point)
            distances_intensities[d] = distances_intensities.get(d, 0) + 1

    elif calculation_type == "for all pairs":
        for i, atom1 in enumerate(self.atoms):
            for atom2 in self.atoms[i+1:]:

                d = dist(atom1.position, atom2.position)
                distances_intensities[d] = distances_intensities.get(d, 0) + 1

    else:
        raise SystemError(
            f"Incorrect argument given. '{calculation_type}' was given. 'for all pairs' or 'from certain atom' was expected.")

    y, y_narrow, x = [], [
    ], linspace(-1, max(distances_intensities.keys())+1, 100000)

    for x_ in x:
        val = 0
        val_narrow = 0
        for d in distances_intensities:
            val += _gaussian(d, x_)*distances_intensities[d]
            val_narrow += _gaussian(d, x_, 0.001) * distances_intensities[d]
        y.append(val)
        y_narrow.append(val_narrow)

    if "rdf_lines" not in self.__dict__:
        self.rdf_lines = []

    if xy:
        return (x, y)
    self.rdf_lines.append(
        {"x": x, "y": y, "title": title})
    self.rdf_lines.append(
        {"x": x, "y": y_narrow, "title": title+"_narrow"})


def get_rdf(self, show=True, html=False, img=False):

    if not self.rdf_frames:
        self.add_rdf_frame()

    # Main rdf lines (start and end)

    main_lines_data = []
    for line in self.rdf_lines:
        main_lines_data.append(go.Scatter(x=line["x"], y=line["y"],
                                          mode='lines',
                                          name=line["title"]))

    # Intermediate results

    fig = go.Figure(
        layout=go.Layout(
            scene=dict(xaxis=dict(range=[0, 7], autorange=False),
                       yaxis=dict(range=[-1, 20], autorange=False)),
            title="RDF",
            updatemenus=[dict(
                type="buttons",
                buttons=[dict(label="Play",
                              method="animate",
                              args=[None, {"frame": {"duration": 1500}, "fromcurrent": True, "transition": {"duration": 2000}}])])]
        ),
        data=[*self.rdf_frames[0].data]+main_lines_data,
        frames=self.rdf_frames[1:],
    )

    if html:
        fig.write_html(html)
    if img:
        fig.write_image(img)
    if show:
        fig.show(equal_axes=True)


def get_totalE_plot(self, show=True, html=None, img=None):
    y = self.energies
    x = [i for i in range(len(y))]
    fig = px.line(x=x, y=y)
    fig.add_scatter(x=x, y=y, mode="markers")
    fig.update_yaxes(range=(-20, 100))

    if html:
        fig.write_html(html)
    if img:
        fig.write_image(img)
    if show:
        fig.show()
