import os
import shutil

INDIR_BASE = './data/roboflow'
LABELS_OUTDIR = './data/labels' 
IMG_OUTDIR = './data/images' 

TRAIN_FILE = 'data/train.txt'
VALID_FILE = 'data/valid.txt'
LABELS_FILE = 'data/duckpuc.names'
CONFIG_FILE = 'data/duckpuc.data'

# Converts the Roboflow Yolo Darknet structure to a structure 
# That works for this project
def handle_roboflow_folder(indir):
    files = os.listdir(indir + '/.')
    labels_file = open(os.path.join(indir, "_darknet.labels"), "r")
    labels = labels_file.readlines()

    box_files = [f for f in files if f.endswith('.txt')]
    images = [f for f in files if f.endswith('.jpg')]

    for txt in box_files:
        shutil.copyfile(os.path.join(indir, txt), os.path.join(LABELS_OUTDIR, txt))

    for img in images:
        shutil.copyfile(os.path.join(indir, img), os.path.join(IMG_OUTDIR, img))

    return images, labels

        
test_images, _ = handle_roboflow_folder(os.path.join(INDIR_BASE, 'test'))
valid_images, _ = handle_roboflow_folder(os.path.join(INDIR_BASE, 'valid'))
train_images, labels = handle_roboflow_folder(os.path.join(INDIR_BASE, 'train'))

# merge test and validation images
test_data = valid_images + test_images
train_data = train_images

print('test:',len(test_data), 'train:', len(train_data))

# Update training data
ftrain_w = open(TRAIN_FILE, 'w+')
for i in train_data:
    ftrain_w.write('./images/'+i+'\n')
ftrain_w.close()

# Update validation data
fvalid_w = open(VALID_FILE, 'w+')
for i in test_data:
    fvalid_w.write('./images/'+i+'\n')
fvalid_w.close()

# Update labels
flabels_w = open(LABELS_FILE, 'w+')
flabels_w.writelines(labels)
flabels_w.close()

# Update config
flabels_w = open(CONFIG_FILE, 'w+')
flabels_w.write('classes={}\n'.format(len(labels)))
flabels_w.write('train={}\n'.format(TRAIN_FILE))
flabels_w.write('valid={}\n'.format(VALID_FILE))
flabels_w.write('names={}'.format(LABELS_FILE))
flabels_w.close()

