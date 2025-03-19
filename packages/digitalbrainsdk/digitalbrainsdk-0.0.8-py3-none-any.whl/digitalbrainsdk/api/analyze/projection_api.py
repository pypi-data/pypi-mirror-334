import pyswcloader
import pyswcloader.brain
import requests
import os
from digitalbrainsdk.config import ConfigManager
import urllib.request


class ProjectionApi:
    """
        A class to represent the Projection API.
        Attributes
        ----------
        data_path : str, optional
            The path to the swc data (default is None).
        annotation_path : str, optional
            The path for nrrd information (default is None).
        resolution : int, optional
            The resolution setting (default is 10).
        cores : int, optional
            The number of cores to use (default is 1).
    '"""

    def __init__(self, data_path=None, annotation_path=None, resolution=10, cores=1):
        """
        Constructs all the necessary attributes for the Projection API object.
        Parameters
        ----------
        data_path : str, optional
            The path to the swc data (default is None).
        annotation_path : str, optional
            The path for nrrd information (default is None).
        resolution : int, optional
            The resolution setting (default is 10).
        cores : int, optional
            The number of cores to use (default is 1).
        """
        self.data_path = data_path
        self.annotation_path = annotation_path
        self.resolution = resolution
        self.cores = cores
        self.cache_dir = None
        cache_dir_name = ConfigManager().get("CACHE", "CacheDir")
        if not self.cache_dir:
            self.cache_dir = os.path.join(os.getcwd(), cache_dir_name, "analyze")

    def batch_projection_length(self):
        """
        Batch projection length
        """
        if self.annotation_path is None:
            print("annotation_path is None, use the default annotation path")
            print(
                "Downloading nrrd from http://download.alleninstitute.org/informatics-archive/current-release/mouse_ccf/annotation/ccf_2017/annotation_10.nrrd"
            )
            self.download_nrrd()
            print(f"Downloaded nrrd to {self.annotation_path}")
        if self.data_path is None:
            raise ValueError("data_path is None, please provide a path to the swc data")

        annotation = pyswcloader.brain.read_nrrd(self.annotation_path)
        try:
            projection_length = pyswcloader.projection_batch.projection_length(
                data_path=self.data_path,
                annotation=annotation,
                resolution=self.resolution,
                cores=self.cores,
            )
            return projection_length
        except Exception as e:
            print(f"Error calculating projection length: {e}")
            return None

    def distance_morphology_matrix(self):
        """
        Distance morphology matrix
        """
        if self.data_path is None:
            raise ValueError("data_path is None, please provide a path to the swc data")

        try:
            scores = pyswcloader.distance.morphology_matrix(self.data_path, self.cores)
            return scores
        except Exception as e:
            print(f"Error calculating distance morphology matrix: {e}")
        return None

    def soma_distribution(self):
        """
        Soma distribution
        """
        if self.data_path is None:
            raise ValueError("data_path is None, please provide a path to the swc data")

        try:
            distribution = pyswcloader.swc.plot_soma_distribution(self.data_path)
            return distribution
        except Exception as e:
            print(f"Error calculating soma distribution: {e}")
        return None

    def download_nrrd(self):
        """
        Download nrrd
        """
        self.annotation_path = os.path.join(
            os.getcwd(), self.cache_dir, "nrrd", "annotation_10.nrrd"
        )
        if not os.path.exists(self.annotation_path):
            os.makedirs(os.path.dirname(self.annotation_path), exist_ok=True)

        try:
            urllib.request.urlretrieve(
                "http://download.alleninstitute.org/informatics-archive/current-release/mouse_ccf/annotation/ccf_2017/annotation_10.nrrd",
                self.annotation_path,
            )
        except Exception as e:
            print(f"Error downloading nrrd: {e}")
            return None
        print(f"Downloaded nrrd to {self.annotation_path}")
        return self.annotation_path

    def set_annotation_path(self, annotation_path):
        """
        Set the annotation path
        Parameters
        ----------
        annotation_path : str
            The path to the annotation file.
        """
        self.annotation_path = annotation_path

    def set_data_path(self, data_path):
        """
        Set the data path
        Parameters
        ----------
        data_path : str
            The path to the swc file.
        """
        self.data_path = data_path

    def set_resolution(self, resolution):
        """
        Set the resolution
        Parameters
        ----------
        resolution
            The resolution setting.
        """
        self.resolution = resolution

    def set_cores(self, cores):
        """
        Set the number of cores
        Parameters
        ----------
        cores
            The number of cores to use.
        """
        self.cores = cores
