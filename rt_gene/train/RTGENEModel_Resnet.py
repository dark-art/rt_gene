import torch
import torch.nn as nn
from torchvision import models


class RTGENEModelResnet50(nn.Module):

    def __init__(self, num_out=2):  # phi, theta
        super(RTGENEModelResnet50, self).__init__()
        _left_model = models.resnet50(pretrained=True)
        _right_model = models.resnet50(pretrained=True)

        # remove the last ConvBRelu layer
        self.left_features = nn.Sequential(
            *list([_left_model.conv1,
                   _left_model.bn1,
                   _left_model.relu,
                   _left_model.maxpool,
                   _left_model.layer1,
                   _left_model.layer2,
                   _left_model.layer3,
                   _left_model.layer4,
                   _left_model.avgpool])
        )

        self.right_features = nn.Sequential(
            *list([_right_model.conv1,
                   _right_model.bn1,
                   _right_model.relu,
                   _right_model.maxpool,
                   _right_model.layer1,
                   _right_model.layer2,
                   _right_model.layer3,
                   _right_model.layer4,
                   _right_model.avgpool])
        )

        for param in self.left_features.parameters():
            param.requires_grad = True
        for param in self.right_features.parameters():
            param.requires_grad = True

        _num_ftrs = _left_model.fc.in_features + _right_model.fc.in_features + 2  # left, right and head_pose
        self.classifier = nn.Sequential(
            nn.Linear(_num_ftrs, _num_ftrs),
            nn.BatchNorm1d(_num_ftrs),
            nn.ReLU(),
            nn.Linear(_num_ftrs, _num_ftrs),
            nn.BatchNorm1d(_num_ftrs),
            nn.ReLU(),
            nn.Linear(_num_ftrs, num_out)
        )

        # self.init_weights()

    def init_weights(self):
        # weight initialization
        for m in self.modules():
            if isinstance(m, nn.Linear):
                nn.init.normal_(m.weight, 0, 0.01)
                nn.init.zeros_(m.bias)

    def forward(self, left_eye, right_eye, headpose):
        left_x = self.left_features(left_eye)
        left_x = torch.flatten(left_x, 1)

        right_x = self.right_features(right_eye)
        right_x = torch.flatten(right_x, 1)

        concat = torch.cat((left_x, right_x, headpose), dim=1)

        fc_output = self.classifier(concat)

        return fc_output


class RTGENEModelResnet101(nn.Module):

    def __init__(self, num_out=2):  # phi, theta
        super(RTGENEModelResnet101, self).__init__()
        _left_model = models.resnet101(pretrained=True)
        _right_model = models.resnet101(pretrained=True)

        # remove the last ConvBRelu layer
        self.left_features = nn.Sequential(
            *list([_left_model.conv1,
                   _left_model.bn1,
                   _left_model.relu,
                   _left_model.maxpool,
                   _left_model.layer1,
                   _left_model.layer2,
                   _left_model.layer3,
                   _left_model.layer4,
                   _left_model.avgpool])
        )

        self.right_features = nn.Sequential(
            *list([_right_model.conv1,
                   _right_model.bn1,
                   _right_model.relu,
                   _right_model.maxpool,
                   _right_model.layer1,
                   _right_model.layer2,
                   _right_model.layer3,
                   _right_model.layer4,
                   _right_model.avgpool])
        )

        for param in self.left_features.parameters():
            param.requires_grad = True
        for param in self.right_features.parameters():
            param.requires_grad = True

        _num_ftrs = _left_model.fc.in_features + _right_model.fc.in_features + 2 # left, right and head_pose
        self.classifier = nn.Sequential(
            nn.Linear(_num_ftrs, _num_ftrs),
            nn.BatchNorm1d(_num_ftrs),
            nn.ReLU(),
            nn.Linear(_num_ftrs, _num_ftrs),
            nn.BatchNorm1d(_num_ftrs),
            nn.ReLU(),
            nn.Linear(_num_ftrs, num_out)
        )

        # self.init_weights()

    def init_weights(self):
        # weight initialization
        for m in self.modules():
            if isinstance(m, nn.Linear):
                nn.init.normal_(m.weight, 0, 0.01)
                nn.init.zeros_(m.bias)

    def forward(self, left_eye, right_eye, headpose):
        left_x = self.left_features(left_eye)
        left_x = torch.flatten(left_x, 1)

        right_x = self.right_features(right_eye)
        right_x = torch.flatten(right_x, 1)

        concat = torch.cat((left_x, right_x, headpose), dim=1)

        fc_output = self.classifier(concat)

        return fc_output


class RTGENEModelResnet18(nn.Module):

    def __init__(self, num_out=2):  # phi, theta
        super(RTGENEModelResnet18, self).__init__()
        _left_model = models.resnet18(pretrained=True)
        _right_model = models.resnet18(pretrained=True)

        # remove the last ConvBRelu layer
        self.left_features = nn.Sequential(
            *list([_left_model.conv1,
                   _left_model.bn1,
                   _left_model.relu,
                   _left_model.maxpool,
                   _left_model.layer1,
                   _left_model.layer2,
                   _left_model.layer3,
                   _left_model.layer4,
                   _left_model.avgpool])
        )

        self.right_features = nn.Sequential(
            *list([_right_model.conv1,
                   _right_model.bn1,
                   _right_model.relu,
                   _right_model.maxpool,
                   _right_model.layer1,
                   _right_model.layer2,
                   _right_model.layer3,
                   _right_model.layer4,
                   _right_model.avgpool])
        )

        for param in self.left_features.parameters():
            param.requires_grad = True
        for param in self.right_features.parameters():
            param.requires_grad = True

        _num_ftrs = _left_model.fc.in_features + _right_model.fc.in_features + 2  # left, right and head_pose
        self.classifier = nn.Sequential(
            nn.Linear(_num_ftrs, _num_ftrs),
            nn.BatchNorm1d(_num_ftrs),
            nn.ReLU(),
            nn.Linear(_num_ftrs, _num_ftrs),
            nn.BatchNorm1d(_num_ftrs),
            nn.ReLU(),
            nn.Linear(_num_ftrs, num_out)
        )

        # self.init_weights()

    def init_weights(self):
        # weight initialization
        for m in self.modules():
            if isinstance(m, nn.Linear):
                nn.init.orthogonal_(m.weight)
                nn.init.zeros_(m.bias)

    def forward(self, left_eye, right_eye, headpose):
        left_x = self.left_features(left_eye)
        left_x = torch.flatten(left_x, 1)

        right_x = self.right_features(right_eye)
        right_x = torch.flatten(right_x, 1)

        concat = torch.cat((left_x, right_x, headpose), dim=1)

        fc_output = self.classifier(concat)

        return fc_output


if __name__ == "__main__":
    from PIL import Image
    from torchvision import transforms
    import os
    import time
    from tqdm import trange

    left_img = Image.open(os.path.abspath(os.path.join("../../data/s001_glasses/", "inpainted/left/", "left_000004_rgb.png")))
    right_img = Image.open(os.path.abspath(os.path.join("../../data/s001_glasses/", "inpainted/right/", "right_000004_rgb.png")))

    trans = transforms.Compose([transforms.Resize(256, Image.BICUBIC),
                                transforms.CenterCrop(224),
                                transforms.ToTensor(),
                                transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                                     std=[0.229, 0.224, 0.225])])

    trans_left_img = trans(left_img).unsqueeze(0).cuda()
    trans_right_img = trans(right_img).unsqueeze(0).cuda()

    model = RTGENEModelResnet50()
    model = model.cuda()
    model.eval()
    start_time = time.time()
    outputs = []
    for _ in trange(100):
        outputs.append(model(trans_left_img, trans_right_img))
    print("Evaluation Frequency: {:.3f}Hz".format(1.0 / ((time.time() - start_time) / 100.0)))
