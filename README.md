[![License:MIT](https://img.shields.io/packagist/l/doctrine/orm.svg)](License.md)
![Python](https://img.shields.io/badge/Python-3.5-orange.svg)
# Neural Network

## Embedded System Project

Final project of the Embedded System course based on the realization of a neural network and its implementation on
[Raspberry Pi model 3](https://www.raspberrypi.org/products/raspberry-pi-3-model-b/) and [Intel Movidius](https://software.intel.com/en-us/neural-compute-stick) neural compute stick.

### Prerequisites
minimum version:
+ python 3.5, 3.6 actually 3.7 is not supported:

```
absl-py==0.4.1
astor==0.7.1
cycler==0.10.0
gast==0.2.0
graphviz==0.9
grpcio==1.14.2
h5py==2.8.0
Keras==2.2.2
Keras-Applications==1.0.4
Keras-Preprocessing==1.0.2
kiwisolver==1.0.1
Markdown==2.6.11
matplotlib==2.2.3
numpy==1.14.5
opencv-python==3.4.3.18
pandas==0.23.4
Pillow==5.2.0
protobuf==3.6.1
pydot==1.2.4
pyparsing==2.2.0
PyQt5==5.11.3
PyQt5-sip==4.19.13
python-dateutil==2.7.3
pytz==2018.5
PyYAML==3.13
scikit-learn==0.19.2
scipy==1.1.0
seaborn==0.9.0
selenium==3.14.0
six==1.11.0
sklearn==0.0
tensorboard==1.10.0
tensorflow==1.10.1
termcolor==1.1.0
urllib3==1.23
Werkzeug==0.14.1  
```
The packages needed are enclosed in file “requirements.txt“, to install, type in the terminal:
```shell
pip3 install -r requirements.txt
```
or
```python
K.set_learning_phase(0)
```
otherwise it will not be possible to convert the model into a graph format, as it will be lost in final values in the forecast.

### GPU
There may be memory allocation problems in the GPU, at the moment this solution
is used in the file *face_recognition.py*
```Python
gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=0.8, allow_growth=False)
sess = tf.Session(config=tf.ConfigProto(gpu_options=gpu_options))
```
## Installation
To clone the repository can use the following command
```shell
git clone https://github.com/frank1789/NeuralNetworks.git
```

To run on Host/Guest machine use:
```shell
cd NeuralNetworks
sh test.sh
```
To run on  guest machine with Intel Movidius use:
 ```shell
cd NeuralNetworks
sh test.sh movidius
```

To run on  Raspberry Pi 3 model B with Intel Movidius use:
 ```shell
cd NeuralNetworks
sh test.sh reduced-nocompile
```
remember the neural compute strick must be attached.

## Install virtual envoirments
Since the development kit provided by intel works in Linux Ubuntu environment it is recommended to install and configure a virtual machine:
+ download [VirtualBox](https://www.virtualbox.org/wiki/Downloads) and VirtualBox Extension Pack
+ download image iso Linux [Ubuntu](https://www.ubuntu-it.org/download) 16.04 LTS (higher OS version are not supported by movidius software)

### Installation & configuration

Proceed with the installation of: VirtualBox, extension package, OS.

Once completed, we configure the virtual guest machine as shown in the following pictures.

<div style="text-align:center"><img src ="https://github.com/frank1789/NeuralNetworks/blob/master/img/fig1.png" /></div>
<div style="text-align:center"><img src ="https://github.com/frank1789/NeuralNetworks/blob/master/img/fig2.png" /></div>
<div style="text-align:center"><img src ="https://github.com/frank1789/NeuralNetworks/blob/master/img/fig3.png" /></div>
<div style="text-align:center"><img src ="https://github.com/frank1789/NeuralNetworks/blob/master/img/fig4.png" /></div>
<div style="text-align:center"><img src ="https://github.com/frank1789/NeuralNetworks/blob/master/img/fig5.png" /></div>
<div style="text-align:center"><img src ="https://github.com/frank1789/NeuralNetworks/blob/master/img/fig6.png" /></div>
<div style="text-align:center"><img src ="https://github.com/frank1789/NeuralNetworks/blob/master/img/fig7.png" /></div>

### Install Intel Movidius sdk

##### Allowing GPU memory growth
By default, TensorFlow maps nearly all of the GPU memory of all GPUs (subject to
   CUDA_VISIBLE_DEVICES) visible to the process. This is done to more
   efficiently use the relatively precious GPU memory resources on the devices
   by reducing memory fragmentation.

In some cases it is desirable for the process to only allocate a subset of the
available memory, or to only grow the memory usage as is needed by the process.
TensorFlow provides two Config options on the Session to control this.

The first is the **allow_growth** option, which attempts to allocate only as
much GPU memory based on runtime allocations: it starts out allocating very
little memory, and as Sessions get run and more GPU memory is needed, we extend
the GPU memory region needed by the TensorFlow process. Note that we do not
release memory, since that can lead to even worse memory fragmentation.
To turn this option on, set the option in the ConfigProto by a script optimized
already implemented:
```python
config = tf.ConfigProto()
config.gpu_options.allow_growth = True  # dynamically grow the memory used on the GPU
config.log_device_placement = True      # to log device placement (on which device the operation ran)
config.allow_soft_placement = True      # search automatically free GPU
sess = tf.Session(config=config)
kbe.set_session(sess)                   # set this TensorFlow session as the default session for Keras
```

The Neural Compute SDK also includes examples. After cloning and running 'make install,' run the following command to install the examples:
```shell
make examples
```
## Make dataset & Training Neural Networks
This script allows you to organize a dataset, downloaded from the internet or made in-house, as a structure of folders containing sets for training, validation and testing of the neural network.
<div style="text-align:center"><img src ="https://github.com/frank1789/NeuralNetworks/blob/master/img/structure.png" /></div>

## License

| Argument |  <nobr>Long Description</nobr> | Help |
|:--------:|--------------|--------|
|-d| --dataset |requires path to train folder|
|-v| --validate|requires path to validate folder|
|-e| --epoch   |requires number of epochs, one forward pass and one backward <br>pass of all the training examples|
|-b| --batch   |requires batch size number of samples that will be <br>propagated through the network|
|-n| <nobr>--neuralnetwork</nobr>|requires to specify an existing neural network as <br>VGG, Inception, ResNet, etc|
|-f| --finetuning|requires the percentage of layers to be trained, taking weights <br>of a trained neural network and use it as initialization for a new<br> model being trained on data from the same domain|
|-is| --imagesize|requires to specify the width and height dimensions of the images|

```shell
python3 train.py -d ..data/train -v ../data/validate -e 10 -b 10 -is 224 224 -n vgg16
```
The following neural networks are available within the script
+ VGG16 (lower case for script argument)
+ VGG19 (lower case for script argument)
+ InceptionV3 (aka *'inception'* argument script)
+ Xception (lower case for script argument)
+ ResNet50 (aka *'resnet50'* argument script)

## Convert from Keras model to NCS
Once you have trained  neural network use model file for conversion in graph format to work on Neural Compute Stick, type command:

```shell
python3 keras2ncsgraph.py -k model.h5 -n converted_model
```

## Report
The report is available on this [branch]() and can be downloaded from the command:
```
git clone -b report https://github.com/frank1789/NeuralNetworks.git
```

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Embedded system lab @UNITN
* HPC Cluster | ICTS - University of Trento - ICTS@unitn
