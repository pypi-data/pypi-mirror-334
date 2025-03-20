from typing import Dict, List, Literal, Optional

import aiofiles
from pydantic import BaseModel, Field
from launart import Launart

from cocotst.message.keyboard import KeyboardContent
from cocotst.network.services import HttpxClientSessionService


class Element(BaseModel):
    """消息元素"""


class MediaElement(Element):
    """媒体消息元素"""

    data: Optional[bytes] = Field(b"", description="媒体资源数据")
    """媒体资源数据"""
    media_id: Optional[str] = Field("", description="媒体资源ID")
    """媒体资源ID"""
    media_url: Optional[str] = Field("", description="媒体资源链接")    
    """媒体资源链接"""
    path: Optional[str] = Field("", description="媒体资源路径")
    """媒体资源路径"""
    type: Literal["image", "video", "voice", "file"] = Field("", description="媒体资源类型")
    """媒体资源类型"""
    url: Optional[str] = Field("", description="媒体资源链接")
    """媒体资源链接"""

    def __init__(self, data: Optional[bytes] = b'', path: Optional[str] = "", url: Optional[str] = ""):
        try:
            assert data or path or url
        except AssertionError:
            raise ValueError("data ,path, url 不能同时为空")
        super().__init__(data=data, path=path, url=url)

    async def as_data_bytes(self):
        """将媒体资源转换为 bytes"""
        if self.data:
            return self.data
        if self.path:
            async with aiofiles.open(self.path, "rb") as f:
                return await f.read()
        if self.url:
            session = Launart.current().get_component(HttpxClientSessionService).async_client
            resp = await session.get(self.url)
            return resp.content


class Image(MediaElement):
    """图片消息元素"""

    type: Literal["image"] = "image"


class Video(MediaElement):
    """视频消息元素"""

    type: Literal["video"] = "video"


class Voice(MediaElement):
    """语音消息元素"""

    type: Literal["voice"] = "voice"


class File(MediaElement):
    """文件消息元素"""

    type: Literal[4] = 4

    def __init__(self, url: Optional[str] = None, path: Optional[str] = None):
        raise NotImplementedError("文件消息元素暂不支持")


class Markdown(Element):
    """Markdown 消息元素"""

    content: str
    """原生 markdown 文本内容"""
    custom_template_id: str
    """markdown 模版id，申请模版后获得"""
    params: List[Dict]
    """{key: xxx, values: xxx}，模版内变量与填充值的kv映射"""
    Keyboard: Optional["Keyboard"] = None
    """依赖于 Markdown 的消息按钮"""


class Keyboard(Element):
    """消息按钮元素，可独立使用，也可依赖于 Markdown，依赖于 Markdown 时请将此元素放在 Markdown 元素内"""

    id: Optional[str] = Field(None, description="申请模版后获得的ID")
    content: Optional[KeyboardContent] = Field(None, description="自定义按钮内容")

    def __init__(self, id: Optional[str] = None, content: Optional[Dict] = None):
        """初始化消息按钮元素

        Args:
            id: 按钮模版ID
            content: 自定义按钮内容
        """
        if bool(id) == bool(content):
            raise ValueError("id 和 content 必须且只能传入其中一个")
        keyboard_content = KeyboardContent(**content) if content else None
        super().__init__(id=id, content=keyboard_content)


class Embed(Element): ...  # Incomplete


class Ark(Element): ...  # Incomplete
