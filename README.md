# DickDetector: Real-time In-browser Dick Detection

### TL;DR 

This model is used by [duckpuc.com](https://duckpuc.com) to detect dicks on an edge device and apply amusing filters to them.
The trained model can be downloaded [here](https://github.com/lizozom/dick-detector-model/blob/master/modeling/weights/best.pt). You can learn more on how to integrate it with a ncnn+WASM app in [this repo]().


## Requirements

Please use Python 3.8 with all [requirements.txt](https://github.com/ultralytics/yolov3/blob/master/requirements.txt) dependencies installed, including `torch>=1.6`. Do not use python 3.9.

```bash
$ pip install -r requirements.txt
```

## Modeling

The data for this model was created and labeled using [`roboflow`](https://roboflow.com/), a platform used for training of computer vision models. If you want to explore the data used to train this model (beware, adult content), please download it from [here]().

If you want to create your own data set, you can use `roboflow` to create a new `Image Dataset`.
To use it in this project, use the `Export > YOLO Darknet` format, download the `zip` file and extract it into the `modeling\data\roboflow` folder.

![roboflow-export.png](https://github.com/lizozom/dick-detector-model/blob/master/img/roboflow-export.png)

The file structure needs to be slightly adjusted to be used by this model. Do so by running:

```
$ cd modeling
$ python prepare_roboflow_data.py
```

This will populate the `modeling/data/images` and `modeling/data/labels` folders.
It will also update the content `modeling.names` and `modeling.names` files.

> **Note**
> At the end of this step you should have a the `modeling/data/images` and `modeling/data/labels` populated with images and `txt` label files.

### Training

Run this code to train the model based on the pretrained weights **yolo-fastest.weights** from COCO.
```bash
$ python3 train.py --cfg yolo-fastest.cfg --data data/modeling.data --weights weights/yolo-fastest.weights --epochs 120
```
The training process would cost several hours. When the training ended, you can use `from utils import utils; utils.plot_results()` to get the training graphs.

<img src="https://github.com/lizozom/dick-detector-model/blob/master/modeling/results.png" width="900">

After training, you can get the model weights [best.pt](https://github.com/waittim/mask-detector/blob/master/modeling/weights/best.pt) with its structure [yolo-fastest.cfg](https://github.com/waittim/mask-detector/blob/master/modeling/cfg/yolo-fastest.cfg). You can also use the following code to get the model weights [best.weights](https://github.com/waittim/mask-detector/blob/master/modeling/weights/best.weights) in Darknet format.

```bash
$ python3  -c "from models import *; convert('cfg/yolo-fastest.cfg', 'weights/best.pt')"
```
### Inference 
With the model you got, the inference could be performed directly in this format: `python3 detect.py --source ...` For instance, if you want to use your webcam, please run `python3 detect.py --source 0`.

## Deployment

If you want to continue and deploy the model to run in a browser, go ahead and checkout the dick-

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
ncnnoptimize yolo-fastest.param yolo-fastest.bin yolo-fastest-opt.param yolo-fastest-opt.bin 65536 
```
### 2. NCNN to WASM

Now you have the **yolo-fastest-opt.param** and **yolo-fastest-opt.bin** as our final model. For making it works in WASM format, you need to re-compile the NCNN library with WASM. you can visit [Tutorial for compiling NCNN with WASM
](https://waittim.github.io/2020/11/15/build-ncnn-wasm/) to find the tutorial. 

Then you need to write a C++ program that calls the NCNN model as input the image data and return the model output. The [C++ code](https://github.com/waittim/facemask-detection/blob/master/yolo.cpp) I used has been uploaded to the [facemask-detection](https://github.com/waittim/facemask-detection) repository. 

Compile the C++ code by `emcmake cmake` and `emmake make`, you can get the **yolo.js**, **yolo.wasm**, **yolo.worker.js** and **yolo.data**. These files are the model in WASM format.

### 3. Build webpage 
After establishing the webpage, you can test it locally with the following steps in the [facemask-detection](https://github.com/waittim/facemask-detection) repository:

1. start a HTTP server `python3 -m http.server 8888`
2. launch google chrome browser, open chrome://flags and enable all experimental webassembly features
3. re-launch google chrome browser, open http://127.0.0.1:8888/test.html, and test it on one frame.
4. re-launch google chrome browser, open http://127.0.0.1:8888/index.html, and test it by webcam.

To publish the webpage, you can use Github Pages as a free server. For more details about it, please visit https://pages.github.com/.


## Acknowledgement

The modeling part is modified based on the code from [waittim](https://github.com/waittim/mask-detector) which is in turn based on  [Ultralytics](https://github.com/ultralytics/yolov3). The model used is modified from the [Yolo-Fastest](https://github.com/dog-qiuqiu/Yolo-Fastest) model shared by dog-qiuqiu. 





