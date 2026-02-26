import torch.nn as nn
import torch
import torchvision.transforms.v2 as T



class Model(nn.Module):
    
    def __init__(self, in_channels=1, num_classes=3, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Encoder - feature extraction
        self.conv1 = nn.Sequential(
            nn.Conv2d(in_channels, 32, kernel_size=3, padding=1),
            nn.BatchNorm2d(32),
            nn.ReLU(inplace=True),
            nn.Conv2d(32, 32, kernel_size=3, padding=1),
            nn.BatchNorm2d(32),
            nn.ReLU(inplace=True)
        )
        
        self.conv2 = nn.Sequential(
            nn.Conv2d(32, 64, kernel_size=3, stride=2, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(inplace=True),
            nn.Conv2d(64, 64, kernel_size=3, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(inplace=True)
        )
        
        self.conv3 = nn.Sequential(
            nn.Conv2d(64, 128, kernel_size=3, stride=2, padding=1),
            nn.BatchNorm2d(128),
            nn.ReLU(inplace=True),
            nn.Conv2d(128, 128, kernel_size=3, padding=1),
            nn.BatchNorm2d(128),
            nn.ReLU(inplace=True)
        )
        
        self.conv4 = nn.Sequential(
            nn.Conv2d(128, 256, kernel_size=3, stride=2, padding=1),
            nn.BatchNorm2d(256),
            nn.ReLU(inplace=True),
            nn.Conv2d(256, 256, kernel_size=3, padding=1),
            nn.BatchNorm2d(256),
            nn.ReLU(inplace=True)
        )
        
        # Decoder - upsampling back to original resolution
        self.upconv3 = nn.Sequential(
            nn.ConvTranspose2d(256, 128, kernel_size=2, stride=2),
            nn.BatchNorm2d(128),
            nn.ReLU(inplace=True)
        )
        
        self.dec3 = nn.Sequential(
            nn.Conv2d(256, 128, kernel_size=3, padding=1),  # 256 because of skip connection
            nn.BatchNorm2d(128),
            nn.ReLU(inplace=True),
            nn.Conv2d(128, 128, kernel_size=3, padding=1),
            nn.BatchNorm2d(128),
            nn.ReLU(inplace=True)
        )
        
        self.upconv2 = nn.Sequential(
            nn.ConvTranspose2d(128, 64, kernel_size=2, stride=2),
            nn.BatchNorm2d(64),
            nn.ReLU(inplace=True)
        )
        
        self.dec2 = nn.Sequential(
            nn.Conv2d(128, 64, kernel_size=3, padding=1),  # 128 because of skip connection
            nn.BatchNorm2d(64),
            nn.ReLU(inplace=True),
            nn.Conv2d(64, 64, kernel_size=3, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(inplace=True)
        )
        
        self.upconv1 = nn.Sequential(
            nn.ConvTranspose2d(64, 32, kernel_size=2, stride=2),
            nn.BatchNorm2d(32),
            nn.ReLU(inplace=True)
        )
        
        self.dec1 = nn.Sequential(
            nn.Conv2d(64, 32, kernel_size=3, padding=1),  # 64 because of skip connection
            nn.BatchNorm2d(32),
            nn.ReLU(inplace=True),
            nn.Conv2d(32, 32, kernel_size=3, padding=1),
            nn.BatchNorm2d(32),
            nn.ReLU(inplace=True)
        )
        
        # Output head - fully convolutional
        # Class prediction: num_classes per spatial location
        self.class_head = nn.Conv2d(32, num_classes, kernel_size=1)
        
        # Adaptive pooling to fixed grid size (3 rows x 3 columns)
        self.grid_pool = nn.AdaptiveAvgPool2d((3, 3))
    
    def forward(self, x):
        # Encoder
        enc1 = self.conv1(x)      # Full resolution
        enc2 = self.conv2(enc1)   # 1/2 resolution
        enc3 = self.conv3(enc2)   # 1/4 resolution
        enc4 = self.conv4(enc3)   # 1/8 resolution
        
        # Decoder with skip connections
        dec3 = self.upconv3(enc4)
        # Handle size mismatch with padding
        if dec3.shape[2:] != enc3.shape[2:]:
            dec3 = nn.functional.pad(dec3, [0, enc3.shape[3] - dec3.shape[3], 0, enc3.shape[2] - dec3.shape[2]])
        dec3 = torch.cat([dec3, enc3], dim=1)  # Skip connection
        dec3 = self.dec3(dec3)
        
        dec2 = self.upconv2(dec3)
        if dec2.shape[2:] != enc2.shape[2:]:
            dec2 = nn.functional.pad(dec2, [0, enc2.shape[3] - dec2.shape[3], 0, enc2.shape[2] - dec2.shape[2]])
        dec2 = torch.cat([dec2, enc2], dim=1)  # Skip connection
        dec2 = self.dec2(dec2)
        
        dec1 = self.upconv1(dec2)
        if dec1.shape[2:] != enc1.shape[2:]:
            dec1 = nn.functional.pad(dec1, [0, enc1.shape[3] - dec1.shape[3], 0, enc1.shape[2] - dec1.shape[2]])
        dec1 = torch.cat([dec1, enc1], dim=1)  # Skip connection
        dec1 = self.dec1(dec1)
        
        # Output prediction
        class_pred = self.class_head(dec1)  # Shape: (B, num_classes, H, W)
        
        # Pool to Connect 4 grid dimensions
        class_pred = self.grid_pool(class_pred)  # Shape: (B, 3, 6, 7)
        
        return class_pred
        

# Define transforms
transform = T.Compose([
    T.Resize((192, 224)),  # height, width
    T.ToTensor(),
    T.Normalize(mean=[0.5], std=[0.5])
])