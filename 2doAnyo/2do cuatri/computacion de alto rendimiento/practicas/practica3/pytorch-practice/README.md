# PyTorch Practice

This project demonstrates the performance comparison between CPU and GPU when processing images using a pre-trained ResNet18 model in PyTorch.

## Project Structure

```
pytorch-practice
├── src
│   └── practica_cpu_vs_gpu.py  # Main code for the practice
├── requirements.txt             # Required Python libraries
└── README.md                    # Project documentation
```

## Setup Instructions

1. **Clone the repository** (if applicable):
   ```
   git clone <repository-url>
   cd pytorch-practice
   ```

2. **Create a virtual environment** (optional but recommended):
   ```
   python -m venv venv
   ```

3. **Activate the virtual environment**:
   - On Windows:
     ```
     .\venv\Scripts\activate
     ```
   - On Linux or Mac:
     ```
     source venv/bin/activate
     ```

4. **Install the required libraries**:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Place your input image in the `src` directory or modify the path in `practica_cpu_vs_gpu.py` to point to your image.
2. Run the main script:
   ```
   python src/practica_cpu_vs_gpu.py
   ```

## Additional Notes

- Ensure you have a compatible GPU with CUDA installed for optimal performance.
- The project can be run on CPU, but using a GPU is recommended for faster processing times.
- Refer to the documentation of the libraries used for more detailed information on their functionalities.