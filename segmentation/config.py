SEED = 42
PATH = "output/segmentation/"

OPTS = {}
OPTS['resource'] = 'cpu'
OPTS['tf_version'] = 2
OPTS['gpu_num'] = '0'
OPTS['img_type'] = '.jpg'
OPTS['number_of_channel'] = 3
OPTS['treshold'] = 0.5
OPTS['k_fold'] = 5

# paths
# aqui pones el directorio donde estan las img
OPTS['test_dir'] = PATH + '/'
OPTS['results_save_path'] = PATH + 'results/'
OPTS['models_save_path_1'] = PATH + 'net-weights/linknet/'
OPTS['models_save_path_2'] = PATH + 'net-weights/unet/'
OPTS['results_save_path_final'] = PATH + \
    'results/final/'  # aqui salen las mascaras
OPTS['pretrained_model_1'] = 'efficientnetb1'
OPTS['pretrained_model_2'] = 'efficientnetb2'
OPTS['use_pretrained_flag'] = 1

OPTS['save_figures'] = 1
