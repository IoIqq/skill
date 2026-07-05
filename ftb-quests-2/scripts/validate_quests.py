#!/usr/bin/env python3
"""Validate FTB Quests configuration files."""

import json
import re
import sys
from pathlib import Path


def parse_json5(text):
    """Basic JSON5 parser (strips comments, allows trailing commas)."""
    text = re.sub(r'//.*', '', text)
    text = re.sub(r'/\*.*?\*/', '', text, flags=re.DOTALL)
    text = re.sub(r',(\s*[}\]])', r'\1', text)
    return json.loads(text)


def validate_quests(quests_dir):
    """Validate FTB Quests config structure."""
    quests_path = Path(quests_dir)
    errors = []
    warnings = []
    
    all_ids = set()
    all_deps = []
    
    if not (quests_path / 'data.json5').exists():
        errors.append('Missing required file: data.json5')
    
    chapters_dir = quests_path / 'chapters'
    if not chapters_dir.exists():
        errors.append('Missing chapters/ directory')
    else:
        for chapter_file in chapters_dir.glob('*.json5'):
            try:
                content = chapter_file.read_text(encoding='utf-8')
                chapter = parse_json5(content)
                
                chapter_id = chapter.get('id')
                if not chapter_id:
                    errors.append(f'{chapter_file.name}: missing chapter id')
                elif chapter_id in all_ids:
                    errors.append(f'{chapter_file.name}: duplicate id {chapter_id}')
                else:
                    all_ids.add(chapter_id)
                
                for quest in chapter.get('quests', []):
                    quest_id = quest.get('id')
                    if not quest_id:
                        errors.append(f'{chapter_file.name}: quest missing id')
                    elif not re.match(r'^[0-9A-F]{16}$', quest_id):
                        errors.append(f'{chapter_file.name}: quest id {quest_id} not 16-char uppercase hex')
                    elif quest_id in all_ids:
                        errors.append(f'{chapter_file.name}: duplicate quest id {quest_id}')
                    else:
                        all_ids.add(quest_id)
                    
                    deps = quest.get('dependencies', [])
                    for dep in deps:
                        all_deps.append((chapter_file.name, quest_id, dep))
                    
                    item = quest.get('item')
                    if item and isinstance(item, str):
                        errors.append(f'{chapter_file.name}: quest {quest_id} has bare string item (should be object)')
                    
                    for task in quest.get('tasks', []):
                        task_id = task.get('id')
                        if not task_id:
                            errors.append(f'{chapter_file.name}: task missing id in quest {quest_id}')
                        elif task_id in all_ids:
                            errors.append(f'{chapter_file.name}: duplicate task id {task_id}')
                        else:
                            all_ids.add(task_id)
                        
                        if task.get('type') == 'ftbquests:item':
                            task_item = task.get('item')
                            if isinstance(task_item, str):
                                errors.append(f'{chapter_file.name}: task {task_id} has bare string item')
                    
                    for reward in quest.get('rewards', []):
                        reward_id = reward.get('id')
                        if not reward_id:
                            errors.append(f'{chapter_file.name}: reward missing id in quest {quest_id}')
                        elif reward_id in all_ids:
                            errors.append(f'{chapter_file.name}: duplicate reward id {reward_id}')
                        else:
                            all_ids.add(reward_id)
            
            except json.JSONDecodeError as e:
                errors.append(f'{chapter_file.name}: JSON parse error: {e}')
    
    for chapter_file, quest_id, dep in all_deps:
        if dep not in all_ids:
            errors.append(f'{chapter_file.name}: quest {quest_id} has unknown dependency {dep}')
    
    lang_dir = quests_path / 'lang' / 'en_us'
    if lang_dir.exists():
        lang_file = lang_dir / 'quests.json5'
        if lang_file.exists():
            try:
                lang_content = lang_file.read_text(encoding='utf-8')
                lang = parse_json5(lang_content)
                
                for obj_id in all_ids:
                    has_title = any(k.endswith(f'.{obj_id}.title') for k in lang.keys())
                    if not has_title:
                        warnings.append(f'No lang entry for {obj_id}.title')
            except json.JSONDecodeError as e:
                errors.append(f'lang/en_us/quests.json5: parse error: {e}')
    
    return errors, warnings


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python validate_quests.py <quests_dir>')
        sys.exit(1)
    
    errors, warnings = validate_quests(sys.argv[1])
    
    if errors:
        print('❌ Errors:')
        for err in errors:
            print(f'  - {err}')
    
    if warnings:
        print('\n⚠️  Warnings:')
        for warn in warnings:
            print(f'  - {warn}')
    
    if not errors and not warnings:
        print('✅ Validation passed')
    
    sys.exit(1 if errors else 0)