import logging

logger = logging.getLogger(__name__)

async def synchronize_records(client, table_id, data, external_id_field="external_id", mapper=None):
    """
    Synchronize records with NocoDB.
    
    Args:
        client: NocoDB client
        table_id: Table ID
        data: Data to sync
        external_id_field: External ID field
        mapper: Optional mapper function
    
    Returns:
        Dictionary mapping external IDs to NocoDB IDs
    """
    logger.info(f"Syncing {len(data)} records to table {table_id}")
    
    # Ensure the external ID column exists
    await client.ensure_external_id_column(table_id, external_id_field)
    
    # Get existing records
    existing_records = await client.get_table_records(table_id)
    
    # Create lookup by external ID
    existing_lookup = {}
    for record in existing_records:
        ext_id = record.get(external_id_field)
        if ext_id:
            existing_lookup[ext_id] = record
        else:
            logger.debug(f"Skip from update record nocodb record without ExternalID field: {external_id_field}")
    
    logger.info(f"Found {len(existing_lookup)} existing records with external IDs")
    
    # Process records
    id_map = {}
    for item in data:
        # Apply mapper if provided
        if mapper:
            record_data = mapper(item)
        else:
            record_data = item
            
        # Get external ID
        external_id = str(item.get("id", ""))
        if not external_id:
            logger.debug(f"Skip from update external record with missing id field")
            continue
            
        # Include external ID in the record data
        if external_id_field not in record_data:
            record_data[external_id_field] = external_id
            
        # Check if record exists
        if external_id in existing_lookup:
            # Update existing record
            existing_record = existing_lookup[external_id]
            record_id = existing_record.get("Id")
            
            # Check if update is needed
            if needs_update(existing_record, record_data):
                logger.debug(f"Updating record {external_id}")
                update_response = await client.update_record(table_id, record_id, record_data)
                id_map[external_id] = update_response
            else:
                id_map[external_id] = existing_record
        else:
            # Create new record
            logger.debug(f"Creating record {external_id}")
            created_record = await client.create_record(table_id, record_data)
            id_map[external_id] = created_record
    
    logger.info(f"Synchronized {len(id_map)} records")
    return id_map
    
def needs_update(existing_record, new_data):
    """
    Check if a record needs to be updated.
    
    Args:
        existing_record: Existing record
        new_data: New data
        
    Returns:
        True if update is needed, False otherwise
    """
    for key, value in new_data.items():
        if key in existing_record and existing_record[key] != value:
            logger.debug(f"Record needs to be updated for {key} {existing_record[key]} -> {value}")
            return True
    return False 