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


OPTS['results_save_path'] = "output/masks/"
OPTS['models_save_path_1'] = 'metadata/weights/linknet/'
OPTS['models_save_path_2'] = 'metadata/weights/unet/'
OPTS['pretrained_model_1'] = 'efficientnetb1'
OPTS['pretrained_model_2'] = 'efficientnetb2'
