"""
Work item tools for Azure DevOps.

This module provides MCP tools for working with Azure DevOps work items.
"""
from typing import Optional, List
from azure.devops.v7_1.work_item_tracking.models import Wiql, WorkItem
from azure.devops.v7_1.work_item_tracking import WorkItemTrackingClient
from mcp_azure_devops.utils.azure_client import get_connection
from mcp_azure_devops.features.work_items.common import get_work_item_client, AzureDevOpsClientError


def _format_work_item_basic(work_item: WorkItem) -> str:
    """
    Format basic work item information.
    
    Args:
        work_item: Work item object to format
        
    Returns:
        String with basic work item details
    """
    fields = work_item.fields or {}
    title = fields.get("System.Title", "Untitled")
    item_type = fields.get("System.WorkItemType", "Unknown")
    state = fields.get("System.State", "Unknown")
    
    # Add link to the work item (if available)
    url_part = ""
    if hasattr(work_item, "url") and work_item.url:
        url_part = f"\nUrl: {work_item.url}"
    
    return f"# Work Item {work_item.id}: {title}\nType: {item_type}\nState: {state}{url_part}"


def _format_work_item_detailed(work_item: WorkItem, basic_info: str) -> str:
    """
    Add detailed information to basic work item information.
    
    Args:
        work_item: Work item object to format
        basic_info: Already formatted basic information
        
    Returns:
        String with comprehensive work item details
    """
    details = [basic_info]  # Start with basic info already provided
    
    fields = work_item.fields or {}
    
    if "System.Description" in fields:
        details.append("\n## Description")
        details.append(fields["System.Description"])
    
    # Add additional details section
    details.append("\n## Additional Details")
    
    if "System.AssignedTo" in fields:
        assigned_to = fields['System.AssignedTo']
        # Handle the AssignedTo object which could be a dict or dictionary-like object
        if hasattr(assigned_to, 'display_name') and hasattr(assigned_to, 'unique_name'):
            # If it's an object with directly accessible properties
            details.append(f"Assigned To: {assigned_to.display_name} ({assigned_to.unique_name})")
        elif isinstance(assigned_to, dict):
            # If it's a dictionary
            display_name = assigned_to.get('displayName', '')
            unique_name = assigned_to.get('uniqueName', '')
            details.append(f"Assigned To: {display_name} ({unique_name})")
        else:
            # Fallback to display the raw value if we can't parse it
            details.append(f"Assigned To: {assigned_to}")
    
    if "System.IterationPath" in fields:
        details.append(f"Iteration: {fields['System.IterationPath']}")
    
    if "System.AreaPath" in fields:
        details.append(f"Area: {fields['System.AreaPath']}")
    
    # Add more fields as needed
    
    return "\n".join(details)


def _get_work_item_impl(
    item_id: int,
    wit_client: WorkItemTrackingClient,
    detailed: bool = False
) -> str:
    """
    Implementation of work item retrieval.
    
    Args:
        item_id: The work item ID
        wit_client: Work item tracking client
        detailed: Whether to return detailed information
            
    Returns:
        Formatted string containing work item information
    """
    try:
        work_item = wit_client.get_work_item(item_id)
        
        # Always format basic info first
        basic_info = _format_work_item_basic(work_item)
        
        # If detailed is requested, add more information
        if detailed:
            return _format_work_item_detailed(work_item, basic_info)
        else:
            return basic_info
            
    except Exception as e:
        return f"Error retrieving work item {item_id}: {str(e)}"




def _query_work_items_impl(
    query: str, 
    top: int,
    wit_client: WorkItemTrackingClient
) -> str:
    """
    Implementation of query_work_items that operates with a client.
    
    Args:
        query: The WIQL query string
        top: Maximum number of results to return
        wit_client: Work item tracking client
            
    Returns:
        Formatted string containing work item details
    """
    
    # Create the WIQL query
    wiql = Wiql(query=query)
    
    # Execute the query
    wiql_results = wit_client.query_by_wiql(wiql, top=top).work_items
    
    if not wiql_results:
        return "No work items found matching the query."
    
    # Get the work items from the results
    work_item_ids = [int(res.id) for res in wiql_results]
    work_items = wit_client.get_work_items(ids=work_item_ids, error_policy="omit")
    
    # Use the same formatting as get_work_item_basic
    formatted_results = []
    for work_item in work_items:
        if work_item:
            formatted_results.append(_format_work_item_basic(work_item))
    
    return "\n\n".join(formatted_results)


def register_tools(mcp) -> None:
    """
    Register work item tools with the MCP server.
    
    Args:
        mcp: The FastMCP server instance
    """
    
    @mcp.tool()
    def query_work_items(
        query: str, 
        top: Optional[int]
    ) -> str:
        """
        Query work items using WIQL.
        
        Args:
            query: The WIQL query string
            top: Maximum number of results to return (default: 30)
                
        Returns:
            Formatted string containing work item details
        """
        try:
            wit_client = get_work_item_client()
            # Ensure top is not None before passing to implementation
            return _query_work_items_impl(query, top or 30, wit_client)
        except AzureDevOpsClientError as e:
            return f"Error: {str(e)}"
    
    @mcp.tool()
    def get_work_item_basic(
        id: int
    ) -> str:
        """
        Get basic information about a work item.
        
        Args:
            id: The work item ID
            
        Returns:
            Formatted string containing basic work item information
        """
        try:
            wit_client = get_work_item_client()
            return _get_work_item_impl(id, wit_client, detailed=False)
        except AzureDevOpsClientError as e:
            return f"Error: {str(e)}"
    
    @mcp.tool()
    def get_work_item_details(
        id: int
    ) -> str:
        """
        Get detailed information about a work item.
        
        Args:
            id: The work item ID
            
        Returns:
            Formatted string containing comprehensive work item information
        """
        try:
            wit_client = get_work_item_client()
            return _get_work_item_impl(id, wit_client, detailed=True)
        except AzureDevOpsClientError as e:
            return f"Error: {str(e)}"
