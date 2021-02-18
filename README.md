# modelbox

> `modelbox`: reducing time-to-model for fun and profit!

![box](images/icon.PNG)

`modelbox` is a (very WIP) high-level package for quickly using machine learning models when you don't want or need to spend a lot of time building them. Basically, we're putting some models in a box.

## Setup

You'll need [PyTorch](https://pytorch.org/), which can be messy to install. I've found it easiest to use [conda](https://docs.conda.io/en/latest/):

```bash
conda install pytorch==1.4.0 torchvision==0.5.0 cudatoolkit=10.1 -c pytorch
```

Then, clone the `modelbox` repo, cd into the directory, and run:

```bash
python setup.py install
```

## Example Usage

Suppose I want to play with an instance of ResNet-101 trained on the ImageNet dataset:

```python
import modelbox

model = modelbox.Resbox()
labels = model.get_labels(
  "https://chuckanddons.com/media/wysiwyg/kitten_blog.jpg",
  topn = 3)
```

`get_labels` accepts either a local image path or a url. Let's take a look at what's in `labels`:

```bash
>>> labels
[('tiger cat', 0.26134470105171204),
('lynx, catamount', 0.2470506727695465),
('Egyptian cat', 0.2197592854499817)]
```

That was easy!

## License
[MIT](https://choosealicense.com/licenses/mit/)
