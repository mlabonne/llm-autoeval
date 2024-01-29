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

# Construct the CUDA device string and determine parallelization
cuda_devices=""
parallelize="false"
for ((i=0; i<gpu_count; i++)); do
    if [ $i -gt 0 ]; then
        cuda_devices+=","
        parallelize="true"
    fi
    cuda_devices+="$i"
done

# Update package lists and install screen, vim, and git-lfs.
apt update
apt install -y screen vim git-lfs

# Start a new screen session.
screen

# Install Python libraries: requests, accelerate, sentencepiece, pytablewriter, einops, protobuf, deepspeed
pip install -q requests accelerate sentencepiece pytablewriter einops protobuf deepspeed

# Clone and setup lm-evaluation-harness
git clone -b agieval https://github.com/EleutherAI/lm-evaluation-harness
cd lm-evaluation-harness
pip install -e ".[vllm,promptsource]"

# If in debug mode, print a message indicating that.
if [ "$DEBUG" == "True" ]; then
    echo "Launch LLM AutoEval in debug mode"
fi

# Store the initial directory to return later
initial_directory=$(pwd)

# Function definitions for nous benchmark
run_benchmark_nous() {
    benchmark=$1
    tasks=$2
    lm_eval --model hf \
        --model_args parallelize=$parallelize,pretrained=$MODEL,trust_remote_code=$TRUST_REMOTE_CODE \
        --tasks $tasks \
        --device cuda:$cuda_devices \
        --batch_size auto \
        --output_path ./${benchmark}.json
}

# Function definitions for openllm benchmark
run_benchmark_openllm() {
    benchmark=$1
    tasks=$2
    num_fewshot=$3
    lm_eval --model vllm \
        --model_args pretrained=${MODEL},dtype=auto,gpu_memory_utilization=0.8,trust_remote_code=$TRUST_REMOTE_CODE \
        --tasks $tasks \
        --num_fewshot $num_fewshot \
        --batch_size auto \
        --output_path ./${benchmark}.json
}

# Run evaluation based on the BENCHMARK environment variable
case "$BENCHMARK" in
  "nous")
    # Run benchmarks for nous
    run_benchmark_nous "agieval" "agieval_aqua_rat,agieval_logiqa_en,agieval_lsat_ar,agieval_lsat_lr,agieval_lsat_rc,agieval_sat_en,agieval_sat_en_without_passage,agieval_sat_math"
    run_benchmark_nous "gpt4all" "hellaswag,openbookqa,winogrande,arc_easy,arc_challenge,boolq,piqa"
    run_benchmark_nous "truthfulqa" "truthfulqa_mc"
    run_benchmark_nous "bigbench" "bigbench_causal_judgement,bigbench_date_understanding,bigbench_disambiguation_qa,bigbench_geometric_shapes,bigbench_logical_deduction_five_objects,bigbench_logical_deduction_seven_objects,bigbench_logical_deduction_three_objects,bigbench_movie_recommendation,bigbench_navigate,bigbench_reasoning_about_colored_objects,bigbench_ruin_names,bigbench_salient_translation_error_detection,bigbench_snarks,bigbench_sports_understanding,bigbench_temporal_sequences,bigbench_tracking_shuffled_objects_five_objects,bigbench_tracking_shuffled_objects_seven_objects,bigbench_tracking_shuffled_objects_three_objects"
    ;;
  "openllm")
    # Run benchmarks for openllm
    run_benchmark_openllm "arc" "arc_challenge" 25
    run_benchmark_openllm "hellaswag" "hellaswag" 10
    run_benchmark_openllm "truthfulqa" "truthfulqa" 0
    run_benchmark_openllm "winogrande" "winogrande" 5
    run_benchmark_openllm "gsm8k" "gsm8k" 5    
    ;;
  *)
    echo "Error: Invalid BENCHMARK value. Please set BENCHMARK to 'nous' or 'openllm'."
    ;;
esac

# Record the end time and calculate the elapsed time.
end=$(date +%s)
echo "Elapsed Time: $(($end-$start)) seconds"

# Return to the initial directory and run the Python script to upload the results
cd /
cd llm-autoeval
if [ -f "main.py" ]; then
    python main.py . $(($end-$start))
else
    echo "Error: main.py not found in the llm-autoeval directory."
fi

# If not in debug mode, remove the pod using the RUNPOD_POD_ID environment variable.
if [ "$DEBUG" == "False" ]; then
    runpodctl remove pod $RUNPOD_POD_ID
fi

# Prevent the script from exiting immediately.
sleep infinity
