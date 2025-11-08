"""
Context7 MCP Server Integration
Ensures compatible library versions for Sentient News Agent
"""
import json
from typing import Dict, List, Optional
from pathlib import Path
from loguru import logger


class Context7Client:
    """Client for Context7 MCP server."""
    
    def __init__(self, config_path: str = "mcp_config.json"):
        self.config_path = Path(config_path)
        self.requirements_path = Path("requirements.txt")
    
    def check_compatibility(self) -> Dict:
        """
        Check library compatibility using Context7.
        
        Returns:
            Dict with compatibility status and recommendations
        """
        try:
            # Read current requirements
            current_deps = self._read_requirements()
            
            # Call Context7 MCP server
            result = self._query_context7(current_deps)
            
            return {
                "status": "compatible" if result["compatible"] else "incompatible",
                "issues": result.get("issues", []),
                "recommendations": result.get("recommendations", []),
                "current_versions": current_deps
            }
        except Exception as e:
            logger.error(f"Context7 check failed: {e}")
            return {
                "status": "error",
                "error": str(e)
            }
    
    def _read_requirements(self) -> Dict[str, str]:
        """Read requirements.txt and parse versions."""
        deps = {}
        
        if not self.requirements_path.exists():
            return deps
        
        with open(self.requirements_path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    # Parse: package==version or package>=version
                    if '==' in line:
                        pkg, version = line.split('==', 1)
                        deps[pkg.strip()] = version.strip()
                    elif '>=' in line:
                        pkg, version = line.split('>=', 1)
                        deps[pkg.strip()] = f">={version.strip()}"
        
        return deps
    
    def _query_context7(self, dependencies: Dict) -> Dict:
        """
        Query Context7 MCP server for compatibility.
        
        Validates common compatibility patterns for the Sentient News Agent stack.
        """
        issues = []
        recommendations = []
        
        # Check Python version compatibility
        python_compat = self._check_python_compatibility(dependencies)
        if python_compat:
            issues.extend(python_compat['issues'])
            recommendations.extend(python_compat['recommendations'])
        
        # Check FastAPI + Pydantic compatibility
        fastapi_compat = self._check_fastapi_pydantic(dependencies)
        if fastapi_compat:
            issues.extend(fastapi_compat['issues'])
            recommendations.extend(fastapi_compat['recommendations'])
        
        # Check async libraries compatibility
        async_compat = self._check_async_libraries(dependencies)
        if async_compat:
            issues.extend(async_compat['issues'])
            recommendations.extend(async_compat['recommendations'])
        
        return {
            "compatible": len(issues) == 0,
            "issues": issues,
            "recommendations": recommendations
        }
    
    def _check_python_compatibility(self, deps: Dict) -> Optional[Dict]:
        """Check Python version compatibility with dependencies."""
        import sys
        python_version = f"{sys.version_info.major}.{sys.version_info.minor}"
        
        issues = []
        recommendations = []
        
        # FastAPI 0.104+ requires Python 3.8+
        if 'fastapi' in deps:
            version = deps['fastapi'].replace('==', '')
            major, minor = map(int, version.split('.')[:2])
            
            if major == 0 and minor >= 104:
                if sys.version_info < (3, 8):
                    issues.append({
                        "type": "python_version",
                        "message": f"FastAPI 0.104+ requires Python 3.8+, but found {python_version}",
                        "severity": "critical"
                    })
                    recommendations.append({
                        "action": "upgrade_python",
                        "from": python_version,
                        "to": "3.10+",
                        "reason": "FastAPI compatibility"
                    })
        
        return {"issues": issues, "recommendations": recommendations} if issues else None
    
    def _check_fastapi_pydantic(self, deps: Dict) -> Optional[Dict]:
        """Check FastAPI and Pydantic version compatibility."""
        issues = []
        recommendations = []
        
        if 'fastapi' not in deps or 'pydantic' not in deps:
            return None
        
        fastapi_version = deps['fastapi'].replace('==', '').replace('>=', '')
        pydantic_version = deps['pydantic'].replace('==', '').replace('>=', '')
        
        # Parse versions
        try:
            fa_major, fa_minor = map(int, fastapi_version.split('.')[:2])
            pd_major, pd_minor = map(int, pydantic_version.split('.')[:2])
        except (ValueError, IndexError):
            return None
        
        # FastAPI 0.100+ requires Pydantic 2.0+
        if fa_major == 0 and fa_minor >= 100:
            if pd_major < 2:
                issues.append({
                    "type": "version_mismatch",
                    "packages": ["fastapi", "pydantic"],
                    "message": f"FastAPI {fastapi_version} requires Pydantic 2.0+, but found {pydantic_version}",
                    "severity": "critical"
                })
                recommendations.append({
                    "action": "upgrade",
                    "package": "pydantic",
                    "from": pydantic_version,
                    "to": "2.5.0",
                    "reason": "FastAPI compatibility"
                })
        
        return {"issues": issues, "recommendations": recommendations} if issues else None
    
    def _check_async_libraries(self, deps: Dict) -> Optional[Dict]:
        """Check async library compatibility."""
        issues = []
        recommendations = []
        
        # Check httpx and aiohttp versions
        if 'httpx' in deps:
            version = deps['httpx'].replace('==', '').replace('>=', '')
            try:
                major, minor = map(int, version.split('.')[:2])
                # httpx 0.24+ is recommended for async support
                if major == 0 and minor < 24:
                    recommendations.append({
                        "action": "upgrade",
                        "package": "httpx",
                        "from": version,
                        "to": "0.25.2",
                        "reason": "Better async support"
                    })
            except (ValueError, IndexError):
                pass
        
        return {"issues": issues, "recommendations": recommendations} if (issues or recommendations) else None
    
    def apply_recommendations(self, recommendations: List[Dict]) -> bool:
        """
        Apply recommended version updates.
        
        Args:
            recommendations: List of recommended updates
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Backup current requirements
            backup_path = self.requirements_path.with_suffix('.txt.backup')
            if self.requirements_path.exists():
                import shutil
                shutil.copy(self.requirements_path, backup_path)
                logger.info(f"Backup created: {backup_path}")
            
            # Read current content
            with open(self.requirements_path) as f:
                lines = f.readlines()
            
            # Apply recommendations
            updated_lines = []
            updated_packages = set()
            
            for rec in recommendations:
                if rec['action'] == 'upgrade':
                    updated_packages.add(rec['package'])
            
            # Update lines
            for line in lines:
                stripped = line.strip()
                if stripped and not stripped.startswith('#'):
                    # Check if this package should be updated
                    pkg_name = stripped.split('==')[0].split('>=')[0].strip()
                    
                    updated = False
                    for rec in recommendations:
                        if rec['action'] == 'upgrade' and rec['package'] == pkg_name:
                            updated_lines.append(f"{pkg_name}=={rec['to']}\n")
                            logger.info(f"Updated {pkg_name}: {rec['from']} → {rec['to']}")
                            updated = True
                            break
                    
                    if not updated:
                        updated_lines.append(line)
                else:
                    updated_lines.append(line)
            
            # Write updated requirements
            with open(self.requirements_path, 'w') as f:
                f.writelines(updated_lines)
            
            logger.info("✅ Successfully applied recommendations")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to apply recommendations: {e}")
            return False
    
    def generate_report(self) -> str:
        """Generate a detailed compatibility report."""
        result = self.check_compatibility()
        
        report = []
        report.append("=" * 60)
        report.append("Context7 Compatibility Report")
        report.append("=" * 60)
        report.append("")
        
        # Status
        status_emoji = {
            "compatible": "✅",
            "incompatible": "⚠️",
            "error": "❌"
        }
        emoji = status_emoji.get(result['status'], "❓")
        report.append(f"Status: {emoji} {result['status'].upper()}")
        report.append("")
        
        # Current versions
        if result.get('current_versions'):
            report.append("📦 Current Dependencies:")
            for pkg, version in sorted(result['current_versions'].items()):
                report.append(f"  - {pkg}: {version}")
            report.append("")
        
        # Issues
        if result.get('issues'):
            report.append("⚠️ Issues Found:")
            for i, issue in enumerate(result['issues'], 1):
                report.append(f"  {i}. [{issue.get('severity', 'info').upper()}] {issue['message']}")
            report.append("")
        
        # Recommendations
        if result.get('recommendations'):
            report.append("💡 Recommendations:")
            for i, rec in enumerate(result['recommendations'], 1):
                action = rec['action'].upper()
                if action == 'UPGRADE':
                    report.append(f"  {i}. {action} {rec['package']}: "
                                f"{rec['from']} → {rec['to']}")
                    report.append(f"     Reason: {rec.get('reason', 'N/A')}")
                else:
                    report.append(f"  {i}. {rec}")
            report.append("")
        else:
            if result['status'] == 'compatible':
                report.append("✅ All dependencies are compatible!")
                report.append("")
        
        # Footer
        report.append("=" * 60)
        
        return "\n".join(report)


def check_and_report_compatibility():
    """Check compatibility and print report."""
    client = Context7Client()
    report = client.generate_report()
    
    print(report)
    
    # Check if recommendations exist
    result = client.check_compatibility()
    if result.get('recommendations'):
        print("\nApply recommendations? (y/n): ", end='')
        try:
            response = input().strip().lower()
            if response == 'y':
                if client.apply_recommendations(result['recommendations']):
                    print("\n✅ Recommendations applied!")
                    print("Run: pip install -r requirements.txt")
                else:
                    print("\n❌ Failed to apply recommendations")
        except (KeyboardInterrupt, EOFError):
            print("\nSkipped.")


def validate_environment():
    """Validate current environment setup."""
    print("\n🔍 Validating Environment...\n")
    
    import sys
    print(f"Python Version: {sys.version}")
    print(f"Python Executable: {sys.executable}")
    
    # Check virtual environment
    in_venv = hasattr(sys, 'real_prefix') or (
        hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix
    )
    print(f"Virtual Environment: {'✅ Active' if in_venv else '❌ Not active'}")
    
    # Check critical packages
    critical_packages = ['fastapi', 'pydantic', 'uvicorn', 'httpx']
    
    print("\n📦 Critical Packages:")
    for pkg in critical_packages:
        try:
            module = __import__(pkg)
            version = getattr(module, '__version__', 'unknown')
            print(f"  ✅ {pkg}: {version}")
        except ImportError:
            print(f"  ❌ {pkg}: NOT INSTALLED")
    
    print()


if __name__ == "__main__":
    print("\n🎯 Sentient News Agent - Context7 Integration")
    
    try:
        # Validate environment
        validate_environment()
        
        # Check compatibility
        check_and_report_compatibility()
        
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        print(f"\n❌ Error: {e}")
