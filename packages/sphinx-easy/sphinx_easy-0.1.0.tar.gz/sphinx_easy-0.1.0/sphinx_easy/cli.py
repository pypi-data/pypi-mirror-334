"""Command line interface for Sphinx documentation."""

import sys
import click
from pathlib import Path
import shutil
from sphinx.cmd.build import build_main
from sphinx.cmd.quickstart import main as quickstart_main

@click.group()
def main():
    """Simplified command line interface for Sphinx documentation."""
    pass

def _init_sphinx(dir, project, author, version, language, makefile, batchfile):
    """内部函数：初始化Sphinx文档项目"""
    click.echo(f"初始化Sphinx文档项目于 {dir}...")
    
    # 准备sphinx-quickstart的参数
    args = [
        '--project=' + project,
        '--author=' + author,
        '--release=' + version,
        '--sep',  # 分离源码和构建目录
        '--dot=_',  # 使用_作为_build中的点
        '--language=' + language,
    ]
    
    if not makefile:
        args.append('--no-makefile')
    
    if not batchfile:
        args.append('--no-batchfile')
        
    args.append(dir)  # 输出目录
    
    # 调用sphinx-quickstart
    sys.argv[1:] = args
    quickstart_main(args)
    
    # 默认添加必要的扩展
    default_extensions = [
        'sphinx.ext.autodoc',
        'sphinx.ext.napoleon',
        'sphinx.ext.viewcode',
        'myst_parser',
        'sphinx_markdown_builder'
    ]
    
    conf_path = Path(dir) / 'source' / 'conf.py'
    if conf_path.exists():
        with open(conf_path, 'r', encoding='utf-8') as f:
            conf_content = f.read()
        
        # 查找扩展列表
        if 'extensions = [' in conf_content:
            # 添加必要的扩展
            extension_str = ', '.join([f"'{ext}'" for ext in default_extensions])
            conf_content = conf_content.replace('extensions = [', f'extensions = [{extension_str}, ')
            
            # 添加myst_parser配置
            if 'myst_parser' in default_extensions and '# -- General configuration ---' in conf_content:
                myst_config = '''
# MyST Parser configuration
myst_enable_extensions = [
    "amsmath",
    "colon_fence",
    "deflist",
    "dollarmath",
    "html_admonition",
    "html_image",
    "linkify",
    "replacements",
    "smartquotes",
    "substitution",
    "tasklist",
]
'''
                conf_content = conf_content.replace('# -- General configuration ---', 
                                                  '# -- General configuration ---\n' + myst_config)
                conf_content = conf_content.replace('------------------------------------------------\n', '')
            
            with open(conf_path, 'w', encoding='utf-8') as f:
                f.write(conf_content)
            
            click.echo(f"已添加默认扩展: {', '.join(default_extensions)}")
    
    click.echo(f"Sphinx文档项目初始化成功: {dir}")

def _build_sphinx(sourcedir, builddir, builder, clean):
    """内部函数：构建Sphinx文档"""
    click.echo(f"使用{builder}构建器构建文档...")
    
    # 确保路径是绝对路径
    sourcedir = Path(sourcedir).absolute()
    builddir = Path(builddir).absolute()
    
    # 准备sphinx-build的参数
    args = []
    
    if clean and builddir.exists():
        click.echo(f"清理构建目录: {builddir}")
        shutil.rmtree(builddir, ignore_errors=True)
    
    builder_dir = builddir / builder
    args.extend([
        '-b', builder,
        str(sourcedir),
        str(builder_dir)
    ])
    
    # 调用sphinx-build
    result = build_main(args)
    if result == 0:
        click.echo(f"文档构建成功，位于: {builder_dir}")
        return True
    else:
        click.echo(f"构建文档时出错。退出代码: {result}", err=True)
        return False

@main.command()
@click.option('--dir', '-d', default='.', help='初始化Sphinx文档的目录。')
@click.option('--project', '-p', default='My Project', help='项目名称。')
@click.option('--author', '-a', default='Author', help='作者名称。')
@click.option('--version', '-v', default='0.1', help='项目版本。')
@click.option('--language', '-l', default='en', help='文档语言。')
@click.option('--makefile/--no-makefile', default=True, help='创建Makefile')
@click.option('--batchfile/--no-batchfile', default=True, help='在Windows上创建批处理文件')
@click.option('--sourcedir', '-s', default='source', help='源码目录。')
@click.option('--builddir', '-b', default='build', help='构建目录。')
@click.option('--builder', '-B', default='markdown', help='要使用的构建器(html, pdf等)。')
@click.option('--clean/--no-clean', default=False, help='构建前清理构建目录。')
@click.option('--skip-init/--no-skip-init', default=False, help='如果已存在配置，跳过初始化步骤。')
def create(dir, project, author, version, language, makefile, batchfile,
           sourcedir, builddir, builder, clean, skip_init):
    """初始化并构建Sphinx文档。
    
    如果指定目录下已存在Sphinx项目（检测conf.py文件），则只执行构建步骤。
    否则，先初始化项目，然后执行构建。
    """
    dir_path = Path(dir)
    source_path = dir_path / sourcedir
    conf_path = source_path / 'conf.py'
    
    # 检查是否已存在Sphinx项目
    sphinx_exists = conf_path.exists()
    
    # 如果不存在或明确指定不跳过初始化，则执行初始化
    if not sphinx_exists or not skip_init:
        try:
            _init_sphinx(dir, project, author, version, language, makefile, batchfile)
        except Exception as e:
            click.echo(f"初始化Sphinx文档时出错: {e}", err=True)
            sys.exit(1)
    else:
        click.echo(f"检测到现有的Sphinx项目，跳过初始化步骤...")
    
    # 执行构建
    try:
        success = _build_sphinx(source_path, dir_path / builddir, builder, clean)
        if not success:
            sys.exit(1)
    except Exception as e:
        click.echo(f"构建文档时出错: {e}", err=True)
        sys.exit(1)

@main.command()
@click.option('--builddir', '-b', default='build/html', help='Build directory containing HTML files.')
@click.option('--port', '-p', default=8000, help='Port to serve documentation on.')
def serve(builddir, port):
    """Serve documentation using a simple HTTP server."""
    builddir = Path(builddir).absolute()
    
    if not builddir.exists():
        click.echo(f"Build directory {builddir} does not exist. Build the documentation first.", err=True)
        sys.exit(1)
    
    click.echo(f"Serving documentation from {builddir} on http://localhost:{port}")
    click.echo("Press Ctrl+C to stop the server")
    
    try:
        import http.server
        import socketserver
        import os  # 仍需保留os导入用于chdir操作
        
        # 使用os.chdir因为http.server需要当前工作目录
        os.chdir(builddir)
        
        Handler = http.server.SimpleHTTPRequestHandler
        httpd = socketserver.TCPServer(("localhost", port), Handler)
        httpd.serve_forever()
    except KeyboardInterrupt:
        click.echo("\nServer stopped")
    except Exception as e:
        click.echo(f"Error serving documentation: {e}", err=True)
        sys.exit(1)

if __name__ == '__main__':
    main()