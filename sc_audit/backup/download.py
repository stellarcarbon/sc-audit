"""
Download backups of DB tables from GitHub.

Author: Alex Olieman <https://keybase.io/alioli>
"""
from base64 import b64decode
from importlib import metadata
from pathlib import Path
import tempfile

from github import Github
from github.GithubObject import NotSet, Opt


github = Github()
repo_name = "stellarcarbon/sc-data"


def download_compatible_dumps() -> Path:
    data_repo = github.get_repo(repo_name)
    package_version = metadata.version("sc_audit")
    matching_refs = data_repo.get_git_matching_refs("tags/sc-audit")
    for ref_obj in matching_refs:
        ref_version = ref_obj.ref.lstrip("refs/tags/sc-audit-v")
        if package_version.startswith(ref_version):
            # tagged data indicates latest compatible version
            return download_dumps(ref=ref_obj.ref)
        
    # it's safe to get the most recent backup
    return download_dumps()


def download_dumps(ref: Opt[str] = NotSet) -> Path:
    """
    Download DB table dump files from GitHub and return the tempdir where they are located.
    The caller of this function is responsible for deleting the tempdir after loading the files.
    """
    data_repo = github.get_repo(repo_name)
    # note: the `get_contents` endpoint will fail for files >100 MB
    dump_cfiles = data_repo.get_contents("sc-audit", ref=ref)
    assert isinstance(dump_cfiles, list)
    temp_dir = Path(tempfile.mkdtemp())
    for cfile in dump_cfiles:
        if cfile.encoding == "base64":
            # file size =< 1 MB, content is loaded
            content_bytes = cfile.decoded_content
        else:
            # file size =< 100 MB, need to fetch content
            git_blob = data_repo.get_git_blob(cfile.sha)
            content_bytes = b64decode(git_blob.content)

        write_path = temp_dir / cfile.name
        with write_path.open('wb') as dump_file:
            dump_file.write(content_bytes)
        
    return temp_dir
