from PIL import Image
import cv2

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
