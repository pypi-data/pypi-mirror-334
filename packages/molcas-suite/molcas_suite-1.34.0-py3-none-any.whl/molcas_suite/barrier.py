"""
This module contains functions for plotting barrier figures from molcas output
files
"""

import jax.numpy as jnp
from .extractor import make_extractor, read_elec_orb
import angmom_suite.multi_electron as me
import angmom_suite.crystal as crys
import angmom_suite.barrier as bar
import numpy as np
import numpy.linalg as la
from angmom_suite.basis import sf2ws, sf2ws_spin, sf2ws_amfi, unitary_transform, \
    from_blocks, dissect_array, extract_blocks, make_angmom_ops_from_mult, \
    rotate_cart, cartesian_op_squared

def barrier(h5name, Zeeman=[0,0,25E-6], num_states=None,
            trans_colour="#ff0000", state_colour="black", show=False,
            save=True, save_name="barrier.png",
            xlabel=r"$\langle \hat{J}_{z} \rangle$",
            ylabel=r"Energy (cm$^{-1}$)", yax2_label="Energy (K)",
            yax2=False, yax2_conv=1.4, print_datafile=True, verbose=True):
    """
    Creates barrier figure from OpenMolcas rassi.h5 file

    Parameters
    ----------
        h5name : str
            Name of the MOLCAS rassi.h5 file.
        Zeeman : float, default=[0,0,25 uT]
            Magnetic field strength in Tesla
        num_states : int
            Number of states to include
        trans_colour : str, defualt "#ff0000" (red)
            Hex code or name specifying arrow colours
        state_colour: str, default "black"
            Hex code or name specifying state colours
        show : bool, default False
            If True, show plot on screen - disabled with `ax_in`
        save : bool, default True
            If True, save plot to file - disabled with `ax_in`
        save_name : str, default "barrier.pdf"
            Filename for saved image
        yax2 : bool, default False
            If True use secondary y (energy) axis
        yax2_conv : float, default 1.4 (cm-1 --> Kelvin)
            Conversion factor from primary to secondary y axis
        yax2_label : str, default "Energy (K)"
            Label for secondary y axis (requires `yax2=True`)
        xlabel : str, default "$\langle \ \hat{J}_{z} \ \rangle$"
            x label
        ylabel : str, default "Energy (cm$^{-1}$)"
            x label
        print_datafile : bool, default True
            If True, save datafile containing energies, Bz, Jz, k_max
            to barrier_data.dat in execution directory
        verbose : bool, default True
            If True, print all saved filenames to screen
    Returns
    -------
        None
    """ # noqa

    muB_au = 2.127191057440e-6 # Eh/Tesla
    ge = 2.00231930436182
    au2cm = 2.1947463e5

    #get data from rassi.h5 file
    angm = make_extractor(h5name, ("rassi", "SFS_angmom"))[()]  # get L = -i r x nabla (Hermitian)
    ener = make_extractor(h5name, ("rassi", "SFS_energies"))[()]
    amfi = make_extractor(h5name, ("rassi", "SFS_AMFIint"))[()]
    spin_mult = make_extractor(h5name, ("rassi", "spin_mult"))[()]

    # spin-free energies; reference to ground state of lowest multiplicity
    sf_ener = list(extract_blocks(ener, spin_mult))

    # build required operators
    ops = {
        'sf_angm': list(extract_blocks(angm, spin_mult, spin_mult)),
        'sf_mch': list(map(lambda e: np.diag(e - sf_ener[0][0]), sf_ener)),
        'sf_amfi': list(map(list, dissect_array(amfi, spin_mult, spin_mult))),
    }
    sf_mult = dict(zip(*np.unique(spin_mult, return_counts=True)))
    smult = np.repeat(list(sf_mult.keys()), list(sf_mult.values()))
    ws_angm = sf2ws(ops['sf_angm'], sf_mult)
    ws_spin = np.array(make_angmom_ops_from_mult(smult)[0:3])
    ws_mch = sf2ws(ops['sf_mch'], sf_mult)
    ws_amfi = sf2ws_amfi(ops['sf_amfi'], sf_mult)

    if num_states is None:
        num_states = ws_amfi.shape[0]

    # add magnetic field and obtain eigenstates
    ws_zee = np.zeros(ws_mch.shape)
    for axis, field in enumerate(Zeeman):
        ws_zee += muB_au * field * (ws_angm[axis] + ge*ws_spin[axis])
    ws_hamiltonian = ws_mch + ws_amfi + ws_zee
    so_eig, so_vec = jnp.linalg.eigh(ws_hamiltonian)
    so_spin = unitary_transform(ws_spin, so_vec)
    so_angmom = unitary_transform(ws_angm, so_vec)
    tot_val = (so_eig - so_eig[0])*au2cm

    # get expectation of J along quantisation axis and magnetic moment matrices including two perpendicular axes
    Zee_length = np.sqrt(Zeeman[0]**2 + Zeeman[1]**2 + Zeeman[2]**2)
    Jz = (1.0/Zee_length)*(Zeeman[0]*(so_spin[0,:,:]+so_angmom[0,:,:]) + Zeeman[1]*(so_spin[1,:,:]+so_angmom[1,:,:]) + Zeeman[2]*(so_spin[2,:,:]+so_angmom[2,:,:]))
    Jz = np.real(np.diag(Jz))
    MuZ = muB_au * (1.0/Zee_length)*(Zeeman[0]*(ge*so_spin[0,:,:]+so_angmom[0,:,:]) + Zeeman[1]*(ge*so_spin[1,:,:]+so_angmom[1,:,:]) + Zeeman[2]*(ge*so_spin[2,:,:]+so_angmom[2,:,:]))
    VecX = [0.0, 0.0, 0.0]
    VecY = [0.0, 0.0, 0.0]
    if Zeeman[2] != 0.0:
        VecX[0] = 1.0
        VecX[1] = 1.0
        VecX[2] = (-Zeeman[0]-Zeeman[1])/Zeeman[2]
    else:
        VecX[0] = 0.0
        VecX[1] = 0.0
        VecX[2] = 1.0
    VecX_length = np.sqrt(VecX[0]**2 + VecX[1]**2 + VecX[2]**2)
    VecY[0] = VecX[1]*Zeeman[2] - VecX[2]*Zeeman[1]
    VecY[1] = VecX[2]*Zeeman[0] - VecX[0]*Zeeman[2]
    VecY[2] = VecX[0]*Zeeman[1] - VecX[1]*Zeeman[0]
    VecY = VecY/Zee_length
    VecY_length = np.sqrt(VecY[0]**2 + VecY[1]**2 + VecY[2]**2)
    MuX = (1.0/VecX_length)*(VecX[0]*(ge*so_spin[0,:,:]+so_angmom[0,:,:]) + VecX[1]*(ge*so_spin[1,:,:]+so_angmom[1,:,:]) + VecX[2]*(ge*so_spin[2,:,:]+so_angmom[2,:,:]))
    MuY = (1.0/VecY_length)*(VecY[0]*(ge*so_spin[0,:,:]+so_angmom[0,:,:]) + VecY[1]*(ge*so_spin[1,:,:]+so_angmom[1,:,:]) + VecY[2]*(ge*so_spin[2,:,:]+so_angmom[2,:,:]))

    # Overall transition probabilties as average of each dipole moment squared
    trans = (np.abs(MuX) ** 2 + np.abs(MuY) ** 2 + np.abs(MuZ) ** 2) * 1. / 3.

    # Create barrier figure
    bar.barrier_figure(
        num_states,
        tot_val[0:num_states],
        Jz[0:num_states],
        trans=trans[0:num_states,0:num_states],
        show=show,
        save=save,
        save_name=save_name,
        trans_colour=trans_colour,
        state_colour=state_colour,
        yax2=yax2,
        yax2_conv=yax2_conv,
        yax2_label=yax2_label,
        ylabel=ylabel,
        xlabel=xlabel
    )

    if save and verbose:
        print(
            "Barrier figure saved to {} in ".format(save_name) +
            "execution directory"
        )

    # Create output datafile

    if print_datafile:
        with open("barrier_data.dat", "w") as df:

            df.write("Barrier figure data for {}\n".format(h5name))
            df.write("\n")

            df.write("Energies with Zeeman term (cm^-1)\n")
            df.write("------------------------------------------------\n")
            for i in range(num_states):
                df.write("{:14.7f}\n".format(tot_val[i]))

            df.write("\n")

            df.write("Jz expectation values with Zeeman term:\n")
            df.write("---------------------------------------\n")
            for i in range(num_states):
                df.write("{: .7f}\n".format(Jz[i]))

    if verbose:
        print("Datafile saved to barrier_data.dat in execution directory")

    return
