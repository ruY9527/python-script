"""
Maven 依赖解析工具

解析项目中的 pom.xml 和其他 XML 文件，提取依赖信息并生成报告。
"""

import argparse
import json
import logging
import re
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional
import xml.etree.ElementTree as ET

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Maven 命名空间
MAVEN_NAMESPACE = {'maven': 'http://maven.apache.org/POM/4.0.0'}


@dataclass
class Dependency:
    """依赖信息数据类"""
    group_id: str
    artifact_id: str
    version: str
    country: str = '未知'
    usage: str = '暂无'
    repo_url: str = ''

    def to_dict(self) -> dict:
        return {
            'groupId': self.group_id,
            'artifactId': self.artifact_id,
            'version': self.version,
            'country': self.country,
            'usage': self.usage,
            'repoUrl': self.repo_url
        }


# 国别映射表
COUNTRY_MAPPING = {
    'org.springframework': '美国',
    'com.alibaba': '中国',
    'org.apache': '美国',
    'com.google': '美国',
    'io.netty': '美国',
    'org.mybatis': '中国',
    'mysql': '美国',
    'com.microsoft': '美国',
    'org.postgresql': '美国',
    'redis.clients': '美国',
    'org.redisson': '俄罗斯',
    'com.belerweb': '中国',
    'eu.bitwalker': '欧盟',
    'com.github': '全球',
    'net.coobird': '美国',
    'pro.fessional': '全球',
    'cn.hutool': '中国',
    'com.baomidou': '中国',
    'org.hibernate': '美国',
    'com.fasterxml': '美国',
    'io.swagger': '美国',
    'org.projectlombok': '美国',
}

# 用途映射表
USAGE_MAPPING = {
    'redisson': '分布式锁和对象存储',
    'pinyin4j': '中文拼音转换',
    'spring-boot': 'Spring应用开发框架',
    'druid': '数据库连接池',
    'useragentutils': '用户代理解析',
    'pagehelper': 'MyBatis分页插件',
    'oshi': '系统信息获取',
    'knife4j': 'API文档生成',
    'commons-io': 'IO操作工具',
    'poi': 'Microsoft Office文档处理',
    'velocity': '模板引擎',
    'commons-collections': '集合操作工具',
    'fastjson': 'JSON处理',
    'jjwt': 'JWT令牌生成和验证',
    'kaptcha': '验证码生成',
    'qlexpress': '规则引擎',
    'thumbnailator': '图片处理',
    'quartz': '定时任务调度',
    'hutool': 'Java工具类库',
    'mybatis-plus': 'MyBatis增强工具',
    'lombok': '代码简化工具',
    'swagger': 'API文档',
    'jackson': 'JSON处理',
    'gson': 'JSON处理',
    'netty': '网络通信框架',
    'shiro': '安全框架',
    'security': '安全框架',
    'log4j': '日志框架',
    'slf4j': '日志门面',
    'junit': '单元测试',
    'mockito': '单元测试Mock',
}


class MavenDependencyParser:
    """Maven 依赖解析器"""

    def __init__(self, target_dir: str):
        self.target_dir = Path(target_dir)
        self.properties: dict[str, str] = {}
        self.dependencies: dict[str, Dependency] = {}

    def get_all_xml_files(self, pattern: str = '*.xml') -> list[Path]:
        """获取目录下所有 XML 文件"""
        return list(self.target_dir.rglob(pattern))

    def extract_properties(self, pom_file: Path) -> dict[str, str]:
        """从 pom.xml 中提取 properties 中的版本信息"""
        properties = {}
        try:
            tree = ET.parse(pom_file)
            root = tree.getroot()
            for prop in root.findall('.//maven:properties/*', MAVEN_NAMESPACE):
                tag = prop.tag.split('}')[-1]
                if prop.text:
                    properties[tag] = prop.text.strip()
        except ET.ParseError as e:
            logger.warning(f"解析 {pom_file} 时出错: {e}")
        return properties

    def parse_pom_dependencies(self, pom_file: Path) -> list[Dependency]:
        """解析 pom.xml 文件，提取依赖信息"""
        dependencies = []
        try:
            tree = ET.parse(pom_file)
            root = tree.getroot()

            for dep in root.findall('.//maven:dependency', MAVEN_NAMESPACE):
                group_id = dep.find('maven:groupId', MAVEN_NAMESPACE)
                artifact_id = dep.find('maven:artifactId', MAVEN_NAMESPACE)
                version = dep.find('maven:version', MAVEN_NAMESPACE)

                if group_id is not None and artifact_id is not None:
                    dep_info = Dependency(
                        group_id=group_id.text.strip(),
                        artifact_id=artifact_id.text.strip(),
                        version=version.text.strip() if version is not None else '${version}'
                    )
                    dependencies.append(dep_info)
        except ET.ParseError as e:
            logger.warning(f"解析 {pom_file} 时出错: {e}")

        return dependencies

    def resolve_version(self, version: str) -> str:
        """解析版本号，替换 ${} 占位符"""
        if version.startswith('${') and version.endswith('}'):
            prop_name = version[2:-1]
            return self.properties.get(prop_name, version)
        return version

    def get_country_by_group_id(self, group_id: str) -> str:
        """根据 groupId 推测国别"""
        for prefix, country in sorted(COUNTRY_MAPPING.items(), key=lambda x: len(x[0]), reverse=True):
            if group_id.startswith(prefix):
                return country
        return '未知'

    def get_usage_by_artifact_id(self, artifact_id: str) -> str:
        """根据 artifactId 推测用途"""
        artifact_lower = artifact_id.lower()
        for keyword, usage in USAGE_MAPPING.items():
            if keyword.lower() in artifact_lower:
                return usage
        return '暂无'

    def parse_all(self) -> dict[str, Dependency]:
        """解析所有依赖"""
        xml_files = self.get_all_xml_files()
        pom_files = [f for f in xml_files if f.name == 'pom.xml']

        logger.info(f"找到 {len(xml_files)} 个 XML 文件，其中 {len(pom_files)} 个是 pom.xml 文件")

        # 提取所有 properties
        for pom_file in pom_files:
            self.properties.update(self.extract_properties(pom_file))

        # 解析所有 pom.xml 依赖
        all_deps = []
        for pom_file in pom_files:
            all_deps.extend(self.parse_pom_dependencies(pom_file))

        # 去重并处理
        for dep in all_deps:
            key = f"{dep.group_id}:{dep.artifact_id}"
            if key not in self.dependencies:
                resolved_version = self.resolve_version(dep.version)
                dep.version = resolved_version
                dep.country = self.get_country_by_group_id(dep.group_id)
                dep.usage = self.get_usage_by_artifact_id(dep.artifact_id)
                dep.repo_url = f"pkg:maven/{dep.group_id.replace('.', '/')}/{dep.artifact_id}@{dep.version}?type=jar"
                self.dependencies[key] = dep

        logger.info(f"共提取 {len(all_deps)} 个依赖，去重后得到 {len(self.dependencies)} 个唯一依赖")
        return self.dependencies

    def generate_table(self, output_file: str = 'dependencies_table.txt') -> None:
        """生成依赖表格"""
        output_path = Path(output_file)

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("序号\t类型\t作者/项目/版本\t国别\t仓库地址\t用途\t是否捐赠基金会\t对应事项\n")

            for i, dep in enumerate(self.dependencies.values(), 1):
                dep_str = f"{dep.artifact_id}/{dep.version}"
                f.write(f"{i}\t开源组件\t{dep_str}\t{dep.country}\t{dep.repo_url}\t{dep.usage}\t否\t动态链接\n")

        logger.info(f"完整表格已保存到 {output_path}")

    def generate_json(self, output_file: str = 'dependencies.json') -> None:
        """生成 JSON 格式的依赖报告"""
        output_path = Path(output_file)

        data = {
            'total': len(self.dependencies),
            'dependencies': [dep.to_dict() for dep in self.dependencies.values()]
        }

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        logger.info(f"JSON 报告已保存到 {output_path}")

    def print_summary(self, limit: int = 20) -> None:
        """打印依赖摘要"""
        print("\n=== 依赖 jar 表格 ===")
        print("序号\t类型\t作者/项目/版本\t国别\t仓库地址\t用途\t是否捐赠基金会\t对应事项")

        for i, dep in enumerate(self.dependencies.values(), 1):
            if i > limit:
                break
            dep_str = f"{dep.artifact_id}/{dep.version}"
            print(f"{i}\t开源组件\t{dep_str}\t{dep.country}\t{dep.repo_url}\t{dep.usage}\t否\t动态链接")

        if len(self.dependencies) > limit:
            print(f"... 共 {len(self.dependencies)} 个依赖")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='Maven 依赖解析工具')
    parser.add_argument('directory', nargs='?', default='.', help='要扫描的目录路径')
    parser.add_argument('-o', '--output', default='dependencies_table.txt', help='输出文件路径')
    parser.add_argument('-j', '--json', default='dependencies.json', help='JSON 输出文件路径')
    parser.add_argument('-l', '--limit', type=int, default=20, help='控制台显示的依赖数量限制')

    args = parser.parse_args()

    # 创建解析器并执行
    maven_parser = MavenDependencyParser(args.directory)
    maven_parser.parse_all()
    maven_parser.print_summary(limit=args.limit)
    maven_parser.generate_table(output_file=args.output)
    maven_parser.generate_json(output_file=args.json)


if __name__ == '__main__':
    main()