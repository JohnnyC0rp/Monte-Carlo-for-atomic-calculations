import plotly.graph_objects as go
import plotly.express as px
from math import dist
from statistics import mode
from numpy import round as round_all_in_array, arange


def visualize(self):

    fig = go.Figure(
        layout=go.Layout(
            margin=dict(l=10, r=10, t=40, b=10),
            title="Atoms",
            updatemenus=[dict(
                type="buttons",
                buttons=[dict(label="Play",
                              method="animate",
                              args=[None])])]
        ),
        data=self.frames[0].data,
        frames=self.frames[1:]
    )
    fig.update_traces(marker_line_width=80)
    fig.show()


def add_frame(self):
    frame = go.Frame(
        data=[go.Scatter3d(
            x=[atom.position[0] for atom in self.ATOMS],
            y=[atom.position[1] for atom in self.ATOMS],
            z=[atom.position[2] for atom in self.ATOMS] if self.dimensions == 3
            else [0 for _ in range(len(self.ATOMS))],
            mode="markers",  # lines, markers,text,none,(lines+markers)
            marker_color='rgb(225,166,29)'

        )]
    )
    self.frames.append(frame)


def get_distances_bar_plot(self, num_most_common=3, accuracy=1):

    y = []

    for i, atom1 in enumerate(self.ATOMS):
        for atom2 in self.ATOMS[i+1:]:
            y.append(dist(atom1.position, atom2.position))

    x = [i for i in range(len(y))]

    fig = px.bar(x=x, y=y, color=y,
                 color_continuous_scale=px.colors.sequential.Cividis_r,
                 title="Distances")

    fig.update_yaxes(range=[0, int(max(y))+1])

    # Adding mode lines
    rounded_y = round_all_in_array(y, accuracy)
    for i in range(num_most_common):

        common = mode(rounded_y)
        fig.add_hline(y=common, line_width=1, line_dash="dash",
                      line_color=f"rgb({i*60},{20},{30})")
        rounded_y = list(filter((common).__ne__, rounded_y))
        if not rounded_y:
            break

    fig.show()


def get_RDF_plot(self):
    d_frequency = {}

    for i, atom1 in enumerate(self.ATOMS):
        for atom2 in self.ATOMS[i+1:]:

            if (dst := round(dist(atom1.position, atom2.position), decimals:=2)) in d_frequency:
                d_frequency[dst] += 1
            else:
                d_frequency[dst] = 1

    y = []
    x = []
    for i in arange(0, int(max(d_frequency.keys())*2), 1/10**decimals):
        x.append(i)
        if i not in d_frequency:
            y.append(0)
        else:
            y.append(d_frequency[i])
    # print(x,y,d_frequency)

    fig = px.line(x=x, y=y)

    fig.show()


if __name__ == '__main__':
    from system import *
    s = System(3)
    s.generate_atoms(10, (10, 20))
    s.add_frame()
    s.visualize()
