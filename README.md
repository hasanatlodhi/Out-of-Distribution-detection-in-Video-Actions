# Out-of-Distribution-detection-in-Video-Actions

Our ongoing project focuses on tackling the challenge of out-of-distribution detection in video actions. By utilizing the widely-used UCF101 dataset, we have implemented a robust framework using the I3d architecture to extract rich features from videos. These features are then leveraged to classify and identify unseen actions accurately.

While the project is still under development, we are committed to sharing our progress and findings with the community. You can find a demo showcasing our methodology on YouTube at the following link:
https://www.youtube.com/watch?v=047P57EPYnw

The primary goal of our project is to develop a state-of-the-art OOD detection system for video actions. We are implementing our solution using the following key components and tools:

- **I3D Architecture:** We utilize the Inflated 3D (I3D) architecture, a well-established choice for extracting spatiotemporal features from videos, enabling us to capture both motion and appearance cues effectively.

- **CuDNN:** CuDNN (CUDA Deep Neural Network Library) is a critical requirement, as it optimizes deep neural network operations and significantly accelerates computations on NVIDIA GPUs, boosting overall performance.

- **PyTorch Modules:** PyTorch serves as the foundational framework for our project. We leverage various PyTorch modules and functionalities to construct, train, and evaluate our neural network models.

- **TensorFlow:** TensorFlow, another leading deep learning framework,  utilized for model development.

- **OpenCV:** OpenCV plays a pivotal role in video preprocessing, manipulation, and feature extraction. It aids in tasks such as frame extraction, resizing, and data augmentation.

- **Selenium:** Selenium, a web automation and scraping tool, is integrated into our workflow. While its exact role might vary, it likely involves data collection, annotation, or other web-related tasks.

- **yt-dlp (YouTube-DL):** yt-dlp, a command-line tool, facilitates the extraction of videos and metadata from YouTube. This tool helps us gather video data or incorporate external video sources into our project.

## Getting Started

To get started with our project, please follow these steps:

1. **Environment Setup:** Ensure you have all the necessary dependencies installed, including CuDNN, PyTorch, TensorFlow, OpenCV, Selenium, and yt-dlp.

2. **Download the project from this link:** : https://drive.google.com/drive/folders/15pD1IW_tBW4vZCCQPUw66qvBESfIAOfT?usp=sharing
