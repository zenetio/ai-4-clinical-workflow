"""
Contains class that runs inferencing
"""
import torch
import numpy as np

from networks.RecursiveUNet import UNet

from utils.utils import med_reshape

class UNetInferenceAgent:
    """
    Stores model and parameters and some methods to handle inferencing
    """
    def __init__(self, parameter_file_path='', model=None, device="cpu", patch_size=64):

        self.model = model
        self.patch_size = patch_size
        self.device = device

        if model is None:
            self.model = UNet(num_classes=3)

        if parameter_file_path:
            self.model.load_state_dict(torch.load(parameter_file_path, map_location=self.device))

        self.model.to(device)

    def single_volume_inference_unpadded(self, volume):
        """
        Runs inference on a single volume of arbitrary patch size,
        padding it to the conformant size first

        Arguments:
            volume {Numpy array} -- 3D array representing the volume

        Returns:
            3D NumPy array with prediction mask
        """
        
        # normalize the data volume 
        image = (volume.astype(np.single) - np.min(volume))/(np.max(volume) - np.min(volume))
        # reshape the image volume to the same patch size used for training
        img_reshaped = med_reshape(image, new_shape=(self.patch_size, self.patch_size, image.shape[2]))
        # create a new 3d mask to store predicted results
        mask3d = np.zeros(img_reshaped.shape)
        # iterate over the image array and predict the all the slices
        for slc_idx in range(img_reshaped.shape[2]):
            # compute for each slice
            slc = torch.from_numpy(img_reshaped[:,:,slc_idx].astype(np.single)).unsqueeze(0).unsqueeze(0)
            # make prediction
            pred = self.model(slc.to(self.device))
            pred = np.squeeze(pred.cpu().detach())
            # store predicted data
            mask3d[:,:,slc_idx] = torch.argmax(pred, dim=0)
        # return the predicted volume
        return mask3d

    def single_volume_inference(self, volume):
        """
        Runs inference on a single volume of conformant patch size

        Arguments:
            volume {Numpy array} -- 3D array representing the volume

        Returns:
            3D NumPy array with prediction mask
        """
        self.model.eval()

        # Assuming volume is a numpy array of shape [X,Y,Z] and we need to slice X axis
        slices = []

        # Write code that will create mask for each slice across the X (0th) dimension. After 
        # that, put all slices into a 3D Numpy array. You can verify if your method is 
        # correct by running it on one of the volumes in your training set and comparing 
        # with the label in 3D Slicer.
        
        # normalize
        image = (volume.astype(np.single) - np.min(volume))/(np.max(volume) - np.min(volume))
        
        new_image = med_reshape(image, new_shape=(self.patch_size, self.patch_size, image.shape[2]))
        mask3d = np.zeros(new_image.shape)
        
        for slc_ix in range(new_image.shape[2]):
            tsr_test = torch.from_numpy(new_image[:,:,slc_ix].astype(np.single)).unsqueeze(0).unsqueeze(0)
            #image = torch.from_numpy(self.data[slc[0]]["image"][:,:,slc[1]]).unsqueeze(0)
            #tsr_test = torch.from_numpy(slc.astype(np.single)).unsqueeze(0).unsqueeze(0)
            pred = self.model(tsr_test.to(self.device))
            pred = np.squeeze(pred.cpu().detach())
            mask3d[:,:,slc_ix] = torch.argmax(pred, dim=0)

        return  mask3d
