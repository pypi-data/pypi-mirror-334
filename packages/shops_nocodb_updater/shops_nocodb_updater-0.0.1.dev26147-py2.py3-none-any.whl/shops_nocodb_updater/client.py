import inspect
import logging
from typing import List, Type, get_origin, get_args, ForwardRef, Dict, Optional, Union, Any

import httpx
from pydantic import HttpUrl

from shops_nocodb_updater.models.base import NocodbModel, ID_FIELD

# Set default timeouts (in seconds)
DEFAULT_TIMEOUT = httpx.Timeout(10.0, connect=5.0)


class NocodbClient:
    """
    Client for interacting with NocoDB API.
    Provides methods for CRUD operations and syncing external records.
    """
    
    def __init__(
        self,
        nocodb_host: str,
        api_key: str,
        project_id: str,
        api_version: str = "v1",
        logger: Optional[logging.Logger] = None,
        product_table_id: Optional[str] = None,
        category_table_id: Optional[str] = None,
    ):
        """
        Initialize the NocoDB client.
        
        Args:
            nocodb_host: The NocoDB host
            api_key: The API key
            project_id: The project ID
            api_version: The API version to use (default: "v1")
            logger: Optional logger
            product_table_id: Optional product table ID
            category_table_id: Optional category table ID
        """
        self.NOCODB_HOST = nocodb_host
        self.API_KEY = api_key
        self.project_id = project_id
        self.API_VERSION = api_version
        self.product_table_id = product_table_id
        self.category_table_id = category_table_id
        self.language = "EN"  # Default language
        
        self.logger = logger or logging.getLogger(__name__)
        
        self.httpx_client = httpx.AsyncClient(
            headers={
                "xc-token": self.API_KEY,
                "Content-Type": "application/json",
            },
            timeout=30.0,
        )
    
    def construct_get_params(
        self,
        required_fields: Optional[list] = None,
        projection: Optional[list] = None,
        extra_where: Optional[str] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
    ) -> dict:
        """
        Construct query parameters for GET requests.
        
        Args:
            required_fields: Fields that must not be null
            projection: Fields to include in the response
            extra_where: Additional where conditions
            offset: Pagination offset
            limit: Pagination limit
            
        Returns:
            Dictionary of query parameters
        """
        extra_params = {}
        if projection:
            extra_params["fields"] = ",".join(projection)
        if required_fields:
            extra_params["where"] = ""
            for field in required_fields:
                extra_params["where"] += f"({field},isnot,null)~and"
            extra_params["where"] = extra_params["where"].rstrip("~and")
        if extra_where:
            if not extra_params.get("where"):
                extra_params["where"] = extra_where
            else:
                extra_params["where"] += f"~and{extra_where}"
        if offset:
            extra_params["offset"] = str(offset)
        if limit:
            extra_params["limit"] = str(limit)
        return extra_params

    async def get_table_records(self, table_id: str) -> List[dict]:
        """Fetches all records from the NocoDB table."""
        records = []
        offset = 0
        limit = 100
        while True:
            result = await self.get_table_records_paginated(table_id, offset=offset, limit=limit)
            records.extend(result["list"])
            if result["pageInfo"]["isLastPage"]:
                break
            offset += limit
        return records

    async def count_table_records(self, table_name: str) -> int:
        url = f"{self.NOCODB_HOST}/api/v2/tables/{table_name}/records/count"
        response = await self.httpx_client.get(url)
        if response.status_code == 200:
            return response.json().get("count", 0)
        raise Exception(response.text)

    async def update_record(self, table_id: str, record_id: str, record_data: dict) -> dict:
        """
        Update a record in a table.
        
        Args:
            table_id: The table ID
            record_id: The record ID
            record_data: The record data
            
        Returns:
            The response data
        """
        if self.API_VERSION == "v1":
            # For v1 API, we need to get the table name from the metadata
            metadata = await self.get_table_metadata(table_id)
            table_name = metadata.get("table_name")
            if not table_name:
                raise Exception(f"Could not determine table name for table ID {table_id}")
                
            url = f"{self.NOCODB_HOST}/api/{self.API_VERSION}/db/data/noco/{self.project_id}/{table_name}/{record_id}"
        else:
            url = f"{self.NOCODB_HOST}/api/{self.API_VERSION}/tables/{table_id}/records/{record_id}"
        
        response = await self.httpx_client.patch(url, json=record_data)
        if response.status_code == 200:
            return response.json()
        raise Exception(response.text)

    async def create_table_record(self, table_id: str, record: dict, external_id_field: str) -> None:
        """
        Create a new record in a table.
        
        Args:
            table_id: The table ID
            record: The record data
            external_id_field: External ID field name
        """
        url = f"{self.NOCODB_HOST}/api/{self.API_VERSION}/db/data/{table_id}/records"
        record_data = record.copy()
        external_id = record.get("id", "")
        if external_id:
            record_data[external_id_field] = external_id
        
        response = await self.httpx_client.post(url, json=record_data)
        if response.status_code != 200:
            raise Exception(response.text)

    async def delete_table_record(self, table_name: str, record_id: str) -> dict:
        """
        Delete a record from a table.
        
        Args:
            table_name: The table name or ID
            record_id: The record ID
            
        Returns:
            The response data
        """
        url = f"{self.NOCODB_HOST}/api/{self.API_VERSION}/db/data/{table_name}/records/{record_id}"
        response = await self.httpx_client.delete(url)
        return response.json()

    async def get_table_metadata(self, table_id: str) -> dict:
        """
        Get a table metadata.
        
        Args:
            table_id: The table ID
            
        Returns:
            The table metadata
        """
        if self.API_VERSION == "v1":
            url = f"{self.NOCODB_HOST}/api/{self.API_VERSION}/db/meta/tables/{table_id}"
        else:
            url = f"{self.NOCODB_HOST}/api/{self.API_VERSION}/tables/{table_id}"
            
        response = await self.httpx_client.get(url)
        if response.status_code == 200:
            return response.json()
        raise Exception(response.text)

    async def create_column(self, table_id: str, column_data: dict) -> dict:
        """
        Create a column in a table.
        
        Args:
            table_id: The table ID
            column_data: The column data
            
        Returns:
            The response data
        """
        url = f"{self.NOCODB_HOST}/api/{self.API_VERSION}/db/meta/tables/{table_id}/columns"
        
        # Adjust column_data format for v1 API if needed
        if self.API_VERSION == "v1":
            # v1 API requires a different format for columns
            column_payload = {
                "column_name": column_data.get("column_name"),
                "title": column_data.get("title", ""),
                "uidt": column_data.get("uidt", "SingleLineText"),
                "dt": "varchar",
                "dtxp": "255",
                "ai": False,
                "pk": False,
                "cdf": None,
                "rqd": False,
                "un": False,
                "ct": "character varying"
            }
        else:
            column_payload = column_data
            
        response = await self.httpx_client.post(url, json=column_payload)
        if response.status_code == 200:
            return response.json()
        raise Exception(response.text)

    async def ensure_external_id_column(self, table_id: str, external_id_field: str) -> None:
        """
        Ensure the external ID column exists in the table.
        
        Args:
            table_id: The table ID
            external_id_field: The external ID field name
        """
        try:
            metadata = await self.get_table_metadata(table_id)
            column_list = metadata.get("columns", [])
            
            # Check if the column already exists
            existing_columns = [col.get("column_name") for col in column_list]
            if external_id_field in existing_columns:
                self.logger.debug(f"Column {external_id_field} already exists")
                return
                
            # Create the column if it doesn't exist
            self.logger.info(f"Creating external ID column: {external_id_field}")
            await self.create_column(
                table_id,
                {
                    "column_name": external_id_field,
                    "title": "External ID",
                    "uidt": "SingleLineText"
                },
            )
        except Exception as e:
            # If the error is about duplicate column, we can ignore it
            if "Duplicate column" in str(e):
                self.logger.debug(f"Column {external_id_field} already exists (detected from error)")
                return
            # Otherwise, re-raise the exception
            raise

    async def get_table_records_paginated(self, table_id: str, offset: int = 0, limit: int = 100) -> dict:
        """Fetches a paginated list of records from the NocoDB table."""
        url = f"{self.NOCODB_HOST}/api/v2/tables/{table_id}/records"
        extra_params = {"offset": offset, "limit": limit}
        response = await self.httpx_client.get(url, params=extra_params)
        if response.status_code == 200:
            return response.json()
        raise Exception(response.text)

    def record_needs_update(self, nocodb_record: dict, external_record: dict) -> bool:
        """
        Check if a record needs to be updated based on differences between NocoDB and external data.
        
        Args:
            nocodb_record: The NocoDB record
            external_record: The external record
            
        Returns:
            True if record needs update, False otherwise
        """
        for field, value in external_record.items():
            if field not in nocodb_record:
                continue
            if nocodb_record[field] != value:
                return True
        return False

    def format_external_record(self, external_record: dict, m2m_column_names: List[str]) -> dict:
        """
        Format an external record for NocoDB compatibility.
        
        Args:
            external_record: The external record
            m2m_column_names: Names of many-to-many columns to skip
            
        Returns:
            Formatted record
        """
        return {k: v for k, v in external_record.items() if k not in m2m_column_names}

    async def sync_records(self, model, data: list) -> dict:
        """
        Sync records to a table.
        
        Args:
            model: The model class
            data: The data to sync
            
        Returns:
            A dictionary mapping external IDs to NocoDB IDs
        """
        from .sync_data import synchronize_records
        from .utils import map_category_fields, get_language_from_project

        self.language = await get_language_from_project(self)
        custom_mapper = lambda x: map_category_fields(x, self.language)

        return await synchronize_records(
            self,
            model.__tableid__,
            data,
            model.__external_id_field__,
            custom_mapper
        )
        
    async def link_table_record(
        self, 
        base_id: str, 
        fk_model_id: str, 
        record_id: str, 
        source_column_id: str, 
        linked_record_id: str
    ) -> dict:
        """
        Link two records together.
        
        Args:
            base_id: The ID of the database base
            fk_model_id: The ID of the linked model
            record_id: The ID of the source record
            source_column_id: The ID of the source column
            linked_record_id: The ID of the linked record
            
        Returns:
            The response data
        """
        path = f"/api/v1/db/data/noco/{base_id}/{fk_model_id}/{record_id}/mm/{source_column_id}/{linked_record_id}"
        response = await self.httpx_client.post(self.NOCODB_HOST + path)
        if response.status_code == 200:
            return response.json()
        self.logger.error(f"Failed to link records: {response.text}")
        raise Exception(response.text)
        
    async def unlink_table_record(
        self, 
        base_id: str, 
        fk_model_id: str, 
        record_id: str, 
        source_column_id: str, 
        linked_record_id: str
    ) -> dict:
        """
        Unlink two records.
        
        Args:
            base_id: The ID of the database base
            fk_model_id: The ID of the linked model
            record_id: The ID of the source record
            source_column_id: The ID of the source column
            linked_record_id: The ID of the linked record
            
        Returns:
            The response data
        """
        path = f"/api/v1/db/data/noco/{base_id}/{fk_model_id}/{record_id}/mm/{source_column_id}/{linked_record_id}"
        response = await self.httpx_client.delete(self.NOCODB_HOST + path)
        if response.status_code == 200:
            return response.json()
        self.logger.error(f"Failed to unlink records: {response.text}")
        raise Exception(response.text)

    async def get_linked_records(
            self,
            base_id: str,
            fk_model_id: str,
            record_id: str,
            source_column_id: str
    ):
        """
        Fetch linked records for a given source record and column, handling pagination.

        Parameters:
        - base_id: The ID of the database base.
        - fk_model_id: The ID of the linked column.
        - record_id: The ID of the source record.
        - source_column_id: The ID of the source column.

        Returns:
        - A list of all linked records.

        Raises:
        - Exception if the request fails.
        """
        path = f"/api/v1/db/data/noco/{base_id}/{fk_model_id}/{record_id}/mm/{source_column_id}"
        limit = 30
        offset = 0
        all_records = []

        while True:
            # Construct the query with limit and offset for pagination
            query = f"?limit={limit}&offset={offset}"
            response = await self.httpx_client.get(self.NOCODB_HOST + path + query)

            if response.status_code == 200:
                data = response.json()
                records = data.get("list", [])
                all_records.extend(records)

                # Check if we've retrieved all records
                if data.get("pageInfo", {}).get("isLastPage", False):
                    break

                # Increment offset for the next batch of records
                offset += limit
            else:
                raise Exception(f"Failed to fetch linked records: {response.text}")

        return all_records

    async def link_synced_records(
        self,
        model,
        linked_model,
        external_records: list,
        source_records_map: dict,
        target_records_map: dict,
        map_records_key: str,
        column_name: str,
    ) -> int:
        """
        Link records based on external data using the correct NocoDB API endpoints.
        Also unlinks records that are no longer related.
        
        Args:
            model: The model class for the source records
            linked_model: The model class for the target records
            external_records: The external data containing the relationships
            source_records_map: Mapping of external product IDs to NocoDB IDs (not used with new implementation)
            target_records_map: Mapping of external category IDs to NocoDB IDs (not used with new implementation)
            map_records_key: Linked field between source_records_map and target_records_map, nested fields is allowed, example 'category.id'
            column_name: The column name in the source table that links to the target table
            
        Returns:
            The number of records updated (linked + unlinked)
        """
        table_id = model.__tableid__
        self.logger.info(f"Starting link_synced_records for table {table_id}, column {column_name}")
        
        # Get table metadata to find the link column
        metadata = await self.get_table_metadata(table_id)
        
        # Find the link column
        linked_column = None
        for col in metadata.get("columns", []):
            if col.get("title") == column_name:
                linked_column = col
                self.logger.debug(f"Found link column with id: {col.get('id')}")
                break
                
        if not linked_column:
            self.logger.error(f"Linked column {column_name} was not found in {table_id}")
            return 0
        
        # Get column options for linking details from colOptions
        col_options = linked_column.get("colOptions", {})
        fk_related_model_id = col_options.get("fk_related_model_id")
        column_id = linked_column.get("id")
        
        self.logger.info(f"Link column details: id={column_id}, fk_related_model_id={fk_related_model_id}")
        
        if not fk_related_model_id:
            self.logger.error(f"Could not determine related model ID for column {column_name}")
            return 0
            
        # Get all records from source and target tables
        # records = await self.get_table_records(table_id)
        linked_table_records = await self.get_table_records(fk_related_model_id)
        
        # self.logger.info(f"Found {len(records)} source records and {len(linked_table_records)} target records")
        
        # Create mappings
        external_id_field = model.__external_id_field__
        target_external_id_field = linked_model.__external_id_field__
        
        self.logger.info(f"Using external ID fields: source={external_id_field}, target={target_external_id_field}")
        
        # Process records with External ID as well
        # source_records_map = {}
        # target_records_map = {}
        
        # Build source records map
        # for record in records:
        #     ext_id = record.get(external_id_field) or record.get("External ID")
        #     if ext_id:
        #         source_records_map[ext_id] = record
                
        # Build target records map
        # for record in linked_table_records:
        #     ext_id = record.get(target_external_id_field) or record.get("External ID")
        #     if ext_id:
        #         target_records_map[ext_id] = record
        
        # Create a mapping from ID to name for better logging
        target_id_to_name = {}
        for record in linked_table_records:
            record_id = record["Id"]
            external_id = record.get("External ID")
            target_id_to_name[str(record_id)] = external_id
        
        # Map external records by ID
        external_records_map = {str(record["id"]): record for record in external_records}
        
        self.logger.info(f"Map sizes: source={len(source_records_map)}, target={len(target_records_map)}, external={len(external_records_map)}")
        
        # Prepare for linking/unlinking
        update_count = 0
        
        # Get the project ID from the URL
        project_id = await self.get_project_id()
        
        # Track what relationships should exist
        desired_relationships: dict[str, list[str]] = {}  # {source_id: [target_id1, target_id2, ...]}
        
        # First identify all desired relationships based on external data
        from pprint import pprint
        pprint(target_records_map)
        for ext_id, external_record in external_records_map.items():
            if ext_id not in source_records_map:
                self.logger.error(f"Product with external ID {ext_id} not found in NocoDB, all external records must be synced before link records")
                continue
                
            source_record = source_records_map[ext_id]
            source_record_id = source_record.get("Id")  # Get the NocoDB record ID
            
            if not source_record_id:
                self.logger.error(f"No ID found for source record with external ID {ext_id}, source_records_map format: [external_id: <nocodb_record>, ...] nocodb_record must have 'Id' attribute")
                continue
                
            # Extract category information from the external record
            target_external_id_field_value = None
            for target_id_field_name in map_records_key.split("."):
                if target_external_id_field_value:
                    if type(target_external_id_field_value) == list:
                        target_external_id_field_value = [target_external_id_field_value_item.get(target_id_field_name) for target_external_id_field_value_item  in target_external_id_field_value]
                    else:
                        target_external_id_field_value = target_external_id_field_value.get(target_id_field_name)
                else:
                    target_external_id_field_value = external_record.get(target_id_field_name)

            if not target_external_id_field_value:
                self.logger.debug(f"Failed to extract value of target ID field using {map_records_key} from {external_record}")
                continue
            elif type(target_external_id_field_value) != list:
                target_external_id_field_values = [str(target_external_id_field_value)]
            else:
                target_external_id_field_values = [str(target_external_id_field_value_item) for target_external_id_field_value_item in target_external_id_field_value]
            # Ensure category_id is a string (hashable)

            self.logger.debug(
                f"Extracted value of target ID field using {map_records_key} from {target_external_id_field_values}")

            # Find the target record by external ID
            for target_external_id_field_value in target_external_id_field_values:
                if target_external_id_field_value not in target_records_map:
                    self.logger.error(f"Record with external ID {target_external_id_field_value} not found in NocoDB, records must exist before link records")
                    continue

                target_record = target_records_map[target_external_id_field_value]
                target_record_id = target_record.get("Id")  # Get the NocoDB record ID

                if not target_record_id:
                    self.logger.debug(f"No ID found for target record with external ID {target_external_id_field_value}, source_records_map format: [external_id: <nocodb_record>, ...] nocodb_record must have 'Id' attribute")
                    continue

                # Add to desired relationships
                if source_record_id not in desired_relationships:
                    desired_relationships[source_record_id] = []
                desired_relationships[source_record_id].append(str(target_record_id))
            
        # Now process each source record to link/unlink as needed
        for ext_id, source_record in source_records_map.items():
            source_record_id = source_record.get("Id")
            if not source_record_id:
                self.logger.error(f"Empty Id field of nocodb record: {source_record}")
                continue
                
            try:
                # Get current linked records
                # existing_linked_records_path = f"/api/v1/db/data/noco/{project_id}/{table_id}/{source_record_id}/mm/{column_id}"
                # existing_response = await self.httpx_client.get(self.NOCODB_HOST + existing_linked_records_path)
                
                # if existing_response.status_code != 200:
                #     self.logger.error(f"Failed to get existing linked records for {ext_id}: {existing_response.text}")
                #     continue
                
                # Handle different response formats - it could be an array or a list of objects
                # existing_linked = existing_response.json()
                # existing_links = []
                # existing_linked_records_path = f"/api/v1/db/data/noco/{project_id}/{fk_model_id=table_id}/{record_id=source_record_id}/mm/{source_column_id=column_id}"
                existing_records = await self.get_linked_records(
                    base_id=project_id,
                    fk_model_id=table_id,
                    record_id=source_record_id,
                    source_column_id=column_id,
                )
                existing_links = [str(record["Id"]) for record  in existing_records]
                self.logger.info(f"Extracted existing links for {ext_id}: {existing_links}")
                
                # Determine what links to add and remove
                desired_links = desired_relationships.get(source_record_id, [])
                links_to_add = [link for link in desired_links if link not in existing_links]
                links_to_remove = [link for link in existing_links if link not in desired_links]
                
                self.logger.info(f"Source {ext_id}: existing={existing_links}, desired={desired_links}, to_add={links_to_add}, to_remove={links_to_remove}")
                
                # Add new links
                for target_id in links_to_add:
                    # Get the external ID for better logging
                    # target_ext_id = "unknown"
                    # for t_ext_id, t_record in target_records_map.items():
                    #     if str(t_record.get("Id")) == target_id:
                    #         target_ext_id = t_ext_id
                    #         break
                    
                    # Get the target name for better logging
                    # target_name = target_id_to_name.get(target_id, "unknown")
                            
                    self.logger.info(f"Linking product {ext_id} (ID: {source_record_id}) to category with ID: {target_id}")

                    # Add link
                    await self.link_table_record(
                        base_id=project_id,
                        fk_model_id=table_id,
                        record_id=source_record_id,
                        source_column_id=column_id,
                        linked_record_id=target_id,
                    )
                
                # Remove old links
                for target_id in links_to_remove:
                    # Get the external ID for better logging
                    # target_ext_id = "unknown"
                    # for t_ext_id, t_record in target_records_map.items():
                    #     if str(t_record.get("Id")) == target_id:
                    #         target_ext_id = t_ext_id
                    #         break
                            
                    # Get the target name for better logging
                    # target_name = target_id_to_name.get(target_id, "unknown")
                            
                    self.logger.info(f"Unlinking product {ext_id} (ID: {source_record_id}) from category ID: {target_id}")

                    await self.unlink_table_record(
                        base_id=project_id,
                        fk_model_id=table_id,
                        record_id=source_record_id,
                        source_column_id=column_id,
                        linked_record_id=target_id,
                    )
                        
            except Exception as e:
                self.logger.error(f"Error processing record {ext_id}: {str(e)}")
                
        self.logger.info(f"Completed linking/unlinking, {update_count} update operations performed")
        return update_count

    async def get_project_id(self) -> str:
        """
        Get the project ID from the NocoDB URL.
        
        Returns:
            Project ID string
        """
        if hasattr(self, "project_id") and self.project_id:
            return self.project_id
            
        # Extract from URL format or fetch from API
        # For now, return the hardcoded project ID
        self.project_id = "pzypsvq4vmejiir"  # This should be extracted properly in production
        return self.project_id
        
    def get_query_params(self, params: dict) -> dict:
        """
        Format query parameters for the NocoDB API.
        
        Args:
            params: The query parameters
            
        Returns:
            The query parameters
        """
        if not params:
            return {}
            
        if self.API_VERSION == "v1":
            # For v1 API, use different parameter names
            query_params = {}
            
            # Handle fields
            if "fields" in params:
                query_params["fields"] = params["fields"]
                
            # Handle where conditions
            if "where" in params:
                # v1 API uses a different format for filters
                conditions = []
                for field, value in params["where"].items():
                    if isinstance(value, dict):
                        # Handle operators
                        for op, val in value.items():
                            conditions.append(f"({field},{self._map_operator(op)},{val})")
                    else:
                        # Equality condition
                        conditions.append(f"({field},eq,{value})")
                        
                if conditions:
                    query_params["where"] = ",".join(conditions)
                    
            # Handle limit and offset
            if "limit" in params:
                query_params["limit"] = params["limit"]
            if "offset" in params:
                query_params["offset"] = params["offset"]
                
            return query_params
        else:
            # v2 API format
            return params
            
    def _map_operator(self, op: str) -> str:
        """Map operators from v2 to v1 format"""
        operator_map = {
            "eq": "eq",
            "neq": "neq", 
            "gt": "gt",
            "lt": "lt",
            "gte": "gte",
            "lte": "lte",
            "like": "like",
            "nlike": "nlike",
            "in": "in"
        }
        return operator_map.get(op, "eq")

    async def query_records(self, table_id: str, params: dict[Any, Any] | None = None) -> list:
        """
        Query records from a table.
        
        Args:
            table_id: The table ID
            params: The query parameters
            
        Returns:
            A list of records
        """
        url = f"{self.NOCODB_HOST}/api/{self.API_VERSION}/tables/{table_id}/records"
        query_params = self.get_query_params(params or {})
        
        response = await self.httpx_client.get(url, params=query_params)
        if response.status_code == 200:
            if self.API_VERSION == "v1":
                return response.json().get("list", [])
            else:
                return response.json().get("list", [])
        raise Exception(response.text)

    async def create_record(self, table_id: str, record_data: dict) -> dict:
        """
        Create a record in a table.
        
        Args:
            table_id: The table ID
            record_data: The record data
            
        Returns:
            The response data
        """
        if self.API_VERSION == "v1":
            # For v1 API, we need to get the table name from the metadata
            metadata = await self.get_table_metadata(table_id)
            table_name = metadata.get("table_name")
            if not table_name:
                raise Exception(f"Could not determine table name for table ID {table_id}")
                
            url = f"{self.NOCODB_HOST}/api/{self.API_VERSION}/db/data/noco/{self.project_id}/{table_name}"
        else:
            url = f"{self.NOCODB_HOST}/api/{self.API_VERSION}/tables/{table_id}/records"
            
        response = await self.httpx_client.post(url, json=record_data)
        if response.status_code == 200:
            return response.json()
        raise Exception(response.text) 