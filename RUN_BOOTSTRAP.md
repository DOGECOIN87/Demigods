# One-time repository extraction

The complete project payload is already stored in `.bootstrap/payload.part.00` through `.bootstrap/payload.part.08`.

To expand it into the organized repository structure:

1. Open the **Actions** tab.
2. Select **Bootstrap repository from issue trigger**.
3. Choose **Run workflow** on the `main` branch.
4. Wait for the workflow to finish.

The workflow reconstructs and commits the following folders:

- `prompts/`
- `docs/`
- `scripts/`
- `config/`
- `images/reference_sheets/`
- `assets/`

It then removes the temporary `.bootstrap` payload and one-time workflow files.
