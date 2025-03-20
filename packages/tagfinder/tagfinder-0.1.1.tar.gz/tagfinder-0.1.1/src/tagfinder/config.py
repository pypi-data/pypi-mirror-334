"""
Configuration management for image tag helper.
"""
import os
import json


class Config:
    """Configuration manager for image tag helper."""
    
    def __init__(self):
        """Initialize configuration."""
        self.config_dir = os.path.expanduser("~/.tagfinder")
        self.config_file = os.path.join(self.config_dir, "config.json")
        self.aliases = {}
        self.default_profile = None
        self._load_config()
    
    def _load_config(self):
        """Load configuration from file."""
        if not os.path.exists(self.config_dir):
            os.makedirs(self.config_dir)
        
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                    self.aliases = config.get('aliases', {})
                    self.default_profile = config.get('default_profile')
            except (json.JSONDecodeError, IOError) as e:
                print(f"Error loading config: {e}")
                self.aliases = {}
                self.default_profile = None
    
    def _save_config(self):
        """Save configuration to file."""
        config = {
            'aliases': self.aliases,
            'default_profile': self.default_profile
        }
        
        try:
            with open(self.config_file, 'w') as f:
                json.dump(config, f, indent=2)
        except IOError as e:
            print(f"Error saving config: {e}")
    
    def set_alias(self, alias, registry, repository):
        """
        Set an alias for a registry and repository combination.
        
        Args:
            alias: Alias name
            registry: Registry URL
            repository: Repository path
        """
        self.aliases[alias] = {
            'registry': registry,
            'repository': repository
        }
        self._save_config()
    
    def get_alias(self, alias):
        """
        Get registry and repository for an alias.
        
        Args:
            alias: Alias name
            
        Returns:
            Tuple of (registry, repository) or (None, None) if alias not found
        """
        if alias in self.aliases:
            return (
                self.aliases[alias]['registry'],
                self.aliases[alias]['repository']
            )
        return None, None
    
    def remove_alias(self, alias):
        """
        Remove an alias.
        
        Args:
            alias: Alias name
        
        Returns:
            True if alias was removed, False if it didn't exist
        """
        if alias in self.aliases:
            del self.aliases[alias]
            self._save_config()
            return True
        return False
    
    def list_aliases(self):
        """
        List all aliases.
        
        Returns:
            Dictionary of aliases
        """
        return self.aliases
    
    def set_default_profile(self, alias):
        """
        Set the default profile.
        
        Args:
            alias: Alias name to set as default
            
        Returns:
            bool: True if successful, False if alias doesn't exist
        """
        if alias in self.aliases:
            self.default_profile = alias
            self._save_config()
            return True
        return False
    
    def get_default_profile(self):
        """
        Get the default profile.
        
        Returns:
            Tuple of (registry, repository) or (None, None) if no default set
        """
        if self.default_profile and self.default_profile in self.aliases:
            return (
                self.aliases[self.default_profile]['registry'],
                self.aliases[self.default_profile]['repository']
            )
        return None, None


# Create a singleton instance
config = Config()
