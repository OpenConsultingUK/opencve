import pathlib

import git
from airflow.exceptions import AirflowException
from includes.operators import KindOperator


class GitFetchOperator(KindOperator):
    def execute(self, context):
        repo_path = self.get_repo_path()

        if not pathlib.Path.exists(repo_path / ".git"):
            raise AirflowException(f"Repository {repo_path} seems empty or broken")

        # Check if remotes is well configured
        repo = git.Repo(repo_path)
        # Set Git user name and email
        repo.config_writer().set_value("user", "name", "Your Name").release()
        repo.config_writer().set_value("user", "email", "you@example.com").release()

        remotes = repo.remotes
        if not remotes:
            raise AirflowException(f"Repository {repo_path} has no remote")

        # Fetch the last changes
        last_commit = repo.head.commit
        self.log.info(f"Local HEAD is {last_commit}")

        self.log.info(f"Fetching last changes from {repo_path}...")
        tracking_branch = repo.active_branch.tracking_branch()
        try:
            # Apply patches
            folder_path = f"/transfer_received/{pathlib.Path(repo_path).name}"
            patch_files = sorted(pathlib.Path(folder_path).glob("**/*.patch"))
            if not patch_files:
                self.log.warning(f"No patch files found in {folder_path}")
                return
            for patch_file in patch_files:
                self.log.info(f"Applying patch {patch_file}")
                repo.git.am(str(patch_file))
                try:
                    patch_file.rename(patch_file.with_suffix('.patch.applied'))
                    # patch_file.unlink()  # Delete the file already processed
                except OSError:
                    self.log.warning(f"Could not rename {patch_file}")
        except git.GitCommandError:
            self.log.exception("Error while fetching")

        if last_commit == repo.head.commit:
            self.log.info("No change detected")
            return

        self.log.info(f"New HEAD is {repo.head.commit})")
