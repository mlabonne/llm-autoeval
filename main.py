#pip install -qqq runpod --progress-bar off

import runpod
import sys

BENCHMARK = "medtasks"
MODEL = sys.argv[1] #"mlabonne/NeuralMarcoro14-7B" # @param {type:"string"}
GPU = sys.argv[2] #"NVIDIA GeForce RTX 3090" # @param ["NVIDIA A100 80GB PCIe", "NVIDIA A100-SXM4-80GB", "NVIDIA A30", "NVIDIA A40", "NVIDIA GeForce RTX 3070", "NVIDIA GeForce RTX 3080", "NVIDIA GeForce RTX 3080 Ti", "NVIDIA GeForce RTX 3090", "NVIDIA GeForce RTX 3090 Ti", "NVIDIA GeForce RTX 4070 Ti", "NVIDIA GeForce RTX 4080", "NVIDIA GeForce RTX 4090", "NVIDIA H100 80GB HBM3", "NVIDIA H100 PCIe", "NVIDIA L4", "NVIDIA L40", "NVIDIA RTX 4000 Ada Generation", "NVIDIA RTX 4000 SFF Ada Generation", "NVIDIA RTX 5000 Ada Generation", "NVIDIA RTX 6000 Ada Generation", "NVIDIA RTX A2000", "NVIDIA RTX A4000", "NVIDIA RTX A4500", "NVIDIA RTX A5000", "NVIDIA RTX A6000", "Tesla V100-FHHL-16GB", "Tesla V100-PCIE-16GB", "Tesla V100-SXM2-16GB", "Tesla V100-SXM2-32GB"]
NUMBER_OF_GPUS = 1 # @param {type:"slider", min:1, max:8, step:1}
CONTAINER_DISK = 50 # @param {type:"slider", min:50, max:500, step:25}
VOLUME_IN_GB = 100
CLOUD_TYPE = "COMMUNITY" # @param ["COMMUNITY", "SECURE"]
REPO = "https://github.com/chenhaodev/llm-autoeval.git" # @param {type:"string"}
TRUST_REMOTE_CODE = False # @param {type:"boolean"}
DEBUG = False # @param {type:"boolean"}

# @markdown ---
RUNPOD_TOKEN = sys.argv[3] #"runpod" # @param {type:"string"}
GITHUB_TOKEN = sys.argv[4] #"github" # @param {type:"string"}
HF_TOKEN = sys.argv[5]

# Environment variables
runpod.api_key = RUNPOD_TOKEN
GITHUB_API_TOKEN = GITHUB_TOKEN

# Create a pod
pod = runpod.create_pod(
    name=f"Eval {MODEL.split('/')[-1]} on {BENCHMARK.capitalize()}",
    image_name="runpod/pytorch:2.0.1-py3.10-cuda11.8.0-devel-ubuntu22.04",
    gpu_type_id=GPU,
    cloud_type=CLOUD_TYPE,
    gpu_count=NUMBER_OF_GPUS,
    volume_in_gb=VOLUME_IN_GB,
    container_disk_in_gb=CONTAINER_DISK,
    template_id="au6nz6emhk",
    env={
        "BENCHMARK": BENCHMARK,
        "MODEL": MODEL,
        "REPO": REPO,
        "TRUST_REMOTE_CODE": TRUST_REMOTE_CODE,
        "DEBUG": DEBUG,
        "GITHUB_API_TOKEN": GITHUB_API_TOKEN,
        "HF_TOKEN": HF_TOKEN,
    }
)

print("Pod started: https://www.runpod.io/console/pods")
