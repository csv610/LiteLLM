"""
Storage Configuration - Centralized LMDB Storage Settings

This module provides a unified StorageConfig dataclass for managing database
storage settings across all modules. Instead of duplicating db_path, db_capacity_mb,
db_store, and db_overwrite in every module's config, modules can now inherit
from or compose StorageConfig.

USAGE:
    from medkit.utils.storage_config import StorageConfig
    from dataclasses import dataclass, field

    @dataclass
    class MedicineInfoConfig(StorageConfig):
        '''Config for medicine info module'''
        verbosity: bool = False
        prompt_style: str = "DETAILED"
        # Inherits: db_path, db_capacity_mb, db_store, db_overwrite

    # Or use composition:
    @dataclass
    class DiseaseInfoConfig:
        storage: StorageConfig = field(default_factory=StorageConfig)
        verbosity: bool = False
"""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional


@dataclass
class StorageConfig:
    """
    Centralized configuration for LMDB database storage.

    This class eliminates duplication of db_path, db_capacity_mb, db_store,
    and db_overwrite across all modules. Each module's Config can inherit
    from StorageConfig or include it as a field.

    Attributes:
        db_path: Path to LMDB database file. Auto-generated per module based on
            __file__ location. Can be overridden.
        db_capacity_mb: Maximum database capacity in MB. Default: 500MB
        db_store: Whether to cache results in database. Default: True (enabled)
        db_overwrite: If True, overwrite existing cached entries.
            If False, use cached entry if exists. Default: False
    """

    db_path: Optional[str] = None
    db_capacity_mb: int = 500
    db_store: bool = True
    db_overwrite: bool = False

    def __post_init__(self):
        """Validate configuration after initialization."""
        if self.db_capacity_mb <= 0:
            raise ValueError("db_capacity_mb must be greater than 0")
        if not isinstance(self.db_store, bool):
            raise ValueError("db_store must be a boolean")
        if not isinstance(self.db_overwrite, bool):
            raise ValueError("db_overwrite must be a boolean")

    @classmethod
    def for_module(cls, module_name: str) -> "StorageConfig":
        """
        Create StorageConfig with auto-generated db_path for a module.

        Args:
            module_name: Name of the module (e.g., "medicine_info", "disease_info")

        Returns:
            StorageConfig with db_path set to: medkit/storage/{module_name}.lmdb
        """
        db_path = str(
            Path(__file__).parent.parent / "storage" / f"{module_name}.lmdb"
        )
        return cls(db_path=db_path)
