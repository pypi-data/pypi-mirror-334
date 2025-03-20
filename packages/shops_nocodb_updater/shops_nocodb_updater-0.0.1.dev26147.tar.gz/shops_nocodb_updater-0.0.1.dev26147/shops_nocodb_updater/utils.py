import logging
from typing import Dict, Any, Optional, List

# Field mappings from the localization files
# Categories
CATEGORY_IMAGE_FIELD = {"RU": "Изображение", "EN": "Image"}
CATEGORY_NAME_FIELD = {"RU": "Название", "EN": "Name"}
CATEGORY_PARENT_FIELD = {"RU": "Назначить родительскую категорию", "EN": "Set parent category"}
CATEGORY_PARENT_ID_FIELD = {"RU": "ID родительской категории", "EN": "ID of parent category"}
CATEGORY_PARENT_NAME_FIELD = {"RU": "Название родительской категории", "EN": "Name of parent category"}
CATEGORY_EXTERNAL_ID_FIELD = {"RU": "Внешний ID", "EN": "External ID"}

# Products
PRODUCT_IMAGE_FIELD = {"RU": "Изображения", "EN": "Images"}
PRODUCT_NAME_FIELD = {"RU": "Название", "EN": "Name"}
PRODUCT_DESCRIPTION_FIELD = {"RU": "Описание", "EN": "Description"}
PRODUCT_PRICE_FIELD = {"RU": "Стоимость", "EN": "Price"}
PRODUCT_DISCOUNT_PRICE_FIELD = {"RU": "Стоимость со скидкой", "EN": "Discounted price"}
PRODUCT_CURRENCY_FIELD = {"RU": "Валюта", "EN": "Currency"}
PRODUCT_STOCK_FIELD = {"RU": "Доступное количество", "EN": "Available quantity"}
PRODUCT_CATEGORY_FIELD = {"RU": "Категория", "EN": "Category"}
PRODUCT_CATEGORY_ID_FIELD = {"RU": "ID Категории", "EN": "ID of category"}
PRODUCT_CATEGORY_NAME_FIELD = {"RU": "Название категорий", "EN": "Name of categories"}
PRODUCT_EXTERNAL_ID_FIELD = {"RU": "Внешний ID", "EN": "External ID"}

# Table names for language detection
CATEGORY_TABLE_NAMES = {"RU": "Категории", "EN": "Categories"}
PRODUCT_TABLE_NAMES = {"RU": "Товары", "EN": "Products"}

logger = logging.getLogger(__name__)

def detect_language(table_names: List[str]) -> str:
    """
    Detect the language based on table names in NocoDB.
    
    Args:
        table_names: List of table names
        
    Returns:
        Language code ("EN" or "RU")
    """
    for table_name in table_names:
        # Check for Russian table names
        if CATEGORY_TABLE_NAMES["RU"] in table_name or PRODUCT_TABLE_NAMES["RU"] in table_name:
            return "RU"
    
    # Default to English
    return "EN"

def get_field_mapping(field_dict: Dict[str, str], language: str) -> str:
    """
    Get the localized field name based on language.
    
    Args:
        field_dict: Dictionary with language codes as keys and field names as values
        language: Language code
        
    Returns:
        Localized field name
    """
    return field_dict.get(language.upper(), field_dict.get("EN", ""))

async def get_language_from_project(client) -> str:
    """
    Determine the language of the NocoDB project by looking at the table names.
    
    Args:
        client: NocoDB client
        
    Returns:
        Language code ("EN" or "RU")
    """
    try:
        table_names = []
        
        # Try to get category table metadata
        if hasattr(client, 'category_table_id') and client.category_table_id:
            try:
                category_metadata = await client.get_table_metadata(client.category_table_id)
                if category_metadata and "table_name" in category_metadata:
                    table_names.append(category_metadata["table_name"])
            except Exception as e:
                logger.warning(f"Failed to get category table metadata: {e}")
                
        # Try to get product table metadata
        if hasattr(client, 'product_table_id') and client.product_table_id:
            try:
                product_metadata = await client.get_table_metadata(client.product_table_id)
                if product_metadata and "table_name" in product_metadata:
                    table_names.append(product_metadata["table_name"])
            except Exception as e:
                logger.warning(f"Failed to get product table metadata: {e}")
        
        # If we found any table names, try to detect the language
        if table_names:
            return detect_language(table_names)
        else:
            logger.warning("No table names found to detect language")
            return "EN"  # Default to English
            
    except Exception as e:
        logger.warning(f"Failed to detect language: {e}")
        return "EN"  # Default to English

def map_category_fields(data: Dict[str, Any], language: str) -> Dict[str, Any]:
    """
    Map category data to NocoDB field names based on language.
    
    Args:
        data: Category data
        language: Language code
        
    Returns:
        Mapped data for NocoDB
    """
    mapped_data = {}
    
    # Map basic fields
    if "name" in data:
        mapped_data[get_field_mapping(CATEGORY_NAME_FIELD, language)] = data["name"]
    
    if "description" in data and data["description"]:
        mapped_data["Description"] = data["description"]
    
    # Map image
    if "preview_url" in data and data["preview_url"]:
        # Format image data
        mapped_data[get_field_mapping(CATEGORY_IMAGE_FIELD, language)] = [{
            "url": data["preview_url"],
            "title": f"image-{data.get('id', '')}.jpg",
            "mimetype": "image/jpeg"
        }]
    
    # Map external ID
    if "id" in data:
        mapped_data[get_field_mapping(CATEGORY_EXTERNAL_ID_FIELD, language)] = data["id"]
    
    # Map parent category
    if "parent_category" in data and data["parent_category"]:
        parent_id = data["parent_category"][0].get("id", "")
        if parent_id:
            mapped_data[get_field_mapping(CATEGORY_PARENT_ID_FIELD, language)] = parent_id
            mapped_data[get_field_mapping(CATEGORY_PARENT_FIELD, language)] = 1  # Enable parent category
    
    return mapped_data

def map_product_fields(data: Dict[str, Any], language: str) -> Dict[str, Any]:
    """
    Map product data to NocoDB field names based on language.
    
    Args:
        data: Product data
        language: Language code
        
    Returns:
        Mapped data for NocoDB
    """
    mapped_data = {}
    
    # Map basic fields
    if "name" in data:
        mapped_data[get_field_mapping(PRODUCT_NAME_FIELD, language)] = data["name"]
    
    if "description" in data and data["description"]:
        mapped_data[get_field_mapping(PRODUCT_DESCRIPTION_FIELD, language)] = data["description"]
    
    if "price" in data:
        mapped_data[get_field_mapping(PRODUCT_PRICE_FIELD, language)] = data["price"]
    
    if "final_price" in data and data["final_price"]:
        mapped_data[get_field_mapping(PRODUCT_DISCOUNT_PRICE_FIELD, language)] = data["final_price"]
    
    if "currency" in data:
        mapped_data[get_field_mapping(PRODUCT_CURRENCY_FIELD, language)] = data["currency"]
    
    if "stock_qty" in data:
        mapped_data[get_field_mapping(PRODUCT_STOCK_FIELD, language)] = data["stock_qty"]
    
    # Map images
    if "preview_url" in data and data["preview_url"]:
        images = []
        for i, url in enumerate(data["preview_url"]):
            images.append({
                "url": url,
                "title": f"image-{data.get('id', '')}-{i}.jpg",
                "mimetype": "image/jpeg"
            })
        mapped_data[get_field_mapping(PRODUCT_IMAGE_FIELD, language)] = images
    
    # Map external ID
    if "id" in data:
        mapped_data[get_field_mapping(PRODUCT_EXTERNAL_ID_FIELD, language)] = data["id"]
    
    # Map extra attributes
    if "extra_attributes" in data and data["extra_attributes"]:
        for attr in data["extra_attributes"]:
            if attr.get("name") and attr.get("description"):
                mapped_data[attr["name"]] = attr["description"]
    
    # Map category link
    if "category_id" in data and data["category_id"]:
        mapped_data[get_field_mapping(PRODUCT_CATEGORY_ID_FIELD, language)] = data["category_id"]
    
    return mapped_data 