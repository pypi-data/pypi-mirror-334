FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    build-essential \
    wget \
    git \
    curl \
    gnupg \
    software-properties-common \
    apt-transport-https \
    ca-certificates \
    lsb-release \
    pkg-config \
    python3 \
    python3-pip \
    python3-dev \
    unzip \
    tar \
    && rm -rf /var/lib/apt/lists/*

RUN wget -O - https://apt.llvm.org/llvm-snapshot.gpg.key | apt-key add - \
    && add-apt-repository "deb http://apt.llvm.org/jammy/ llvm-toolchain-jammy-16 main" \
    && apt-get update \
    && apt-get install -y \
    clang-16 \
    libomp-16-dev \
    && rm -rf /var/lib/apt/lists/*

RUN update-alternatives --remove-all cc && update-alternatives --remove-all c++ \
    && update-alternatives --install /usr/bin/clang clang /usr/bin/clang-16 100 \
    && update-alternatives --install /usr/bin/clang++ clang++ /usr/bin/clang++-16 100 \
    && update-alternatives --install /usr/bin/cc clang /usr/bin/clang-16 100 \
    && update-alternatives --install /usr/bin/c++ clang++ /usr/bin/clang++-16 100

WORKDIR /tmp

## CMake - most recent.
RUN wget https://github.com/Kitware/CMake/releases/download/v3.28.1/cmake-3.28.1-linux-x86_64.sh \
    && chmod +x cmake-3.28.1-linux-x86_64.sh \
    && ./cmake-3.28.1-linux-x86_64.sh --skip-license --prefix=/usr/local \
    && rm cmake-3.28.1-linux-x86_64.sh

## OpenMPI - most recent.
RUN apt-get update && apt-get install -y \
    openmpi-bin \
    libopenmpi-dev \
    && rm -rf /var/lib/apt/lists/*

## CUDA 12.2
RUN wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/cuda-keyring_1.1-1_all.deb \
    && dpkg -i cuda-keyring_1.1-1_all.deb \
    && apt-get update \
    && apt-get install -y cuda-toolkit-12-2 \
    && rm -rf /var/lib/apt/lists/* \
    && rm cuda-keyring_1.1-1_all.deb

RUN pip install tqdm

# Make sure we can find CUDA
ENV PATH=/usr/local/cuda-12.2/bin:${PATH}
ENV LD_LIBRARY_PATH=/usr/local/cuda-12.2/lib64:${LD_LIBRARY_PATH}

WORKDIR /workspace

# Create entrypoint script
RUN echo '#!/bin/bash\n\
echo "Development environment ready!"\n\
echo "Installed software versions:"\n\
echo "Clang: $(clang --version | head -n 1)"\n\
echo "CMake: $(cmake --version | head -n 1)"\n\
echo "CUDA: $(nvcc --version | tail -n 1)"\n\
echo "OpenMPI: $(mpirun --version | head -n 1)"\n\
echo "Python: $(python3 --version)"\n\
exec "$@"' > /entrypoint.sh \
    && chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
CMD ["/bin/bash"]
