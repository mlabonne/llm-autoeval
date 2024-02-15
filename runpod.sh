#!/bin/bash

start=$(date +%s)

# Detect the number of NVIDIA GPUs and create a device string
gpu_count=$(nvidia-smi -L | wc -l)
if [ $gpu_count -eq 0 ]; then
    echo "No NVIDIA GPUs detected. Exiting."
    exit 1
fi
# Construct the CUDA device string
cuda_devices=""
for ((i=0; i<gpu_count; i++)); do
    if [ $i -gt 0 ]; then
        cuda_devices+=","
    fi
    cuda_devices+="$i"
done

# Install dependencies
apt update
apt install -y screen vim git-lfs
screen

# Install common libraries

if [ "$DEBUG" == "True" ]; then
    echo "Launch LLM AutoEval in debug mode"
fi

# Run evaluation
cd /workspace/; mkdir -p cache model; git clone https://github.com/chenhaodev/lm-evaluation-harness; cd lm-evaluation-harness; pip install -e .;
pip install huggingface_hub; huggingface-cli login --token $HF_TOKEN; huggingface-cli download --resume-download $MODEL --local-dir /workspace/model --local-dir-use-symlinks False --cache-dir /workspace/cache;

lm_eval --model hf \
    --model_args pretrained=/workspace/model,trust_remote_code=$TRUST_REMOTE_CODE,parallelize=True \
    --tasks ocn,aocnp,medmcqa,pubmedqa,mmlu_clinical_knowledge,mmlu_college_medicine,mmlu_professional_medicine \
    --device cuda:$cuda_devices \
    --batch_size auto \
    --limit 100 \
    --output_path ./result.log

end=$(date +%s)
echo "Elapsed Time: $(($end-$start)) seconds" >> ./result.log

python ../llm-autoeval/upload-result.py . $(($end-$start))

if [ "$DEBUG" == "False" ]; then
    runpodctl remove pod $RUNPOD_POD_ID
fi
sleep infinity
