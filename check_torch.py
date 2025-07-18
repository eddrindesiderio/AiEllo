try:
    import torch
    print('✅ PyTorch version:', torch.__version__)
    print('✅ CUDA available:', torch.cuda.is_available())
except ImportError:
    print('❌ PyTorch not installed')
