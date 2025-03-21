"""SpeeDBeeSynapse custom component development environment tool."""
from __future__ import annotations

import copy
import importlib
import importlib.resources
import json
import sys
import uuid
import warnings
from pathlib import Path
from typing import Optional

from . import pack, utils
from . import resources as sccde_resources

INFO_FILE_NAME = 'scc-info.json'
SCC_INFO = {
    'package-name': '',
    'package-version': '0.1.0',
    'package-uuid': '',
    'package-description': 'Your package descrition here',
    'python-components-source-dir': 'source/python',
    'author': '',
    'license': '',
    'license-file': '',
    'components': {},
}


def get_components(info_path: Path) -> list[str]:
    """Return module list for syntax-check."""
    # 環境情報ファイルを読み込み
    with info_path.open(mode='rt') as fo:
        info = json.load(fo)

    # module
    return [ c['modulename'] for c in info['components'].values() ]


def check_python(info_path: Path, target: str) -> None:
    """Check python module syntax."""
    # 環境情報ファイルを読み込み
    with info_path.open(mode='rt') as fo:
        info = json.load(fo)

    # speedbeesynapse.component.base用のPYTHONPATH
    current_dir = Path(__file__).parent
    sys.path.append(str(current_dir / 'synapse_fw'))

    # ユーザーカスタムコンポーネント用のPYTHONPATH
    sys.path.append(str(info_path.parent / info['python-components-source-dir']))

    # ユーザーカスタムコンポーネントのimport.
    mod = importlib.import_module(target)
    utils.print_info(mod.HiveComponent)
    utils.print_info(mod.HiveComponent._hive_uuid) # noqa: SLF001
    utils.print_info(mod.HiveComponent._hive_name) # noqa: SLF001
    utils.print_info(mod.HiveComponent._hive_tag) # noqa: SLF001
    utils.print_info(mod.HiveComponent._hive_inports) # noqa: SLF001
    utils.print_info(mod.HiveComponent._hive_outports) # noqa: SLF001


class Sccde:

    """Sccde directory management class."""

    def __init__(self, work_dir: Path) -> None:
        """Initialize."""
        self.work_dir = work_dir

    def init(self, package_name: str) -> None:
        """Initialize resource repogitory."""
        with (self.work_dir / INFO_FILE_NAME).open(mode='wt') as fo:
            info = copy.deepcopy(SCC_INFO)
            info['package-name'] = package_name
            info['package-uuid'] = str(uuid.uuid4())

            json.dump(info, fo, ensure_ascii=False, indent=2)
            fo.write('\n')

    def add_sample(self, sample_lang: str, sample_type: str) -> None:
        """Add sample into the current environment."""
        if sample_lang == 'none':
            return

        info_path = self.work_dir / INFO_FILE_NAME

        # 環境情報ファイルを読み込み
        with info_path.open(mode='rt') as fo:
            info = json.load(fo)

        # 追加するサンプルのUUIDの生成、ファイル名サフィックスの決定
        suffix_num = len(info['components']) + 1
        new_uuid = str(uuid.uuid4())

        if sample_lang == 'python':
            # Python用のディレクトリの準備
            python_dir = info_path.parent / info['python-components-source-dir']
            python_dir.mkdir(parents=True, exist_ok=True)

            # Pythonカスタムコンポーネントサンプルのコピー
            with (python_dir / f'sample_{sample_type}_{suffix_num}.py').open(mode='w', encoding='utf-8') as fo:
                with warnings.catch_warnings():
                    warnings.simplefilter('ignore')
                    content = importlib.resources.read_text(sccde_resources, f'sample_{sample_type}.py')
                    content = content.replace('{{REPLACED-UUID}}', new_uuid)
                fo.write(content)

            # カスタムUIファイルのコピー
            parameter_ui_dir = info_path.parent / f'parameter_ui/sample_{sample_type}_{suffix_num}'
            parameter_ui_dir.mkdir(parents=True, exist_ok=True)
            with (parameter_ui_dir / 'custom_ui.json').open(mode='w', encoding='utf-8') as fo:
                with warnings.catch_warnings():
                    warnings.simplefilter('ignore')
                    content = importlib.resources.read_text(sccde_resources, f'sample_{sample_type}_ui.json')
                fo.write(content)

            # 環境情報ファイルの更新
            info['components'][new_uuid] = {
                'name': f'Sample {sample_type}',
                'description': '',
                'component-type': 'python',
                'modulename': f'sample_{sample_type}_{suffix_num}',
                'parameter-ui-type': 'json',
                'parameter-ui': f'parameter_ui/sample_{sample_type}_{suffix_num}/custom_ui.json',
            }

        elif sample_lang == 'c':
            utils.print_error('c component sample is not supported now')

        # 環境情報ファイルの出力
        with info_path.open(mode='wt') as fo:
            json.dump(info, fo, ensure_ascii=False, indent=2)
            fo.write('\n')

    def make_package(self, out: Optional[Path]) -> None:
        """Initialize resource repogitory."""
        info_path = self.work_dir / INFO_FILE_NAME
        pack.make_package(info_path, out)
