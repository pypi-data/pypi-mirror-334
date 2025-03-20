from typing import List, Optional, Dict, Any

from pydantic import BaseModel, HttpUrl

from shops_nocodb_updater.models.base import NocodbModel
from shops_nocodb_updater.models.mapping import ModelMapper, format_image_list


class ExtraAttribute(BaseModel):
    """
    Model for product extra attributes.
    """
    name: str
    description: str


class ProductModel(NocodbModel):
    """
    Model for products in NocoDB.
    """
    __tableid__: str = "product_table_id"  # Replace with actual table ID
    __skip_update_attributes__: List[str] = ["CreatedAt", "UpdatedAt"]
    
    id: str
    name: str
    description: Optional[str] = ""
    price: float
    currency: str = "USD"
    stock_qty: int = 0
    final_price: Optional[float] = None
    preview_url: List[str] = []
    extra_attributes: Optional[List[ExtraAttribute]] = None


class ProductMapper(ModelMapper):
    """
    Mapper for ProductModel.
    Handles transformations between external data and NocoDB format.
    """
    
    def __init__(self, language: str = "en"):
        """
        Initialize the product mapper.
        
        Args:
            language: The language code for product fields
        """
        super().__init__(ProductModel)
        self.language = language
        
        # Define field mappings based on language
        self.field_mappings = {
            "name": f"name_{language}",
            "description": f"description_{language}",
            "price": f"price_{language}",
            "currency": f"currency_{language}",
            "stock_qty": f"stock_qty_{language}",
            "final_price": f"final_price_{language}",
            "preview_url": f"images_{language}",
        }
        
    def map_to_nocodb(self, external_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Map external product data to NocoDB format.
        
        Args:
            external_data: External product data
            
        Returns:
            Mapped data for NocoDB
        """
        nocodb_data = {}
        
        # Map standard fields
        for external_field, nocodb_field in self.field_mappings.items():
            if external_field in external_data:
                if external_field == "preview_url" and external_data[external_field]:
                    # Format image URLs
                    nocodb_data[nocodb_field] = format_image_list(external_data[external_field])
                else:
                    nocodb_data[nocodb_field] = external_data[external_field]
        
        # Include ID field
        if "id" in external_data:
            nocodb_data["id"] = external_data["id"]
        
        # Map extra attributes
        if "extra_attributes" in external_data and external_data["extra_attributes"]:
            for attr in external_data["extra_attributes"]:
                nocodb_data[attr.name] = attr.description
        
        return nocodb_data
    
    def map_from_nocodb(self, nocodb_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Map NocoDB product data to external format.
        
        Args:
            nocodb_data: NocoDB product data
            
        Returns:
            Mapped data for external use
        """
        external_data = {
            "id": nocodb_data.get("Id") or nocodb_data.get("id"),
            "name": nocodb_data.get(self.field_mappings["name"], ""),
            "description": nocodb_data.get(self.field_mappings["description"], ""),
            "price": nocodb_data.get(self.field_mappings["price"], 0.0),
            "currency": nocodb_data.get(self.field_mappings["currency"], "USD"),
            "stock_qty": nocodb_data.get(self.field_mappings["stock_qty"], 0),
            "final_price": nocodb_data.get(self.field_mappings["final_price"]),
        }
        
        # Handle image URLs
        preview_url = []
        if self.field_mappings["preview_url"] in nocodb_data and nocodb_data[self.field_mappings["preview_url"]]:
            for image_data in nocodb_data[self.field_mappings["preview_url"]]:
                if image_data.get("signedUrl"):
                    preview_url.append(image_data["signedUrl"])
                else:
                    preview_url.append(image_data["url"])
        external_data["preview_url"] = preview_url
        
        # Extract extra attributes (fields not in standard mappings)
        primary_keys = list(self.field_mappings.values()) + ["Id", "id", "CreatedAt", "UpdatedAt"]
        extra_attributes = []
        
        for key, value in nocodb_data.items():
            if (
                key not in primary_keys
                and value is not None
                and isinstance(value, (str, int, float))
                and not key.startswith("SYS-")
            ):
                extra_attributes.append(ExtraAttribute(name=key, description=str(value)))
        
        if extra_attributes:
            external_data["extra_attributes"] = extra_attributes
            
        return external_data 