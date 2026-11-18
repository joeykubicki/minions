# Working on the minions kit

This repo is a **kit** that gets copied into other projects. It isn't an application. Read `README.md` and `DESIGN.md` before changing anything.

- `template/` is installed verbatim into projects. Everything in it must be **project-agnostic**: no stack assumptions, no project-specific facts. Placeholders stay `TBD`.
- `library/agents/` holds optional agents. `library/addons/<name>/` holds optional add-ons: a `files/` tree copied into the project, plus an optional `settings.json` whose hooks `install.sh` merges into the project's settings. `install.sh` is the installer.
- Follow the style guide in `DESIGN.md` for agent and skill files. Keep the core small: a new core agent or skill needs a concrete reason from real usage.
- **YAML:** never put `: ` inside an unquoted frontmatter value. The file will silently fail to load.
- After changing `template/` or `install.sh`: install into a temp dir (`./install.sh "$(mktemp -d)"`) and confirm it runs cleanly. If agents or skills changed, open Claude Code in that temp dir and check `/agents` and the `/` menu.
- For any user-visible change, bump `VERSION` (semver) and add a `CHANGELOG.md` entry.
- When applying feedback harvested from a project's `docs/ai/MINIONS.md`, note the source project in the changelog entry.
