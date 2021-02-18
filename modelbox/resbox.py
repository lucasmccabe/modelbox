from PIL import Image
import requests
from io import BytesIO
import torch
from torchvision import models, transforms

class Resbox():
    """ResNet in a box."""

    def __init__(self):
        """Constructor for the Resbox class."""
        self.preprocesser = transforms.Compose(
            [
             transforms.Resize(256),
             transforms.CenterCrop(224),
             transforms.ToTensor(),
             transforms.Normalize(
                 mean= [0.485, 0.456, 0.406],
                 std = [0.229, 0.224, 0.225]
            )])
        self.resnet = models.resnet101(pretrained=True)
        self.resnet.eval()

        with open("data/imagenet_classes.txt") as f:
            self.labels = [line.strip() for line in f.readlines()]

    def preprocess(self, floc):
        """
        Preprocess image, either from local path or URL.

        Parameters
        ----------
        floc : `str`
            image location. could be local path or url

        Returns
        -------
        preprocessed image (a tensor)
        """
        try:
            img = Image.open(floc).convert('RGB')
        except:
            response = requests.get(floc)
            img = Image.open(BytesIO(response.content)).convert('RGB')
        img = self.preprocesser(img)
        return torch.unsqueeze(img, 0)

    def get_labels(self, floc, topn = 1, with_confidence = True):
        """
        Inference step. Returns a list of (topn) labels and (optionally)
        "confidence" scores.

        Parameters
        ----------
        floc : `str`
            image location. could be local path or url

        Returns
        -------
        labels : `List`
            either:
                - a list of the topn class labels
                - a list of the topn class tuples, each consisting of:
                    - class label
                    - softmax "confidence" score
        """
        output = self.resnet(
            self.preprocess(floc))
        _, indices = torch.sort(output, descending=True)
        if with_confidence:
            confidence_scores = torch.nn.functional.softmax(
                output,
                dim=1)[0]
            labels = [(self.labels[i.item()],
                        confidence_scores[i.item()].item()) \
                     for i in indices[0][:topn]]
        else:
            labels = [self.labels[i.item()] \
                     for i in indices[0][:topn]]
        return labels
