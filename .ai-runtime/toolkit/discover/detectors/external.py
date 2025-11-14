"""
External Tool Detector - 检测系统已安装的外部CLI工具
"""

import yaml
import shutil
from pathlib import Path
from typing import List, Optional, Dict, Any
from .base import ToolDetector
from ..models import ExternalTool, ToolMetadata
from ..config import EXTERNAL_TOOLS_CONFIG


class ExternalToolDetector(ToolDetector):
    """外部工具检测器"""

    def __init__(self, root_path: Path):
        super().__init__(root_path)
        self._configs = self._load_config()

    def _load_config(self) -> List[Dict[str, Any]]:
        """加载外部工具配置"""
        try:
            with open(EXTERNAL_TOOLS_CONFIG, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
                return config.get('tools', [])
        except Exception as e:
            # 如果配置文件不存在，返回空列表
            return []

    def detect(self) -> List[ExternalTool]:
        """
        检测已安装的外部工具

        Returns:
            List[ExternalTool]: 检测到的外部工具列表
        """
        self._tools = []

        for config in self._configs:
            tool = self._detect_single_tool(config)
            if tool:
                self._tools.append(tool)

        return self._tools

    def _detect_single_tool(self, config: Dict[str, Any]) -> Optional[ExternalTool]:
        """检测单个工具是否已安装"""
        try:
            command = config["command"].split()[0]  # 获取命令名（去除参数）
            is_installed = shutil.which(command) is not None
            tool_path = shutil.which(command)

            # 创建metadata
            metadata = ToolMetadata(
                tool_id=config["tool_id"],
                tool_name=config["tool_name"],
                description=config["description"]
            )

            return ExternalTool(
                metadata=metadata,
                command=config["command"],
                category=config["category"],
                use_cases=config.get("use_cases", []),
                install_guide=config["install_guide"],
                installed=is_installed,
                path=tool_path
            )

        except Exception as e:
            # 静默失败单个工具的检测
            return None

    def refresh(self):
        """刷新工具列表"""
        self._configs = self._load_config()
        super().refresh()

    def find_tool(self, name_or_id: str) -> Optional[ExternalTool]:
        """
        查找外部工具

        Args:
            name_or_id: 工具名称或ID

        Returns:
            ExternalTool: 找到的工具，如果未找到返回None
        """
        # 先尝试精确匹配
        for tool in self._tools:
            if tool.tool_id == name_or_id or tool.tool_name == name_or_id:
                return tool

        # 尝试模糊匹配（名称包含）
        matches = [t for t in self._tools if name_or_id.lower() in t.tool_name.lower()]

        if len(matches) == 1:
            return matches[0]
        elif len(matches) > 1:
            # 不打印，由调用者处理
            return None

        return None

    def get_uninstalled_tools(self) -> List[ExternalTool]:
        """获取未安装的工具列表"""
        return [t for t in self._tools if not t.installed]

    def get_installed_tools(self) -> List[ExternalTool]:
        """获取已安装的工具列表"""
        return [t for t in self._tools if t.installed]
