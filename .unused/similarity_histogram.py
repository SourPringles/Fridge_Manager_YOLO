import cv2
import numpy as np

def extract_features_histogram(image, bbox):
    x1, y1, x2, y2 = bbox

    roi = image[y1:y2, x1:x2]  # 관심 영역 (Region of Interest) 추출

    # 관심 영역이 너무 작으면 처리 스킵
    if roi.shape[0] < 10 or roi.shape[1] < 10:
        return {
            "color_hist": np.zeros(32*3),
            "upper_color_hist": np.zeros(32*3),
            "lower_color_hist": np.zeros(32*3),
            "edge_hist": np.zeros(9)
        }
    
    roi_resized = cv2.resize(roi, (100, 100))

    features = {}

    # 색상 히스토그램 추출
    hsv_roi = cv2.cvtColor(roi_resized, cv2.COLOR_BGR2HSV)
    h_bins, s_bins, v_bins = 32, 32, 32
    hist_full = cv2.calcHist(
        [hsv_roi], 
        [0, 1, 2], 
        None, 
        [h_bins, s_bins, v_bins], 
        [0, 180, 0, 256, 0, 256]
    )
    cv2.normalize(hist_full, hist_full, 0, 1.0, cv2.NORM_MINMAX)
    features["color_hist"] = hist_full.flatten()

    # 상,하단 색상 히스토그램 추출 (뚜껑, 용기)
    h, w = roi_resized.shape[:2]
    upper_half = roi_resized[:h//2, :]
    lower_half = roi_resized[h//2:, :]

    # 상단
    hsv_upper = cv2.cvtColor(upper_half, cv2.COLOR_BGR2HSV)
    hist_upper = cv2.calcHist(
        [hsv_upper], 
        [0, 1, 2], 
        None, 
        [h_bins, s_bins, v_bins], 
        [0, 180, 0, 256, 0, 256]
    )
    cv2.normalize(hist_upper, hist_upper, 0, 1.0, cv2.NORM_MINMAX)
    features["upper_color_hist"] = hist_upper.flatten()

    # 하단
    hsv_lower = cv2.cvtColor(lower_half, cv2.COLOR_BGR2HSV)
    hist_lower = cv2.calcHist(
        [hsv_lower], 
        [0, 1, 2], 
        None, 
        [h_bins, s_bins, v_bins], 
        [0, 180, 0, 256, 0, 256]
    )
    cv2.normalize(hist_lower, hist_lower, 0, 1.0, cv2.NORM_MINMAX)
    features["lower_color_hist"] = hist_lower.flatten()

    # 용기 형태 (edge) 히스토그램 추출
    gray = cv2.cvtColor(roi_resized, cv2.COLOR_BGR2GRAY)
    gx = cv2.Sobel(gray, cv2.CV_32F, 1, 0, ksize=3)
    gy = cv2.Sobel(gray, cv2.CV_32F, 0, 1, ksize=3)
    mag, angle = cv2.cartToPolar(gx, gy, angleInDegrees=True)

    edge_bins = 9
    edge_hist = np.zeros(edge_bins)
    
    # 강한 엣지만 고려 (노이즈 제거)
    threshold = np.mean(mag) * 2
    strong_edges = mag > threshold
    
    for i in range(edge_bins):
        bin_start = i * 20
        bin_end = (i + 1) * 20
        mask = (angle >= bin_start) & (angle < bin_end) & strong_edges
        edge_hist[i] = np.sum(mask)
    
    # 정규화
    if np.sum(edge_hist) > 0:
        edge_hist = edge_hist / np.sum(edge_hist)
    
    features["edge_hist"] = edge_hist

    return features

    
    
