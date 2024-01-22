import cv2
import numpy as np
from sklearn.cluster import KMeans

def create_histogram(cluster):
    """
    Create a histogram with k clusters
    """
    num_clusters = np.arange(0, len(np.unique(cluster.labels_)) + 1)
    (histogram, _) = np.histogram(cluster.labels_, bins=num_clusters)

    histogram = histogram.astype("float")
    histogram /= histogram.sum()

    return histogram

def display_color_bar(histogram, cluster_centers):
    """
    Plot the colors in the histogram
    """
    color_bar = np.zeros((50, 300, 3), dtype="uint8")
    bar_start = 0

    for (percentage, color) in zip(histogram, cluster_centers):
        bar_end = bar_start + (percentage * 300)
        cv2.rectangle(color_bar, (int(bar_start), 0), (int(bar_end), 50),
                      color.astype("uint8").tolist(), -1)
        bar_start = bar_end

    return color_bar

def main():
    video_capture = cv2.VideoCapture(0)

    while True:
        ret, current_frame = video_capture.read()
        if not ret:
            break

        # Define the central rectangle dimensions
        frame_height, frame_width, _ = current_frame.shape
        center_x, center_y = frame_width // 2, frame_height // 2
        rectangle_width, rectangle_height = 100, 100  # Adjust size of the rectangle
        start_x, start_y = center_x - rectangle_width // 2, center_y - rectangle_height // 2
        end_x, end_y = center_x + rectangle_width // 2, center_y + rectangle_height // 2

        # Extract the central rectangle
        central_rect = current_frame[start_y:end_y, start_x:end_x]
        central_rect = central_rect.reshape((central_rect.shape[0] * central_rect.shape[1], 3))

        # Apply KMeans clustering
        kmeans_cluster = KMeans(n_clusters=1)  # We want the most dominant color
        kmeans_cluster.fit(central_rect)

        histogram = create_histogram(kmeans_cluster)
        dominant_color_bar = display_color_bar(histogram, kmeans_cluster.cluster_centers_)

        # Display the dominant color bar
        cv2.imshow("Dominant Color", dominant_color_bar)

        # Display the frame with a rectangle
        cv2.rectangle(current_frame, (start_x, start_y), (end_x, end_y), (0, 255, 0), 2)
        cv2.imshow("Video Feed", current_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()