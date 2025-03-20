# Copyright (c) 2024 The KUTE contributors

import numpy as np
import h5py
import getpass

from kute import __version__
from MDAnalysis.analysis.base import AnalysisBase, Results
from MDAnalysis import Universe

class ElectricCurrent(AnalysisBase):
    """
    Class to calculate electric currents from MD trajectories.

    Args:
        universe (MDAnalysis.Universe): Universe containig the simulation
        filename (str, optional): Name of the h5 file to which the current will be saved. 
                                  Defaults to "current.h5".
    """
    
    def __init__(self, universe: Universe, filename: str="current.h5", **kwargs):

        super().__init__(universe.trajectory, **kwargs)
        self.u = universe
        self._total_steps = len(universe.trajectory)
        self.filename = filename
        self.results = Results()

    def _prepare(self):
        atom_masses = self.u.atoms.masses
        residue_masses = np.array([ a.residue.mass for a in self.u.atoms ])
        residue_charges = np.array([ a.residue.charge for a in self.u.atoms ])

        self._weights = residue_charges * atom_masses / residue_masses
        
        self.results.current = np.zeros((self._total_steps, 3))

    def _single_frame(self):

        self.results.current[self._frame_index, :] = np.sum(self.u.atoms.velocities * self._weights[:, np.newaxis], axis=0)

    def _conclude(self):

        self.write_h5_file()


    def write_h5_file(self):
        """
        Write the current to an h5 file
        """

        with h5py.File(self.filename, "w") as file:

            ## Metadata group

            file.create_group('information')
            file['information'].attrs['kute_version'] = __version__
            file['information'].attrs['author'] = getpass.getuser()
            file['information'].create_group('units')
            file['information/units'].attrs['time'] = "ps"
            file['information/units'].attrs['electric_current'] = "e * A / ps"

            ## Data group

            file.create_group('timeseries')
            file['timeseries'].create_dataset('time', data = self.times, maxshape=(None,))
            file['timeseries'].create_dataset('current', data = self.results.current, maxshape=(None, 3))
