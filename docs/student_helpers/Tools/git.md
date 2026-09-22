# Git

Use your own GitHub account. Replace `OWNER` with the course organization or repository owner's username, and `REPOSITORY` with the repository name.

## Connect to GitHub with SSH

Create a key using your own email address. If this key already exists, reuse it instead of overwriting it.

```sh
ssh-keygen -t ed25519 -C "student@example.com" -f ~/.ssh/id_ed25519_course
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519_course
cat ~/.ssh/id_ed25519_course.pub
```

Add the displayed **public key** to your GitHub account under **Settings → SSH and GPG keys → New SSH key**. Keep the file without `.pub` private.

```sh
ssh -T git@github.com
```

On the first connection, verify the host fingerprint using [GitHub's SSH instructions](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/testing-your-ssh-connection). The greeting should show your username; “does not provide shell access” is normal.

## Clone and set your commit identity

```sh
git clone git@github.com:OWNER/REPOSITORY.git
cd REPOSITORY
git config user.name "Your Name"
git config user.email "student@example.com"
```

These settings label your commits in this repository; your SSH key controls which GitHub account authenticates.

## Update repositories

Inside one repository, check for local changes before pulling:

```sh
git status
git pull
```

To check and update the workspace repositories, run from `ROB4_Fraunhofer`:

```sh
vcs status
vcs pull
```

Commit or stash unfinished changes first. Editing a branch in a `.repos` file does not switch an existing checkout when you run `vcs pull`.

## Change a repository's remote

Run inside the repository:

```sh
git remote set-url origin git@github.com:OWNER/REPOSITORY.git
git remote -v
```

## When using multiple GitHub accounts (avoid that)

Keep a separate key for each account. Use the course key above for your school account; create a personal key if you do not already have one:

```sh
ssh-keygen -t ed25519 -C "personal@example.com" -f ~/.ssh/id_ed25519_personal
```

Add each `.pub` key to its matching GitHub account. Add these aliases to `~/.ssh/config`, keeping any existing configuration:

```text
Host github-school
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_ed25519_course
    IdentitiesOnly yes

Host github-personal
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_ed25519_personal
    IdentitiesOnly yes
```

Test both aliases and check the usernames in the greetings:

```sh
ssh -T git@github-school
ssh -T git@github-personal
```

Inside a repository, select the account through its remote URL:

```sh
git remote set-url origin git@github-school:OWNER/REPOSITORY.git
```

Use `github-personal` instead for your personal account; the same aliases work in `git clone` URLs. `ssh -T` only tests authentication—it does not switch accounts. Set the commit name and email separately in each repository as shown above.

Reference: [GitHub's multiple-account guide](https://docs.github.com/en/account-and-profile/how-tos/account-management/managing-multiple-accounts).
