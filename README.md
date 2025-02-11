
## Overview
This repository focuses on **Out-of-Distribution (OOD) detection** in video action recognition. We propose a novel loss function designed to effectively separate unseen actions from seen ones, enhancing the robustness of action recognition models.

Our model is trained on the **UCF101 dataset**, achieving:
- **93% accuracy** for seen data
- **80%+ accuracy** for unseen data

The model utilizes **I3D (Inflated 3D Convolutional Network) feature extraction** from videos, incorporating both **RGB and optical flow** inputs.

For a detailed explanation of the methodology, training process, and results, refer to our research paper:  
[Read the Research Paper](https://d197for5662m48.cloudfront.net/documents/publicationstatus/174932/preprint_pdf/b99f44959e71e8336d6252c68b80df16.pdf)

---

## Features
✔️ **Custom Loss Function** – Ensures effective separation of unseen data from seen classes.  
✔️ **State-of-the-Art Model** – Uses I3D-based feature extraction for superior action recognition.  
✔️ **Pre-trained Weights Available** – Trained on the UCF101 dataset.  
✔️ **Web Application Interface** – Allows users to:
   - Provide YouTube & Facebook video links.
   - Automatically extract and process videos.
   - Perform action recognition and classify actions.
   - Identify unseen actions using our OOD detection approach.

---

