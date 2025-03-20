import httpx

from ._client import AsyncAPIClient
from ._constants import DEFAULT_MAX_RETRIES, DEFAULT_TIMEOUT
from ._types import AllowedExtensionsResponse, Document, DocumentResponse, ParseParams


class AsyncParse(AsyncAPIClient):
    def __init__(
        self,
        base_url="http://localhost:8000",
        timeout: httpx.Timeout = DEFAULT_TIMEOUT,
        max_retries: int = DEFAULT_MAX_RETRIES,
    ):
        super().__init__(base_url=base_url, timeout=timeout, max_retries=max_retries)
        self.parse_endpoint = "parse"

    async def allowed_extensions(self) -> list[str]:
        res = await self.get(
            self.parse_endpoint + "/allowed_extensions",
            cast_to=AllowedExtensionsResponse,
        )
        return res.data.allowed_extensions

    async def parse(
        self,
        file_path: str,
        has_watermark: bool | None = None,
        force_convert_pdf: bool | None = None,
        force_ocr_all_pages: bool | None = None,
        timeout: httpx.Timeout | None = None,
        use_olm_pdf: bool | None = None,
        olm_api_url: str | None = None,
    ) -> Document:
        params = ParseParams(
            has_watermark=has_watermark,
            force_convert_pdf=force_convert_pdf,
            force_ocr_all_pages=force_ocr_all_pages,
            use_olm_pdf=use_olm_pdf,
            olm_api_url=olm_api_url,
        )
        
        # 将所有非空参数放入 data 字典中
        data_dict = params.model_dump(exclude_none=True)
        res = await self.post(
            self.parse_endpoint,
            cast_to=DocumentResponse,
            options={
                "files": {"file": open(file_path, "rb")},
                "data": data_dict,
                "timeout": timeout,
            },
        )
        return res.data
