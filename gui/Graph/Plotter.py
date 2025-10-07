import pandas as pd
import plotly.graph_objects as go
import argparse

class Plotter:
    def __init__(self, csv_file):
        self.csv_file = csv_file
        self.df = None

    def load_csv(self):
        """Load the CSV file into a pandas DataFrame."""
        try:
            self.df = pd.read_csv(self.csv_file)
            print(f"CSV file '{self.csv_file}' loaded successfully.")
        except Exception as e:
            print(f"Error loading CSV file: {e}")
            exit(1)

    def plot_2d(self, x_axis, magnitude_column, frequency_column):
        """Plot 2D data with lines for frequencies."""
        if x_axis not in self.df.columns:
            print(f"Error: The CSV file does not contain the column '{x_axis}'.")
            exit(1)
        if magnitude_column not in self.df.columns:
            print(f"Error: The CSV file does not contain the column '{magnitude_column}'.")
            exit(1)
        if frequency_column not in self.df.columns:
            print(f"Error: The CSV file does not contain the column '{frequency_column}'.")
            exit(1)

        unique_frequencies = self.df[frequency_column].unique()
        frames = []
        for freq in unique_frequencies:
            df_freq = self.df[self.df[frequency_column] == freq]
            frames.append(go.Scatter(
                x=df_freq[x_axis],
                y=df_freq[magnitude_column],
                mode='lines+markers',
                name=f"Frequency: {freq} GHz"
            ))

        fig = go.Figure(
            data=frames[0],
            layout=go.Layout(
                title=f"2D Plot: {x_axis} vs {magnitude_column}",
                xaxis_title=x_axis,
                yaxis_title=magnitude_column,
                updatemenus=[{
                    "buttons": [
                        {
                            "args": [{"visible": [i == j for i in range(len(frames))]}],
                            "label": f"{unique_frequencies[j]} GHz",
                            "method": "update"
                        }
                        for j in range(len(frames))
                    ],
                    "direction": "down",
                    "showactive": True
                }]
            )
        )

        for frame in frames:
            fig.add_trace(frame)

        fig.show()

    def plot_3d(self, x_axis, y_axis, frequency_column, magnitude_column):
            """Plot 3D data as a surface for each frequency."""
            if frequency_column not in self.df.columns:
                print(f"Error: The CSV file does not contain the column '{frequency_column}'.")
                exit(1)
            if magnitude_column not in self.df.columns:
                print(f"Error: The CSV file does not contain the column '{magnitude_column}'.")
                exit(1)
            if x_axis not in self.df.columns or y_axis not in self.df.columns:
                print(f"Error: The CSV file does not contain the specified axes: '{x_axis}' or '{y_axis}'.")
                exit(1)

            unique_frequencies = self.df[frequency_column].unique()
            frames = []

            for freq in unique_frequencies:
                df_freq = self.df[self.df[frequency_column] == freq]
                
                # Create a grid using pivot for the given frequency
                pivot_table = df_freq.pivot(index=y_axis, columns=x_axis, values=magnitude_column)
                x_grid = pivot_table.columns.values
                y_grid = pivot_table.index.values
                z_grid = pivot_table.values

                frames.append(go.Surface(
                    x=x_grid,
                    y=y_grid,
                    z=z_grid,
                    name=f"Frequency: {freq} GHz"
                ))

            # Create the plot with frequency dropdown
            fig = go.Figure(
                data=[frames[0]],  # Show the first frame initially
                layout=go.Layout(
                    title=f"3D Plot: {x_axis}, {y_axis} vs {magnitude_column}",
                    scene=dict(
                        xaxis_title=x_axis,
                        yaxis_title=y_axis,
                        zaxis_title=magnitude_column
                    ),
                    updatemenus=[{
                        "buttons": [
                            {
                                "args": [{"visible": [i == j for i in range(len(frames))]}],
                                "label": f"{unique_frequencies[j]} GHz",
                                "method": "update"
                            }
                            for j in range(len(frames))
                        ],
                        "direction": "down",
                        "showactive": True
                    }]
                )
            )

            # Add all frames to the figure
            for frame in frames:
                fig.add_trace(frame)

            fig.show()

    def run(self, plot_type, x_axis, y_axis=None, magnitude_column='Magnitude', frequency_column='Frequency'):
        """Run the sequence of loading and plotting."""
        self.load_csv()
        self.df = self.df.dropna()  # Drop rows with missing values
        self.df[frequency_column] = self.df[frequency_column] / (1e9)  # Convert Hz to GHz
        if plot_type == "2d":
            self.plot_2d(x_axis, magnitude_column, frequency_column)
        elif plot_type == "3d":
            self.plot_3d(x_axis, y_axis, frequency_column, magnitude_column)
        else:
            print("Error: Invalid plot type. Use '2d' or '3d'.")


if __name__ == "__main__":
    # parser = argparse.ArgumentParser(description="Plot data from a CSV file.")
    # parser.add_argument("csv_file", type=str, help="Path to the CSV file.")
    # parser.add_argument(
    #     "-p",
    #     "--plot_type",
    #     type=str,
    #     choices=["2d", "3d"],
    #     required=True,
    #     help="Type of plot: '2d' or '3d'."
    # )
    # parser.add_argument(
    #     "-x",
    #     "--x_axis",
    #     type=str,
    #     choices=["X", "Y", "Z", "Polar", "Azimuth", "Elevation"],
    #     required=True,
    #     help="Column to use for the X-axis."
    # )
    # parser.add_argument(
    #     "-y",
    #     "--y_axis",
    #     type=str,
    #     choices=["X", "Y", "Z", "Polar", "Azimuth", "Elevation"],
    #     help="Column to use for the Y-axis (only for 3D plots)."
    # )
    # parser.add_argument(
    #     "-m",
    #     "--magnitude_column",
    #     type=str,
    #     default="Magnitude",
    #     help="Column to use for the Y-axis in 2D plots or Z-axis in 3D plots. Default is 'Magnitude'."
    # )
    # parser.add_argument(
    #     "-f",
    #     "--frequency_column",
    #     type=str,
    #     default="Frequency",
    #     help="Column to use for the slider. Default is 'Frequency'."
    # )

    # args = parser.parse_args()
    # plotter = Plotter(args.csv_file)
    # plotter.run(args.plot_type, args.x_axis, args.y_axis, args.magnitude_column, args.frequency_column)
    plotter = Plotter("Scan.csv")
    plotter.run("2d", "Azimuth", 'Elevation', "Magnitude", "Frequency")
