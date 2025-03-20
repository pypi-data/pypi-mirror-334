import recovar.config
from importlib import reload
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objs as go
import plotly.offline as py
from recovar.fourier_transform_utils import fourier_transform_utils
import jax.numpy as jnp
ftu = fourier_transform_utils(jnp)
from recovar import image_assignment, noise
from sklearn.metrics import confusion_matrix
from recovar import simulate_scattering_potential as ssp
from recovar import simulator, utils, image_assignment, noise, output, dataset
import prody
reload(simulator)

def main():
    ## CHANGE THESE FOLDERS
    output_folder = '/home/mg6942/mytigress/hard_assignment_exp/'
    pdb_folder = './'

    # Some parameters to set
    n_images = 100000
    grid_size = 256
    Bfactor = 60 
    noise_level_tests = np.logspace(1,6,20) # these seem reasonble.
    # This would produce 2 million images of size 256x256

    ## Make volumes from PDB
    pdbs = [ '3down_nogly.pdb', 'up_nogly.pdb']

    voxel_size =1.3 * 256 / grid_size
    volume_shape = tuple(3*[grid_size])

    # Center atoms (but shift by same amount)
    pdb_atoms = [ prody.parsePDB(pdb_folder + '/' +  pdb_i) for pdb_i in pdbs ]
    atoms =pdb_atoms[0]
    coords = atoms.getCoords()
    offset = ssp.get_center_coord_offset(coords)
    # coords = coords - offset
    for atoms in pdb_atoms:
        atoms.setCoords(atoms.getCoords() - offset)

        
    ## Make B-factored volumes (will be considered g.t.)     
    Bfaced_vols = len(pdbs)*[None]
    for idx, atoms in enumerate(pdb_atoms):
        volume = ssp.generate_molecule_spectrum_from_pdb_id(atoms, voxel_size = voxel_size,  grid_size = grid_size, do_center_atoms = False, from_atom_group = True)
        Bfaced_vols[idx] = simulator.Bfactorize_vol(volume.reshape(-1), voxel_size, Bfactor, volume_shape)

    disc_type_sim = 'nearest'
    disc_type_infer = 'nearest'
    # disc_type_sim = 'linear_interp'
    # disc_type_infer = 'linear_interp'


    volume_folder = output_folder + 'true_volumes/'
    output.mkdir_safe(volume_folder)
    output.save_volumes( Bfaced_vols, volume_folder, from_ft= True)

    # plt.imshow(ftu.get_idft3(Bfaced_vols[0].reshape(volume_shape)).sum(axis=0).real)
    # plt.figure()
    # plt.imshow(ftu.get_idft3(Bfaced_vols[1].reshape(volume_shape)).sum(axis=0).real)
    

    error_observed = np.zeros(noise_level_tests.size)
    error_predicted= np.zeros(noise_level_tests.size)

    for idx, noise_level in enumerate(noise_level_tests):
        
        # Generate dataset
        volume_distribution = np.array([0.8,0.2])
        noise_level = noise_level
        dataset_folder = output_folder + f'/dataset{idx}/'
        image_stack, sim_info = simulator.generate_synthetic_dataset(dataset_folder, voxel_size, volume_folder, n_images,
            outlier_file_input = None, grid_size = grid_size,
            volume_distribution = volume_distribution,  dataset_params_option = "uniform", noise_level = noise_level,
            noise_model = "white", put_extra_particles = False, percent_outliers = 0.00, 
            volume_radius = 0.7, trailing_zero_format_in_vol_name = True, noise_scale_std = 0, contrast_std = 0, disc_type = disc_type_sim)
        
        volumes = simulator.load_volumes_from_folder(sim_info['volumes_path_root'], sim_info['grid_size'] , sim_info['trailing_zero_format_in_vol_name'], normalize=False )
        gt_volumes = volumes * sim_info['scale_vol']

        
        dataset_options = dataset.get_default_dataset_option()
        dataset_options['particles_file'] = dataset_folder + f'particles.{grid_size}.mrcs'
        dataset_options['ctf_file'] = dataset_folder + f'ctf.pkl'
        dataset_options['poses_file'] = dataset_folder + f'poses.pkl'
        cryo = dataset.load_dataset_from_dict(dataset_options, lazy = False)
        


        # Compute hard-assignment
        batch_size = 1000
        image_cov_noise = np.asarray(noise.make_radial_noise(sim_info['noise_variance'], cryo.image_shape))
        log_likelihoods = image_assignment.compute_image_assignment(cryo, gt_volumes,  image_cov_noise, batch_size, disc_type = disc_type_infer)
        assignments = jnp.argmin(log_likelihoods, axis = 0)
        
        from recovar import synthetic_dataset
        SD = synthetic_dataset.load_heterogeneous_reconstruction(sim_info)
        mean = SD.get_mean()
        gpu_memory = 40

        from recovar import covariance_estimation
        options = covariance_estimation.get_default_covariance_options()
        options["mask_images_in_H_B"] = False
        options["right_kernel"] = False
        options["left_kernel"] = "square"
        options["right_kernel"] = "square"
        options["left_kernel_width"] = 1
        options["right_kernel_width"] = 1
        options["disc_type"] = disc_type_infer
        options["disc_type_u"] = disc_type_infer
        dilated_volume_mask = np.ones_like(mean).real
        import pickle
        picked_frequencies = pickle.load(open('/home/mg6942/mytigress/uniform/newagain/model/params.pkl', 'rb'))['picked_frequencies']
        H, B = covariance_estimation.compute_H_B_in_volume_batch(cryo, mean, dilated_volume_mask, picked_frequencies, gpu_memory, image_cov_noise, False, options = options)

        covariance_cols = SD.get_covariance_columns()
        # # First approximation of eigenvalue decomposition
        # u,s = covariance_estimation.get_cov_svds(covariance_cols, picked_frequencies, volume_mask, volume_shape, vol_batch_size, gpu_memory_to_use, False, covariance_options['randomized_sketch_size'])
        
        # Check for NaN or Inf values in u and s

        # # Let's see?
        # if noise_model == "white":
        #     cov_noise = cov_noise
        # else:
        #     # This probably should be moved into embedding
        # if options['ignore_zero_frequency']:
        #     # Make the noise in 0th frequency gigantic. Effectively, this ignore this frequency when fitting.
        #     logger.info('ignoring zero frequency')
        #     cov_noise[0] *=1e16
        cov_noise = sim_info['noise_variance']
        image_cov_noise = np.asarray(noise.make_radial_noise(cov_noise, cryos[0].image_shape))
        true_covariance_cols = SD.get_covariance_columns(picked_frequencies, contrasted = False )
        variances = SD.get_fourier_variances(contrasted = False)
        variances_squared = variances @ variances[picked_frequencies].T
        regularization = variances_squared / cov_noise[0,0]**2
        covariance_cols = B / ( H + 1/regularization)




        u['rescaled'], s['rescaled'] = covariance_estimation.pca_by_projected_covariance(cryos, u['real'], means['combined'], image_cov_noise, dilated_volume_mask, disc_type = covariance_options['disc_type'], disc_type_u = covariance_options['disc_type_u'], gpu_memory_to_use= gpu_memory_to_use, use_mask = covariance_options['mask_images_in_proj'], parallel_analysis = False ,ignore_zero_frequency = False, n_pcs_to_compute = covariance_options['n_pcs_to_compute'])

        
        # covariance_cols, picked_frequencies, column_fscs = covariance_estimation.compute_regularized_covariance_columns_in_batch(cryos, means, mean_prior, cov_noise, volume_mask, dilated_volume_mask, valid_idx, gpu_memory_to_use, noise_model, covariance_options, picked_frequencies)
