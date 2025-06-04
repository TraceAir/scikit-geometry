#!/bin/sh
# Script to build scikit-geometry wheel inside the Docker container

set -xe  # Exit on error

echo "Starting scikit-geometry wheel build process..."

# Build scikit-geometry wheel
echo "Building scikit-geometry wheel..."
python3.${PYTHON_VERSION_MINOR} setup.py build_ext --inplace

# Run unit tests
echo "Running unit tests..."
python3.${PYTHON_VERSION_MINOR} -m pytest test -v

# Build the wheel
echo "Building the wheel..."
python3.${PYTHON_VERSION_MINOR} setup.py bdist_wheel
auditwheel repair dist/skgeom-*.whl -w dist/

# Copy wheel to output directory
echo "Copying wheel to output directory..."
cp dist/*.whl /app/output/
chown -R "${USER_GROUP}" /app/output/*
echo "✅ scikit-geometry wheel built successfully!"
echo "Wheel file is available in the mounted output directory"

#If arguments are passed to the script, execute them
if [ $# -gt 0 ]; then
    exec "$@"
else
    # Keep container running if no arguments
    echo "Container will now exit. Mount the output directory to access the wheel file."
fi