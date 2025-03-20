import numpy as np
import h5py
import getpass

from kute import __version__
from MDAnalysis.analysis.base import AnalysisBase
from MDAnalysis import Universe
from MDAnalysis.analysis.base import Results



class PressureTensor(AnalysisBase):
    """
    Class to calculate the off diagonal components of the pressure tensor from MD trajectories.

    Args:
        universe (MDAnalysis.Universe): Universe containig the simulation
        filename (str, optional): Name of the h5 file to which the pressure will be saved. 
                                  Defaults to "pressure_tensor.h5".
    """

    def __init__(self, universe: Universe, filename: str="pressure_tensor.h5", **kwargs):

        super().__init__(universe.trajectory, **kwargs)
        self.u = universe
        self._total_steps = len(universe.trajectory)
        self.filename = filename
        self.results = Results()

    def _prepare(self):

        self.results.off_diagonal = np.zeros((self._total_steps, 3))

    def _single_frame(self):
        
        positions = self.u.atoms.positions * 1e-10
        velocities = self.u.atoms.velocities * 1e-10 / 1e-12
        forces = self.u.atoms.forces * 1e3 / (1e-10 * 6.02214076e23)
        volume = self.u.dimensions[:3].prod() * 1e-30

        m_v_v_tensor = 1.66054e-27 * np.tensordot(self.u.atoms.masses[:, np.newaxis]*velocities, velocities, axes=(0, 0))

        r_f_tensor = np.tensordot(positions, forces, axes=(0, 0))

        tensor = np.triu(m_v_v_tensor + r_f_tensor, k=1)

        self.results.off_diagonal[self._frame_index, :] = tensor.flatten()[np.flatnonzero(tensor)] / volume

    def _conclude(self):

        self.write_h5_file()
    
    def write_h5_file(self):
        """
        Write the pressure to an h5 file
        """

        with h5py.File(self.filename, "w") as file:

            ## Metadata group

            file.create_group('information')
            file['information'].attrs['kute_version'] = __version__
            file['information'].attrs['author'] = getpass.getuser()
            file['information'].create_group('units')
            file['information/units'].attrs['time'] = "ps"
            file['information/units'].attrs['pressure_tensor'] = "Pa"

            ## Data group

            file.create_group('timeseries')
            file['timeseries'].create_dataset('time', data = self.times, maxshape=(None,))
            file['timeseries'].create_dataset('pressure_tensor', data = self.results.off_diagonal, maxshape=(None, 3))
