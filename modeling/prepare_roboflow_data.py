import os
import shutil
import xml.etree.ElementTree as ET

indir_base = './data/roboflow' # input folder
xml_outdir = './data/labels'  #txt folder
img_outdir = './data/images'  # image folder

# Converts the structure of roboflow label xmls in a given folder
# and copies corresponding image to the image folder.
# Returns a list of processed image names
def handle_roboflow_folder(indir):
    files = os.listdir(indir + '/.')
    xmls = [f for f in files if f.endswith('.xml')]
    images = [f for f in files if f.endswith('.jpg')]
    for xml in xmls: 
        txt_file_name = xml.replace('.xml', '.txt')
        output_txt_file_path = os.path.join(xml_outdir, txt_file_name)
        file_handle = open(output_txt_file_path, 'w+')

        # actual parsing
        xml_path = os.path.join(indir, xml)
        print("opening", xml_path)
        in_file = open(xml_path)
        tree = ET.parse(in_file)
        root = tree.getroot()
        
        # Get the image size
        img_size = root.find('size')
        image_width = int(img_size.find('width').text)
        image_height = int(img_size.find('height').text)

        info = get_info_from_xml(root, image_width, image_height)
        for inf in info:
            file_handle.write(' '.join(inf) + '\n')

    for img in images:
        shutil.copyfile(os.path.join(indir, img), os.path.join(img_outdir, img))

    return images

def get_info_from_xml(root, image_width, image_height):
    result = []
    for obj in root.iter('object'):
        name = obj.find('name').text   #get the class name then transfer to number
        if name == 'dick':
            class_number = '0'
        elif name == 'dick-head':
            class_number = '1'
        else: 
            class_number = '2' #wrong class
            print("unknown class") # if return any wrong class, get correct it

        xmlbox = obj.find('bndbox')
        xmin = int(xmlbox.find('xmin').text)
        xmax = int(xmlbox.find('xmax').text)
        ymin = int(xmlbox.find('ymin').text)
        ymax = int(xmlbox.find('ymax').text)
        
        x_center = str((xmin + xmax) / 2 / image_width)
        y_center = str((ymin + ymax) / 2 / image_height)
        width = str((xmax - xmin) / image_width)
        height = str((ymax - ymin) / image_height)

        result.append([
            class_number,
            x_center, 
            y_center, 
            width,
            height
        ])
    
    return result
        
test_images = handle_roboflow_folder(os.path.join(indir_base, 'test'))
valid_images = handle_roboflow_folder(os.path.join(indir_base, 'valid'))
train_images = handle_roboflow_folder(os.path.join(indir_base, 'train'))

# merge test and validation images
test_data = valid_images + test_images
train_data = train_images

print('test:',len(test_data), 'train:', len(train_data))

f_w = open('./data/train.txt', 'w+')
for i in train_data:
    f_w.write('./images/'+i+'\n')
f_w.close()

f_w = open('./data/valid.txt', 'w+')
for i in test_data:
    f_w.write('./images/'+i+'\n')
f_w.close()

