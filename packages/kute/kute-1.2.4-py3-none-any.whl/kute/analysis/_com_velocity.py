# Copyright (c) 2024 The KUTE contributors

import numpy as np
import h5py
import getpass

from kute import __version__
from MDAnalysis.analysis.base import AnalysisBase
from MDAnalysis import Universe
from MDAnalysis.analysis.base import Results


class COMVelocity(AnalysisBase):
    """
    Class to calculate center of mass velocities from MD trajectories.

    Args:
        universe (MDAnalysis.Universe): Universe containig the simulation
        filename (str, optional): Name of the h5 file to which the velocities will be saved. 
                                  Defaults to "com_velocity.h5".
    """
    def __init__(self, universe: Universe, filename:str="com_velocity.h5", **kwargs):

        super().__init__(universe.trajectory, **kwargs)
        self.u = universe
        self._total_steps = len(universe.trajectory)
        self.filename = filename
        self.results = Results()

    
    def _prepare(self):

        atom_residue_masses = np.array([ a.residue.mass for a in self.u.atoms ])
        atom_masses = self.u.atoms.masses
        weights = atom_masses / atom_residue_masses
        self._matrix = np.zeros((self.u.residues.n_residues, self.u.atoms.n_atoms))

        for i, res in enumerate(self.u.residues):
            for atom in res.atoms:
                j = atom.index
                self._matrix[i, j] = weights[j]

        self.results.com_vel = np.zeros((self._total_steps, self.u.residues.n_residues, 3))

    def _single_frame(self):

        self.results.com_vel[self._frame_index, :, :] = self._matrix @ self.u.atoms.velocities
    
    def _conclude(self):

        self.write_h5_file()

    def write_h5_file(self):

        with h5py.File(self.filename, "w") as file:

        ## Metadata group

            file.create_group('information')
            file['information'].attrs['kute_version'] = __version__
            file['information'].attrs['author'] = getpass.getuser()
            file['information'].create_group('units')
            file['information/units'].attrs['time'] = "ps"
            file['information/units'].attrs['com_velocities'] = "A / ps"

            ## Residue identificators

            file.create_group('residues')
            names = self.u.residues.resnames
            for name in np.unique(names):
                where = np.where(names==name)[0]
                file['residues'].create_dataset(name, data=where, dtype=int)

            ## Data group

            file.create_group('timeseries')
            file['timeseries'].create_dataset('time', data=self.times, maxshape=(None,))
            file['timeseries'].create_dataset('com_velocities', data=self.results.com_vel, maxshape=(None, self.u.residues.n_residues, 3))