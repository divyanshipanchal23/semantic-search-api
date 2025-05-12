import pandas as pd
from typing import List, Dict, Any, Optional
import logging
from pathlib import Path

from app.core.config import settings
from app.core.models import Company

logger = logging.getLogger(__name__)

class DataProcessor:
    """
    Processor for loading company metadata from CSV.
    Simplified to focus only on essential functionality.
    """
    
    # Column name mappings for newdata.csv
    COLUMN_MAPPINGS = {
        "name": "company_name",
        "symbol": "stock_symbol",
        "sector": "sector",
        "description": "description"
    }
    
    def __init__(self, data_path: Optional[str] = None):
        """
        Initialize the data processor.
        
        Args:
            data_path: Path to the CSV data file. If None, uses default from settings.
        """
        self.data_path = data_path or settings.DATA_PATH
        self.companies = []
    
    def get_companies(self) -> List[Company]:
        """
        Load and process company data from CSV file.
        
        Returns:
            List of Company objects.
        """
        if not self.companies:
            logger.info(f"Loading data from {self.data_path}")
            try:
                # Load CSV data
                raw_data = pd.read_csv(self.data_path)
                logger.info(f"Successfully loaded {len(raw_data)} companies")
                
                # Handle missing values
                processed_data = raw_data.fillna("")
                
                # Normalize column names
                processed_data = self._normalize_column_names(processed_data)
                
                # Create companies list
                self.companies = []
                
                for _, row in processed_data.iterrows():
                    # Create combined text for semantic search (used by data_embedding_setup.py)
                    combined_text = f"{row['company_name']} {row['stock_symbol']} {row['sector']} {row['description']}"
                    
                    # Create company object
                    company = Company(
                        company_name=row['company_name'],
                        stock_symbol=row['stock_symbol'],
                        sector=row['sector'],
                        description=row['description'],
                        combined_text=combined_text
                    )
                    
                    self.companies.append(company)
                
                logger.info(f"Successfully processed {len(self.companies)} companies")
            except Exception as e:
                logger.error(f"Error processing data: {str(e)}")
                raise
        
        return self.companies
    
    def _normalize_column_names(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Normalize column names to a standard format.
        
        Args:
            df: DataFrame with original column names
            
        Returns:
            DataFrame with normalized column names
        """
        column_mapping = {}
        for col in df.columns:
            if col in self.COLUMN_MAPPINGS:
                column_mapping[col] = self.COLUMN_MAPPINGS[col]
        
        if column_mapping:
            return df.rename(columns=column_mapping)
        return df 