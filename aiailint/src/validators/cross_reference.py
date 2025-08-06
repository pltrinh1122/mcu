"""
Cross-Reference Validator for AIAI Scripts

Validates cross-references, detects loops, and ensures ID resolution.
Error Codes: E500-E699 (Cross-reference and loop detection errors)
"""

from pathlib import Path
from typing import Dict, Any, List, Set, Tuple, Optional
from collections import defaultdict, deque
from utils.validation_result import ValidationResult


class CrossReferenceValidator:
    """Validates cross-references and detects loops in AIAI Scripts"""
    
    def __init__(self, verbose=False):
        self.verbose = verbose
    
    def validate(self, data: Dict[str, Any], file_path: Path) -> ValidationResult:
        """
        Validate cross-references and detect loops
        
        Args:
            data: Parsed AIAI Script data
            file_path: Path to the file being validated
            
        Returns:
            ValidationResult with cross-reference validation results
        """
        errors = []
        warnings = []
        info = []
        
        if self.verbose:
            print("→ Running cross-reference validation...")
        
        # Build ID registry
        id_registry = self._build_id_registry(data)
        
        # Check for duplicate IDs
        duplicate_errors = self._check_duplicate_ids(id_registry)
        errors.extend(duplicate_errors)
        
        # Build dependency graphs
        command_graph = self._build_command_dependency_graph(data, id_registry)
        script_graph = self._build_script_dependency_graph(data, id_registry)
        
        # Validate references
        reference_errors = self._validate_references(data, id_registry)
        errors.extend(reference_errors)
        
        # Detect loops
        loop_errors = self._detect_loops(command_graph, script_graph)
        errors.extend(loop_errors)
        
        # Check for unreachable elements
        unreachable_warnings = self._check_unreachable_elements(data, command_graph, script_graph)
        warnings.extend(unreachable_warnings)
        
        if self.verbose:
            if errors:
                print(f"  ✗ Found {len(errors)} cross-reference errors")
            elif warnings:
                print(f"  ⚠ Found {len(warnings)} cross-reference warnings")
            else:
                print("  ✓ Cross-reference validation passed")
        
        success = len(errors) == 0
        return ValidationResult(success, errors, warnings, info, str(file_path))
    
    def _build_id_registry(self, data: Dict[str, Any]) -> Dict[str, List[Dict[str, Any]]]:
        """Build registry of all IDs and their locations"""
        registry = defaultdict(list)
        self._collect_ids(data, registry, "")
        return dict(registry)
    
    def _collect_ids(self, data: Dict[str, Any], registry: Dict[str, List], path: str):
        """Recursively collect all IDs with location information"""
        if isinstance(data, dict):
            if 'id' in data and isinstance(data['id'], str):
                registry[data['id']].append({
                    'path': path,
                    'type': data.get('type', 'unknown'),
                    'data': data
                })
            
            for key, value in data.items():
                new_path = f"{path}.{key}" if path else key
                if isinstance(value, (dict, list)):
                    self._collect_ids(value, registry, new_path)
        
        elif isinstance(data, list):
            for i, item in enumerate(data):
                new_path = f"{path}[{i}]"
                if isinstance(item, (dict, list)):
                    self._collect_ids(item, registry, new_path)
    
    def _check_duplicate_ids(self, id_registry: Dict[str, List[Dict[str, Any]]]) -> List[str]:
        """Check for duplicate IDs"""
        errors = []
        
        for id_str, locations in id_registry.items():
            if len(locations) > 1:
                paths = [loc['path'] for loc in locations]
                errors.append(f"E603: Duplicate ID '{id_str}' found at: {', '.join(paths)}")
        
        return errors
    
    def _build_command_dependency_graph(self, data: Dict[str, Any], id_registry: Dict[str, List]) -> Dict[str, Set[str]]:
        """Build dependency graph for command references in conditionals"""
        graph = defaultdict(set)
        
        # Find all conditionals and their command references
        conditionals = self._find_conditionals(data)
        
        for conditional in conditionals:
            condition = conditional.get('condition', {})
            source_id = condition.get('source')
            
            if source_id:
                # Add edges to commands in then/else branches
                then_commands = self._extract_command_ids_from_branch(conditional.get('then', []))
                else_commands = self._extract_command_ids_from_branch(conditional.get('else', []))
                
                for cmd_id in then_commands | else_commands:
                    graph[source_id].add(cmd_id)
        
        return dict(graph)
    
    def _build_script_dependency_graph(self, data: Dict[str, Any], id_registry: Dict[str, List]) -> Dict[str, Set[str]]:
        """Build dependency graph for script references in BR paths"""
        graph = defaultdict(set)
        
        # Find all BR paths (conditional then/else with script arrays)
        br_paths = self._find_br_paths(data)
        
        for path_info in br_paths:
            script_array = path_info['scripts']
            source_conditional = path_info['conditional_id']
            
            # Add sequential dependencies in the script array
            for i in range(len(script_array) - 1):
                current_script = script_array[i]
                next_script = script_array[i + 1]
                graph[current_script].add(next_script)
        
        return dict(graph)
    
    def _find_conditionals(self, data: Dict[str, Any], result: List = None) -> List[Dict[str, Any]]:
        """Find all conditional elements in the script"""
        if result is None:
            result = []
        
        if isinstance(data, dict):
            if data.get('type') == 'conditional':
                result.append(data)
            
            for value in data.values():
                if isinstance(value, (dict, list)):
                    self._find_conditionals(value, result)
        
        elif isinstance(data, list):
            for item in data:
                if isinstance(item, (dict, list)):
                    self._find_conditionals(item, result)
        
        return result
    
    def _find_br_paths(self, data: Dict[str, Any], result: List = None) -> List[Dict[str, Any]]:
        """Find all BR paths (script arrays in conditionals)"""
        if result is None:
            result = []
        
        conditionals = self._find_conditionals(data)
        
        for conditional in conditionals:
            conditional_id = conditional.get('id', 'unknown')
            
            # Check then branch
            then_branch = conditional.get('then', [])
            if isinstance(then_branch, list):
                for item in then_branch:
                    if isinstance(item, list):  # Script array
                        result.append({
                            'conditional_id': conditional_id,
                            'branch': 'then',
                            'scripts': item
                        })
            
            # Check else branch
            else_branch = conditional.get('else', [])
            if isinstance(else_branch, list):
                for item in else_branch:
                    if isinstance(item, list):  # Script array
                        result.append({
                            'conditional_id': conditional_id,
                            'branch': 'else',
                            'scripts': item
                        })
        
        return result
    
    def _extract_command_ids_from_branch(self, branch: List[Any]) -> Set[str]:
        """Extract command IDs from a conditional branch"""
        command_ids = set()
        
        for item in branch:
            if isinstance(item, dict):
                if item.get('type') == 'command' and 'id' in item:
                    command_ids.add(item['id'])
                # Recursively check nested structures
                nested_ids = self._extract_command_ids_from_branch([item])
                command_ids.update(nested_ids)
            elif isinstance(item, list):
                nested_ids = self._extract_command_ids_from_branch(item)
                command_ids.update(nested_ids)
        
        return command_ids
    
    def _validate_references(self, data: Dict[str, Any], id_registry: Dict[str, List]) -> List[str]:
        """Validate that all references can be resolved"""
        errors = []
        
        # Check conditional source references
        conditionals = self._find_conditionals(data)
        for conditional in conditionals:
            condition = conditional.get('condition', {})
            source_id = condition.get('source')
            
            if source_id and source_id not in id_registry:
                conditional_id = conditional.get('id', 'unknown')
                errors.append(f"E602: Unresolved command reference '{source_id}' in conditional '{conditional_id}'")
        
        # Check BR path script references
        br_paths = self._find_br_paths(data)
        for path_info in br_paths:
            for script_id in path_info['scripts']:
                if script_id not in id_registry:
                    conditional_id = path_info['conditional_id']
                    errors.append(f"E601: Unresolved script reference '{script_id}' in BR path of conditional '{conditional_id}'")
        
        return errors
    
    def _detect_loops(self, command_graph: Dict[str, Set[str]], script_graph: Dict[str, Set[str]]) -> List[str]:
        """Detect cycles in dependency graphs using DFS"""
        errors = []
        
        # Detect command loops
        command_cycles = self._detect_cycles_dfs(command_graph)
        for cycle in command_cycles:
            cycle_str = " → ".join(cycle + [cycle[0]])
            errors.append(f"E502: Infinite loop detected in command references: {cycle_str}")
        
        # Detect script loops
        script_cycles = self._detect_cycles_dfs(script_graph)
        for cycle in script_cycles:
            cycle_str = " → ".join(cycle + [cycle[0]])
            errors.append(f"E501: Circular reference detected in BR paths: {cycle_str}")
        
        return errors
    
    def _detect_cycles_dfs(self, graph: Dict[str, Set[str]]) -> List[List[str]]:
        """Detect cycles using depth-first search with colors"""
        WHITE, GRAY, BLACK = 0, 1, 2
        colors = {node: WHITE for node in graph}
        cycles = []
        
        def dfs(node: str, path: List[str]):
            if colors.get(node, WHITE) == GRAY:
                # Found cycle - extract it
                cycle_start = path.index(node)
                cycle = path[cycle_start:]
                cycles.append(cycle)
                return
            
            if colors.get(node, WHITE) == BLACK:
                return
            
            colors[node] = GRAY
            path.append(node)
            
            for neighbor in graph.get(node, set()):
                dfs(neighbor, path)
            
            path.pop()
            colors[node] = BLACK
        
        for node in graph:
            if colors.get(node, WHITE) == WHITE:
                dfs(node, [])
        
        return cycles
    
    def _check_unreachable_elements(self, data: Dict[str, Any], command_graph: Dict[str, Set[str]], script_graph: Dict[str, Set[str]]) -> List[str]:
        """Check for unreachable commands or scripts"""
        warnings = []
        
        # Find all IDs that are defined but never referenced
        all_ids = set()
        referenced_ids = set()
        
        # Collect all defined IDs
        id_registry = self._build_id_registry(data)
        all_ids = set(id_registry.keys())
        
        # Collect all referenced IDs
        for sources in command_graph.values():
            referenced_ids.update(sources)
        
        for sources in script_graph.values():
            referenced_ids.update(sources)
        
        # Find conditionals that reference commands
        conditionals = self._find_conditionals(data)
        for conditional in conditionals:
            condition = conditional.get('condition', {})
            source_id = condition.get('source')
            if source_id:
                referenced_ids.add(source_id)
        
        # Find unreferenced IDs (excluding main script and root elements)
        unreachable = all_ids - referenced_ids
        
        for unreachable_id in unreachable:
            # Skip main script and metadata elements
            locations = id_registry[unreachable_id]
            for location in locations:
                if location['type'] not in ['script'] or 'main' not in unreachable_id.lower():
                    path = location['path']
                    warnings.append(f"W601: Potentially unreachable element '{unreachable_id}' at {path}")
        
        return warnings


def validate_cross_references(data: Dict[str, Any], file_path: str = "", verbose=False) -> ValidationResult:
    """
    Standalone function to validate cross-references and detect loops
    
    Args:
        data: AIAI Script data to validate
        file_path: Path to file being validated
        verbose: Enable verbose output
        
    Returns:
        ValidationResult with cross-reference validation results
    """
    validator = CrossReferenceValidator(verbose=verbose)
    return validator.validate(data, Path(file_path))