from typing import List, Optional, Dict, Any

from pydantic import BaseModel

from shops_nocodb_updater.models.base import NocodbModel
from shops_nocodb_updater.models.mapping import ModelMapper, format_image_data


class ImageMetadata(BaseModel):
    """
    Model for image metadata.
    """
    url: str
    title: str
    mimetype: str
    signedUrl: Optional[str] = None


class CategoryModel(NocodbModel):
    """
    Model for categories in NocoDB.
    """
    __tableid__: str = "category_table_id"  # Replace with actual table ID
    __skip_update_attributes__: List[str] = ["CreatedAt", "UpdatedAt"]
    
    id: str
    name: str
    parent_category: Optional[List[Dict[str, Any]]] = None
    preview_url: Optional[str] = None
    images: Optional[List[ImageMetadata]] = None


class CategoryMapper(ModelMapper):
    """
    Mapper for CategoryModel.
    Handles transformations between external data and NocoDB format.
    """
    
    def __init__(self, language: str = "en"):
        """
        Initialize the category mapper.
        
        Args:
            language: The language code for category fields
        """
        super().__init__(CategoryModel)
        self.language = language
        
        # Define field mappings based on language
        self.field_mappings = {
            "name": f"name_{language}",
            "parent_category": f"parent_category_{language}",
            "preview_url": f"image_{language}",
        }
        
    def map_to_nocodb(self, external_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Map external category data to NocoDB format.
        
        Args:
            external_data: External category data
            
        Returns:
            Mapped data for NocoDB
        """
        nocodb_data = {}
        
        # Map standard fields
        for external_field, nocodb_field in self.field_mappings.items():
            if external_field in external_data and external_data[external_field] is not None:
                if external_field == "preview_url" and external_data[external_field]:
                    # Format image URL
                    nocodb_data[nocodb_field] = [format_image_data(external_data[external_field])]
                else:
                    nocodb_data[nocodb_field] = external_data[external_field]
        
        # Include ID field
        if "id" in external_data:
            nocodb_data["id"] = external_data["id"]
            
        return nocodb_data
    
    def map_from_nocodb(self, nocodb_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Map NocoDB category data to external format.
        
        Args:
            nocodb_data: NocoDB category data
            
        Returns:
            Mapped data for external use
        """
        external_data = {
            "id": nocodb_data.get("Id") or nocodb_data.get("id"),
            "name": nocodb_data.get(self.field_mappings["name"], ""),
            "parent_category": nocodb_data.get(self.field_mappings["parent_category"], []),
        }
        
        # Handle image URL
        preview_url = ""
        images = []
        
        if self.field_mappings["preview_url"] in nocodb_data and nocodb_data[self.field_mappings["preview_url"]]:
            image_data = nocodb_data[self.field_mappings["preview_url"]][0]
            if image_data.get("signedUrl", ""):
                preview_url = image_data["signedUrl"]
                images.append(ImageMetadata(**image_data))
            else:
                preview_url = image_data.get("url", "")
                if preview_url:
                    images.append(ImageMetadata(**image_data))
                
        external_data["preview_url"] = preview_url
        external_data["images"] = images
            
        return external_data
        
    def parse_category_id(self, data: dict) -> str:
        """
        Parse category ID from NocoDB data.
        
        Args:
            data: NocoDB category data
            
        Returns:
            Category ID as string
        """
        return str(data.get("Id") or data.get("id", "")) 