from typing import List
from pydantic import BaseModel, Field

from botrun_hatch.models.upload_file import UploadFile


class Hatch(BaseModel):
    """
    @user_prompt_prefix: 每次的 user prompt 前面都會加入這段文字
    @search_domain_filter: 搜尋的網域限制, 目前只有針對 perplexit 有效, 範例：["*.gov.tw", "-*.gov.cn"]
    @files: 上傳的檔案，這裡存的是 metadata，真正的檔案會存在 gcs，以 user_id/id 為 key來存，目前只會存extract後純文字的內容
    @agent_model_name: 使用 agent 時的 model 名稱
    """

    user_id: str
    id: str
    model_name: str = ""
    agent_model_name: str = ""
    prompt_template: str
    user_prompt_prefix: str = ""
    name: str = ""  # 将 name 设为可选字段，默认为空字符串
    is_default: bool = False
    enable_search: bool = False
    related_question_prompt: str = ""
    search_vendor: str = "perplexity"
    search_domain_filter: List[str] = []
    files: List[UploadFile] = []
    enable_agent: bool = False
    enable_api: bool = False
