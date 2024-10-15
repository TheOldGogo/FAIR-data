# 2024-09-03 - JG: trying to create an example nexus file, based on Rod's example "NXopt_minimal_example_2D_data.py"
# 2024-09-14 - JG: so minimum working and uploaded data done
# 2024-09-24 - JG: now adding everything that we normally include in the setup description

# Import h5py, to write an hdf5 file
import h5py
# Import numpy for simple math stuff
import numpy as np

##################################################################################################
###                                            BEGIN                                           ###
##################################################################################################

# create a h5py file in writing mode with given name "NXopt_minimal_example", file extension "nxs"
f = h5py.File("NXta_test.nxs", "w")

#create a group, called "entry"
f.create_group('/entry')

# assign the group "entry" an attribute
# The attribute is "NX_class"(a NeXus class) with the value of this class is "NXentry"
f['/entry'].attrs['NX_class'] = 'NXentry'

# Create datafield called "definition" inside the entry, and assign it the value "NXopt"
f['/entry/definition'] = 'NXoptical_spectroscopy'

# All following commands are only repeatitions of the previous ones.
# In principle a NeXus file can be hardcoded with these commands
# By following the definitions and structure for NXopt 
# given at https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXopt.html
# a respective FAIR NeXus file can be created


# Assign datafield attributes "url" and "version" with respective strings
f['/entry/definition'].attrs['url'] = 'https://github.com/FAIRmat-NFDI/nexus_definitions/blob/98d6784fe4e4ec23067aa1e6e6b64601b6d1aebc/contributed_definitions/NXoptical_spectroscopy.nxdl.xml'
f['/entry/definition'].attrs['version'] = 'v2024.02'


# General NeXus file information
f['/entry/title'] = 'Attempt to create a TA nexus file'
f['/entry/start_time'] = '2024-09-03T11:20:45+03'
f['/entry/experiment_type'] = 'transmission spectroscopy'
f['/entry/experiment_sub_type'] = ['time resolved', 'pump-probe']

f.create_group('/entry/experiment_identifier')
#note: Ron created it as a group. While I used attribute. Check if I'm wrong. -> I am
f['/entry/experiment_identifier'].attrs['NX_class'] = 'NXidentifier'
f['/entry/experiment_identifier/identifier'] = 'Coherent Lengend DUO (room 210)_ksc'
f['/entry/experiment_identifier/service'] = 'RC KSC'
f['/entry/experiment_identifier/identifier_type'] = 'local'

# User informations
f.create_group('entry/USER')
f['/entry/USER'].attrs['NX_class'] = 'NXuser'
f['/entry/USER/name'] = 'Julien Gorenflot'
f['/entry/USER/role'] = 'Custodian'
f['/entry/USER/affiliation'] = 'Materials Science and Engineering Program (MSE), \n \
Physical Science and Engineering Division (PSE), \n \
King Abdullah University of Science and Technology (KAUST), \n \
Thuwal 23955-6900, Kingdom of Saudi Arabia'
f['/entry/USER/address'] = 'King Abdullah University of Science and Technology (KAUST), \n \
Building 3, Level 3, Sea side, Office 3231, Work Station 12, \n \
Thuwal 23955-6900, Kingdom of Saudi Arabia'
f['/entry/USER/email'] = 'julien.gorenflot@kaust.edu.sa'
f.create_group('entry/USER/ORCID')
f['/entry/USER/ORCID'].attrs['NX_Class'] = 'NXidentifier'
f['/entry/USER//identifier'] = '0000-0002-0533-3205'
f['/entry/USER/ORCID/is_persistent'] = True


# Generic information about the instrumental setup
f.create_group('/entry/instrument_TA_Setup')
f['/entry/instrument_TA_Setup'].attrs['NX_class'] = 'NXinstrument'
f['/entry/instrument_TA_Setup/angle_reference_frame'] = 'sample normal centered'
f['/entry/instrument_TA_Setup/angle_of_incidence'] = 0
f['/entry/instrument_TA_Setup/angle_of_incidence'].attrs['units'] = 'deg'
f['/entry/instrument_TA_Setup/angle_of_incidence'].attrs['unit'] = 'NX_ANGLE'
f['/entry/instrument_TA_Setup/angle_of_detection'] = 180
f['/entry/instrument_TA_Setup/angle_of_detection'].attrs['units'] = 'deg'
f['/entry/instrument_TA_Setup/angle_of_detection'].attrs['unit'] = 'NX_ANGLE'
f['/entry/instrument_TA_Setup/angle_of_incident_and_detection_beam'] = 180
f['/entry/instrument_TA_Setup/angle_of_incident_and_detection_beam'].attrs['units'] = 'deg'
f['/entry/instrument_TA_Setup/angle_of_incident_and_detection_beam'].attrs['unit'] = 'NX_ANGLE'

# NXbeam entry: probe beam
f.create_group('/entry/instrument_TA_Setup/beam_probe')
f['/entry/instrument_TA_Setup/beam_probe'].attrs['NX_class'] = 'NXbeam'
f['/entry/instrument_TA_Setup/beam_probe/parameter_reliability'] = 'measured'   # measured, but not reagularly, possibly add a date for the measurement
        # for this beam it is actually measured, but after the sample
        # and very convoluted with the detector array's callibration
        # maybe after the chamber but without sample would make sense?
        # but in anycase, it's not really an "incident" beam which is measure as a result
        # maybe there's a place where I can indicate the beam characterization path
        # anyway, I'm going to use that -> first need to lead the file
Wavelengths = 1240/np.loadtxt('AS228A_SD730nm_11uW_delta_TPump-on.txt')[1:,0]
time_delays = np.loadtxt('AS228A_SD730nm_11uW_delta_TPump-on.txt')[0,1:]
Ts= np.loadtxt('AS228A_SD730nm_11uW_delta_TPump-on.txt')[1:,1:]
f['/entry/instrument_TA_Setup/beam_probe/incident_wavelength'] = Wavelengths
f['/entry/instrument_TA_Setup/beam_probe/incident_wavelength'].attrs['units'] = 'nm'
f['/entry/instrument_TA_Setup/beam_probe/incident_wavelength'].attrs['unit'] = 'NX_WAVELENGTH'
        # so here should be the WL array but again, it's not really "incident" as it is measured at the end of the whole system
        # note: I could use the wavelength_spread, which seems to be meant for a continuous light,
            # but it is defined by it's FWHM and most of the part we use is actually below the HM
            # + the distribution is far from being Gaussian due to all the filters we put on the way.
            # Or maybe I just put the overall extend without adding the weight.
f['/entry/instrument_TA_Setup/beam_probe/incident_wavelength_spread'] = np.ones(len(Wavelengths))
f['/entry/instrument_TA_Setup/beam_probe/incident_wavelength_spread'].attrs['units'] = 'nm'
f['/entry/instrument_TA_Setup/beam_probe/incident_wavelength_spread'].attrs['unit'] = 'NX_WAVELENGTH'
f['/entry/instrument_TA_Setup/beam_probe/incident_wavelength_weights'] = np.transpose(Ts)
        # I transposed it. Will have to check if this is the right way
f['/entry/instrument_TA_Setup/beam_probe/pulse_delay'] = time_delays
f['/entry/instrument_TA_Setup/beam_probe/pulse_delay'].attrs['units'] = 'ps'
f['/entry/instrument_TA_Setup/beam_probe/pulse_delay'].attrs['unit'] = 'NX_TIME'
f['/entry/instrument_TA_Setup/beam_probe/pulse_delay'].attrs['reference_beam'] = '/entry/instrument_TA_Setup/beam_pump'
f['/entry/instrument_TA_Setup/beam_probe/extent'] = [0.6,0.6]
        # gonna need to be add one dimension for the other "peaks"
        # + I don't like the fact that it can be square only
f['/entry/instrument_TA_Setup/beam_probe/extent'].attrs['units'] = 'mm'
f['/entry/instrument_TA_Setup/beam_probe/extent'].attrs['unit'] = 'NX_LENGTH'
f['/entry/instrument_TA_Setup/beam_probe/associated_source'] = '/entry/instrument_TA_Setup/source_WL_crystal'
        # I believe it makes more sense to have the crystal as the source for the WL, although at the end of the day
        # we need to specify somewhere what was pumping this WL
f['/entry/instrument_TA_Setup/beam_probe/beam_polarization_type'] = 'linear'
f['/entry/instrument_TA_Setup/beam_probe/linear_beam_sample_polarization'] = 0
        # ultimately it would be better to define a coordinate system and use the
        # incident polarization instead
f['/entry/instrument_TA_Setup/beam_probe/linear_beam_sample_polarization'].attrs['units'] = 'deg'
f['/entry/instrument_TA_Setup/beam_probe/linear_beam_sample_polarization'].attrs['unit'] = 'NX_ANGLE'

# NXbeam entry: pump beam
f.create_group('/entry/instrument_TA_Setup/beam_pump')
f['/entry/instrument_TA_Setup/beam_pump'].attrs['NX_class'] = 'NXbeam'
f['/entry/instrument_TA_Setup/beam_pump/parameter_reliability'] = 'measured'
f['/entry/instrument_TA_Setup/beam_pump/incident_wavelength'] = 730
f['/entry/instrument_TA_Setup/beam_pump/incident_wavelength'].attrs['units'] = 'nm'
f['/entry/instrument_TA_Setup/beam_pump/incident_wavelength'].attrs['unit'] = 'NX_WAVELENGTH'
        # to be updated regularly
f['/entry/instrument_TA_Setup/beam_pump/incident_wavelength_spread'] = 1
        # to check or remove
f['/entry/instrument_TA_Setup/beam_pump/extent'] = [1,1]
        # to be updated regularly
f['/entry/instrument_TA_Setup/beam_pump/extent'].attrs['units'] = 'mm'
f['/entry/instrument_TA_Setup/beam_pump/extent'].attrs['unit'] = 'NX_LENGTH'
f['/entry/instrument_TA_Setup/beam_pump/associated_source'] = '/entry/instrument_TA_Setup/source_TOPAS'
        # for our app: make cases 1- TOPAS 2- AOT
f['/entry/instrument_TA_Setup/beam_pump/beam_polarization_type'] = 'linear'
f['/entry/instrument_TA_Setup/beam_pump/linear_beam_sample_polarization'] = 54.7356
        # check
        # ultimately it would be better to define a coordinate system and use the
        # incident polarization instead
f['/entry/instrument_TA_Setup/beam_pump/linear_beam_sample_polarization'].attrs['units'] = 'deg'
f['/entry/instrument_TA_Setup/beam_pump/linear_beam_sample_polarization'].attrs['unit'] = 'NX_ANGLE'

f.create_group('/entry/instrument_TA_Setup/beam_pump_LD')
f['/entry/instrument_TA_Setup/beam_pump_LD'].attrs['NX_class'] = 'NXbeam'
f['/entry/instrument_TA_Setup/beam_pump_LD/parameter_reliability'] = 'measured'
f['/entry/instrument_TA_Setup/beam_pump_LD/incident_wavelength'] = 532
f['/entry/instrument_TA_Setup/beam_pump_LD/incident_wavelength'].attrs['units'] = 'nm'
f['/entry/instrument_TA_Setup/beam_pump_LD/incident_wavelength'].attrs['unit'] = 'NX_WAVELENGTH'
f['/entry/instrument_TA_Setup/beam_pump_LD/incident_wavelength_spread'] = 1
        # to check or remove
f['/entry/instrument_TA_Setup/beam_pump_LD/extent'] = [0.6,0.6]
        # to be updated regularly
f['/entry/instrument_TA_Setup/beam_pump_LD/extent'].attrs['units'] = 'mm'
f['/entry/instrument_TA_Setup/beam_pump_LD/extent'].attrs['unit'] = 'NX_LENGTH'
f['/entry/instrument_TA_Setup/beam_pump_LD/associated_source'] = '/entry/instrument_TA_Setup/source_AOT'
        # for our app: make cases 1- TOPAS 2- AOT
f['/entry/instrument_TA_Setup/beam_pump_LD/beam_polarization_type'] = 'linear'
f['/entry/instrument_TA_Setup/beam_pump_LD/linear_beam_sample_polarization'] = 54.7356
        # check
        # ultimately it would be better to define a coordinate system and use the
        # incident polarization instead
f['/entry/instrument_TA_Setup/beam_pump_LD/linear_beam_sample_polarization'].attrs['units'] = 'deg'
f['/entry/instrument_TA_Setup/beam_pump_LD/linear_beam_sample_polarization'].attrs['unit'] = 'NX_ANGLE'


# NXdetector entry
f.create_group('/entry/instrument_TA_Setup/detector_BroadBand')
f['/entry/instrument_TA_Setup/detector_BroadBand'].attrs['NX_class'] = 'NXdetector'
f['/entry/instrument_TA_Setup/detector_BroadBand/detector_channel_type'] = 'multichannel'
f['/entry/instrument_TA_Setup/detector_BroadBand/detector_number'] = 512
f['/entry/instrument_TA_Setup/detector_BroadBand/detector_type'] = 'Photodiode'

f.create_group('/entry/instrument_TA_Setup/detector_BroadBand/device_information')
f['/entry/instrument_TA_Setup/detector_BroadBand/device_information'].attrs['NX_class'] = 'NXfabrication'
f['/entry/instrument_TA_Setup/detector_BroadBand/device_information/vendor'] = 'Hamamatsu'
f['/entry/instrument_TA_Setup/detector_BroadBand/device_information/model'] = '512-pixel CMOS linear image sensor Hamamatsu G11608-512A'

f['/entry/instrument_TA_Setup/detector_BroadBand/additional_detector_hardware'] ='Custom made prism spectrograph from Entwicklungsbuero Stresing'
# # oh Actually there is a MONOCHROMATOR entry -> go to there
f['/entry/instrument_TA_Setup/detector_BroadBand/associated_beam'] = '/entry/instrument_TA_Setup/beam_Probe'
# #   Could be good to add raw_data 

# NXsource entry
f.create_group('/entry/instrument_TA_Setup/source_Legend')
f['/entry/instrument_TA_Setup/source_Legend'].attrs['NX_class'] = 'NXsource'
f['/entry/instrument_TA_Setup/source_Legend/type'] = 'laser'
f['/entry/instrument_TA_Setup/source_Legend/name'] = 'Coherent LEGEND DUO'
f['/entry/instrument_TA_Setup/source_Legend/type_other'] = 'titanium:sapphire amplifier'
# not clear to me what standard means. that's my interpretation of it
f['/entry/instrument_TA_Setup/source_Legend/wavelength'] = 800
f['/entry/instrument_TA_Setup/source_Legend/wavelength'].attrs['units'] = 'nm'
f['/entry/instrument_TA_Setup/source_Legend/wavelength'].attrs['unit'] = 'NX_WAVELENGTH'
f['/entry/instrument_TA_Setup/source_Legend/pulse_energy'] = 4.5
f['/entry/instrument_TA_Setup/source_Legend/pulse_energy'].attrs['units'] = 'mJ'
f['/entry/instrument_TA_Setup/source_Legend/pulse_energy'].attrs['unit'] = 'NX_ENERGY'
f['/entry/instrument_TA_Setup/source_Legend/pulse_width'] = 100
f['/entry/instrument_TA_Setup/source_Legend/pulse_width'].attrs['units'] = 'fs'
f['/entry/instrument_TA_Setup/source_Legend/pulse_energy'].attrs['unit'] = 'NX_TIME'
f['/entry/instrument_TA_Setup/source_Legend/frequency'] = 3
f['/entry/instrument_TA_Setup/source_Legend/frequency'].attrs['units'] = 'kHz'
f['/entry/instrument_TA_Setup/source_Legend/frequency'].attrs['unit'] = 'NX_FREQUENCY'
# Maybe need to add a beam splitter there and what energy goes on each path?
# todo
# Should I mention the frequency on the other places too? (other beams, detection, etc)
f['/entry/instrument_TA_Setup/source_Legend/associated_beam1'] = '/entry/instrument_TA_Setup/beam_Pump'
f['/entry/instrument_TA_Setup/source_Legend/associated_beam2'] = '/entry/instrument_TA_Setup/beam_Probe'

# NXsource entry : 
    # todo
f.create_group('/entry/instrument_TA_Setup/source_TOPAS')
f['/entry/instrument_TA_Setup/source_TOPAS'].attrs['NX_class'] = 'NXsource'
f['/entry/instrument_TA_Setup/source_TOPAS/type'] = 'other'
f['/entry/instrument_TA_Setup/source_TOPAS/type_other'] = 'Optical Parametric Amplifier'
# that defintely going to have to make its way to the main list for the standard definition
f['/entry/instrument_TA_Setup/source_TOPAS/name'] = 'Light Conversion TOPAS Prime'
f['/entry/instrument_TA_Setup/source_TOPAS/local_identifier'] = 'T2220'
f['/entry/instrument_TA_Setup/source_Legend/wavelength'] = 730
f['/entry/instrument_TA_Setup/source_Legend/wavelength'].attrs['units'] = 'nm'
f['/entry/instrument_TA_Setup/source_Legend/wavelength'].attrs['unit'] = 'NX_WAVELENGTH'
f['/entry/instrument_TA_Setup/source_Legend/pulse_energy'] = None
f['/entry/instrument_TA_Setup/source_Legend/pulse_energy'].attrs['units'] = 'mJ'
f['/entry/instrument_TA_Setup/source_Legend/pulse_energy'].attrs['unit'] = 'NX_ENERGY'

f['/entry/instrument_TA_Setup/source_TOPAS/associated_beam'] = '/entry/instrument_TA_Setup/beam_Pump'
f['/entry/instrument_TA_Setup/source_TOPAS/previous_source'] = '/entry/instrument_TA_Setup/source_Legend'


# NXsource entry
    # todo
f.create_group('/entry/instrument_TA_Setup/source_WL_crystal')
f['/entry/instrument_TA_Setup/source_WL_crystal'].attrs['NX_class'] = 'NXsource'
f['/entry/instrument_TA_Setup/source_WL_crystal/type'] = 'other'
f['/entry/instrument_TA_Setup/source_WL_crystal/type_other'] = 'Supercontinuum generation crystal'
f['/entry/instrument_TA_Setup/source_WL_crystal/standard'] = 'Sapphire 3mm C-cut'
#check for the C-cut
f['/entry/instrument_TA_Setup/source_WL_crystal/wavelength'] = 1150
f['/entry/instrument_TA_Setup/source_WL_crystal/wavelength'].attrs['units'] = 'nm'
f['/entry/instrument_TA_Setup/source_WL_crystal/wavelength'].attrs['unit'] = 'NX_WAVELENGTH'
f['/entry/instrument_TA_Setup/source_WL_crystal/wavelength_spread'] = 575
f['/entry/instrument_TA_Setup/source_WL_crystal/wavelength_spread'].attrs['units'] = 'nm'
f['/entry/instrument_TA_Setup/source_WL_crystal/wavelength_spread'].attrs['unit'] = 'NX_WAVELENGTH'

f['/entry/instrument_TA_Setup/source_WL_crystal/associated_beam'] = '/entry/instrument_TA_Setup/beam_Probe'
f['/entry/instrument_TA_Setup/source_WL_crystal/previous_source'] = '/entry/instrument_TA_Setup/source_Legend'




#NXmonochromator
    #done(?)
f.create_group('/entry/instrument_TA_Setup/Spectrograph')
f['/entry/instrument_TA_Setup/Spectrograph'].attrs['NX_class'] = 'NXmonochromator'

f.create_group('/entry/instrument_TA_Setup/Spectrograph/device_information')
f['/entry/instrument_TA_Setup/Spectrograph/device_information'].attrs['NX_class'] = 'NXfabrication'
f['/entry/instrument_TA_Setup/Spectrograph/device_information/vendor'] = 'Entwicklungsbuero Stresing'
f['/entry/instrument_TA_Setup/Spectrograph/device_information/model'] = 'Custom made prism spectrograph'



# NXsample entry
    #todo
f.create_group('/entry/sample')
f['/entry/sample'].attrs['NX_class'] = 'NXsample'
f['/entry/sample/sample_name'] = 'arbitrary sample name'

#### DATA part todo

f.create_group('/entry/TAsignal_DeltaT_T')
f['/entry/TAsignal_DeltaT_T'].attrs['NX_class'] = 'NXdata'
f['/entry/TAsignal_DeltaT_T'].attrs['axes'] = ['Probe_Energy','Delays']
f['/entry/TAsignal_DeltaT_T'].attrs['signal'] = 'Signal'
f['/entry/TAsignal_DeltaT_T'].attrs['Probe_Energy_indices']=0
f['/entry/TAsignal_DeltaT_T'].attrs['Delays_indices']=1


Energies = np.loadtxt('AS228A_SD730nm_11uW_delta_T.txt')[1:,0]
time_delays = np.loadtxt('AS228A_SD730nm_11uW_delta_T.txt')[0,1:]
DeltaT_T= np.loadtxt('AS228A_SD730nm_11uW_delta_T.txt')[1:,1:]

f['/entry/TAsignal_DeltaT_T/Probe_Energy'] = Energies
f['/entry/TAsignal_DeltaT_T/Probe_Energy'].attrs['long_name'] = 'Probe photon energy'
f['/entry/TAsignal_DeltaT_T/Probe_Energy'].attrs['units'] = 'eV'
f['/entry/TAsignal_DeltaT_T/Probe_Energy'].attrs['unit'] = 'NX_ENERGY'
# not sure (at all) that this is the right syntax
# Solved -> from MArkus Kuehbach: in Nexus "units' is the unit and 'unit' is the type of unit
f['/entry/TAsignal_DeltaT_T/Delays'] = time_delays
f['/entry/TAsignal_DeltaT_T/Delays'].attrs['long_name'] = 'Pump-probe delay'
f['/entry/TAsignal_DeltaT_T/Delays'].attrs['units'] = 'ps'
f['/entry/TAsignal_DeltaT_T/Delays'].attrs['unit'] = 'NX_TIME'

f['/entry/TAsignal_DeltaT_T/Signal'] = DeltaT_T
f['/entry/TAsignal_DeltaT_T/Signal'].attrs['long_name'] = '\u0394T/T'


# X = np.linspace(0,10, 201)
# Y = np.linspace(0,4, 201)
# XX, YY = np.meshgrid(X, Y)
# xx_yy_coordinates = np.stack((XX, YY), axis=0)
# Z = np.sin(XX * YY)


# f.create_group('/entry/dataset_example')
# f['/entry/dataset_example'].attrs['NX_class'] = 'NXdata'
# f['/entry/dataset_example'].attrs['signal'] = 'z'
# f['/entry/dataset_example'].attrs['axes'] = 'xy'

# f['/entry/dataset_example/x'] = X
# f['/entry/dataset_example/y'] = Y
# f['/entry/dataset_example/xy'] = xx_yy_coordinates
# f['/entry/dataset_example/z'] = [Z]