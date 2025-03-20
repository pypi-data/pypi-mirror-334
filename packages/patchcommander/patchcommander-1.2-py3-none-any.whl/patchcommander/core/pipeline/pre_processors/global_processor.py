"""
Global pre-processor parsing tags from the input text.
"""
import re
import os
from typing import List, Dict
from rich.console import Console
from ..models import PatchOperation
from ..processor_base import GlobalPreProcessor
from ....core.text_utils import normalize_line_endings

console = Console()

class TagParser(GlobalPreProcessor):
    """
    Global pre-processor parsing PatchCommander tags from the input text.
    """

    def __init__(self):
        """Initializes the parser."""
        self.valid_operations = {"FILE", "OPERATION"}

    def process(self, input_text: str) -> List[PatchOperation]:
        from ....core.text_utils import normalize_line_endings, normalize_indentation

        # Apply both normalizations
        normalized_text = normalize_line_endings(input_text)
        normalized_text = normalize_indentation(normalized_text)

        operations = []
        tag_pattern = re.compile('<(FILE|OPERATION)(\\s+[^>]*)?(?:>(.*?)</\\1\\s*>|/>)', re.DOTALL)
        for match in tag_pattern.finditer(normalized_text):
            tag_type = match.group(1)
            attr_str = match.group(2) or ''
            content = match.group(3) or ''
            attributes = self._parse_attributes(attr_str)
            if tag_type == 'FILE':
                if 'path' not in attributes:
                    console.print("[bold red]FILE tag requires a 'path' attribute.[/bold red]")
                    continue
            elif tag_type == 'OPERATION':
                if 'action' not in attributes:
                    console.print("[bold red]OPERATION tag requires an 'action' attribute.[/bold red]")
                    continue
                action = attributes['action']
                if action == 'move_file':
                    if 'source' not in attributes or 'target' not in attributes:
                        console.print("[bold red]move_file operation requires 'source' and 'target' attributes.[/bold red]")
                        continue
                elif action == 'delete_file':
                    if 'source' not in attributes:
                        console.print("[bold red]delete_file operation requires a 'source' attribute.[/bold red]")
                        continue
                elif action == 'delete_method':
                    if 'source' not in attributes or 'class' not in attributes or 'method' not in attributes:
                        console.print("[bold red]delete_method operation requires 'source', 'class', and 'method' attributes.[/bold red]")
                        continue
            is_duplicate = False
            if tag_type == 'FILE' and 'xpath' in attributes:
                for existing_op in operations:
                    if existing_op.name == 'FILE' and existing_op.path == attributes.get('path') and (existing_op.xpath == attributes.get('xpath')):
                        console.print(f"[bold yellow]Warning: Duplicate operation found for {attributes.get('path')} xpath={attributes.get('xpath')}. Skipping.[/bold yellow]")
                        is_duplicate = True
                        break
            if is_duplicate:
                continue
            operation = PatchOperation(name=tag_type, path=attributes.get('path', attributes.get('source', '')), content=content.strip(), xpath=attributes.get('xpath', None), action=attributes.get('action', None), attributes=attributes)
            if operation.path:
                (_, ext) = os.path.splitext(operation.path)
                operation.file_extension = ext.lower()[1:] if ext else ''
            operations.append(operation)
        return operations

    def _parse_attributes(self, attr_str: str) -> Dict[str, str]:
        if not attr_str:
            return {}
        attrs = {}
        pattern = '(\\w+)\\s*=\\s*"([^"]*)"'
        for match in re.finditer(pattern, attr_str):
            (key, value) = match.groups()
            attrs[key] = value
        return attrs
