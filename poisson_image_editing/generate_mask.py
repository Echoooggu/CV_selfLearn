import cv2
import numpy as np

def interactive_generate_mask(source_path, mask_save_path):
    source = cv2.imread(source_path)
    clone = source.copy()
    mask = np.zeros(source.shape[:2], dtype=np.uint8)
    points = []
    drawing = False

    def draw_mask(event, x, y, flags, param):
        nonlocal drawing, points
        if event == cv2.EVENT_LBUTTONDOWN:
            drawing = True
            points = [(x, y)]
            cv2.circle(clone, (x, y), 2, (0, 0, 255), -1)
        elif event == cv2.EVENT_MOUSEMOVE and drawing:
            points.append((x, y))
            cv2.line(clone, points[-2], points[-1], (0, 0, 255), 2)
            cv2.line(mask, points[-2], points[-1], 255, 2)
        elif event == cv2.EVENT_LBUTTONUP:
            drawing = False
            points.append((x, y))
            cv2.line(clone, points[-2], points[-1], (0, 0, 255), 2)
            cv2.line(mask, points[-2], points[-1], 255, 2)
            cv2.line(clone, points[-1], points[0], (0, 0, 255), 2)
            cv2.line(mask, points[-1], points[0], 255, 2)

            # 自动填充轮廓内部
            # 使用多边形填充掩码
            cv2.fillPoly(mask, [np.array(points)], 255)
            print("✅ 掩码绘制完成，按 's' 保存，或 'r' 重画")

    cv2.namedWindow('Draw Mask')
    cv2.startWindowThread()

    cv2.setMouseCallback('Draw Mask', draw_mask)

    while True:
        cv2.imshow('Draw Mask', clone)
        cv2.imshow('Mask Preview', mask)
        key = cv2.waitKey(10) & 0xFF

        if key == ord('s'):
            cv2.imwrite(mask_save_path, mask)
            print(f"✅ 掩码已保存至 {mask_save_path}")
            break
        elif key == ord('r'):
            clone = source.copy()
            mask[:] = 0
            print("🔁 重置绘制")
        elif key == ord('q'):# Ctrl+q的ASCII码
            print("❌ 用户取消绘制")
            break

    cv2.destroyAllWindows()