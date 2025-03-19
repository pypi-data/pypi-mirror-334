import os
import pyswcloader
import pyswcloader.visualization


class SWCVisualization:
    def __init__(self):
        pass

    @staticmethod
    def view_swc(file_path):
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"The file {file_path} does not exist.")
        
        return pyswcloader.visualization.plot_neuron_3d(file_path)

