#!/bin/bash

# Install dependencies
apt update
apt install -y screen vim git-lfs
screen

# Install common libraries
pip install -q requests accelerate sentencepiece pytablewriter

if [ "$DEBUG" == "True" ]; then
    echo "Launch LLM AutoEval in debug mode"
fi

# Run evaluation
if [ "$BENCHMARK" == "nous" ]; then
    git clone -b add-agieval https://github.com/dmahan93/lm-evaluation-harness
    cd lm-evaluation-harness
    pip install -e .

    benchmark="agieval"
    python main.py \
        --model hf-causal \
        --model_args pretrained=$MODEL \
        --tasks agieval_aqua_rat,agieval_logiqa_en,agieval_lsat_ar,agieval_lsat_lr,agieval_lsat_rc,agieval_sat_en,agieval_sat_en_without_passage,agieval_sat_math \
        --device cuda:0 \
        --batch_size auto \
        --output_path ./${benchmark}.json

    benchmark="gpt4all"
    python main.py \
        --model hf-causal \
        --model_args pretrained=$MODEL \
        --tasks hellaswag,openbookqa,winogrande,arc_easy,arc_challenge,boolq,piqa \
        --device cuda:0 \
        --batch_size auto \
        --output_path ./${benchmark}.json

    benchmark="truthfulqa"
    python main.py \
        --model hf-causal \
        --model_args pretrained=$MODEL \
        --tasks truthfulqa_mc \
        --device cuda:0 \
        --batch_size auto \
        --output_path ./${benchmark}.json

    benchmark="bigbench"
    python main.py \
        --model hf-causal \
        --model_args pretrained=$MODEL \
        --tasks bigbench_causal_judgement,bigbench_date_understanding,bigbench_disambiguation_qa,bigbench_geometric_shapes,bigbench_logical_deduction_five_objects,bigbench_logical_deduction_seven_objects,bigbench_logical_deduction_three_objects,bigbench_movie_recommendation,bigbench_navigate,bigbench_reasoning_about_colored_objects,bigbench_ruin_names,bigbench_salient_translation_error_detection,bigbench_snarks,bigbench_sports_understanding,bigbench_temporal_sequences,bigbench_tracking_shuffled_objects_five_objects,bigbench_tracking_shuffled_objects_seven_objects,bigbench_tracking_shuffled_objects_three_objects \
        --device cuda:0 \
        --batch_size auto \
        --output_path ./${benchmark}.json
    
    python ../llm-autoeval/main.py .

elif [ "$BENCHMARK" == "openllm" ]; then
    git clone https://github.com/EleutherAI/lm-evaluation-harness
    cd lm-evaluation-harness
    pip install -e ".[vllm,promptsource]"
    pip install langdetect immutabledict

    # benchmark="arc"
    # lm_eval --model vllm \
    #     --model_args pretrained=${MODEL},dtype=auto,gpu_memory_utilization=0.8 \
    #     --tasks arc_challenge \
    #     --num_fewshot 25 \
    #     --batch_size auto \
    #     --output_path ./${benchmark}.json

    # benchmark="hellaswag"
    # lm_eval --model vllm \
    #     --model_args pretrained=${MODEL},dtype=auto,gpu_memory_utilization=0.8 \
    #     --tasks hellaswag \
    #     --num_fewshot 10 \
    #     --batch_size auto \
    #     --output_path ./${benchmark}.json

    benchmark="mmlu"
    lm_eval --model vllm \
        --model_args pretrained=${MODEL},dtype=auto,gpu_memory_utilization=0.8 \
        --tasks hendrycksTest-abstract_algebra,hendrycksTest-anatomy,hendrycksTest-astronomy,hendrycksTest-business_ethics,hendrycksTest-clinical_knowledge,hendrycksTest-college_biology,hendrycksTest-college_chemistry,hendrycksTest-college_computer_science,hendrycksTest-college_mathematics,hendrycksTest-college_medicine,hendrycksTest-college_physics,hendrycksTest-computer_security,hendrycksTest-conceptual_physics,hendrycksTest-econometrics,hendrycksTest-electrical_engineering,hendrycksTest-elementary_mathematics,hendrycksTest-formal_logic,hendrycksTest-global_facts,hendrycksTest-high_school_biology,hendrycksTest-high_school_chemistry,hendrycksTest-high_school_computer_science,hendrycksTest-high_school_european_history,hendrycksTest-high_school_geography,hendrycksTest-high_school_government_and_politics,hendrycksTest-high_school_macroeconomics,hendrycksTest-high_school_mathematics,hendrycksTest-high_school_microeconomics,hendrycksTest-high_school_physics,hendrycksTest-high_school_psychology,hendrycksTest-high_school_statistics,hendrycksTest-high_school_us_history,hendrycksTest-high_school_world_history,hendrycksTest-human_aging,hendrycksTest-human_sexuality,hendrycksTest-international_law,hendrycksTest-jurisprudence,hendrycksTest-logical_fallacies,hendrycksTest-machine_learning,hendrycksTest-management,hendrycksTest-marketing,hendrycksTest-medical_genetics,hendrycksTest-miscellaneous,hendrycksTest-moral_disputes,hendrycksTest-moral_scenarios,hendrycksTest-nutrition,hendrycksTest-philosophy,hendrycksTest-prehistory,hendrycksTest-professional_accounting,hendrycksTest-professional_law,hendrycksTest-professional_medicine,hendrycksTest-professional_psychology,hendrycksTest-public_relations,hendrycksTest-security_studies,hendrycksTest-sociology,hendrycksTest-us_foreign_policy,hendrycksTest-virology,hendrycksTest-world_religions \
        --num_fewshot 5 \
        --batch_size auto \
        --verbosity DEBUG \
        --output_path ./${benchmark}.json
    
    # benchmark="truthfulqa"
    # lm_eval --model vllm \
    #     --model_args pretrained=${MODEL},dtype=auto,gpu_memory_utilization=0.8 \
    #     --tasks truthfulqa \
    #     --num_fewshot 0 \
    #     --batch_size auto \
    #     --output_path ./${benchmark}.json
    
    # benchmark="winogrande"
    # lm_eval --model vllm \
    #     --model_args pretrained=${MODEL},dtype=auto,gpu_memory_utilization=0.8 \
    #     --tasks winogrande \
    #     --num_fewshot 5 \
    #     --batch_size auto \
    #     --output_path ./${benchmark}.json
    
    # benchmark="gsm8k"
    # lm_eval --model vllm \
    #     --model_args pretrained=${MODEL},dtype=auto,gpu_memory_utilization=0.8 \
    #     --tasks gsm8k \
    #     --num_fewshot 5 \
    #     --batch_size auto \
    #     --output_path ./${benchmark}.json

    python ../llm-autoeval/main.py .
else
    echo "Error: Invalid BENCHMARK value. Please set BENCHMARK to 'nous' or 'openllm'."
fi

if [ "$DEBUG" == "False" ]; then
    runpodctl remove pod $RUNPOD_POD_ID
fi
sleep infinity