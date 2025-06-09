import torch
import os
import sys
from tqdm import tqdm

def download_stable_diffusion_upscaler():
    """
    StableDiffusionUpscalePipeline 모델을 미리 다운로드합니다.
    """
    print("Starting to download Stable Diffusion Upscaler model...")
    
    try:
        from diffusers import StableDiffusionUpscalePipeline
        
        # CUDA 가용성 확인
        device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Available device: {device}")
        
        # CUDA 버전 정보 출력 (CUDA 사용 가능한 경우)
        if device == "cuda":
            print(f"CUDA version: {torch.version.cuda}")
            print(f"Installed PyTorch CUDA version: {torch.version.cuda}")
        
        # 모델 다운로드 진행 상태 표시
        print("Downloading model... (This may take a few minutes)")
        
        # 모델 다운로드 및 로드
        model_id = "stabilityai/stable-diffusion-x4-upscaler"
        revision = "fp16" if torch.cuda.is_available() else "main"
        dtype = torch.float16 if torch.cuda.is_available() else torch.float32
        
        model = StableDiffusionUpscalePipeline.from_pretrained(
            model_id,
            torch_dtype=dtype,
            revision=revision
        )
        
        # VAE scaling_factor 설정
        model.vae.config.scaling_factor = 0.08333
        
        # 모델을 장치로 이동
        model = model.to(device)
        
        # 간단한 테스트 실행 (빈 이미지로)
        print("Running test initialization for the model...")
        from PIL import Image
        import numpy as np
        
        # 간단한 더미 이미지 생성 (8x8 검은색 이미지)
        test_image = Image.fromarray(np.zeros((8, 8, 3), dtype=np.uint8))
        
        with torch.no_grad():
            try:
                # 무시할 경고가 있으므로 실제 추론은 하지 않고 모델만 초기화
                model.unet(torch.zeros((1, 4, 8, 8), device=device, dtype=dtype))
                print("Model initialization complete")
            except Exception as e:
                print(f"Error during test run: {e}")
        
        print("Stable Diffusion Upscaler model download and initialization completed!")
        return True
        
    except Exception as e:
        print(f"Error during model download: {e}")
        print("\nPlease check if the following packages are installed:")
        print("- torch (with CUDA support)")
        print("- diffusers")
        print("- transformers")
        print("- accelerate")
        return False

def check_dependencies():
    """
    필요한 의존성 패키지가 설치되어 있는지 확인합니다.
    """
    required_packages = ["torch", "diffusers", "transformers", "accelerate", "tqdm"]
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("The following packages are not installed:")
        for package in missing_packages:
            print(f"- {package}")
        print("\nYou can install the required packages with the following command:")
        print(f"pip install {' '.join(missing_packages)}")
        
        # PyTorch CUDA 버전 안내
        if "torch" in missing_packages:
            print("\nTo install PyTorch, use the following command:")
            print("pip install torch==2.6.0 torchvision==0.21.0")
            
            print("\nIf you want using CUDA, use the following command:")
            print("pip install torch==2.6.0+cu124 torchvision==0.21.0+cu124 --index-url https://download.pytorch.org/whl/cu124")

            
        return False
    return True

if __name__ == "__main__":
    print("Running AI model download script.")
    
    if not check_dependencies():
        print("Please install the required dependency packages first.")
        sys.exit(1)
    
    success = download_stable_diffusion_upscaler()
    
    if success:
        print("All models have been successfully downloaded.")
    else:
        print("There was a problem downloading the models. Please check the logs.")