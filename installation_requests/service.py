"""Service."""
import json
from datetime import datetime, timezone
from typing import Any

from marshmallow import ValidationError
from nameko.events import EventDispatcher
from nameko.web.handlers import HttpRequestHandler
from nameko_sqlalchemy import DatabaseSession
from werkzeug import Response
from installation_requests.exceptions import BadRequest, HttpError, NotFound
from installation_requests.models import DeclarativeBase, InstallationRequest
from installation_requests.schemas import CreateInstallationRequestSchema, InstallationRequestSchema


class HttpEntrypoint(HttpRequestHandler):
    """Control formatting of errors returned from the service by overriding response_from_exception().

    more https://nameko.readthedocs.io/en/stable/built_in_extensions.html#http.
    """

    def response_from_exception(self, exc: Exception) -> Response:
        """Response_from_exception."""

        if isinstance(exc, HttpError):
            response = Response(
                json.dumps(
                    {
                        "errors": exc.args[0],
                    }
                ),
                status=exc.status_code,
                mimetype="application/json",
            )
            return response
        return HttpRequestHandler.response_from_exception(self, exc)


http = HttpEntrypoint.decorator


class InstallationRequestsService:
    """InstallationRequestsService."""

    name = "installation_requests"

    db = DatabaseSession(DeclarativeBase)
    event_dispatcher = EventDispatcher()

    @http("GET", "/installation-requests/<int:request_id>", expected_exceptions=NotFound)
    def get_installation_request(self, request: Any, request_id: int) -> Response:
        """Get Installation Request by Id."""

        installation_request = self.db.query(InstallationRequest).get(request_id)

        if not installation_request:
            raise NotFound("Element not found !")

        return Response(
            InstallationRequestSchema().dumps(installation_request),
            mimetype="application/json",
        )

    @http("GET", "/installation-requests")
    def get_all_installation_requests(self, request: Any) -> Response:
        """Get All Installation Requests."""

        installation_requests = self.db.query(InstallationRequest).all()

        return Response(
            InstallationRequestSchema(many=True).dumps(installation_requests),
            mimetype="application/json",
        )

    @http("POST", "/installation-requests")
    def create_installation_request(self, request: Any) -> Response:
        """Create Installation Request."""

        schema = CreateInstallationRequestSchema(exclude=("created_at", "updated_at"))
        try:
            # use marshmallow schema for validation
            # Note - this may raise `ValueError` for invalid json,
            # or `ValidationError` if data is invalid.
            installation_request = schema.load(
                json.loads(request.get_data(as_text=True)), session=self.db
            )
        except ValidationError as exc:
            raise BadRequest(exc.messages)

        self.db.add(installation_request)
        self.db.commit()
        return Response(
            json.dumps({"id": installation_request.id}),
            mimetype="application/json",
        )

    @http("DELETE", "/installation-requests/<int:request_id>")
    def delete_installation_request(self, request: Any, request_id: int) -> Any:
        """Delete Installation Request."""

        installation_request = self.db.query(InstallationRequest).get(request_id)

        if not installation_request:
            raise NotFound("Element not found !")

        self.db.delete(installation_request)
        self.db.commit()
        return 204, "Ressource deleted successfully"

    @http("PUT", "/installation-requests/<int:request_id>")
    def update_installation_request(self, request: Any, request_id: int) -> Response:
        """Update Installation Request."""

        installation_request = self.db.query(InstallationRequest).get(request_id)

        if not installation_request:
            raise NotFound("Element not found !")

        request_body = json.loads(request.get_data(as_text=True))
        installation_request.updated_at = datetime.now(timezone.utc)
        installation_request.status = request_body.get("status") or installation_request.status
        installation_request.type = (
            request_body.get("equipment_type") or installation_request.equipment_type
        )
        installation_request.brand = (
            request_body.get("equipment_brand") or installation_request.equipment_brand
        )
        installation_request.model = (
            request_body.get("equipment_model") or installation_request.equipment_model
        )
        installation_request.comment = request_body.get("comment") or installation_request.comment

        self.db.commit()
        return 200, "Element updated successfully"
