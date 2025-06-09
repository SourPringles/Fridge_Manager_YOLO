# Base Libraries

# Libraries
from PIL import Image
import cv2
# Custom Modules


def convert_cv2_to_pil(image):
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    pil_image = Image.fromarray(rgb_image)

    return pil_image

# bbox = [x_min, y_min, x_max, y_max]
def crop_object(image, bbox):
    """
    openCV 이미지 객체를 PIL객체로 변환 후 bbox 영역을 잘라내는 함수
    - image: OpenCV 이미지 객체
    - bbox: 잘라낼 영역의 바운딩 박스 (x_min, y_min, x_max, y_max)
    - 반환값: 잘라낸 이미지 (PIL 객체)
    """
    # OpenCV 이미지를 RGB로 변환 (OpenCV는 BGR 포맷을 사용하므로)
    pil_image = convert_cv2_to_pil(image)

    cropped = pil_image.crop(bbox)
    return cropped

def enhance_image_quality(image, outscale=4):
    """
    생성형 AI를 활용한 초해상화 (최신 huggingface_hub API 사용)
    
    Args:
        image: PIL 이미지
        outscale: 출력 이미지의 스케일 배율 (기본값: 4)
    
    Returns:
        PIL.Image: 향상된 이미지
    """
    try:
        import torch
        from PIL import Image
        
        # 이미지 크기 확인
        if image.width * image.height > 1024 * 1024:
            # 큰 이미지의 경우 기본 방식으로 처리
            return image.resize((int(image.width * outscale), int(image.height * outscale)), Image.LANCZOS)
        
        # 디바이스 선택
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        
        # 모델 로드 (처음 실행 시 다운로드됨)
        if not hasattr(enhance_image_quality, 'model_loaded'):
            try:
                import diffusers
                from diffusers import StableDiffusionUpscalePipeline
                
                # huggingface_hub 최신 버전 대응
                enhance_image_quality.model = StableDiffusionUpscalePipeline.from_pretrained(
                    "stabilityai/stable-diffusion-x4-upscaler", 
                    torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
                    revision="fp16" if torch.cuda.is_available() else "main"
                )
                # VAE scaling_factor 수정
                enhance_image_quality.model.vae.config.scaling_factor = 0.08333
                enhance_image_quality.model = enhance_image_quality.model.to(device)
                enhance_image_quality.model_loaded = True
                print("초해상화 AI 모델 로드 완료")
            except Exception as e:
                print(f"AI 모델 로드 실패: {e}")
                # 모델 로드 실패 시 기본 방식으로 대체
                return image.resize((int(image.width * outscale), int(image.height * outscale)), Image.LANCZOS)
        
        # 이미지 크기가 지원 범위인지 확인하고 조정
        if image.width > 512 or image.height > 512:
            # 모델 입력 크기 제한으로 인해 리사이징
            # aspect_ratio = image.width / image.height
            # if aspect_ratio > 1:
            #     new_width = 512
            #     new_height = int(512 / aspect_ratio)
            # else:
            #     new_height = 512
            #     new_width = int(512 * aspect_ratio)
            # image = image.resize((new_width, new_height), Image.LANCZOS)

            # 이미지 해상도가 정상이라면 기존 크기 유지
            return image
        
        # 생성형 AI로 업스케일링
        prompt = "high resolution, detailed image"
        
        with torch.no_grad():
            upscaled = enhance_image_quality.model(
                prompt=prompt,
                image=image,
                noise_level=5,
                num_inference_steps=20,
            ).images[0]
        
        return upscaled
        
    except Exception as e:
        print(f"생성형 AI 초해상화 중 오류 발생: {e}")
        # 오류 발생 시 기본 방식으로 대체
        return image.resize((int(image.width * outscale), int(image.height * outscale)), Image.LANCZOS)
    
def enhance_image_quality_consistent(image, outscale=4, seed=42):
    """
    일관된 결과를 생성하는 초해상화 함수
    
    Args:
        image: PIL 이미지
        outscale: 출력 이미지의 스케일 배율 (기본값: 4)
        seed: 결과 일관성을 위한 시드값 (기본값: 42)
    
    Returns:
        PIL.Image: 향상된 이미지
    """
    try:
        import torch
        from PIL import Image
        
        # 이미지 크기 확인
        if image.width * image.height > 1024 * 1024:
            return image.resize((int(image.width * outscale), int(image.height * outscale)), Image.LANCZOS)
        
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        print(f"Using device: {device}")
        
        # 모델 로드 (처음 실행 시 다운로드됨)
        if not hasattr(enhance_image_quality_consistent, 'model_loaded'):
            try:
                import diffusers
                from diffusers import StableDiffusionUpscalePipeline
                
                enhance_image_quality_consistent.model = StableDiffusionUpscalePipeline.from_pretrained(
                    "stabilityai/stable-diffusion-x4-upscaler", 
                    torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
                    use_auth_token=False,
                    revision="fp16" if torch.cuda.is_available() else "main"
                )
                enhance_image_quality_consistent.model.vae.config.scaling_factor = 0.08333
                enhance_image_quality_consistent.model = enhance_image_quality_consistent.model.to(device)
                enhance_image_quality_consistent.model_loaded = True
                print("일관된 초해상화 AI 모델 로드 완료")
            except Exception as e:
                print(f"AI 모델 로드 실패: {e}")
                return image.resize((int(image.width * outscale), int(image.height * outscale)), Image.LANCZOS)
        
        # 이미지 크기 제한 확인
        if image.width > 512 or image.height > 512:
            return image
        
        # 시드 설정으로 일관성 유지
        generator = torch.Generator(device).manual_seed(seed)
        
        # 생성형 AI로 업스케일링
        prompt = "high resolution, detailed image"
        
        with torch.no_grad():
            upscaled = enhance_image_quality_consistent.model(
                prompt=prompt,
                image=image,
                noise_level=5,
                num_inference_steps=20,
                generator=generator,  # 시드가 적용된 생성기 사용
            ).images[0]
        
        return upscaled
        
    except Exception as e:
        print(f"생성형 AI 초해상화 중 오류 발생: {e}")
        return image.resize((int(image.width * outscale), int(image.height * outscale)), Image.LANCZOS)

# 모델 로딩딩
def preload_models():
    print("초해상화 모델을 미리 로드 중...")
    dummy_image = Image.new('RGB', (128, 128), color='white')
    _ = enhance_image_quality_consistent(dummy_image)
    print("모델 미리 로드 완료")


def generate_food_name(image):
    """이미지를 분석하여 반찬 이름을 자동으로 생성
    
    Args:
        image: PIL Image 객체 또는 이미지 경로 문자열
    
    Returns:
        str: 생성된 반찬 이름
    """
    from openai import OpenAI
    import base64
    import io
    import os

    # API 키 설정
    client = OpenAI(api_key="your_openai_api_key_here")  # OpenAI API 키를 여기에 입력하세요
    
    # 이미지 타입 확인 및 처리
    if isinstance(image, str) and os.path.isfile(image):
        # 파일 경로인 경우
        with open(image, "rb") as image_file:
            image_bytes = image_file.read()
    elif hasattr(image, 'save'):
        # PIL Image 객체인 경우
        with io.BytesIO() as image_buffer:
            image.save(image_buffer, format="JPEG")
            image_bytes = image_buffer.getvalue()
    else:
        raise TypeError("지원되지 않는 이미지 타입입니다. PIL Image 객체 또는 이미지 파일 경로를 제공해주세요.")
    
    # 이미지를 base64로 인코딩
    base64_image = base64.b64encode(image_bytes).decode('utf-8')
    
    # API 요청
    try:
        response = client.chat.completions.create(
            model="gpt-4.1",
            messages=[
                {"role": "system", "content": "당신은 식재료 전문가 입니다."},
                {"role": "system", "content": "제공된 이미지는 조리된 음식과 조리되지 않은 식재료가 포함되어 있습니다."},
                {"role": "system", "content": "답변은 '김치', '버섯', '토마토'와 같이 한국어로 정확한 식재료,반찬 이름만 간결하게 작성하세요."},
                {"role": "system", "content": "확실하지 않은 경우에는 가장 유사한 하나의 식재료 이름을 제시하되, 가능한 정확하게 답변하세요."},
                {"role": "user", "content": [{"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}]}
            ],
            max_tokens=50,
            temperature=0.2
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"식재료 이름 생성 중 오류 발생: {e}")
        return "알 수 없는 식재료"