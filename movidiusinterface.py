#! /usr/bin/env python3
# ! -*- coding:utf-8 -*-

# Python script to open and close a single NCS device API v2
from mvnc import mvncapi


# main entry point for the program
class MovidiusInterface(object):
    def __init__(self):
        # set the logging level for the NC API
        mvncapi.global_set_option(mvncapi.GlobalOption.RW_LOG_LEVEL, mvncapi.LogLevel.WARN)
        # get a list of names for all the devices plugged into the system
        device_list = mvncapi.enumerate_devices()
        if not device_list:
            raise Exception("Error - No neural compute devices detected.")

        else:
            print(len(device_list), "neural compute devices found!")

        # Get a list of valid device identifiers
        device_list = mvncapi.enumerate_devices()
        # Create a Device instance for the first device found
        self._device = mvncapi.Device(device_list[0])
        # Open communication with the device
        # try to open the device.  this will throw an exception if someone else
        # has it open already
        try:
            self._device.open()
            print("Hello NCS! Device opened normally.")
        except Exception:
            raise Exception("Error - Could not open NCS device.")

    def __del__(self):
        pass


class GraphNeuralNetwork(MovidiusInterface):
    __fifo_in = None
    __fifo_out = None
    graph = None

    def __init__(self):
        super(GraphNeuralNetwork, self).__init__()

    def __str__(self):
        return "GraphNeuralNetwork"

    def load_graph(self):
        """
        Load a graph file onto the NCS device
        :return:
        """
        # Read the graph file into a buffer
        with open(ARGS.graph, mode='rb') as f:
            blob = f.read()
        # Load the graph buffer into the NCS
        self.graph = mvnc.Graph(ARGS.graph)
        # Set up fifos
        self.__fifo_in, self.__fifo_out = self.graph.allocate_with_fifos(self._device, blob)

    # ---- Step 3: Pre-process the images ----------------------------------------

    # def pre_process_image():
    #
    #     # Read & resize image [Image size is defined during training]
    #     img = skimage.io.imread( ARGS.image )
    #     img = skimage.transform.resize( img, ARGS.dim, preserve_range=True )
    #
    #     # Convert RGB to BGR [skimage reads image in RGB, but Caffe uses BGR]
    #     if( ARGS.colormode == "BGR" ):
    #         img = img[:, :, ::-1]
    #
    #     # Mean subtraction & scaling [A common technique used to center the data]
    #     img = ( img - ARGS.mean ) * ARGS.scale
    #
    #     return img

    # ---- Step 4: Read & print inference results from the NCS -------------------

    def infer_image(self, img):
        """
        Read & print inference results from the NCS
        :param img:
        """
        # Load the labels file
        labels = [line.rstrip('\n') for line in open(ARGS.labels) if line != 'classes\n']

        # The first inference takes an additional ~20ms due to memory
        # initializations, so we make a 'dummy forward pass'.
        self.graph.queue_inference_with_fifo_elem(self.__fifo_in,
                                                  self.__fifo_out,
                                                  img.astype(numpy.float32),
                                                  None)
        output, userobj = self.__fifo_out.read_elem()

        # Load the image as an array
        self.graph.queue_inference_with_fifo_elem(self.__fifo_in,
                                                  self.__fifo_out,
                                                  img.astype(numpy.float32),
                                                  None)
        # Get the results from NCS
        output, userobj = self.__fifo_out.read_elem()
        # Sort the indices of top predictions
        order = output.argsort()[::-1][:NUM_PREDICTIONS]
        # Get execution time
        inference_time = self.graph.get_option(mvnc.GraphOption.RO_TIME_TAKEN)

        # Print the results
        print("\n==============================================================")
        print("Top predictions for", ntpath.basename(ARGS.image))
        print("Execution time: " + str(numpy.sum(inference_time)) + "ms")
        print("--------------------------------------------------------------")
        for i in range(0, NUM_PREDICTIONS):
            print("%3.1f%%\t" % (100.0 * output[order[i]]) + labels[order[i]])
        print("==============================================================")

        # If a display is available, show the image on which inference was performed
        if 'DISPLAY' in os.environ:
            skimage.io.imshow(ARGS.image)
        skimage.io.show()

    def __del__(self):
        """
        Close and clean up fifos, graph
        :param self:
        """
        if self.__fifo_in is not None:
            self.__fifo_in.destroy()
        if self.__fifo_out is not None:
            self.__fifo_out.destroy()
        if self.graph is not None:
            self.graph.destroy()
        # Close the device and destroy the device handle
        try:
            self._device.close()
            self._device.destroy()
            print("Goodbye NCS! Device closed normally.")
            print("NCS device working.")
        except:
            raise Exception("Error - could not close NCS device.")


a = GraphNeuralNetwork()