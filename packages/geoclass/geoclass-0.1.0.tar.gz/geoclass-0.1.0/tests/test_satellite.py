"""
Tests for the satellite image classification module.
"""

import pytest
import numpy as np
from pathlib import Path
from geoclass.satellite import ImageClassifier

def test_image_classifier_initialization():
    """Test ImageClassifier initialization."""
    classifier = ImageClassifier()
    assert classifier.model is None
    assert len(classifier.class_labels) > 0
    assert "land" in classifier.class_labels

def test_preprocess_image(tmp_path):
    """Test image preprocessing."""
    # Create a dummy image file
    dummy_image = np.random.rand(100, 100, 3)
    image_path = tmp_path / "test_image.tif"
    
    # Note: This is a simplified test. In a real scenario,
    # you would need to properly create a GeoTIFF file
    with pytest.raises(RuntimeError):
        classifier = ImageClassifier()
        classifier.preprocess_image(image_path)

def test_classify_without_model():
    """Test classification without loaded model."""
    classifier = ImageClassifier()
    with pytest.raises(RuntimeError):
        classifier.classify("dummy_path.tif")

def test_save_classified_image(tmp_path):
    """Test saving classified images."""
    classifier = ImageClassifier()
    classified_masks = {
        "land": np.zeros((100, 100), dtype=np.uint8),
        "road": np.ones((100, 100), dtype=np.uint8)
    }
    
    output_path = tmp_path / "output"
    classifier.save_classified_image(classified_masks, output_path)
    
    assert output_path.exists()
    assert (output_path / "land_mask.tif").exists()
    assert (output_path / "road_mask.tif").exists() 