"""
Excel 转 JSON 工具模块

提供 Excel 文件读取、过滤和转换为 JSON 的功能。
"""

import json
import logging
from pathlib import Path
from typing import Any, Callable, Union

import pandas as pd

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def excel_to_json_with_filter(
    excel_file: Union[str, Path],
    sheet_name: Union[str, int, None] = None,
    filter_conditions: dict[str, Union[Any, Callable]] = None,
    output_file: Union[str, Path, None] = None,
    encoding: str = 'utf-8'
) -> list[dict]:
    """
    读取 Excel 文件，应用过滤条件，并将结果转换为 JSON 格式。

    Args:
        excel_file: Excel 文件路径
        sheet_name: 工作表名称或索引，默认为第一个工作表
        filter_conditions: 过滤条件字典，格式为 {列名: 过滤值或过滤函数}
        output_file: 输出 JSON 文件路径，默认为 None（不保存文件）
        encoding: 输出文件编码，默认为 'utf-8'

    Returns:
        过滤后的数据列表（JSON 格式）

    Raises:
        FileNotFoundError: Excel 文件不存在
        ValueError: 指定的工作表不存在

    Example:
        >>> # 简单过滤
        >>> data = excel_to_json_with_filter('data.xlsx', filter_conditions={'状态': '有效'})

        >>> # 函数过滤
        >>> data = excel_to_json_with_filter(
        ...     'data.xlsx',
        ...     filter_conditions={'金额': lambda x: x > 1000}
        ... )
    """
    excel_path = Path(excel_file)
    if not excel_path.exists():
        raise FileNotFoundError(f"Excel 文件不存在: {excel_path}")

    # 读取 Excel 文件
    try:
        df = pd.read_excel(excel_path, sheet_name=sheet_name)
    except Exception as e:
        logger.error(f"读取 Excel 文件失败: {e}")
        raise

    # 处理多工作表情况
    if isinstance(df, dict):
        first_sheet = list(df.keys())[0]
        logger.warning(f"检测到多个工作表，使用第一个工作表: {first_sheet}")
        df = df[first_sheet]

    logger.info(f"原始数据行数: {len(df)}")

    # 应用过滤条件
    if filter_conditions:
        for column, condition in filter_conditions.items():
            if column not in df.columns:
                logger.warning(f"列 '{column}' 不存在，跳过该过滤条件")
                continue
            if callable(condition):
                df = df[df[column].apply(condition)]
            else:
                df = df[df[column] == condition]

    logger.info(f"过滤后数据行数: {len(df)}")

    # 转换为 JSON 格式
    json_data = df.to_dict('records')

    # 处理 NaN 值
    for record in json_data:
        for key, value in record.items():
            if pd.isna(value):
                record[key] = None

    # 保存到文件
    if output_file:
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding=encoding) as f:
            json.dump(json_data, f, ensure_ascii=False, indent=2)
        logger.info(f"JSON 数据已保存到: {output_path}")

    return json_data


def main():
    """示例用法"""
    # 示例 Excel 文件路径
    excel_file = Path(__file__).parent / 'db' / 'mysql' / '数据库表结构导出.xlsx'

    if not excel_file.exists():
        logger.error(f"示例文件不存在: {excel_file}")
        return

    # 示例 1: 无过滤条件
    print("=== 示例1: 无过滤条件，读取所有数据 ===")
    json_result1 = excel_to_json_with_filter(
        excel_file=excel_file,
        sheet_name='gen_table',
        output_file='output_all.json'
    )
    print(f"转换后的数据条数: {len(json_result1)}")

    # 示例 2: 简单过滤
    print("\n=== 示例2: 简单过滤 - 过滤出'允许空'为'NO'的行 ===")
    json_result2 = excel_to_json_with_filter(
        excel_file=excel_file,
        sheet_name='gen_table',
        filter_conditions={'允许空': 'NO'},
        output_file='output_filtered_no.json'
    )
    print(f"转换后的数据条数: {len(json_result2)}")

    # 示例 3: 函数过滤
    print("\n=== 示例3: 函数过滤 - 过滤出数据类型包含'varchar'的行 ===")
    json_result3 = excel_to_json_with_filter(
        excel_file=excel_file,
        sheet_name='gen_table',
        filter_conditions={'数据类型': lambda x: 'varchar' in str(x)},
        output_file='output_filtered_varchar.json'
    )
    print(f"转换后的数据条数: {len(json_result3)}")

    # 示例 4: 多重过滤
    print("\n=== 示例4: 多重过滤 - 过滤出'允许空'为'YES'且数据类型包含'int'的行 ===")
    json_result4 = excel_to_json_with_filter(
        excel_file=excel_file,
        sheet_name='gen_table',
        filter_conditions={
            '允许空': 'YES',
            '数据类型': lambda x: 'int' in str(x)
        },
        output_file='output_filtered_multi.json'
    )
    print(f"转换后的数据条数: {len(json_result4)}")


if __name__ == '__main__':
    main()