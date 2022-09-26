# DickDetector: Real-time In-browser Dick Detection

### TL;DR 

This model is used by [duckpuc.com](https://duckpuc.com) to detect dicks on an edge device and apply amusing filters to them.
The trained model can be downloaded in [PyTorch](https://github.com/lizozom/dick-detector-model/blob/master/modeling/weights/best.pt) or [Darknet](https://github.com/lizozom/dick-detector-model/blob/master/modeling/weights/best.weights) formats. You can learn more on how to integrate it with a ncnn+wasm app in the [dick-detection-app](https://github.com/lizozom/dick-detection-app).


## Requirements

Please use Python 3.8 with all [requirements.txt](https://github.com/ultralytics/yolov3/blob/master/requirements.txt) dependencies installed, including `torch>=1.6`. Do not use python 3.9.

```bash
$ pip install -r requirements.txt
```

## Modeling 

### Building the dataset using Roboflow
The data for this model was created and labeled using [`roboflow`](https://roboflow.com/), a platform used for training of computer vision models. If you want to explore the data used to train this model (beware, adult content), please download it from [here](https://github.com/lizozom/dick-detector-model/blob/master/misc/duckpuc_pub.v7i.darknet.zip).

If you want to create your own data set, you can use `roboflow` to create a new `Image Dataset`.
To use it in this project, use the `Export > YOLO Darknet` format, download the `zip` file and extract it into the `modeling\data\roboflow` folder.

![roboflow-export.png](https://github.com/lizozom/dick-detector-model/blob/master/misc/roboflow-export.png)

The file structure needs to be slightly adjusted to be used by this model. Do so by running:

```
$ cd modeling
$ python prepare_roboflow_data.py
```

This will populate the `modeling/data/images` and `modeling/data/labels` folders.
It will also update the content `modeling.names` and `modeling.names` files.

> :heavy_check_mark: **Check**
> 
> By the end of this step you should have images and labels in `modeling/data/images` and `modeling/data/labels` respectivey.
> You should also have the configurations in `modeling.names` and `modeling.names` updated according to your model.

### Training

Run this code to train the model based on the pretrained weights **yolo-fastest.weights** from COCO.

```bash
$ python3 train.py --cfg yolo-fastest.cfg --data data/modeling.data --weights weights/yolo-fastest.weights --epochs 120
```
The training process would cost several hours. When the training ended, you can use the following script to get the training graphs.

```bash
$ python3  -c "from utils import utils; utils.plot_results()"
```

<img src="https://github.com/lizozom/dick-detector-model/blob/master/modeling/results.png" width="900">

At this stage, the model weights file [best.pt](https://github.com/waittim/mask-detector/blob/master/modeling/weights/best.pt) is stored in `PyTorch` format.

If you want to use the model with the ncnn+wasm app, you need to first convert them to `Darknet` format by running: 

```bash
$ python3  -c "from models import *; convert('cfg/yolo-fastest.cfg', 'weights/best.pt')"
```

> :heavy_check_mark: **Check**
> 
> By the end of this step you should have a file named `best.weights` in the `modeling\weights` directory.

### Inference 
With the model you got, the inference could be performed directly in this format: `python3 detect.py --source ...` For instance, if you want to use your webcam, please run `python3 detect.py --source 0`.

## Deployment

The deployment part works based on NCNN and WASM.

### 1. Pytorch to NCNN
At first, you need to compile the NCNN library. For more details, use the [tutorial for compiling NCNN library
](https://waittim.github.io/2020/11/10/build-ncnn/) by @waittim.

When the compilation process of NCNN has been completed, you can start to use various tools in the **ncnn/build/tools** folder to help us convert the model. 

For example, you can copy the **yolo-fastest.cfg** and **best.weights** files of the darknet model to the **ncnn/build/tools/darknet**, and use this code to convert to the NCNN model.

```bash
./darknet2ncnn yolo-fastest.cfg best.weights yolo-fastest.param yolo-fastest.bin 1
```

For compacting the model size, you can move the **yolo-fastest.param** and **yolo-fastest.bin** to **ncnn/build/tools**, then run the ncnnoptimize program.

```bash
./ncnnoptimize yolo-fastest.param yolo-fastest.bin yolo-fastest-opt.param yolo-fastest-opt.bin 65536 
```

> :heavy_check_mark: **Check**
> 
> By the end of this step you should have two files named `yolo-fastest-opt.bin` and `yolo-fastest-opt.param` in your `ncnn\build\tools\` directory.

### 2. NCNN to WASM

Now you have the **yolo-fastest-opt.param** and **yolo-fastest-opt.bin** as our final model. 
Please continue the deployment as documented in the [dick-detection-app](https://github.com/lizozom/dick-detection-app) repository.

## Acknowledgement

The modeling part is modified based on the code from [waittim](https://github.com/waittim/mask-detector) which is in turn based on  [Ultralytics](https://github.com/ultralytics/yolov3). The model used is modified from the [Yolo-Fastest](https://github.com/dog-qiuqiu/Yolo-Fastest) model shared by @dog-qiuqiu. 





