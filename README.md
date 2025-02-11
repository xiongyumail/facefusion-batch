```bash 
conda create --name facefusion python=3.12
conda activate facefusion
conda install conda-forge::openvino=2025.0.0
python install.py --onnxruntime openvino --skip-conda
python facefusion.py run --execution-providers openvino --ui-layouts benchmark
```