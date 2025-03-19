"""
MCP Scholar 服务
提供谷歌学术搜索、论文详情、引用信息和论文总结功能
"""

import logging
import sys
import json
from mcp.server.fastmcp import FastMCP, Context
from mcp_scholar.scholar import (
    search_scholar,
    get_paper_detail,
    get_paper_references,
    parse_profile,
    extract_profile_id_from_url,
)
from typing import Dict, List, Any, Optional

logger = logging.getLogger(__name__)
# 设置日志级别
logging.basicConfig(level=logging.DEBUG)

# 创建MCP服务器
mcp = FastMCP(
    "ScholarServer",
    dependencies=["scholarly", "httpx", "beautifulsoup4"],
    verbose=True,
    debug=True,
)


@mcp.tool()
async def scholar_search(ctx: Context, keywords: str, count: int = 5) -> Dict[str, Any]:
    """
    搜索谷歌学术并返回论文摘要

    Args:
        keywords: 搜索关键词
        count: 返回结果数量，默认为5

    Returns:
        Dict: 包含论文列表的字典
    """
    try:
        # 移除进度显示
        logger.info(f"正在搜索谷歌学术: {keywords}...")
        results = await search_scholar(keywords, count)

        papers = []
        for p in results:
            papers.append(
                {
                    "title": p["title"],
                    "authors": p["authors"],
                    "abstract": (
                        p["abstract"][:200] + "..."
                        if len(p["abstract"]) > 200
                        else p["abstract"]
                    ),
                    "citations": p["citations"],
                    "year": p.get("year", "Unknown"),
                    "paper_id": p.get("paper_id", None),
                }
            )

        return {"status": "success", "papers": papers}
    except Exception as e:
        # 移除错误通知
        logger.error(f"搜索失败: {str(e)}", exc_info=True)
        return {"status": "error", "message": "学术搜索服务暂时不可用", "error": str(e)}


@mcp.tool()
async def paper_detail(ctx: Context, paper_id: str) -> Dict[str, Any]:
    """
    获取论文详细信息

    Args:
        paper_id: 论文ID

    Returns:
        Dict: 论文详细信息
    """
    try:
        # 移除进度显示
        logger.info(f"正在获取论文ID为 {paper_id} 的详细信息...")
        detail = await get_paper_detail(paper_id)

        if detail:
            return {"status": "success", "detail": detail}
        else:
            # 移除错误通知
            logger.warning(f"未找到ID为 {paper_id} 的论文")
            return {"status": "error", "message": f"未找到ID为 {paper_id} 的论文"}
    except Exception as e:
        # 移除错误通知
        logger.error(f"获取论文详情失败: {str(e)}", exc_info=True)
        return {"status": "error", "message": "论文详情服务暂时不可用", "error": str(e)}


@mcp.tool()
async def paper_references(
    ctx: Context, paper_id: str, count: int = 5
) -> Dict[str, Any]:
    """
    获取引用指定论文的文献列表

    Args:
        paper_id: 论文ID
        count: 返回结果数量，默认为5

    Returns:
        Dict: 引用论文列表
    """
    try:
        # 移除进度显示
        logger.info(f"正在获取论文ID为 {paper_id} 的引用...")
        references = await get_paper_references(paper_id, count)

        refs = []
        for ref in references:
            refs.append(
                {
                    "title": ref["title"],
                    "authors": ref["authors"],
                    "abstract": (
                        ref["abstract"][:200] + "..."
                        if len(ref["abstract"]) > 200
                        else ref["abstract"]
                    ),
                    "citations": ref["citations"],
                    "year": ref.get("year", "Unknown"),
                    "paper_id": ref.get("paper_id", None),
                }
            )

        return {"status": "success", "references": refs}
    except Exception as e:
        error_msg = f"获取论文引用失败: {str(e)}"
        # 移除错误通知
        logger.error(error_msg, exc_info=True)
        return {"status": "error", "message": "论文引用服务暂时不可用", "error": str(e)}


@mcp.tool()
async def profile_papers(
    ctx: Context, profile_url: str, count: int = 5
) -> Dict[str, Any]:
    """
    获取学者的高引用论文

    Args:
        profile_url: 谷歌学术个人主页URL
        count: 返回结果数量，默认为5

    Returns:
        Dict: 论文列表
    """
    try:
        # 移除进度显示
        logger.info(f"正在解析个人主页 {profile_url}...")
        profile_id = extract_profile_id_from_url(profile_url)

        if not profile_id:
            # 移除错误通知
            logger.error("无法从URL中提取学者ID")
            return {"status": "error", "message": "无法从URL中提取学者ID"}

        papers = await parse_profile(profile_id, count)

        result_papers = []
        for p in papers:
            result_papers.append(
                {
                    "title": p["title"],
                    "authors": p["authors"],
                    "abstract": (
                        p["abstract"][:200] + "..."
                        if len(p["abstract"]) > 200
                        else p["abstract"]
                    ),
                    "citations": p["citations"],
                    "year": p.get("year", "Unknown"),
                    "venue": p.get("venue", ""),
                    "paper_id": p.get("paper_id", None),
                }
            )

        return {"status": "success", "papers": result_papers}
    except Exception as e:
        error_msg = f"获取学者论文失败: {str(e)}"
        # 移除错误通知
        logger.error(error_msg, exc_info=True)
        return {"status": "error", "message": "学者论文服务暂时不可用", "error": str(e)}


@mcp.tool()
async def summarize_papers(ctx: Context, topic: str, count: int = 5) -> str:
    """
    搜索并总结特定主题的论文

    Args:
        topic: 研究主题
        count: 返回结果数量，默认为5

    Returns:
        str: 论文总结的Markdown格式文本
    """
    try:
        # 移除进度显示
        logger.info(f"正在搜索并总结关于 {topic} 的论文...")

        # 搜索论文
        results = await search_scholar(topic, count)

        if not results:
            return f"未找到关于 {topic} 的论文。"

        # 构建总结
        summary = f"# {topic} 相关研究总结\n\n"
        summary += f"以下是关于 {topic} 的 {len(results)} 篇高引用研究论文的总结：\n\n"

        for i, paper in enumerate(results):
            summary += f"### {i+1}. {paper['title']}\n"
            summary += f"**作者**: {paper['authors']}\n"
            summary += f"**引用量**: {paper['citations']}\n"
            summary += f"**摘要**: {paper['abstract']}\n\n"

        return summary
    except Exception as e:
        # 移除错误通知
        logger.error(f"论文总结失败: {str(e)}", exc_info=True)
        return "论文总结服务暂时不可用"


@mcp.tool()
async def health_check(ctx: Context) -> str:
    """
    健康检查端点，用于验证服务是否正常运行

    Returns:
        str: 服务状态信息
    """
    return "MCP Scholar服务运行正常"


def cli_main():
    """
    CLI入口点，使用STDIO交互
    """
    print("MCP Scholar STDIO服务准备启动...", file=sys.stderr)

    try:
        # 启动STDIO服务器
        sys.stderr.write("MCP Scholar STDIO服务已启动，等待输入...\n")
        sys.stderr.flush()
        mcp.run()
    except Exception as e:
        print(f"服务启动失败: {str(e)}", file=sys.stderr)


def main():
    """
    服务入口点函数，使用WebSocket交互
    """
    try:
        # 启动WebSocket服务器
        mcp.run(host="0.0.0.0", port=8765)
    except Exception as e:
        print(f"服务启动失败: {str(e)}", file=sys.stderr)


if __name__ == "__main__":
    main()
