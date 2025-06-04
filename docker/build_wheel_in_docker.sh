#!/bin/bash
# Script to build scikit-geometry wheel using Docker
# Usage: ./build_wheel_in_docker.sh [output_path] [--python_version_minor <version>] [--cgal_version_tag <tag>]

set -xe  # Exit on error

# Default values
PYTHON_VERSION_MINOR="10"  # Default Python minor version
CGAL_VERSION_TAG="v5.6"  # Default CGAL version tag
OUTPUT_PATH="./output"     # Default output path

# Display usage information
function show_usage {
    echo "Usage: $0 [output_path] [--python_version_minor <version>] [--cgal_version_tag <tag>]"
    echo ""
    echo "Arguments:"
    echo "  output_path           Path for output wheel files (default: ./output)"
    echo "  --python_version_minor  Python minor version (default: 10 for Python 3.10)"
    echo "  --cgal_version_tag      CGAL version tag (default: v5.6)"
    echo ""
    exit 1
}

# Check if help is requested
if [[ "$1" == "--help" || "$1" == "-h" ]]; then
    show_usage
fi

# Check if the first argument is a path or an option
if [[ "$1" != "--"* && -n "$1" ]]; then
    OUTPUT_PATH="$1"
    shift
fi

# Parse optional named arguments
while [[ $# -gt 0 ]]; do
    case "$1" in
        --python_version_minor)
            PYTHON_VERSION_MINOR="$2"
            shift 2
            ;;
        --cgal_version_tag)
            CGAL_VERSION_TAG="$2"
            shift 2
            ;;
        *)
            echo "❌ Error: Invalid argument $1"
            show_usage
            ;;
    esac
done

# Create output directory if it doesn't exist
mkdir -p "$OUTPUT_PATH"

echo "Building scikit-geometry builder Docker image..."
docker build \
    --build-arg PYTHON_VERSION_MINOR="$PYTHON_VERSION_MINOR" \
    --build-arg CGAL_VERSION_TAG="$CGAL_VERSION_TAG" \
    -t scikit-geometry-builder .. -f ./Dockerfile-buildwheel

echo "Building scikit-geometry wheel..."
docker run --rm -it \
    -e USER_GROUP="$(id -u):$(id -g)" \
    -e PYTHON_VERSION_MINOR="$PYTHON_VERSION_MINOR" \
    -v "$OUTPUT_PATH:/app/output" \
    scikit-geometry-builder

if [ $? -eq 0 ]; then
    echo "✅ scikit-geometry wheel built successfully!"
    echo "Wheel file is available in: $OUTPUT_PATH"
    echo ""
    echo "Build completed with:"
    echo "  Python version minor: $PYTHON_VERSION_MINOR"
    echo "  CGAL version tag:     $CGAL_VERSION_TAG"
    echo "  Output path:          $OUTPUT_PATH"
else
    echo "❌ Build failed. Please check the error messages above."
    exit 1
fi
