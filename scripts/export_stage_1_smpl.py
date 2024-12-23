import torch 
from argparse import ArgumentParser
import os
from os.path import join

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument('--net_save_path', type=str, required=True)
    parser.add_argument('--smpl_parms_path', type=str, required=True)
    parser.add_argument('--net_name', type=str, default='net.pth')
    args = parser.parse_args()

    net_save_path = args.net_save_path
    smpl_parms_path = args.smpl_parms_path
    net_name = args.net_name


    saved_model_state = torch.load(
        os.path.join(net_save_path, net_name))
    print('load pth: ', join(net_save_path, net_name))
    smpl_data = torch.load(join(smpl_parms_path, 'smpl_parms.pth'))

    ### model define 
    num_training_frames = len(os.listdir(join(smpl_parms_path, 'images')))
    pose = torch.nn.Embedding(num_training_frames, 72, sparse=True).cuda()
    transl = torch.nn.Embedding(num_training_frames, 3, sparse=True).cuda()


    pose.load_state_dict(saved_model_state["pose"], strict=False)
    transl.load_state_dict(saved_model_state["transl"], strict=False)

    smpl_data['body_pose'][:num_training_frames, :] = pose.weight.cpu().detach()
    smpl_data['trans'][:num_training_frames,:] = transl.weight.cpu().detach()

    torch.save(smpl_data, join(smpl_parms_path, 'smpl_parms_pred.pth'))
