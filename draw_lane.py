from lane_detection import *
import grab


def add_images(img, initial_img):
    return cv2.add(initial_img, img)

def draw_lane(original_img, lane, left_color, right_color, thickness=5):
    img = np.zeros((original_img.shape[0], original_img.shape[1], 3), dtype=np.uint8)
    polygon_points = None
    offset_from_lane_edge = 8

    # draw lane lines
    if lane[0]:
        for x1, y1, x2, y2 in [lane[0]]:
            cv2.line(img, (int(x1), int(y1)), (int(x2), int(y2)), left_color, thickness)
    if lane[1]:
        for x1, y1, x2, y2 in [lane[1]]:
            cv2.line(img, (int(x1), int(y1)), (int(x2), int(y2)), right_color, thickness)

    # color the lane
    if lane[0] and lane[1]:
        lane_color = [40, 60, 0]
        for x1, y1, x2, y2 in [lane[0]]:
            p1 = (x1 + offset_from_lane_edge, y1)
            p2 = (x2 + offset_from_lane_edge, y2)

        for x1, y1, x2, y2 in [lane[1]]:
            p3 = (x2 - offset_from_lane_edge, y2)
            p4 = (x1 - offset_from_lane_edge, y1)

        polygon_points = np.array([[p1, p2, p3, p4]], np.int32)
        cv2.fillPoly(img, polygon_points, lane_color)

    return add_images(img, original_img)


def main():
    while True:
        original_img = grab.screen()
        # 1. convert to gray
        image = grayscale(crop(original_img))
        # 2. apply gaussian filter
        image = gaussian_blur(image, 7)
        # 3. canny
        image = canny(image, 50, 100)
        # 4. ROI
        image = region_of_interest(image, np.array([[(0, 190), (0, 70), (187, 0),
                                                     (613, 0), (800, 70), (800, 190)]], np.int32))
        # 5. Hough lines
        lines = hough_lines(image)
        # 6. construct lane
        lane = construct_lane(lines)
        # 7. Place lane detection output on the original image
        original_img[280:-130, :, :] = draw_lane(original_img[280:-130, :, :], lane, [0, 255, 0],
                                                 [0, 255, 0])

        cv2.imshow("Frame", original_img)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            cv2.destroyAllWindows()
            break


if __name__ == '__main__':
    main()