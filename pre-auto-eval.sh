#!/bin/bash

sh base-auto-train.sh

# Detect the number of NVIDIA GPUs and create a device string
gpu_count=$(nvidia-smi -L | wc -l)
if [ $gpu_count -eq 0 ]; then
    echo "No NVIDIA GPUs detected. Exiting."
    exit 1
fi

# Install dependencies
apt update
apt install -y screen vim git-lfs

cd /workspace/; mkdir -p cache model; git clone https://github.com/chenhaodev/lm-evaluation-harness; cd lm-evaluation-harness; pip install -e .;
pip install transformers_stream_generator einops bitsandbytes tiktoken;

echo "lm_eval --model hf --model_args pretrained=/workspace/model,trust_remote_code=True,parallelize=True,load_in_4bit=True --tasks ocn,aocnp,medmcqa,pubmedqa,mmlu_clinical_knowledge,mmlu_college_medicine,mmlu_professional_medicine  --device cuda:0  --batch_size auto  --limit 100 | tee result.log; " > run-eval.sh 
echo "cd /workspace/; python /workspace/llm-autoeval/upload-result.py . 9999" > run-upload.sh 

pip install huggingface_hub; huggingface-cli login --token $HF_TOKEN; huggingface-cli download --resume-download $MODEL --local-dir /workspace/model --local-dir-use-symlinks False --cache-dir /workspace/cache;

sleep infinity
