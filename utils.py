# ====================================================
# @Time    : 11/21/19 7:42 PM
# @Author  : Xiao Junbin
# @Email   : junbin@comp.nus.edu.sg
# @File    : utils.py
# ====================================================
import json
import os
import os.path as osp
import shutil
import numpy as np


def clip_gradient(optimizer, grad_clip):
    """
    Clips gradients computed during backpropagation to avoid explosion of gradients.
    :param optimizer: optimizer with the gradients to be clipped
    :param grad_clip: clip value
    """
    for group in optimizer.param_groups:
        for param in group['params']:
            if param.grad is not None:
                param.grad.data.clamp_(-grad_clip, grad_clip)


def save_results(save_name, data):

    print('Save to {}'.format(save_name))

    path = osp.dirname(save_name)
    if not osp.exists(path):
        os.makedirs(path)

    with open(save_name, 'w') as fp:
        json.dump(data, fp)


def delete(vname):
    if vname != '':
        frame_dir = '../ground_data/vidor/frames/'
        print('Clean up {}'.format(vname))
        shutil.rmtree(osp.join(frame_dir, vname))

def sort_bbox(bboxes, width, height):
    """
    sort bbox according to the top-left to bottom-right order
    :param bboxes:
    :return:
    """
    x_c = (bboxes[:, 2] - bboxes[:, 0]) / 2
    y_c = (bboxes[:, 3] - bboxes[:, 1]) / 2

    points =  []
    for x, y in zip(x_c, y_c):
        points.append((y-1)*width+x)

    index = np.argsort(points)

    return index






