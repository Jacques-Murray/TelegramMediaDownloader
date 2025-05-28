"""Helper utilities and functions."""

from pathlib import Path
from typing import List

from ..models.channel_stats import ChannelStats
from ..models.download_session import DownloadSession


def print_session_summary(session: DownloadSession) -> None:
    """
    Print a detailed summary of the download session.

    Args:
        session: DownloadSession object with results
    """
    print(f"\n{'='*60}")
    print("TELEGRAM MEDIA DOWNLOADER - SESSION SUMMARY")
    print(f"{'='*60}")

    # Basic stats
    print(f"Duration: {session.duration}")
    print(f"Channels processed: {session.total_channels}")
    print(f"Total unread messages: {session.total_unread}")
    print(f"Total media messages: {session.total_media}")
    print(f"Total files downloaded: {session.total_downloaded}")
    print(f"Success rate: {session.success_rate:.1f}%")

    if session.total_downloaded > 0:
        print(
            f"Average files per active channel: {session.average_files_per_channel:.1f}"
        )

    # Channel breakdown
    if session.channel_stats:
        print(f"\n{'='*60}")
        print("PER-CHANNEL BREAKDOWN")
        print(f"{'='*60}")
        print(
            f"{'Channel':<35} {'Unread':<8} {'Media':<8} {'Downloaded':<12} {'Errors':<8}"
        )
        print(f"{'-'*75}")

        for stats in session.channel_stats:
            print(
                f"{stats.name[:34]:<35} {stats.unread_count:<8} "
                f"{stats.media_count:<8} {stats.downloaded_count:<12} {stats.error_count:<8}"
            )

    # Successful channels
    successful_channels = session.channels_with_downloads
    if successful_channels:
        print(f"\n{'='*60}")
        print("CHANNELS WITH DOWNLOADS")
        print(f"{'='*60}")
        for stats in successful_channels:
            print(
                f"✓ {stats.name}: {stats.downloaded_count} files "
                f"({stats.success_rate:.1f}% success rate)"
            )

    # Channels with errors
    error_channels = session.channels_with_errors
    if error_channels:
        print(f"\n{'='*60}")
        print("CHANNELS WITH ERRORS")
        print(f"{'='*60}")
        for stats in error_channels:
            print(f"⚠ {stats.name}: {stats.error_count} errors")
            for error in stats.errors[:3]:  # Show first 3 errors
                print(f"    - {error}")
            if len(stats.errors) > 3:
                print(f"    ... and {len(stats.errors) - 3} more errors")

    # Session errors
    if session.errors:
        print(f"\n{'='*60}")
        print("SESSION ERRORS")
        print(f"{'='*60}")
        for error in session.errors:
            print(f"❌ {error}")

    print(f"\n{'='*60}")


def format_file_size(size_bytes: int) -> str:
    """
    Format file size in human-readable format.

    Args:
        size_bytes: Size in bytes

    Returns:
        Formatted size string (e.g., "1.5 MB")
    """
    if size_bytes == 0:
        return "0 B"

    size_names = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1

    return f"{size_bytes:.1f} {size_names[i]}"


def validate_channel_names(
    channel_names: List[str], available_channels: List[str]
) -> List[str]:
    """
    Validate channel names against available channels.

    Args:
        channel_names: List of channel names to validate
        available_channels: List of available channel names

    Returns:
        List of valid channel names
    """
    valid_channels = []
    invalid_channels = []

    for name in channel_names:
        if name in available_channels:
            valid_channels.append(name)
        else:
            invalid_channels.append(name)

    if invalid_channels:
        print(f"Warning: The following channels were not found: {invalid_channels}")
        print(f"Available channels: {available_channels}")

    return valid_channels


def create_download_summary_file(session: DownloadSession, filepath: str) -> None:
    """
    Create a text file with download session summary.

    Args:
        session: DownloadSession object
        filepath: Path where to save the summary file
    """
    with open(filepath, "w", encoding="utf-8") as f:
        f.write("TELEGRAM MEDIA DOWNLOADER - SESSION SUMMARY\n")
        f.write("=" * 50 + "\n\n")

        # Session info
        f.write(f"Start Time: {session.start_time}\n")
        f.write(f"End Time: {session.end_time}\n")
        f.write(f"Duration: {session.duration}\n\n")

        # Summary stats
        summary = session.get_summary_dict()
        for key, value in summary.items():
            f.write(f"{key.replace('_', ' ').title()}: {value}\n")

        # Channel details
        f.write("\n" + "=" * 50 + "\n")
        f.write("CHANNEL DETAILS\n")
        f.write("=" * 50 + "\n\n")

        for stats in session.channel_stats:
            f.write(f"Channel: {stats.name}\n")
            f.write(f"  Unread Messages: {stats.unread_count}\n")
            f.write(f"  Media Messages: {stats.media_count}\n")
            f.write(f"  Downloaded: {stats.downloaded_count}\n")
            f.write(f"  Success Rate: {stats.success_rate:.1f}%\n")

            if stats.errors:
                f.write(f"  Errors ({len(stats.errors)}):\n")
                for error in stats.errors:
                    f.write(f"    - {error}\n")
            f.write("\n")

        # Session errors
        if session.errors:
            f.write("SESSION ERRORS:\n")
            for error in session.errors:
                f.write(f"  - {error}\n")


def print_available_channels(channels: List[str]) -> None:
    """
    Print list of available channels in a formatted way.

    Args:
        channels: List of channel names
    """
    if not channels:
        print("No channels found.")
        return

    print(f"\nAvailable Channels ({len(channels)}):")
    print("-" * 40)

    for i, channel in enumerate(channels, 1):
        print(f"{i:2d}. {channel}")

    print("-" * 40)


def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename for cross-platform compatibility.

    Args:
        filename: Original filename

    Returns:
        Sanitized filename
    """
    # Characters not allowed in filenames
    invalid_chars = '<>:"/\\|?*'

    # Replace invalid characters with underscore
    for char in invalid_chars:
        filename = filename.replace(char, "_")

    # Remove multiple consecutive underscores
    while "__" in filename:
        filename = filename.replace("__", "_")

    # Trim underscores and limit length
    filename = filename.strip("_")[:255]

    return filename or "unnamed_file"


def calculate_total_download_size(download_path: Path) -> int:
    """
    Calculate total size of all downloaded files.

    Args:
        download_path: Path to downloads directory

    Returns:
        Total size in bytes
    """
    total_size = 0

    if not download_path.exists():
        return 0

    for file_path in download_path.rglob("*"):
        if file_path.is_file() and not file_path.name.endswith(".txt"):
            try:
                total_size += file_path.stat().st_size
            except (OSError, IOError):
                # Skip files we can't read
                continue

    return total_size


def get_file_statistics(download_path: Path) -> dict:
    """
    Get detailed statistics about downloaded files.

    Args:
        download_path: Path to downloads directory

    Returns:
        Dictionary with file statistics
    """
    stats = {
        "total_files": 0,
        "total_size": 0,
        "file_types": {},
        "channels": {},
        "largest_file": None,
        "smallest_file": None,
    }

    if not download_path.exists():
        return stats

    largest_size = 0
    smallest_size = float("inf")

    for file_path in download_path.rglob("*"):
        if file_path.is_file() and not file_path.name.endswith(".txt"):
            try:
                file_size = file_path.stat().st_size
                stats["total_files"] += 1
                stats["total_size"] += file_size

                # Track file types
                ext = file_path.suffix.lower()
                stats["file_types"][ext] = stats["file_types"].get(ext, 0) + 1

                # Track channels
                channel = file_path.parent.name
                if channel not in stats["channels"]:
                    stats["channels"][channel] = {"files": 0, "size": 0}
                stats["channels"][channel]["files"] += 1
                stats["channels"][channel]["size"] += file_size

                # Track largest and smallest files
                if file_size > largest_size:
                    largest_size = file_size
                    stats["largest_file"] = {
                        "path": str(file_path),
                        "size": file_size,
                        "size_formatted": format_file_size(file_size),
                    }

                if file_size < smallest_size:
                    smallest_size = file_size
                    stats["smallest_file"] = {
                        "path": str(file_path),
                        "size": file_size,
                        "size_formatted": format_file_size(file_size),
                    }

            except (OSError, IOError):
                continue

    return stats


def print_file_statistics(download_path: Path) -> None:
    """
    Print detailed statistics about downloaded files.

    Args:
        download_path: Path to downloads directory
    """
    stats = get_file_statistics(download_path)

    print(f"\n{'='*50}")
    print("FILE STATISTICS")
    print(f"{'='*50}")

    print(f"Total Files: {stats['total_files']}")
    print(f"Total Size: {format_file_size(stats['total_size'])}")

    if stats["file_types"]:
        print(f"\nFile Types:")
        for ext, count in sorted(stats["file_types"].items()):
            print(f"  {ext or 'no extension'}: {count} files")

    if stats["channels"]:
        print(f"\nChannels:")
        for channel, data in sorted(stats["channels"].items()):
            print(
                f"  {channel}: {data['files']} files ({format_file_size(data['size'])})"
            )

    if stats["largest_file"]:
        print(f"\nLargest File: {stats['largest_file']['size_formatted']}")
        print(f"  {Path(stats['largest_file']['path']).name}")

    if stats["smallest_file"]:
        print(f"\nSmallest File: {stats['smallest_file']['size_formatted']}")
        print(f"  {Path(stats['smallest_file']['path']).name}")


def cleanup_empty_directories(download_path: Path) -> int:
    """
    Remove empty directories from download path.

    Args:
        download_path: Path to downloads directory

    Returns:
        Number of directories removed
    """
    removed_count = 0

    if not download_path.exists():
        return 0

    # Walk through directories bottom-up to handle nested empty dirs
    for dir_path in sorted(
        download_path.rglob("*"), key=lambda p: len(p.parts), reverse=True
    ):
        if dir_path.is_dir() and dir_path != download_path:
            try:
                # Check if directory is empty
                if not any(dir_path.iterdir()):
                    dir_path.rmdir()
                    removed_count += 1
            except OSError:
                # Directory not empty or permission denied
                continue

    return removed_count


def generate_download_report(session: DownloadSession, download_path: Path) -> str:
    """
    Generate a comprehensive download report.

    Args:
        session: Download session data
        download_path: Path to downloads directory

    Returns:
        Formatted report as string
    """
    stats = get_file_statistics(download_path)

    report = []
    report.append("TELEGRAM MEDIA DOWNLOADER - COMPREHENSIVE REPORT")
    report.append("=" * 60)
    report.append("")

    # Session summary
    report.append("SESSION SUMMARY")
    report.append("-" * 30)
    report.append(f"Start Time: {session.start_time}")
    report.append(f"End Time: {session.end_time}")
    report.append(f"Duration: {session.duration}")
    report.append(f"Channels Processed: {session.total_channels}")
    report.append(f"Unread Messages: {session.total_unread}")
    report.append(f"Media Messages: {session.total_media}")
    report.append(f"Files Downloaded: {session.total_downloaded}")
    report.append(f"Success Rate: {session.success_rate:.1f}%")
    report.append("")

    # File statistics
    report.append("FILE STATISTICS")
    report.append("-" * 30)
    report.append(f"Total Files on Disk: {stats['total_files']}")
    report.append(f"Total Size: {format_file_size(stats['total_size'])}")
    report.append("")

    if stats["file_types"]:
        report.append("File Types:")
        for ext, count in sorted(stats["file_types"].items()):
            report.append(f"  {ext or 'no extension'}: {count} files")
        report.append("")

    # Channel breakdown
    if session.channel_stats:
        report.append("CHANNEL BREAKDOWN")
        report.append("-" * 30)
        for channel_stat in session.channel_stats:
            report.append(f"Channel: {channel_stat.name}")
            report.append(f"  Unread: {channel_stat.unread_count}")
            report.append(f"  Media: {channel_stat.media_count}")
            report.append(f"  Downloaded: {channel_stat.downloaded_count}")
            report.append(f"  Success Rate: {channel_stat.success_rate:.1f}%")
            if channel_stat.errors:
                report.append(f"  Errors: {len(channel_stat.errors)}")
            report.append("")

    # Errors
    if session.errors or any(stats.errors for stats in session.channel_stats):
        report.append("ERRORS")
        report.append("-" * 30)

        if session.errors:
            report.append("Session Errors:")
            for error in session.errors:
                report.append(f"  - {error}")
            report.append("")

        for channel_stat in session.channel_stats:
            if channel_stat.errors:
                report.append(f"{channel_stat.name} Errors:")
                for error in channel_stat.errors:
                    report.append(f"  - {error}")
                report.append("")

    return "\n".join(report)
