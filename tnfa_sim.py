from netpyne import specs, sim

# a NetPyNE model requires a netParams (network parameters) object
# and a simConfig (simulation configuration) object
netParams = specs.NetParams()
simConfig = specs.SimConfig()

# import a morphology from an swc file
cellRule = netParams.importCellParams(
    label='swc_cell', 
    fileName='BS0284.swc', 
    cellName='BS0284', 
    importSynMechs=False,
    )

# add channels to the morphology (Hodgkin-Huxley in soma, passive elsewhere)
for secName in cellRule['secs']:
    cellRule['secs'][secName]['geom']['cm'] = 1
    if secName.startswith('soma'):
        cellRule['secs'][secName]['mechs']['hh'] = {
            'gnabar': 0.12, 
            'gkbar': 0.036, 
            'gl': 0.003, 
            'el': -70,
            }
    else:
        cellRule['secs'][secName]['mechs']['pas'] = {
            'g': 0.0000357, 
            'e': -70,
            }

# create a population of one cell
netParams.popParams['my_pop'] = {'cellType': 'swc_cell', 'numCells': 1}

# add a current clamp stimulation
netParams.stimSourceParams['IClamp0'] = {
    'type': 'IClamp', 
    'del': 300, 
    'dur': 100, 
    'amp': 5.0,
    }

# connect the stimulation to our cell
netParams.stimTargetParams['IClamp0->cell0'] = {
    'source': 'IClamp0', 
    'sec':'soma', 
    'loc': 0.5, 
    'conds': {'cellList': [0]},
    }


# set up the simulation configuration
simConfig.filename = 'tnfa'
simConfig.duration = 1000.0

simConfig.recordCells = ['all']
simConfig.recordTraces = {
    'V_soma': {
        'sec': 'soma_0',
        'loc': 0.5,
        'var': 'v',
        },
    }

simConfig.analysis = {
    'plotTraces': {
        'include': ['all'],
        'saveFig': True,
        },
    'plotShape': {
        'saveFig': True,
        }
    }

# create, simulate, and analyze the model
sim.createSimulateAnalyze(netParams=netParams, simConfig=simConfig)

