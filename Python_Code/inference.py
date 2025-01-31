import os
import torch
import numpy as np
from PIL import Image
from torch.utils.data import Dataset, DataLoader
import matplotlib.pyplot as plt
import tempfile
import shutil
import torch.nn as nn
from streamlit import session_state as stt

# Device configuration
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Pixel-to-class mapping
pixel_to_class = {0: 0, 70: 1, 162: 2, 213: 3}

# Color map for visualization
color_map = {
    0: [0, 0, 0],        # Black for class 0
    1: [255, 0, 0],      # Red for class 1
    2: [255, 165, 0],    # Yellow for class 2
    3: [255, 255, 0],    # Orange for class 3
}

# Function to map pixel values to class indices
def map_pixel_to_class(image):
    img_array = np.array(image)
    return np.vectorize(lambda x: pixel_to_class.get(x, 0))(img_array)

class ConvLSTM(nn.Module):
    def __init__(self, input_channels=1, hidden_channels=64, kernel_size=3, output_channels=4):
        super(ConvLSTM, self).__init__()

        # ConvLSTM layer for temporal processing
        self.conv_lstm = nn.LSTM(input_size=input_channels, hidden_size=hidden_channels)

        # Convolutional layers for spatial processing
        self.conv1 = nn.Conv2d(input_channels, hidden_channels, kernel_size=kernel_size, padding=1)
        self.bn1 = nn.BatchNorm2d(hidden_channels)
        self.conv2 = nn.Conv2d(hidden_channels, hidden_channels, kernel_size=kernel_size, padding=1)
        self.bn2 = nn.BatchNorm2d(hidden_channels)
        self.conv3 = nn.Conv2d(hidden_channels, output_channels, kernel_size=kernel_size, padding=1)

        # Dropout for regularization
        self.dropout = nn.Dropout(p=0.3)

        # Upsampling layer to resize output to 400x400
        self.upsample = nn.Upsample(size=(400, 400), mode='bilinear', align_corners=False)

        self.relu = nn.ReLU()

    def forward(self, x):
        # x: Shape: [batch_size, seq_len, channels, height, width]
        batch_size, seq_len, channels, height, width = x.size()

        # Initialize hidden state for LSTM
        h_t = torch.zeros(batch_size, channels, height, width).to(x.device)

        # Loop through sequence
        for t in range(seq_len):
            x_t = x[:, t, :, :, :]  # Get the t-th image in the sequence

            # Convolutional block with BatchNorm and Dropout
            x_t = self.relu(self.bn1(self.conv1(x_t)))
            x_t = self.dropout(x_t)
            x_t = self.relu(self.bn2(self.conv2(x_t)))

            # Residual connection to carry forward spatial features
            h_t = h_t + self.conv3(x_t)

        # Upsample to desired output size (400x400)
        h_t = self.upsample(h_t)

        return h_t

class DroughtDataset(Dataset):
    def __init__(self, sequences, folder, resize_size=(256, 256)):
        self.sequences = sequences
        self.folder = folder
        self.resize_size = resize_size

    def __len__(self):
        return len(self.sequences)

    def __getitem__(self, idx):
        # Get the sequence
        input_files = self.sequences[idx]

        # Load and resize the images
        input_images = [Image.open(os.path.join(self.folder, f)).resize(self.resize_size) for f in input_files]

        # Map pixels to class labels
        input_images = [map_pixel_to_class(img) for img in input_images]

        # Add an extra dimension for the channel (1 for grayscale)
        input_images = [np.expand_dims(img, axis=0) for img in input_images]  # Shape: (1, 256, 256) for each image

        # Stack the sequence images
        input_tensor = torch.tensor(np.stack(input_images), dtype=torch.long)  # Shape: (sequence_len, 1, 256, 256)

        return input_tensor

# Function to perform inference and overlay result on base image
def process_masks(mask_paths,date_selected):
    # Create a temporary folder to save mask images
    temp_folder = tempfile.mkdtemp()

    # Copy masks to the temporary folder
    for idx, mask_path in enumerate(mask_paths):
        shutil.copy(mask_path, os.path.join(temp_folder, f"mask_{idx+1}.png"))

    # Create sequences from the two mask files
    sequences = [['mask_1.png', 'mask_2.png']]

    # Create the dataset and DataLoader
    dataset = DroughtDataset(sequences, temp_folder)
    inference_loader = DataLoader(dataset, batch_size=1, shuffle=False)

    # Load the trained model
    # Load model for inference (ensure it loads on CPU if CUDA is not available)
    model = ConvLSTM(input_channels=1, hidden_channels=64, kernel_size=3, output_channels=4)
    model.load_state_dict(torch.load("Trained_Model/trained_model_v5.pth", map_location=torch.device('cpu')))
    model.to(device)
    model.eval()

    # Perform inference
    for inputs in inference_loader:
        # Move inputs to the same device as the model
        inputs = inputs.to(device).float()
        with torch.no_grad():
            predictions = model(inputs)

        # Convert logits to predicted class indices
        predictions = torch.argmax(predictions, dim=1)
        break  # Process one batch for testing

    # Convert predictions to numpy array
    predictions_np = predictions.squeeze(0).cpu().numpy()

    # Map indices to colors for visualization
    segmented_image = np.zeros((*predictions_np.shape, 3), dtype=np.uint8)
    for class_idx, color in color_map.items():
        segmented_image[predictions_np == class_idx] = color

    # Convert the segmented image to a PIL image
    segmented_mask = Image.fromarray(segmented_image, mode="RGB").convert("RGBA")

    # Remove black background by setting it as transparent
    data = segmented_mask.getdata()
    new_data = []
    for item in data:
        if item[:3] == (0, 0, 0):  # Ignore alpha channel
            new_data.append((0, 0, 0, 0))  # Fully transparent
        else:
            new_data.append(item)  # Keep original color

    segmented_mask.putdata(new_data)

    # Load the base image
    base_image = Image.open("assets/BaseMap_Morocco.png").convert("RGBA")

    # Resize mask to match base image size (if needed)
    segmented_mask = segmented_mask.resize(base_image.size, resample=Image.NEAREST)

    # Overlay the mask on the base image
    overlayed_image = Image.alpha_composite(base_image, segmented_mask)

    # Save and display the result
    output_path = f"Inference_results/{date_selected}.png"
    overlayed_image.save(output_path)
    #overlayed_image.show()

    print(f"Overlayed map saved at {output_path}")

    # Clean up the temporary folder
    shutil.rmtree(temp_folder)