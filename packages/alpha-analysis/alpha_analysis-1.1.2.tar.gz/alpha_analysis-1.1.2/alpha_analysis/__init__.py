__version__ = "0.1.0"
__author__ = "ArtemBurenok"
__email__ = "burenok023@gmail.com"

# Open Source
from .data import data_loader, data_cleaning
from .visualizations import plots, indicators
from .models import classical_models, ml_models
from .portfolio import risk_analysis, clustering
from .signal_generation import technical_signals

from .data import feature_engineering
from .models import deep_learning_models, auto_ml
from .trading import backtesting, risk_management
from .portfolio import optimization
from .signal_generation import fundamental_signals, sentiment_analysis

__all__ = [
    "data", "visualizations", "models", "portfolio", "signal_generation", "trading"
]

