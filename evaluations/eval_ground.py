import os.path as osp
import numpy as np
from common import voc_ap, tiou
from util import load_file

def eval_ground_scores(gt_relations, pred_relations, tiou_threshold):
    """

    :param gt_relations:
    :param pred_relations:
    :param tiou_threshold:
    :return:
    """
    # pred_relations = sorted(pred_relations, key=lambda x: x['score'], reverse=True)

    relation_num = len(gt_relations)
    predict, predict_sub, predict_obj = 0, 0, 0

    for relation, pred_trajs in pred_relations.items():
        gt_trajs = gt_relations[relation]

        pred_sub = pred_trajs['sub']
        pred_obj = pred_trajs['obj']
        flag, flag_s, flag_o = False, False, False

        for gt_traj in gt_trajs:
            gt_sub = gt_traj['sub']
            gt_obj = gt_traj['obj']
            s_tiou = tiou(pred_sub, gt_sub)
            o_tiou = tiou(pred_obj, gt_obj)
            r_iou = min(s_tiou, o_tiou)

            if r_iou >= tiou_threshold:
                flag = True
            if s_tiou >= tiou_threshold:
                flag_s = True
            if o_tiou >= tiou_threshold:
                flag_o = True
        if flag:
            predict += 1
        if flag_s:
            predict_sub += 1
        if flag_o:
            predict_obj += 1

    predict = predict / relation_num
    predict_sub = predict_sub /relation_num
    predict_obj = predict_obj /relation_num

    return predict, predict_sub, predict_obj, relation_num


def evaluate(groundtruth, prediction, tiou_threshold=0.5):
    """ evaluate visual relation detection and visual 
    relation tagging.
    """

    video_num = len(groundtruth)
    print('Computing grounding accuracy over {} videos...'.format(video_num))
    acc, acc_sub, acc_obj = 0, 0, 0

    gt_rnum = 0
    for qid, relation_gt in groundtruth.items():

        if qid not in prediction:
            continue
        relation_pred = prediction[qid]
        if len(relation_pred) == 0:
            continue

        video_acc, video_acc_sub, video_acc_obj, relation_num = eval_ground_scores(relation_gt, relation_pred, tiou_threshold)
        # print('{} {:.6f} {:.6f} {:.6f}'.format(qid, video_acc_sub, video_acc_obj, video_acc))

        acc += video_acc
        acc_sub += video_acc_sub
        acc_obj += video_acc_obj
        gt_rnum += relation_num


    acc /= video_num
    acc_sub /= video_num
    acc_obj /= video_num

    print(gt_rnum)

    print('Subject: {:.6f}, Object: {:.6f}, All: {:.6f}'.format(acc_sub, acc_obj, acc))



def main():

    groundtruth_dir = '../dataset/vidvrd/'
    gt_file = osp.join(groundtruth_dir, 'gt_relation.json')

    result_dir = '../results/'
    res_file = osp.join(result_dir, 'ground_result_nobg.json')

    grountruth = load_file(gt_file)
    prediction = load_file(res_file)

    evaluate(grountruth, prediction)


if __name__ == "__main__":
    main()



