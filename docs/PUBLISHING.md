# Publishing the UnReal World repositories

The three folders are independent Git repositories. The source can be
published through GitHub CLI, command-line Git or GitHub Desktop.

Using GitHub CLI (browser authentication):

1. Run `gh auth login --hostname github.com --git-protocol https --web`
   and approve access on the official GitHub device-login page.
2. Run `gh auth setup-git --hostname github.com`.
3. Create the initial commit in each source folder, if needed.
4. For a new, unpublished repository run
   `gh repo create Librianets/REPOSITORY --public --source . --remote origin --push`.
   For an existing repository use its existing remote and push normally.
5. Publish the two ZIPs from the main translation repository as release
   assets for tag `hook-0.20`. Verify their sizes and SHA256 after upload.

Account passwords are not accepted for Git HTTPS operations. Never put an
access token in a repository, remote URL, shell command or publication log.

Using GitHub Desktop:

1. Choose Add local repository and select one prepared source folder.
2. Review the changes and create the first commit.
3. Choose Publish repository, use the matching folder name and deselect
   Keep this code private for the public project. This creates its GitHub
   repository; do not create an empty repository on the website first.
4. Repeat for the other two folders.
5. In UnRealWorld_MultiTranslate create a GitHub Release for tag hook-0.20.
   Attach dist/Hook_0.20.zip and dist/Hook_0.20_lite.zip as release assets.
   Describe compatibility as UnReal World3.89, runtime0.20, RU/FI.

With command-line Git, first create an empty matching public repository on
GitHub without an automatically generated README or license. Then run these
commands in each source folder, replacing
REPOSITORY with that folder's matching name:

```
git status
git add .
git commit -m "Prepare Hook 0.20 for UnReal World 3.89"
git remote add origin https://github.com/Librianets/REPOSITORY.git
git push -u origin main
```

When publishing through Git, .gitignore excludes runtime binaries, dist ZIPs,
logs, local game files and build products. A manual browser upload does not
apply .gitignore: do not drag the entire working folder into the upload form.
Upload the Git source through Git/GitHub Desktop and the ZIPs through Releases.

Our authored code/build tools/documentation use0BSD. Preserve MinHook/HDE
notices. Translation data and fonts retain the scope described in
LICENSE_SCOPE.txt. Source publication does not change game ownership.

The staged0.20 archives contain the verified0.20 runtime and language data,
with licensing notices added for publication. This is not the unreleased0.21
plant-message fix. Original published packages elsewhere remain untouched.
