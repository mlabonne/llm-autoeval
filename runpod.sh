#!/bin/bash

# Record the start time of the script.
start=$(date +%s)

# Count the number of NVIDIA GPUs available
gpu_count=$(nvidia-smi -L | wc -l)

# If no NVIDIA GPUs are detected, print a message and exit the script.
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
    # Create a string of CUDA device IDs (0,1,2,...) based on the number of GPUs.
    cuda_devices+="$i"
done

# Update package lists and install screen, vim, and git-lfs.
apt update
apt install -y screen vim git-lfs

# Start a new screen session.
screen

# Install Python libraries: requests, accelerate, sentencepiece, pytablewriter, einops, and protobuf.
pip install -q requests accelerate sentencepiece pytablewriter einops protobuf

# If in debug mode, print a message indicating that.
if [ "$DEBUG" == "True" ]; then
    echo "Launch LLM AutoEval in debug mode"
fi

# Run evaluation based on the BENCHMARK environment variable
# The following block is executed if BENCHMARK is set to 'nous'.
if [ "$BENCHMARK" == "nous" ]; then
    # Clone a specific branch of a GitHub repository
    git clone -b add-agieval https://github.com/dmahan93/lm-evaluation-harness
    # Enter the directory of the cloned repository
    cd lm-evaluation-harness
    # Install its contents
    pip install -e .

    # Several benchmarks are run with different tasks, each writing results to a JSON file.
    benchmark="agieval"
    python main.py \
    --model hf-causal \
        --model_args pretrained=$MODEL,trust_remote_code=$TRUST_REMOTE_CODE \
        --tasks agieval_aqua_rat,agieval_logiqa_en,agieval_lsat_ar,agieval_lsat_lr,agieval_lsat_rc,agieval_sat_en,agieval_sat_en_without_passage,agieval_sat_math \
        --device cuda:$cuda_devices \
        --batch_size auto \
        --output_path ./${benchmark}.json
        
    benchmark="gpt4all"
    python main.py \
    --model hf-causal \
        --model_args pretrained=$MODEL,trust_remote_code=$TRUST_REMOTE_CODE \
        --tasks hellaswag,openbookqa,winogrande,arc_easy,arc_challenge,boolq,piqa \
        --device cuda:$cuda_devices \
        --batch_size auto \
        --output_path ./${benchmark}.json

    benchmark="truthfulqa"
    python main.py \
    --model hf-causal \
    --model_args pretrained=$MODEL,trust_remote_code=$TRUST_REMOTE_CODE \
    --tasks truthfulqa_mc \
    --device cuda:$cuda_devices \
    --batch_size auto \
    --output_path ./${benchmark}.json

    benchmark="bigbench"
    python main.py \
    --model hf-causal \
    --model_args pretrained=$MODEL,trust_remote_code=$TRUST_REMOTE_CODE \
    --tasks bigbench_causal_judgement,bigbench_date_understanding,bigbench_disambiguation_qa,bigbench_geometric_shapes,bigbench_logical_deduction_five_objects,bigbench_logical_deduction_seven_objects,bigbench_logical_deduction_three_objects,bigbench_movie_recommendation,bigbench_navigate,bigbench_reasoning_about_colored_objects,bigbench_ruin_names,bigbench_salient_translation_error_detection,bigbench_snarks,bigbench_sports_understanding,bigbench_temporal_sequences,bigbench_tracking_shuffled_objects_five_objects,bigbench_tracking_shuffled_objects_seven_objects,bigbench_tracking_shuffled_objects_three_objects \
        --device cuda:$cuda_devices \
        --batch_size auto \
        --output_path ./${benchmark}.json
        
    # Record the end time and calculate the elapsed time.
    end=$(date +%s)
    echo "Elapsed Time: $(($end-$start)) seconds"
 
    # Run another Python script to upload the results as a GitHub gist.
    python ../main.py . $(($end-$start))
    ### Note: I changed this and this resolved the error of the results not uploading.
    ### from: ../llm-evaluation/main.py . $(($end-$start))
    ### to: ../main.py . $(($end-$start))

# Run evaluation based on the BENCHMARK environment variable
# The following block is executed if BENCHMARK is set to 'openllm'.
elif [ "$BENCHMARK" == "openllm" ]; then
    git clone https://github.com/EleutherAI/lm-evaluation-harness
    cd lm-evaluation-harness
    pip install -e ".[vllm,promptsource]"
    pip install langdetect immutabledict

    benchmark="arc"
    lm_eval --model vllm \
        --model_args pretrained=${MODEL},dtype=auto,gpu_memory_utilization=0.8,trust_remote_code=$TRUST_REMOTE_CODE \
        --tasks arc_challenge \
        --num_fewshot 25 \
        --batch_size auto \
        --output_path ./${benchmark}.json

    benchmark="hellaswag"
    lm_eval --model vllm \
        --model_args pretrained=${MODEL},dtype=auto,gpu_memory_utilization=0.8,trust_remote_code=$TRUST_REMOTE_CODE \
        --tasks hellaswag \
        --num_fewshot 10 \
        --batch_size auto \
        --output_path ./${benchmark}.json

    # benchmark="mmlu"
    # lm_eval --model vllm \
    #     --model_args pretrained=${MODEL},dtype=auto,gpu_memory_utilization=0.8,trust_remote_code=$TRUST_REMOTE_CODE \
    #     --tasks mmlu \
    #     --num_fewshot 5 \
    #     --batch_size auto \
    #     --verbosity DEBUG \
    #     --output_path ./${benchmark}.json
    
    benchmark="truthfulqa"
    lm_eval --model vllm \
        --model_args pretrained=${MODEL},dtype=auto,gpu_memory_utilization=0.8,trust_remote_code=$TRUST_REMOTE_CODE \
        --tasks truthfulqa \
        --num_fewshot 0 \
        --batch_size auto \
        --output_path ./${benchmark}.json
    
    benchmark="winogrande"
    lm_eval --model vllm \
        --model_args pretrained=${MODEL},dtype=auto,gpu_memory_utilization=0.8,trust_remote_code=$TRUST_REMOTE_CODE \
        --tasks winogrande \
        --num_fewshot 5 \
        --batch_size auto \
        --output_path ./${benchmark}.json
    
    benchmark="gsm8k"
    lm_eval --model vllm \
        --model_args pretrained=${MODEL},dtype=auto,gpu_memory_utilization=0.8,trust_remote_code=$TRUST_REMOTE_CODE \
        --tasks gsm8k \
        --num_fewshot 5 \
        --batch_size auto \
        --output_path ./${benchmark}.json

    # Record the end time and calculate the elapsed time.
    end=$(date +%s)
    echo "Elapsed Time: $(($end-$start)) seconds"

    # Run another Python script to upload the results as a GitHub gist.
    python ../main.py . $(($end-$start))
    ### Note: I changed this and this resolved the error of the results not uploading.
    ### from: ../llm-evaluation/main.py . $(($end-$start))
    ### to: ../main.py . $(($end-$start))

# If BENCHMARK is neither 'nous' nor 'openllm', print an error message.
else
    echo "Error: Invalid BENCHMARK value. Please set BENCHMARK to 'nous' or 'openllm'."
fi

# If not in debug mode, remove the pod using the RUNPOD_POD_ID environment variable.
if [ "$DEBUG" == "False" ]; then
    runpodctl remove pod $RUNPOD_POD_ID
fi

# Prevent the script from exiting immediately.
sleep infinity
