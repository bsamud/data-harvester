"""Pytest fixtures for benchmarks."""
import pytest
import json
from pathlib import Path

@pytest.fixture
def sample_short_text():
    """Short text for quick benchmarks."""
    return "Apple Inc. announced new products in Cupertino, California."

@pytest.fixture
def sample_medium_text():
    """Medium-length text for benchmarks."""
    return """
    Machine learning has revolutionized how we approach data analysis.
    Companies like Google, Microsoft, and Amazon are investing heavily
    in AI research. The technology is being applied across healthcare,
    finance, and manufacturing sectors. Natural language processing
    enables chatbots to understand human queries better than ever before.
    """ * 10

@pytest.fixture
def sample_long_text():
    """Long text for stress testing."""
    return """
    The field of artificial intelligence has seen remarkable progress
    in recent years. Deep learning models can now generate text that
    is nearly indistinguishable from human writing. Computer vision
    systems can identify objects with superhuman accuracy. Reinforcement
    learning agents have mastered complex games like Go and StarCraft.
    These advances have been driven by increases in computational power
    and the availability of large datasets for training.
    """ * 100

@pytest.fixture
def sample_html_text():
    """HTML text for cleaning benchmarks."""
    return """
    <html><head><title>Test</title></head>
    <body>
    <div class="content">
        <h1>Welcome to Data Harvester</h1>
        <p>This is a <strong>sample</strong> document with various HTML tags.</p>
        <ul>
            <li>Item 1</li>
            <li>Item 2</li>
            <li>Item 3</li>
        </ul>
    </div>
    </body></html>
    """ * 50

@pytest.fixture
def sample_texts_batch():
    """Batch of texts for parallel processing benchmarks."""
    base_texts = [
        "Apple Inc. is based in Cupertino.",
        "Microsoft was founded by Bill Gates.",
        "Amazon started as an online bookstore.",
        "Google dominates the search engine market.",
        "Meta owns Facebook and Instagram.",
    ]
    return base_texts * 20  # 100 texts

@pytest.fixture
def seed_articles():
    """Load seed data articles for benchmarks."""
    seed_path = Path(__file__).parent.parent / "seed_data" / "web_content" / "articles.json"
    if seed_path.exists():
        with open(seed_path) as f:
            return json.load(f)
    return []

@pytest.fixture
def training_data():
    """Sample training data for classification benchmarks."""
    texts = [
        "New smartphone release announced today",
        "Stock market reaches all-time high",
        "Local team wins championship game",
        "Scientists discover new exoplanet",
        "Recipe for homemade pasta",
    ] * 20

    labels = ["tech", "finance", "sports", "science", "food"] * 20
    return texts, labels
