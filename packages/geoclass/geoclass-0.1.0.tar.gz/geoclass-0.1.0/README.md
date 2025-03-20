# GeoClass - Land Classification and Valuation System

A Python module for satellite image classification and land valuation using machine learning.

## Features

- Satellite image classification into different land categories
- Automated land scoring based on proximity to key features
- Real estate data scraping from major property websites
- Machine learning-based land price prediction

## Installation

```bash
pip install -r requirements.txt
```

## Project Structure

```
geoclass/
├── geoclass/
│   ├── satellite/          # Satellite image processing
│   ├── scoring/            # Land scoring system
│   ├── scraper/           # Web scraping modules
│   ├── ml/                # Machine learning models
│   └── utils/             # Helper functions
├── tests/                 # Unit tests
└── examples/              # Usage examples
```

## Usage

```python
from geoclass.satellite import ImageClassifier
from geoclass.scoring import LandScorer
from geoclass.scraper import PropertyScraper
from geoclass.ml import PricePredictor

# Initialize components
classifier = ImageClassifier()
scorer = LandScorer()
scraper = PropertyScraper()
predictor = PricePredictor()

# Process satellite image
classified_image = classifier.classify("path/to/satellite_image.tif")

# Score land parcels
land_scores = scorer.score_land(classified_image)

# Scrape property data
property_data = scraper.scrape_properties(latitude, longitude)

# Predict land prices
predictions = predictor.predict(property_data, land_scores)
```

## Development

To run tests:
```bash
pytest tests/
```

## License

MIT License 