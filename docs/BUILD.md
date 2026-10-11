# Build Vesper

Use Windows x64, Rust 1.94+ MSVC, Visual Studio C++ build tools and Windows SDK.

Clone this repository only, then enter `apps/vesper`:

```powershell
cargo fmt --package vesper -- --check
cargo clippy --locked --release --all-targets --no-deps -- -D warnings
cargo test --locked --release --all-targets -- --test-threads=1
cargo build --locked --release
```

Keep Cargo.lock unchanged. Shared UI/art source is included in this repository.
Runtime users do not need developer tools. Format tests use owned generated media;
conditional Windows codec tests can report explicit skips when extensions are absent.
Physical input, media keys and perceptual checks are separate from CI.

First run `python scripts/fetch-decoder.py --out apps/vesper/vendor/runtime` from the root
(Python 3.11+ and 7-Zip required). It validates exact pinned MSYS2 archives and DLL hashes.
Set VESPER_TEST_DLL to the absolute runtime/libmpv-2.dll path for real decoder tests. Copy
all runtime DLLs beside target/release/vesper.exe for ordinary launching. Run headless tests
before the final desktop build because they can overwrite that target EXE.
The decoder-source release asset includes native sources/recipes/metadata and all Vesper
Rust dependency source. See its README for offline Rust and MSYS2 rebuild instructions.

## Package

Python 3.11+ and NSIS are developer prerequisites. From the root:

```powershell
python scripts/package-release.py --app vesper --exe apps/vesper/target/release/vesper.exe --out dist/release --decoder apps/vesper/vendor/runtime --decoder-notices decoder-source/licenses
```

Pass --nsis with the path to makensis.exe if it is not at the script's default location.
Use a fresh output directory. It creates a complete portable ZIP, per-user installer,
notices, documentation and manifest. Vesper packaging also needs the matching source
asset's extracted licenses directory. Never omit notices or corresponding-source access.
