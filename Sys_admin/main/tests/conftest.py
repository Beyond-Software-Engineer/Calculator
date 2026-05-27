import os
import pytest
from openai import OpenAI
from dotenv import load_dotenv
from datetime import datetime

# 加载环境变量
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

# 配置OpenAI客户端（使用1.0+版本API，兼容DeepSeek等模型）
client = OpenAI(
    api_key=os.getenv('AI_API_KEY'),
    base_url=os.getenv('AI_API_BASE_URL', 'https://api.deepseek.com')
)

# 存储AI测试结果
ai_test_results = []

def pytest_addoption(parser):
    """添加--ai-report命令行选项"""
    parser.addoption(
        "--ai-report",
        action="store",
        default=None,
        help="生成AI测试报告的文件名（HTML格式）"
    )

def pytest_configure(config):
    """配置pytest"""
    config.addinivalue_line("markers", "ai_test: 标记需要AI分析的测试")

@pytest.fixture(autouse=True)
def ai_test_fixture(request):
    """AI测试夹具，用于收集测试信息并调用AI分析"""
    if request.node.get_closest_marker('ai_test'):
        test_name = request.node.name
        test_doc = request.node.function.__doc__ or ""
        start_time = datetime.now()

        yield

        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        status = "PASSED" if request.node.report.passed else "FAILED"
        error_message = str(request.node.report.longrepr) if not request.node.report.passed else ""

        # 调用AI分析测试结果
        ai_analysis = analyze_with_ai(test_name, test_doc, status, error_message, duration)

        ai_test_results.append({
            'name': test_name,
            'doc': test_doc,
            'status': status,
            'duration': duration,
            'error_message': error_message,
            'ai_analysis': ai_analysis
        })

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """捕获测试报告并保存到测试节点"""
    outcome = yield
    report = outcome.get_result()
    item.report = report

def analyze_with_ai(test_name, test_doc, status, error_message, duration):
    """调用AI大模型分析测试结果"""
    api_key = os.getenv('AI_API_KEY')
    if not api_key or api_key == "your-api-key-here":
        return "未配置有效的AI API密钥，跳过AI分析"

    try:
        prompt = f"""
        请分析以下测试用例的执行结果：

        测试名称: {test_name}
        测试描述: {test_doc}
        执行状态: {status}
        执行时长: {duration:.2f}秒
        错误信息: {error_message}

        请提供以下分析：
        1. 测试用例的目的和覆盖的功能
        2. 如果测试通过，分析测试结果是否符合预期
        3. 如果测试失败，分析可能的原因和修复建议
        4. 改进测试用例的建议
        """

        response = client.chat.completions.create(
            model=os.getenv('AI_MODEL', 'deepseek-chat'),
            messages=[
                {"role": "system", "content": "你是一位专业的软件测试工程师，擅长分析测试用例和提供改进建议。"},
                {"role": "user", "content": prompt}
            ],
            max_tokens=int(os.getenv('AI_MAX_TOKENS', 1024)),
            temperature=float(os.getenv('AI_TEMPERATURE', 0.7))
        )

        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"AI分析失败: {str(e)}"

def pytest_sessionfinish(session, exitstatus):
    """测试会话结束时生成AI报告"""
    ai_report_path = session.config.getoption("--ai-report")
    if ai_report_path and ai_test_results:
        generate_html_report(ai_report_path, ai_test_results)

def generate_html_report(file_path, results):
    """生成HTML格式的AI测试报告（支持Markdown渲染）"""
    html_content = f"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI测试报告</title>
    <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; padding: 20px; background-color: #f5f5f5; }}
        .container {{ max-width: 1200px; margin: 0 auto; background-color: white; padding: 30px; border-radius: 10px; box-shadow: 0 0 20px rgba(0,0,0,0.1); }}
        h1 {{ color: #333; text-align: center; margin-bottom: 30px; }}
        .test-item {{ margin-bottom: 25px; padding: 20px; border-radius: 8px; border-left: 4px solid; }}
        .test-item.passed {{ border-color: #28a745; background-color: #f8fff9; }}
        .test-item.failed {{ border-color: #dc3545; background-color: #fff5f5; }}
        .test-name {{ font-size: 18px; font-weight: bold; margin-bottom: 10px; }}
        .test-doc {{ color: #666; margin-bottom: 10px; font-style: italic; }}
        .test-meta {{ font-size: 14px; color: #888; margin-bottom: 15px; }}
        .status {{ display: inline-block; padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: bold; }}
        .status.passed {{ background-color: #28a745; color: white; }}
        .status.failed {{ background-color: #dc3545; color: white; }}
        .ai-analysis {{ background-color: #e9f5ff; padding: 15px; border-radius: 6px; margin-top: 15px; }}
        .ai-analysis h4 {{ margin-top: 0; color: #007bff; }}
        .error-message {{ color: #dc3545; font-family: monospace; font-size: 14px; }}
        .summary {{ margin-bottom: 30px; padding: 20px; background-color: #f8f9fa; border-radius: 8px; }}
        .summary div {{ display: inline-block; margin-right: 30px; font-size: 16px; }}
        .summary span {{ font-weight: bold; }}
        .timestamp {{ text-align: center; color: #999; font-size: 14px; margin-top: 30px; }}

        /* Markdown 渲染样式 */
        .markdown-content {{ line-height: 1.6; }}
        .markdown-content h1, .markdown-content h2, .markdown-content h3, .markdown-content h4 {{ color: #333; margin-top: 20px; margin-bottom: 10px; font-weight: bold; }}
        .markdown-content h1 {{ font-size: 1.5em; border-bottom: 2px solid #007bff; padding-bottom: 10px; }}
        .markdown-content h2 {{ font-size: 1.3em; border-bottom: 1px solid #ddd; padding-bottom: 8px; }}
        .markdown-content h3 {{ font-size: 1.1em; }}
        .markdown-content h4 {{ font-size: 1em; color: #007bff; margin-top: 15px; }}
        .markdown-content p {{ margin: 10px 0; }}
        .markdown-content ul, .markdown-content ol {{ margin: 10px 0; padding-left: 25px; }}
        .markdown-content li {{ margin: 5px 0; }}
        .markdown-content strong {{ color: #d63384; }}
        .markdown-content code {{ background-color: #f4f4f4; padding: 2px 6px; border-radius: 3px; font-family: 'Consolas', 'Monaco', monospace; font-size: 0.9em; }}
        .markdown-content pre {{ background-color: #f8f9fa; padding: 15px; border-radius: 6px; overflow-x: auto; border: 1px solid #e9ecef; }}
        .markdown-content pre code {{ background-color: transparent; padding: 0; }}
        .markdown-content blockquote {{ border-left: 4px solid #007bff; background-color: #f8f9fa; margin: 10px 0; padding: 10px 15px; color: #666; }}
        .markdown-content hr {{ border: none; border-top: 1px solid #ddd; margin: 20px 0; }}
        .markdown-content table {{ border-collapse: collapse; width: 100%; margin: 15px 0; }}
        .markdown-content table th, .markdown-content table td {{ border: 1px solid #ddd; padding: 10px; text-align: left; }}
        .markdown-content table th {{ background-color: #f8f9fa; font-weight: bold; }}
        .markdown-content table tr:nth-child(even) {{ background-color: #f9f9f9; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🤖 AI测试报告</h1>

        <div class="summary">
            <div>总测试数: <span>{len(results)}</span></div>
            <div>通过: <span style="color: #28a745;">{sum(1 for r in results if r['status'] == 'PASSED')}</span></div>
            <div>失败: <span style="color: #dc3545;">{sum(1 for r in results if r['status'] == 'FAILED')}</span></div>
            <div>总时长: <span>{sum(r['duration'] for r in results):.2f}秒</span></div>
        </div>
        {''.join([generate_test_item_html(result) for result in results])}
        <div class="timestamp">报告生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</div>
    </div>
    <script>
        // 使用 marked.js 渲染 Markdown 内容
        document.addEventListener('DOMContentLoaded', function() {{
            const markdownContents = document.querySelectorAll('.markdown-content');
            markdownContents.forEach(function(element) {{
                const markdownText = element.textContent;
                element.innerHTML = marked.parse(markdownText);
            }});
        }});
    </script>
</body>
</html>
"""

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

def generate_test_item_html(result):
    """生成单个测试项的HTML内容"""
    return f"""
<div class="test-item {'passed' if result['status'] == 'PASSED' else 'failed'}">
    <div class="test-name">
        {result['name']}
        <span class="status {'passed' if result['status'] == 'PASSED' else 'failed'}">{result['status']}</span>
    </div>
    {f'<div class="test-doc">📝 {result["doc"]}</div>' if result['doc'] else ''}
    <div class="test-meta">
        ⏱️ 执行时长: {result['duration']:.2f}秒
    </div>
    {f'<div class="error-message">❌ 错误信息: {result["error_message"]}</div>' if result['error_message'] else ''}
    <div class="ai-analysis">
        <h4>🧠 AI分析结果</h4>
        <div class="markdown-content">{result['ai_analysis']}</div>
    </div>
</div>
"""

# 自定义ai_test装饰器
def ai_test(func):
    """标记测试用例需要AI分析的装饰器"""
    func.__ai_test__ = True
    return pytest.mark.ai_test(func)
