from git import Repo


class GitTool(Repo):
    updated_files = None
    updated_features = None

    def filter_updated_feature_files(self):
        self.updated_features = [
            f"{self.working_dir}/{path_to_file}"
            for path_to_file in self.updated_files
            if path_to_file.endswith(".feature")
        ]
        return self.updated_features

    def set_and_filter_updated_files(self, updated_files):
        self.updated_files = updated_files
        return self.filter_updated_feature_files()

    def get_updated_features_from_local(self, diff_of_what=None):
        updated_files = self.index.diff(diff_of_what)
        updated_files = [item.a_path for item in updated_files]
        return self.set_and_filter_updated_files(updated_files)

    def get_updated_features_from_commit(self):
        updated_files = self.commit("HEAD")
        updated_files = updated_files.stats.files
        return self.set_and_filter_updated_files(updated_files)

    def get_updated_features_from_branch(self):
        self.get_updated_features_from_local(diff_of_what="master")

    def get_updated_features(self, *changes):
        """
        "local" - The local not committed and pushed yet feature files will be exported
        "commit" - feature files from the current commit of the current branch will be exported
        "branch" - feature files which have been updated in the current branch will be exported. Be sure that the master
                   branch is up-to-date, and you have merged the latest changes from it to the current branch
        """
        select_changes = {
            "local": self.get_updated_features_from_local,
            "commit": self.get_updated_features_from_commit,
            "branch": self.get_updated_features_from_branch,
        }
        updated_feature_files = []
        for change in changes:
            select_changes[change]()
            updated_feature_files.extend(self.filter_updated_feature_files())

        assert updated_feature_files, f"Updated feature files has not been found...\n{self.updated_files}"
        return updated_feature_files
