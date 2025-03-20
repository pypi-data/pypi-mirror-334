from easy_kubeflow import EasyJobs, JobSpec

if __name__ == '__main__':
    runs = EasyJobs()
    runs.login(username="liuweibin@stonewise.cn",
               password="liuweibin@StoneWise2021",
               cloud="tencent")

    # 定义任务结构体example
    test = JobSpec("sdk-test-alluxio-350w",
                   job_type="pytorch-ddp")  # 任务命令规范：https://wiki.stonewise.cn/display/~liuweibin/submit+jobs
    test.cpu("40") \
        .mem("400Gi") \
        .gpu("8") \
        .affinity("none") \
        .image("harbor.stonewise.cn/kubeflow/transformer-3dmg-job:mlp-fp32") \
        .command("/bin/bash -c") \
        .args("cd /home/jovyan/transformer-3dmg/stonewise_mg/mains/lingo3dmol/ && accelerate launch --multi_gpu --num_machines 8 --num_processes 64 --dynamo_backend no --machine_rank ${RANK} --main_process_ip ${MASTER_ADDR} --main_process_port ${MASTER_PORT} training.py --train_list /home/jovyan/wanghan_data/3DMG_data/alluxio/RComplex_96w/path.csv,/home/jovyan/wanghan_data/3DMG_data/alluxio/RComplex_252w/path.csv,/home/jovyan/wanghan_data/3DMG_data/alluxio/pdbbind2020_20230216/path.csv --eval_list /home/jovyan/wanghan_data/3DMG_data/alluxio/business/path.csv --learning_rate 1e-4 --weight_decay 0.01 --output_dir /home/jovyan/wanghan_data/transformer-3dmg/logs/rcomplex96w-1b --model_path /home/jovyan/wanghan_data/transformer-3dmg/logs/old_109w_decoder12_relf_rcomplex96w_ce_wo_leakage/0226/1/checkpoints/checkpoint_200/model.safetensors --per_gpu_train_batch_size 64 --per_gpu_eval_batch_size 64 --pocket_vocab_size 32 --ligand_vocab_size 256 --encoder_num_hidden_layers 6 --decoder_num_hidden_layers 12 --hidden_size 512 --num_attention_heads 8 --intermediate_size 1024 --head_hidden_size 256 --head_num_hidden_layers 2 --head_relative_first --ignore_pdb_ids '' --overwrite_output_dir --use_sfs_store") \
        .fusevols(path="/alluxio/fuse/mol/3dmg/complex", mount_path="/home/jovyan/wanghan_data/3DMG_data/alluxio") \
        .hostvols(host_path="/kubeflow/mount/logs", mount_path="/home/jovyan/wanghan_data/transformer-3dmg/logs") \
        .retry(1) \
        .workers(7)

    # # standalone
    # test = JobSpec("sdk-test-350",
    #                job_type="standalone")  # 任务命令规范：https://wiki.stonewise.cn/display/~liuweibin/submit+jobs
    # test.cpu("40") \
    #     .mem("400Gi") \
    #     .gpu("8") \
    #     .affinity("none") \
    #     .image("harbor.stonewise.cn/kubeflow/transformer-3dmg-job:mlp-fp32") \
    #     .command("/bin/bash -c") \
    #     .args(
    #     "cd /home/jovyan/transformer-3dmg/stonewise_mg/mains/lingo3dmol/ && accelerate launch --multi_gpu --main_process_port 23456 --num_machines 1 --num_processes 8 --mixed_precision no --dynamo_backend no training.py --train_list /home/jovyan/wanghan_data/3DMG_data/alluxio/RComplex_96w/path.csv,/home/jovyan/wanghan_data/3DMG_data/alluxio/RComplex_252w/path.csv,/home/jovyan/wanghan_data/3DMG_data/alluxio/pdbbind2020_20230216/path.csv --eval_list /home/jovyan/wanghan_data/3DMG_data/alluxio/business/path.csv --learning_rate 1e-4 --weight_decay 0.01 --output_dir /home/jovyan/wanghan_data/transformer-3dmg/logs/rcomplex96w-1b --model_path /home/jovyan/wanghan_data/transformer-3dmg/logs/old_109w_decoder12_relf_rcomplex96w_ce_wo_leakage/0226/1/checkpoints/checkpoint_200/model.safetensors --per_gpu_train_batch_size 64 --per_gpu_eval_batch_size 64 --pocket_vocab_size 32 --ligand_vocab_size 256 --encoder_num_hidden_layers 6 --decoder_num_hidden_layers 12 --hidden_size 512 --num_attention_heads 8 --intermediate_size 1024 --head_hidden_size 256 --head_num_hidden_layers 2 --head_relative_first --ignore_pdb_ids '' --overwrite_output_dir --use_sfs_store") \
    #     .fusevols(path="/alluxio/fuse/mol/3dmg/complex", mount_path="/home/jovyan/wanghan_data/3DMG_data/alluxio") \
    #     .hostvols(host_path="/kubeflow/mount/logs", mount_path="/home/jovyan/wanghan_data/transformer-3dmg/logs") \
    #     .retry(1) \
    #     .workers(1)

    # 创建任务
    #runs.create(test)

    # 查询任务
    runs.get(test)  # 指定任务名称或者对象

    # # 删除任务
    # runs.delete(test)  # 指定任务名称或者对象

    # 查剩余资源
    runs.resources(cpu=40, memory="400Gi", gpu=8)
