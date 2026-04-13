"""Example of batch management operations.

This example demonstrates:
- Listing all batches
- Getting details of a specific batch
- Stopping a batch
"""

import asyncio
from kiota_abstractions.authentication import AnonymousAuthenticationProvider
from kiota_http.httpx_request_adapter import HttpxRequestAdapter
from src.mt_http_client import MtHttpClient


async def manage_batches():
    """Demonstrate batch management operations."""
    
    # Configuration - Replace with your actual values
    BASE_URL = "https://smsgw.puzzel.com"
    SERVICE_ID = 12345  # Your Puzzel service ID
    BATCH_REFERENCE = "your-batch-reference"  # Replace with actual batch reference
    
    # Setup client
    auth_provider = AnonymousAuthenticationProvider()
    request_adapter = HttpxRequestAdapter(auth_provider)
    request_adapter.base_url = BASE_URL
    
    client = MtHttpClient(request_adapter)
    
    print("=== Batch Management Examples ===\n")
    
    # 1. List all batches for a service
    print("1. Listing all batches...")
    try:
        batch_list = await client.management.by_service_id(SERVICE_ID).batch.get()
        
        print(f"✓ Found {len(batch_list.message_batch)} batches")
        
        for batch in batch_list.message_batch:
            print(f"\n  Batch Reference: {batch.client_batch_reference}")
            print(f"  Total Messages: {batch.total_size}")
            print(f"  Messages On Hold: {batch.on_hold}")
            print(f"  Messages Sent: {batch.total_size - batch.on_hold}")
            
    except Exception as e:
        print(f"✗ Failed to list batches: {e}")
    
    print("\n" + "="*50 + "\n")
    
    # 2. Get details of a specific batch
    print("2. Getting batch details...")
    try:
        batch_details = await client.management.by_service_id(SERVICE_ID).batch.by_client_batch_reference(BATCH_REFERENCE).get()
        
        batch = batch_details.message_batch
        print(f"✓ Batch details retrieved")
        print(f"\n  Batch Reference: {batch.client_batch_reference}")
        print(f"  Total Size: {batch.total_size}")
        print(f"  On Hold: {batch.on_hold}")
        print(f"  Completion: {((batch.total_size - batch.on_hold) / batch.total_size * 100):.1f}%")
        
    except Exception as e:
        print(f"✗ Failed to get batch details: {e}")
    
    print("\n" + "="*50 + "\n")
    
    # 3. Stop a batch (uncomment to actually stop)
    print("3. Stopping a batch...")
    print("⚠️  This operation is commented out to prevent accidental batch stopping")
    print("    Uncomment the code below to actually stop a batch\n")
    
    # Uncomment the following code to actually stop a batch:
    """
    try:
        stop_response = await client.management.by_service_id(SERVICE_ID).batch.by_client_batch_reference(BATCH_REFERENCE).delete()
        
        print(f"✓ Batch stopped successfully")
        print(f"\n  Service ID: {stop_response.service_id}")
        print(f"  Batch Reference: {stop_response.client_batch_reference}")
        print(f"  Stopped Messages: {len(stop_response.stopped_messages)}")
        
        for stopped in stop_response.stopped_messages:
            print(f"\n    Message ID: {stopped.message_id}")
            print(f"    Client Reference: {stopped.client_message_reference}")
            
    except Exception as e:
        print(f"✗ Failed to stop batch: {e}")
    """
    
    print("\n" + "="*50 + "\n")
    
    # 4. Monitor batch until complete
    print("4. Monitoring batch until complete...")
    print("⚠️  This operation is commented out to prevent long-running monitoring")
    print("    Uncomment the code below to actually monitor a batch\n")
    
    # Uncomment the following code to monitor a batch:
    """
    try:
        check_interval = 5  # seconds
        max_checks = 20
        
        for i in range(max_checks):
            batch_details = await client.management.by_service_id(SERVICE_ID).batch.by_client_batch_reference(BATCH_REFERENCE).get()
            batch = batch_details.message_batch
            
            print(f"Check {i+1}/{max_checks}:")
            print(f"  Total: {batch.total_size}, On Hold: {batch.on_hold}, Sent: {batch.total_size - batch.on_hold}")
            
            if batch.on_hold == 0:
                print("✓ All messages sent!")
                break
            
            if i < max_checks - 1:
                print(f"  Waiting {check_interval} seconds...\n")
                await asyncio.sleep(check_interval)
        else:
            print("⚠️  Max checks reached, batch still has pending messages")
            
    except Exception as e:
        print(f"✗ Failed to monitor batch: {e}")
    """


if __name__ == "__main__":
    asyncio.run(manage_batches())
