from django.conf import settings
import json
import logging
from datetime import datetime, timezone
from asgiref.sync import async_to_sync  # Import this for async execution in Django
from foxsenseinnovations.vigil.vigil_utils.common_utils import mask_sensitive_data
from foxsenseinnovations.vigil.vigil_utils.api_monitoring_utils_django import (
    get_request_fields, get_response_fields, is_monitor_api, generate_path
)
from foxsenseinnovations.vigil.vigil import Vigil
from foxsenseinnovations.vigil.vigil_types.api_monitoring_types import ApiMonitoringOptions, MaskAttributes
from foxsenseinnovations.vigil.api_service_async import ApiServiceAsync
from foxsenseinnovations.vigil.constants.route_constants import RouteConstants

logging.basicConfig(level=logging.INFO, format='%(message)s')

class ApiMonitoringMiddleware:
    """
    ApiMonitoringMiddleware captures and monitors API requests and responses in a Django application.
    It utilizes the Vigil API monitoring system to record and analyze interactions, capturing details like
    headers, parameters, and timing. Integration provides insights for performance optimization and debugging.
    Middleware for monitoring API requests and responses asynchronously.
    """
    def __init__(self, get_response):
        """
        Initializes the ApiMonitoringMiddleware with the given get_response function.
        Args:
            get_response: A function to get the response for the request.
        Returns:
            None
        """
        self.get_response = get_response
        self.options = getattr(settings, 'API_MONITORING_OPTIONS', ApiMonitoringOptions())

    def __call__(self, request):
        """
            	Handles API requests and responses.
        """
        try:
            start_time = datetime.now(timezone.utc).isoformat()
            request.original_body = request.body
            monitor_api = is_monitor_api(
                request,
                request.method,
                request.path if request.path else request.get_full_path(),
                getattr(self.options, "exclude", None),
            )

            response = self.get_response(request)

            if monitor_api:
                end_time = datetime.now(timezone.utc).isoformat()
                api_request = get_request_fields(request)
                api_response = get_response_fields(response)

                mask_attrs = getattr(self.options, "maskAttributes", MaskAttributes())

                request_data = {
                    "host": api_request.host,
                    "userAgent": api_request.request_details["userAgent"],
                    "httpMethod": api_request.httpMethod,
                    "cookies": api_request.request_details["cookies"],
                    "ip": api_request.request_details["ip"],
                    "headers": mask_sensitive_data(api_request.request_details["headers"], mask_attrs.requestHeaders),
                    "requestBody": mask_sensitive_data(api_request.request_details["requestBody"], mask_attrs.requestBody),
                    "protocol": api_request.request_details["protocol"],
                    "hostName": api_request.request_details["hostName"],
                    "url": api_request.url,
                    "path": api_request.request_details["path"],
                    "originalUrl": api_request.originalUrl,
                    "baseUrl": api_request.baseUrl,
                    "query": api_request.request_details["query"],
                    "subDomains": api_request.request_details["subdomains"],
                    "uaVersionBrand": api_request.request_details["uaVersionBrand"],
                    "uaMobile": api_request.request_details["uaMobile"],
                    "uaPlatform": api_request.request_details["uaPlatform"],
                    "reqAcceptEncoding": api_request.request_details["reqAcceptEncoding"],
                    "reqAcceptLanguage": api_request.request_details["reqAcceptLanguage"],
                    "rawHeaders": mask_sensitive_data(api_request.request_details["rawHeaders"], mask_attrs.requestHeaders),
                    "httpVersion": api_request.httpVersion,
                    "remoteAddress": api_request.request_details["remoteAddress"],
                    "remoteFamily": api_request.request_details["remoteFamily"],
                    "params": api_request.request_details["params"],
                }

                try:
                    response_body_dict = json.loads(api_response.responseBody)
                except json.JSONDecodeError:
                    logging.info('Error while converting to json::')
                    raise

                api_response.responseBody = mask_sensitive_data(response_body_dict, mask_attrs.responseBody)
                api_response.responseHeaders = mask_sensitive_data(api_response.responseHeaders, mask_attrs.responseHeaders)

                data = {
                    "clientVersion": self.options.clientVersion if self.options.clientVersion is not None else Vigil.version,
                    "startTime": start_time,
                    "endTime": end_time,
                    "request": request_data,
                    "response": api_response.__dict__
                }

                # Call the async method inside a sync wrapper
                async_to_sync(self.trigger_api_call)(data)

            return response
        except Exception as e:
            logging.error(f"[Vigil] Error in API monitoring middleware: {e}")

    async def trigger_api_call(self, data):
        """
        Asynchronous method to send API monitoring data to an external service.
        """
        try:
            await ApiServiceAsync.make_api_call(
                Vigil.instance_url,
                RouteConstants.API_MONITORING,
                data,
                Vigil.api_key,
            )
            logging.info(
                f"[Vigil] API monitoring record created successfully for {data['request']['path']}"
            )
        except Exception as err:
            logging.error(f"[Vigil] Error while creating API monitoring record: {err}")