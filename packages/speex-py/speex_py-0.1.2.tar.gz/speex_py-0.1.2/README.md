# Python Bindings to speexdsp using rust and maturin/pyo3

install: `uv sync`

test: `uv run invoke example --name basic `


## Publish

If not installed, install `cargo install cargo-workspaces`

On main, run `cargo ws version patch` / `cargo ws version minor` / `cargo ws version major` etc. based on what to bump
-> this will update the Cargo.toml version, create a new git tag and push