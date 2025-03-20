from .handler_cli import HandlerCli
from src.services.virustotal.cli.virustotal_cli_service import VirustotalCliService
from src.interfaces.success_response import SuccessResponse
from src.core.application.response.cli.failed_response_builder import FailureResponseBuilder

class VirustotalHandler(HandlerCli):
    
    
    def run_service(self, uri, success_response: SuccessResponse):
        try:
            return VirustotalCliService(success_response=success_response).read(uri=uri)
        except Exception as ex:
            failed_response = FailureResponseBuilder().build_invalid_request_exception_object(ex)
            print(failed_response) 
    
    def __str__(self) -> str:
        return 'Using Virustotal'
        
            