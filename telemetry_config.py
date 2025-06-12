import logging
import boto3
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.resources import Resource

def setup_telemetry(service_name="agent-service", bucket_name="your-s3-bucket-name"):
    # Set up resource with service info
    resource = Resource.create({"service.name": service_name})
    
    # Configure tracer provider with the resource
    tracer_provider = TracerProvider(resource=resource)
    trace.set_tracer_provider(tracer_provider)
    
    # Create S3 client for logs
    s3_client = boto3.client('s3')
    
    # Set up logging to S3
    logger = logging.getLogger("agent_telemetry")
    logger.setLevel(logging.INFO)
    
    # Create custom S3 handler
    class S3LogHandler(logging.Handler):
        def __init__(self, bucket_name, log_prefix="agent-logs/"):
            super().__init__()
            self.bucket_name = bucket_name
            self.log_prefix = log_prefix
            self.s3_client = s3_client
            self.buffer = []
            
        def emit(self, record):
            log_entry = self.format(record)
            self.buffer.append(log_entry)
            if len(self.buffer) >= 10:  # Adjust batch size as needed
                self.flush()
                
        def flush(self):
            if not self.buffer:
                return
                
            log_content = "\n".join(self.buffer)
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
            key = f"{self.log_prefix}{timestamp}.log"
            
            try:
                self.s3_client.put_object(
                    Bucket=self.bucket_name,
                    Key=key,
                    Body=log_content
                )
                self.buffer = []
            except Exception as e:
                print(f"Error uploading logs to S3: {e}")
    
    # Add S3 handler to logger
    s3_handler = S3LogHandler(bucket_name)
    formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')
    s3_handler.setFormatter(formatter)
    logger.addHandler(s3_handler)
    
    return logger, trace.get_tracer(service_name)