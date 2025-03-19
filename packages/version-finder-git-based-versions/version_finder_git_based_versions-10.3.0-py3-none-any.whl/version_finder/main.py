import os
import sys
import subprocess
from .common import parse_arguments, args_to_command
from .version_finder import VersionFinder


class ExternalInterfaceNotSupportedError(Exception):
    """Raised when the external interface is not supported."""

    def __init__(self, interface: str):
        installation_instructions = (
            f"Please install the CLI app using 'pip install version-finder-git-based-versions-{interface}'.")
        super().__init__(f"External interface '{interface}' is not supported. {installation_instructions}")


def is_package_installed(package_name: str) -> bool:
    """Verify if the package is installed in the system using pip show."""
    try:
        print(f"Verifying installation of CLI: {package_name}")
        result = subprocess.run(
            [sys.executable, '-m', 'pip', 'show', package_name],
            capture_output=True,
            text=True
        )
        return result.returncode == 0
    except Exception:
        return False


def call_cli_app(args):
    """Call the CLI app."""
    # Verify if the CLI app installed in the system
    if not is_package_installed("version-finder-git-based-versions-cli"):
        raise ExternalInterfaceNotSupportedError("cli")

    # Call the CLI app with the provided arguments
    os.system(f"version-finder-cli {args_to_command(args)}")
    return 0


def call_gui_app(args):
    """Call the GUI app."""
    # Verify if the GUI app installed in the system
    if not is_package_installed("version-finder-git-based-versions-gui-app"):
        raise ExternalInterfaceNotSupportedError("gui")
    # Call the GUI app with the provided arguments
    os.system(f"version-finder-gui {args_to_command(args)}")
    return 0


def main():
    """Main entry point for the application."""
    args = parse_arguments()

    if args.version:
        from .__version__ import __version__
        print(f"version_finder v{__version__}")
        return 0

    if args.cli:
        call_cli_app(args)
    elif args.gui:
        call_gui_app(args)
    else:
        if args.path is None:
            args.path = os.getcwd()
        if args.path and args.branch and args.commit:
            try:
                # Initialize with force parameter
                vf = VersionFinder(path=args.path, force=args.force)
                
                # Check for uncommitted changes
                state = vf.get_saved_state()
                if state.get("has_changes", False) and not args.force:
                    proceed = input("Repository has uncommitted changes. Proceed anyway? (y/N): ").lower() == 'y'
                    if not proceed:
                        print("Operation cancelled by user")
                        return 0
                
                vf.update_repository(args.branch)
                version = vf.find_first_version_containing_commit(args.commit, args.submodule)
                
                if version:
                    print(f"The first version which includes commit {args.commit} is {version}")
                else:
                    print(f"No version found for commit {args.commit}")
                    
                # Restore original state if requested
                if args.restore_state:
                    print("Restoring original repository state")
                    
                    # Get the state before restoration for logging
                    state = vf.get_saved_state()
                    has_changes = state.get("has_changes", False)
                    stash_created = state.get("stash_created", False)
                    
                    if has_changes:
                        if stash_created:
                            print("Attempting to restore stashed changes")
                        else:
                            print("Warning: Repository had changes but they were not stashed")
                    
                    # Perform the restoration
                    if vf.restore_repository_state():
                        print("Original repository state restored successfully")
                        
                        # Verify the restoration
                        if has_changes and vf.has_uncommitted_changes():
                            print("Uncommitted changes were successfully restored")
                        elif has_changes and not vf.has_uncommitted_changes():
                            print("Error: Failed to restore uncommitted changes")
                    else:
                        print("Failed to restore original repository state")
                        
            except Exception as e:
                print(f"Error: {str(e)}")
                return 1
        else:
            print("Please provide a path, branch, and commit to search for.")
            print("Or add --cli or --gui to run the CLI or GUI version respectively.")


if __name__ == "__main__":
    main()
