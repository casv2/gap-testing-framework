# This script defines a test case which computes one or more physical
# properties with a given model
#
# INPUTS: 
#   model.calculator -- an ase.calculator.Calculator instance
#     this script can assume the calculator is checkpointed.
#
# OUTPUTS:
#   properties -- dictionary of key/value pairs corresponding
#     to physical quantities computed by this test

# standard ASE structure generation routines
from ase.lattice.cubic import BodyCenteredCubic

# set of utility routines specific this this model/testing framework
from utilities import relax_atoms, relax_atoms_cell

# the current model
import model 

a0 = 3.32 # initial guess at lattice constant, cell will be relaxed below
fmax = 0.01 # maximum force following relaxtion [eV/A]

# set up the a
bulk = BodyCenteredCubic(symbol='Ti', latticeconstant=a0)

# specify that we will use model.calculator to compute forces, energies and stresses
bulk.set_calculator(model.calculator)

# use one of the routines from utilities module to relax the initial
# unit cell and atomic positions
bulk = relax_atoms_cell(bulk, tol=fmax, traj_file=None)

# set up supercell
bulk *= (10, 1, 1)

def surface_energy(bulk):
    Nat = bulk.get_number_of_atoms()

    # relax atom positions, holding cell fixed
    # vac = relax_atoms(vac, fmax=fmax)

    # compute surface formation energy as difference of bulk and expanded cell
    ebulk = bulk.get_potential_energy()
    print 'bulk cell energy', ebulk

    bulk.cell[0,:] += [10.0,0.0,0.0]
    eexp  = bulk.get_potential_energy()
    
    print 'expanded cell energy', eexp
    e_form = (eexp - ebulk) / (bulk.cell[1,1]*bulk.cell[2,2])
    print 'unrelaxed 100 surface formation energy', e_form
    return e_form

# dictionary of computed properties - this is output of this test, to
#   be compared with other models
properties = {'surface_energy_100_unrelaxed':
                surface_energy(bulk) }
