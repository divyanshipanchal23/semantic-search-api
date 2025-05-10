import pandas as pd
from typing import List, Dict, Any, Optional
import logging
from pathlib import Path
import os

from app.core.config import settings
from app.core.models import Company

logger = logging.getLogger(__name__)

class DataProcessor:
    """
    Processor for loading and handling company data.
    """
    
    # Column name mappings between different dataset formats
    COLUMN_MAPPINGS = {
        # Original dataset.csv column names
        "Company Name": "company_name",
        "Stock Symbol": "stock_symbol",
        "Sector": "sector",
        "Company Description": "description",
        
        # newdata.csv column names
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
        # Override default data path if a new one is provided in settings
        default_data_path = settings.DATA_PATH
        # Check if newdata.csv exists and use it instead if available
        newdata_path = os.path.join(os.path.dirname(default_data_path), "newdata.csv")
        if os.path.exists(newdata_path) and data_path is None:
            logger.info(f"Found newdata.csv, using it instead of dataset.csv")
            self.data_path = newdata_path
        else:
            self.data_path = data_path or default_data_path
            
        self.raw_data = None
        self.processed_data = None
        self.companies = []
    
    def load_data(self) -> pd.DataFrame:
        """
        Load company data from CSV file.
        
        Returns:
            Pandas DataFrame containing the company data.
        """
        logger.info(f"Loading data from {self.data_path}")
        try:
            self.raw_data = pd.read_csv(self.data_path)
            logger.info(f"Successfully loaded {len(self.raw_data)} companies")
            return self.raw_data
        except Exception as e:
            logger.error(f"Error loading data: {str(e)}")
            raise
    
    def _normalize_column_names(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Normalize column names to a standard format regardless of input dataset.
        
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
    
    def process_data(self) -> List[Company]:
        """
        Process and clean the company data, creating combined text for embeddings.
        
        Returns:
            List of Company objects with processed data.
        """
        if self.raw_data is None:
            self.load_data()
        
        logger.info("Processing company data")
        
        # Clean and process data
        try:
            # Handle missing values
            self.processed_data = self.raw_data.fillna("")
            
            # Normalize column names
            self.processed_data = self._normalize_column_names(self.processed_data)
            
            # Create companies list
            self.companies = []
            
            for _, row in self.processed_data.iterrows():
                # Create combined text for semantic search
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
            return self.companies
            
        except Exception as e:
            logger.error(f"Error processing data: {str(e)}")
            raise
    
    def get_companies(self) -> List[Company]:
        """
        Get the processed company data.
        
        Returns:
            List of Company objects.
        """
        if not self.companies:
            self.process_data()
        
        return self.companies 