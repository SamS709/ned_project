import torch.nn as nn
import torchvision
import torchvision.transforms.v2 as T

class Model(nn.Module):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Encoder - feature extraction
        pretrained = torchvision.models.resnet18(torchvision.models.ResNet18_Weights.IMAGENET1K_V1)
        
        pretrained = list(pretrained.children())
        self.pretrained = nn.Sequential(*pretrained[:-1]) 
        self.output = nn.Linear(512, 3 * 42)
        
        
    
    def forward(self, X):
        X = self.pretrained(X).squeeze(-1).squeeze(-1)
        X = self.output(X)
        return X.view(-1, 3, 6, 7)
        
# Define transforms
transform = T.Compose([
    T.Resize((192, 224)),  # height, width
    T.ToTensor(),
    T.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])
