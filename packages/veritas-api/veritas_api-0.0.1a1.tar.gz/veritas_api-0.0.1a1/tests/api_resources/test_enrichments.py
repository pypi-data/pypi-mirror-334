# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from veritas_api import VeritasAPI, AsyncVeritasAPI
from veritas_api.types import (
    EnrichmentCreateBulkResponse,
    EnrichmentRetrieveStatusResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestEnrichments:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_create_bulk(self, client: VeritasAPI) -> None:
        enrichment = client.enrichments.create_bulk(
            candidates=[{"name": "name"}],
        )
        assert_matches_type(EnrichmentCreateBulkResponse, enrichment, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_create_bulk(self, client: VeritasAPI) -> None:
        response = client.enrichments.with_raw_response.create_bulk(
            candidates=[{"name": "name"}],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        enrichment = response.parse()
        assert_matches_type(EnrichmentCreateBulkResponse, enrichment, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_create_bulk(self, client: VeritasAPI) -> None:
        with client.enrichments.with_streaming_response.create_bulk(
            candidates=[{"name": "name"}],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            enrichment = response.parse()
            assert_matches_type(EnrichmentCreateBulkResponse, enrichment, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_retrieve_status(self, client: VeritasAPI) -> None:
        enrichment = client.enrichments.retrieve_status(
            "id",
        )
        assert_matches_type(EnrichmentRetrieveStatusResponse, enrichment, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_retrieve_status(self, client: VeritasAPI) -> None:
        response = client.enrichments.with_raw_response.retrieve_status(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        enrichment = response.parse()
        assert_matches_type(EnrichmentRetrieveStatusResponse, enrichment, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_retrieve_status(self, client: VeritasAPI) -> None:
        with client.enrichments.with_streaming_response.retrieve_status(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            enrichment = response.parse()
            assert_matches_type(EnrichmentRetrieveStatusResponse, enrichment, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_retrieve_status(self, client: VeritasAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.enrichments.with_raw_response.retrieve_status(
                "",
            )


class TestAsyncEnrichments:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_create_bulk(self, async_client: AsyncVeritasAPI) -> None:
        enrichment = await async_client.enrichments.create_bulk(
            candidates=[{"name": "name"}],
        )
        assert_matches_type(EnrichmentCreateBulkResponse, enrichment, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_create_bulk(self, async_client: AsyncVeritasAPI) -> None:
        response = await async_client.enrichments.with_raw_response.create_bulk(
            candidates=[{"name": "name"}],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        enrichment = await response.parse()
        assert_matches_type(EnrichmentCreateBulkResponse, enrichment, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_create_bulk(self, async_client: AsyncVeritasAPI) -> None:
        async with async_client.enrichments.with_streaming_response.create_bulk(
            candidates=[{"name": "name"}],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            enrichment = await response.parse()
            assert_matches_type(EnrichmentCreateBulkResponse, enrichment, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_retrieve_status(self, async_client: AsyncVeritasAPI) -> None:
        enrichment = await async_client.enrichments.retrieve_status(
            "id",
        )
        assert_matches_type(EnrichmentRetrieveStatusResponse, enrichment, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_retrieve_status(self, async_client: AsyncVeritasAPI) -> None:
        response = await async_client.enrichments.with_raw_response.retrieve_status(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        enrichment = await response.parse()
        assert_matches_type(EnrichmentRetrieveStatusResponse, enrichment, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_retrieve_status(self, async_client: AsyncVeritasAPI) -> None:
        async with async_client.enrichments.with_streaming_response.retrieve_status(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            enrichment = await response.parse()
            assert_matches_type(EnrichmentRetrieveStatusResponse, enrichment, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_retrieve_status(self, async_client: AsyncVeritasAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.enrichments.with_raw_response.retrieve_status(
                "",
            )
