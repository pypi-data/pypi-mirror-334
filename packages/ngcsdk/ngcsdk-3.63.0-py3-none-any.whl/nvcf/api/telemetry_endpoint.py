#
# Copyright (c) 2025 NVIDIA CORPORATION & AFFILIATES. ALL RIGHTS RESERVED.
#
# This software product is a proprietary product of Nvidia Corporation and its affiliates
# (the "Company") and all right, title, and interest in and to the software
# product, including all associated intellectual property rights, are and
# shall remain exclusively with the Company.
#
# This software product is governed by the End User License Agreement
# provided with the software product.
#
from __future__ import annotations

import http
import json
from typing import Any, Optional, TYPE_CHECKING, Union

from ngcbase.api.utils import DotDict
from ngcbase.errors import NgcAPIError

if TYPE_CHECKING:
    import ngcsdk

    import ngccli.api.apiclient

    Client = Union[ngccli.api.apiclient.APIClient, ngcsdk.APIClient]


class TelemetryEndpointAPI:  # noqa: D101
    def __init__(self, api_client) -> None:
        self.connection = api_client.connection
        self.config = api_client.config
        self.client = api_client

    @staticmethod
    def _construct_telemetry_ep(
        org_name: str,
        team_name: Optional[str] = None,
        telemetry_id: Optional[str] = None,
    ) -> str:
        parts = ["v2/orgs", org_name]
        if team_name:
            parts.extend(["teams", team_name])
        parts.extend(["nvcf", "telemetries"])
        if telemetry_id:
            parts.append(telemetry_id)
        return "/".join(parts)

    def list(self) -> DotDict:
        """List Telemetry endpoints.

        Returns:
            dict: Keyed List of Functions.
        """
        self.config.validate_configuration()
        org_name: str = self.config.org_name
        team_name: Optional[str] = self.config.team_name
        url = self._construct_telemetry_ep(org_name, team_name)
        response = self.connection.make_api_request(
            "GET",
            url,
            auth_org=org_name,
            auth_team=team_name,
            operation_name="list telemetry-endpoints",
        )
        return DotDict(response)

    def create(
        self,
        name: str,
        endpoint: str,
        protocol: str,
        provider: str,
        key: str,
        types: list[str],
    ) -> DotDict:
        """Add Telemetry endpoints.

        Returns:
            dict: Keyed List of Functions.
        """
        self.config.validate_configuration()
        org_name: str = self.config.org_name
        team_name: Optional[str] = self.config.team_name
        url = self._construct_telemetry_ep(org_name, team_name)
        value = ""
        if provider == "GRAFANA_CLOUD":
            value = {"instanceId": "test2", "apiKey": "test"}
        if provider == "DATADOG":
            value = key
        secret = {"name": name, "value": value}

        payload: dict[str, Any] = {
            "endpoint": endpoint,
            "provider": provider,
            "protocol": protocol,
            "types": types,
            "secret": secret,
        }
        response = self.connection.make_api_request(
            "POST",
            url,
            payload=json.dumps(payload),
            auth_org=org_name,
            auth_team=team_name,
            operation_name="create telemetry-endpoint",
        )
        return DotDict(response)

    def delete(self, telemetry_id: str):
        """Delete Telemetry endpoint.

        Returns:
            dict: Keyed List of Functions.
        """
        self.config.validate_configuration()
        org_name: str = self.config.org_name
        team_name: Optional[str] = self.config.team_name
        url = self._construct_telemetry_ep(org_name, team_name, telemetry_id)
        try:
            self.connection.make_api_request(
                "DELETE",
                url,
                auth_org=org_name,
                auth_team=team_name,
                operation_name="delete telemetry-endpoint",
            )
        except NgcAPIError as e:
            if (
                e.response.status_code != http.client.NO_CONTENT
            ):  # Delete endpoint throws 204 which by default throws exception.
                raise NgcAPIError(e) from e
