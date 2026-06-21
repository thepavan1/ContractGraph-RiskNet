import torch
import torch.nn as nn

class ContractGraphRiskNet(nn.Module):
    """
    PyTorch Model for Contract Risk Prediction.
    Architecture:
    - Input Layer: 15 features (3 project + 8 KG + 4 semantic)
    - Project Encoder: Linear(15, 32) -> ReLU -> BatchNorm -> Dropout(0.3)
    - Risk Reasoner: Linear(32, 16) -> ReLU -> BatchNorm -> Dropout(0.3)
    - Classifier: Linear(16, 1) -> Sigmoid
    """
    def __init__(self, input_dim=15):
        super(ContractGraphRiskNet, self).__init__()
        
        # Project Encoder Layer
        self.project_encoder = nn.Sequential(
            nn.Linear(input_dim, 32),
            nn.ReLU(),
            nn.Dropout(0.3)
        )
        
        # Risk Reasoner Layer
        self.risk_reasoner = nn.Sequential(
            nn.Linear(32, 16),
            nn.ReLU(),
            nn.Dropout(0.3)
        )
        
        # Final Classifier
        self.classifier = nn.Sequential(
            nn.Linear(16, 1),
            nn.Sigmoid()
        )

    def forward(self, x):
        # Forward pass through the network
        encoded = self.project_encoder(x)
        reasoned = self.risk_reasoner(encoded)
        risk_prob = self.classifier(reasoned)
        return risk_prob
