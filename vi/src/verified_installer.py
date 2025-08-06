#!/usr/bin/env python3
"""
Verified Installer (VI) - Python OOP Implementation
Generic installation verification and validation system
Version: 5.0

Purpose: Reusable framework for verifying various types of installations
         Uses JSON viScript files to define verification steps and expected patterns

Usage: sudo python3 verified_installer.py <viScript_file> [OPTIONS]
       <viScript_file>       : Mandatory viScript file (e.g., system_validation_viScript.json)
       --verbose             : Show detailed output
       --help, -h            : Show help message

Note: viScript files must use the new severity system. Legacy critical/weight fields are not supported.

See VERIFIED_INSTALLER.md for complete viScript schema documentation
"""

import sys
import os
import json
import subprocess
import argparse
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
import logging
from datetime import datetime

# Import viscriptlint (distributed together)
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "viscriptlint" / "src"))
from viscriptlint import ViscriptLinter, ValidationResult


class Severity(Enum):
    """Severity levels for checks"""
    CRITICAL = "critical"
    INFORMATIONAL = "informational"


class ValidationType(Enum):
    """Validation types for checks"""
    RETURN_VALUE = "return_value"
    OUTPUT_PATTERN = "output_pattern"
    BOTH = "both"
    NONE = "none"


@dataclass
class CheckResult:
    """Result of a single check execution"""
    name: str
    description: str
    severity: Severity
    success: bool
    output: str
    return_code: int
    expected_return: Optional[int] = None
    expected_pattern: Optional[str] = None
    validation_type: ValidationType = ValidationType.RETURN_VALUE
    weight: int = 1
    failure_reason: Optional[str] = None


@dataclass
class PhaseResult:
    """Result of a phase execution"""
    name: str
    description: str
    checks: List[CheckResult] = field(default_factory=list)
    success: bool = True
    total_checks: int = 0
    successful_checks: int = 0
    failed_checks: int = 0
    warning_checks: int = 0


@dataclass
class VerificationSummary:
    """Overall verification summary"""
    viscript_file: Path
    installation_type: str
    timestamp: datetime
    phases: List[PhaseResult] = field(default_factory=list)
    total_checks: int = 0
    successful_checks: int = 0
    failed_checks: int = 0
    warning_checks: int = 0
    success_rate: float = 0.0
    overall_success: bool = True


class VerifiedInstaller:
    """Main verified installer class with OOP design"""
    
    def __init__(self, verbose: bool = False):
        """Initialize the verified installer"""
        self.verbose = verbose
        self.viscript_file: Optional[Path] = None
        self.viscript_data: Optional[Dict[str, Any]] = None
        self.installation_type: str = "unknown"
        self.log_file = Path(f"/tmp/verified_installer_{datetime.now().strftime('%Y%m%d-%H%M%S')}.log")
        
        # Initialize viscriptlint for validation
        self.linter = ViscriptLinter(verbose=verbose)
        
        # Setup logging
        self._setup_logging()
    
    def _setup_logging(self) -> None:
        """Setup logging configuration"""
        log_level = logging.DEBUG if self.verbose else logging.INFO
        logging.basicConfig(
            level=log_level,
            format='%(asctime)s [%(levelname)s] %(message)s',
            handlers=[
                logging.FileHandler(self.log_file),
                logging.StreamHandler() if self.verbose else logging.NullHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def show_help(self) -> None:
        """Display help information"""
        help_text = """
Verified Installer (VI) v5.0

Usage: sudo python3 verified_installer.py <viScript_file> [OPTIONS]

ARGUMENTS:
    <viScript_file>       Mandatory viScript file (e.g., system_validation_viScript.json)

OPTIONS:
    --verbose             Show detailed output
    --help, -h            Show this help message

EXAMPLES:
    # System validation
    sudo python3 verified_installer.py system_validation_viScript.json

    # BTRFS installation verification with output redirection
    sudo python3 verified_installer.py btrfs_viScript.json --verbose > btrfs_report.txt

    # Docker installation with custom checks
    sudo python3 verified_installer.py ../ubuntu-btrfs-installer/src/docker_viScript.json

VISCRIPT:
    The framework uses JSON viScript files to define verification steps.
    See documentation for viScript file format and examples.
"""
        print(help_text)
    
    def validate_viscript(self, viscript_file: Path) -> bool:
        """Validate viScript using viscriptlint"""
        self.logger.info(f"Validating viScript: {viscript_file}")
        
        # Use viscriptlint for comprehensive validation
        result = self.linter.validate_viscript(viscript_file)
        
        if result.success:
            self.logger.info("viScript validation passed")
            return True
        else:
            self.logger.error("viScript validation failed:")
            for error in result.errors:
                self.logger.error(f"  {error}")
            return False
    
    def load_viscript(self, viscript_file: Path) -> bool:
        """Load and validate viScript file"""
        if not viscript_file.exists():
            self.logger.error(f"viScript file not found: {viscript_file}")
            return False
        
        # Validate the viScript first
        if not self.validate_viscript(viscript_file):
            return False
        
        # Load the viScript data
        try:
            with open(viscript_file, 'r') as f:
                self.viscript_data = json.load(f)
            
            self.viscript_file = viscript_file
            self.installation_type = self.viscript_data.get("installation_type", "unknown")
            
            self.logger.info(f"viScript loaded: {self.installation_type}")
            return True
            
        except json.JSONDecodeError as e:
            self.logger.error(f"Invalid JSON in viScript file: {e}")
            return False
        except Exception as e:
            self.logger.error(f"Error loading viScript: {e}")
            return False
    
    def prompt_prerequisite_confirmation(self) -> bool:
        """Prompt user for prerequisite confirmation"""
        if not self.viscript_data:
            return False
        
        prerequisites = self.viscript_data.get("prerequisites", {})
        required_scripts = prerequisites.get("required_viScripts", [])
        warnings = prerequisites.get("warnings", [])
        
        print("\n=== viScript Execution Confirmation ===")
        print(f"viScript: {self.viscript_file}")
        print(f"Type: {self.installation_type}")
        
        if not required_scripts:
            print("Prerequisites: None (first viScript in sequence)")
        else:
            print("Prerequisites that must be completed:")
            for script in required_scripts:
                print(f"  - {script}")
        
        if warnings:
            print("\nWarnings:")
            for warning in warnings:
                print(f"  WARNING: {warning}")
        
        print("\nPlease confirm that ALL prerequisite viScripts have been completed successfully.")
        print("This viScript will modify system configuration and cannot be safely undone.")
        
        response = input("\nConfirm prerequisites completed and ready to proceed? (Y/N): ")
        return response.lower() in ['y', 'yes']
    
    def execute_check(self, phase_name: str, check_name: str) -> CheckResult:
        """Execute a single check from the viScript"""
        # Find the check in the viScript data
        check_data = None
        for phase in self.viscript_data.get("phases", []):
            if phase.get("name") == phase_name:
                for check in phase.get("checks", []):
                    if check.get("name") == check_name:
                        check_data = check
                        break
                break
        
        if not check_data:
            return CheckResult(
                name=check_name,
                description="Check not found",
                severity=Severity.CRITICAL,
                success=False,
                output="",
                return_code=-1,
                failure_reason=f"Check '{check_name}' not found in phase '{phase_name}'"
            )
        
        # Extract check parameters
        description = check_data.get("description", "Check")
        command = check_data.get("command", "")
        validation_type = ValidationType(check_data.get("validation_type", "return_value"))
        expected_return = check_data.get("expected_return", 0)
        expected_pattern = check_data.get("expected_pattern", "")
        severity = Severity(check_data.get("severity", "informational"))
        
        # Determine weight based on severity
        weight = 3 if severity == Severity.CRITICAL else 1
        
        if not command:
            return CheckResult(
                name=check_name,
                description=description,
                severity=severity,
                success=False,
                output="",
                return_code=-1,
                expected_return=expected_return,
                expected_pattern=expected_pattern,
                validation_type=validation_type,
                weight=weight,
                failure_reason="No command specified"
            )
        
        # Execute the command
        self.logger.debug(f"Executing check: {check_name} ({validation_type.value})")
        
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )
            
            output = result.stdout + result.stderr
            return_code = result.returncode
            
            # Validate based on validation type
            success, failure_reason = self._validate_check_result(
                validation_type, return_code, output, expected_return, expected_pattern
            )
            
            return CheckResult(
                name=check_name,
                description=description,
                severity=severity,
                success=success,
                output=output,
                return_code=return_code,
                expected_return=expected_return,
                expected_pattern=expected_pattern,
                validation_type=validation_type,
                weight=weight,
                failure_reason=failure_reason
            )
            
        except subprocess.TimeoutExpired:
            return CheckResult(
                name=check_name,
                description=description,
                severity=severity,
                success=False,
                output="",
                return_code=-1,
                expected_return=expected_return,
                expected_pattern=expected_pattern,
                validation_type=validation_type,
                weight=weight,
                failure_reason="Command execution timed out"
            )
        except Exception as e:
            return CheckResult(
                name=check_name,
                description=description,
                severity=severity,
                success=False,
                output="",
                return_code=-1,
                expected_return=expected_return,
                expected_pattern=expected_pattern,
                validation_type=validation_type,
                weight=weight,
                failure_reason=f"Command execution failed: {e}"
            )
    
    def _validate_check_result(
        self,
        validation_type: ValidationType,
        return_code: int,
        output: str,
        expected_return: int,
        expected_pattern: str
    ) -> Tuple[bool, Optional[str]]:
        """Validate check result based on validation type"""
        
        if validation_type == ValidationType.RETURN_VALUE:
            success = return_code == expected_return
            failure_reason = None if success else f"Return code {return_code} != {expected_return}"
            return success, failure_reason
        
        elif validation_type == ValidationType.OUTPUT_PATTERN:
            success = expected_pattern in output
            failure_reason = None if success else f"Pattern '{expected_pattern}' not found in output"
            return success, failure_reason
        
        elif validation_type == ValidationType.BOTH:
            return_success = return_code == expected_return
            pattern_success = expected_pattern in output
            
            success = return_success and pattern_success
            
            if not success:
                reasons = []
                if not return_success:
                    reasons.append(f"Return code {return_code} != {expected_return}")
                if not pattern_success:
                    reasons.append(f"Pattern '{expected_pattern}' not found")
                failure_reason = "; ".join(reasons)
            else:
                failure_reason = None
            
            return success, failure_reason
        
        elif validation_type == ValidationType.NONE:
            # Always succeed if command executed
            return True, None
        
        else:
            return False, f"Unknown validation type: {validation_type.value}"
    
    def execute_phase(self, phase_name: str) -> PhaseResult:
        """Execute all checks in a phase"""
        phase_data = None
        for phase in self.viscript_data.get("phases", []):
            if phase.get("name") == phase_name:
                phase_data = phase
                break
        
        if not phase_data:
            return PhaseResult(
                name=phase_name,
                description="Phase not found",
                success=False
            )
        
        phase_result = PhaseResult(
            name=phase_name,
            description=phase_data.get("description", phase_name)
        )
        
        print(f"\n=== Phase: {phase_name} ===")
        if phase_result.description != phase_name:
            print(f"Description: {phase_result.description}")
        
        # Execute each check in the phase
        for check in phase_data.get("checks", []):
            check_name = check.get("name")
            if check_name:
                check_result = self.execute_check(phase_name, check_name)
                phase_result.checks.append(check_result)
                
                # Update phase statistics
                phase_result.total_checks += check_result.weight
                if check_result.success:
                    phase_result.successful_checks += check_result.weight
                elif check_result.severity == Severity.CRITICAL:
                    phase_result.failed_checks += check_result.weight
                    phase_result.success = False
                else:
                    phase_result.warning_checks += check_result.weight
                
                # Output result
                status = "SUCCESS" if check_result.success else "FAILED" if check_result.severity == Severity.CRITICAL else "WARNING"
                print(f"{status}: {check_result.description}")
                
                if not check_result.success and check_result.failure_reason:
                    print(f"  Reason: {check_result.failure_reason}")
                
                # Stop on critical failure
                if not check_result.success and check_result.severity == Severity.CRITICAL:
                    break
        
        return phase_result
    
    def run_verification(self) -> VerificationSummary:
        """Run the complete verification process"""
        self.logger.info("Running viScript-driven verification")
        
        summary = VerificationSummary(
            viscript_file=self.viscript_file,
            installation_type=self.installation_type,
            timestamp=datetime.now()
        )
        
        # Execute each phase
        for phase in self.viscript_data.get("phases", []):
            phase_name = phase.get("name")
            if phase_name:
                phase_result = self.execute_phase(phase_name)
                summary.phases.append(phase_result)
                
                # Update overall statistics
                summary.total_checks += phase_result.total_checks
                summary.successful_checks += phase_result.successful_checks
                summary.failed_checks += phase_result.failed_checks
                summary.warning_checks += phase_result.warning_checks
                
                # Stop on critical failure
                if not phase_result.success:
                    summary.overall_success = False
                    break
        
        # Calculate success rate
        if summary.total_checks > 0:
            summary.success_rate = (summary.successful_checks / summary.total_checks) * 100
        
        return summary
    
    def generate_summary(self, summary: VerificationSummary) -> None:
        """Generate and display verification summary"""
        print("\n=== VERIFICATION SUMMARY ===")
        print(f"Timestamp: {summary.timestamp}")
        print(f"Installation Type: {summary.installation_type}")
        print(f"Total Checks: {summary.total_checks}")
        print(f"Successful: {summary.successful_checks}")
        print(f"Failed: {summary.failed_checks}")
        print(f"Warnings: {summary.warning_checks}")
        print(f"Success Rate: {summary.success_rate:.1f}%")
        
        if summary.overall_success:
            print("Status: PASSED")
            print("Installation verification completed successfully")
        else:
            print("Status: FAILED")
            print("Installation verification failed - review required")
    
    def run(self, viscript_file: Path) -> int:
        """Main execution method"""
        print(f"=== Verified Installer (VI) v5.0 ===")
        print(f"Timestamp: {datetime.now()}")
        print(f"viScript File: {viscript_file}")
        if self.verbose:
            print("VERBOSE MODE: Detailed output enabled")
        print(f"Log file: {self.log_file}")
        print()
        
        # Load and validate viScript
        if not self.load_viscript(viscript_file):
            return 1
        
        # Prompt for prerequisite confirmation
        if not self.prompt_prerequisite_confirmation():
            print("Execution cancelled by user")
            return 0
        
        # Run verification
        summary = self.run_verification()
        
        # Generate summary
        self.generate_summary(summary)
        
        # Return appropriate exit code
        return 0 if summary.overall_success else 1


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Verified Installer (VI) - Installation verification system",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
EXAMPLES:
    # System validation
    sudo python3 verified_installer.py system_validation_viScript.json

    # BTRFS installation verification with output redirection
    sudo python3 verified_installer.py btrfs_viScript.json --verbose > btrfs_report.txt

    # Docker installation with custom checks
    sudo python3 verified_installer.py ../ubuntu-btrfs-installer/src/docker_viScript.json
        """
    )
    
    parser.add_argument(
        "viscript_file",
        type=Path,
        help="Mandatory viScript file (e.g., system_validation_viScript.json)"
    )
    
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show detailed output"
    )
    
    args = parser.parse_args()
    
    # Validate viScript file exists
    if not args.viscript_file.exists():
        print(f"Error: viScript file '{args.viscript_file}' not found")
        return 1
    
    # Create and run installer
    installer = VerifiedInstaller(verbose=args.verbose)
    return installer.run(args.viscript_file)


if __name__ == "__main__":
    sys.exit(main()) 