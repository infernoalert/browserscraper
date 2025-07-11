"""
Configuration management for browser scraper
"""

import json
import os
from typing import Dict, Any, Optional
from dataclasses import dataclass, asdict


@dataclass
class BrowserConfig:
    """Browser configuration settings"""
    browser_type: str = "chrome"
    headless: bool = False
    window_size: tuple = (1200, 800)
    implicit_wait: int = 10
    page_load_timeout: int = 30
    disable_gpu: bool = True
    disable_images: bool = False
    user_agent: Optional[str] = None


@dataclass
class ScrapingConfig:
    """Scraping configuration settings"""
    default_delay: float = 1.0
    retry_attempts: int = 3
    retry_delay: float = 2.0
    respect_robots_txt: bool = True
    max_pages: int = 100


@dataclass
class OutputConfig:
    """Output configuration settings"""
    output_dir: str = "output"
    output_format: str = "json"  # json, csv, xml
    filename_prefix: str = "scraped_data"
    include_timestamp: bool = True
    create_backup: bool = True


@dataclass
class AppConfig:
    """Main application configuration"""
    browser: BrowserConfig
    scraping: ScrapingConfig
    output: OutputConfig
    log_level: str = "INFO"
    log_file: str = "scraper.log"
    
    
class ConfigManager:
    """Manages configuration loading and saving"""
    
    def __init__(self, config_file: str = "config.json"):
        self.config_file = config_file
        self.config = self._load_config()
    
    def _load_config(self) -> AppConfig:
        """Load configuration from file or create default"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    data = json.load(f)
                return self._dict_to_config(data)
            except Exception as e:
                print(f"Warning: Could not load config file {self.config_file}: {e}")
                print("Using default configuration")
        
        return self._create_default_config()
    
    def _create_default_config(self) -> AppConfig:
        """Create default configuration"""
        return AppConfig(
            browser=BrowserConfig(),
            scraping=ScrapingConfig(),
            output=OutputConfig()
        )
    
    def _dict_to_config(self, data: Dict[str, Any]) -> AppConfig:
        """Convert dictionary to configuration object"""
        browser_data = data.get('browser', {})
        scraping_data = data.get('scraping', {})
        output_data = data.get('output', {})
        
        return AppConfig(
            browser=BrowserConfig(**browser_data),
            scraping=ScrapingConfig(**scraping_data),
            output=OutputConfig(**output_data),
            log_level=data.get('log_level', 'INFO'),
            log_file=data.get('log_file', 'scraper.log')
        )
    
    def save_config(self) -> None:
        """Save current configuration to file"""
        try:
            config_dict = asdict(self.config)
            with open(self.config_file, 'w') as f:
                json.dump(config_dict, f, indent=2)
        except Exception as e:
            print(f"Warning: Could not save config file {self.config_file}: {e}")
    
    def get_config(self) -> AppConfig:
        """Get current configuration"""
        return self.config
    
    def update_config(self, **kwargs) -> None:
        """Update configuration with new values"""
        for key, value in kwargs.items():
            if hasattr(self.config, key):
                setattr(self.config, key, value)
    
    def create_default_config_file(self) -> None:
        """Create a default configuration file"""
        default_config = self._create_default_config()
        self.config = default_config
        self.save_config()
        print(f"Created default configuration file: {self.config_file}")


# Global configuration instance
config_manager = ConfigManager() 