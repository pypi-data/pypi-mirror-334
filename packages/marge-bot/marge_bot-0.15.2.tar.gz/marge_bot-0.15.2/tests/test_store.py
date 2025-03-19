import os.path
import tempfile
from unittest import mock

import marge.git
import marge.store
import marge.user
from tests.test_git import get_calls as get_git_calls
from tests.test_project import INFO as PRJ_INFO
from tests.test_user import INFO as USER_INFO


# pylint: disable=attribute-defined-outside-init
@mock.patch("marge.git._run")
class TestRepoManager:
    def setup_method(self, _method):
        user = marge.user.User(
            api=None,
            info=dict(USER_INFO, name="Peter Parker", email="pparker@bugle.com"),
        )
        self.root_dir = (
            # pylint: disable=consider-using-with
            tempfile.TemporaryDirectory()
        )
        self.repo_manager = marge.store.SshRepoManager(
            user=user, root_dir=self.root_dir.name, ssh_key_file="/ssh/key"
        )

    def teardown_method(self, _method):
        self.root_dir.cleanup()

    def new_project(self, project_id, path_with_namespace):
        ssh_url_to_repo = f"ssh://buh.com/{path_with_namespace}.git"
        info = dict(
            PRJ_INFO,
            id=project_id,
            path_with_namespace=path_with_namespace,
            ssh_url_to_repo=ssh_url_to_repo,
        )
        return marge.project.Project(api=None, info=info)

    def test_creates_and_initializes_repo(self, git_run):
        repo_manager = self.repo_manager
        project = self.new_project(1234, "some/stuff")

        git_run.assert_not_called()

        repo = repo_manager.repo_for_project(project)

        assert os.path.dirname(repo.local_path) == repo_manager.root_dir
        assert repo.local_path != repo_manager.root_dir

        env = (
            f"GIT_SSH_COMMAND='{marge.git.GIT_SSH_COMMAND} -F /dev/null "
            f"-o IdentitiesOnly=yes -i /ssh/key'"
        )
        assert get_git_calls(git_run) == [
            f"{env} git clone --origin=origin --filter=blob:none {project.ssh_url_to_repo} "
            f"{repo.local_path}",
            f"{env} git -C {repo.local_path} config user.email pparker@bugle.com",
            f"{env} git -C {repo.local_path} config user.name 'Peter Parker'",
        ]

    def test_caches_repos_by_id(self, git_run):
        repo_manager = self.repo_manager
        project = self.new_project(1234, "some/stuff")
        same_project = marge.project.Project(
            api=None, info=dict(project.info, name="same/stuff")
        )

        assert git_run.call_count == 0

        repo_first_call = repo_manager.repo_for_project(project)
        assert git_run.call_count == 3

        repo_second_call = repo_manager.repo_for_project(same_project)
        assert repo_second_call is repo_first_call
        assert git_run.call_count == 3

    def test_stops_caching_if_ssh_url_changed(self, git_run):
        repo_manager = self.repo_manager
        project = self.new_project(1234, "some/stuff")

        assert git_run.call_count == 0

        repo_first_call = repo_manager.repo_for_project(project)
        assert git_run.call_count == 3

        different_ssh_url = self.new_project(1234, "same/stuff")

        repo_second_call = repo_manager.repo_for_project(different_ssh_url)
        assert git_run.call_count == 6
        assert (
            repo_first_call.remote_url
            != repo_second_call.remote_url
            == different_ssh_url.ssh_url_to_repo
        )

    def test_handles_different_projects(self, git_run):
        repo_manager = self.repo_manager
        project_1 = self.new_project(1234, "some/stuff")
        project_2 = self.new_project(5678, "other/things")

        assert git_run.call_count == 0

        repo_1 = repo_manager.repo_for_project(project_1)
        assert git_run.call_count == 3

        repo_2 = repo_manager.repo_for_project(project_2)
        assert git_run.call_count == 6

        assert repo_1.local_path != repo_2.local_path
