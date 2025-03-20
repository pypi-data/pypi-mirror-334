# Changelog

## 0.1.0-alpha.8 (2025-03-17)

Full Changelog: [v0.1.0-alpha.7...v0.1.0-alpha.8](https://github.com/jc-nana/lucere-python/compare/v0.1.0-alpha.7...v0.1.0-alpha.8)

### Bug Fixes

* **ci:** ensure pip is always available ([#72](https://github.com/jc-nana/lucere-python/issues/72)) ([31ba387](https://github.com/jc-nana/lucere-python/commit/31ba3870cdd231127e0bb186b2052c6af7a6529a))
* **ci:** remove publishing patch ([#74](https://github.com/jc-nana/lucere-python/issues/74)) ([18791e8](https://github.com/jc-nana/lucere-python/commit/18791e8f4f7156e3d152030173d4a1f73bc2adcc))

## 0.1.0-alpha.7 (2025-03-15)

Full Changelog: [v0.1.0-alpha.6...v0.1.0-alpha.7](https://github.com/jc-nana/lucere-python/compare/v0.1.0-alpha.6...v0.1.0-alpha.7)

### Bug Fixes

* **types:** handle more discriminated union shapes ([#70](https://github.com/jc-nana/lucere-python/issues/70)) ([5c83b2f](https://github.com/jc-nana/lucere-python/commit/5c83b2fb6747e8f5ba8d0543afcd253df2703cae))


### Chores

* **docs:** update client docstring ([#64](https://github.com/jc-nana/lucere-python/issues/64)) ([bb6982e](https://github.com/jc-nana/lucere-python/commit/bb6982e3ae427b0e377265d3a6dbfe328211724f))
* **internal:** bump rye to 0.44.0 ([#69](https://github.com/jc-nana/lucere-python/issues/69)) ([4123c5b](https://github.com/jc-nana/lucere-python/commit/4123c5b87a78610314593e0243a0ebc5b5499f33))
* **internal:** codegen related update ([#68](https://github.com/jc-nana/lucere-python/issues/68)) ([2fcb90c](https://github.com/jc-nana/lucere-python/commit/2fcb90c02cff571dd596285614705a34975ee5e9))
* **internal:** fix devcontainers setup ([#60](https://github.com/jc-nana/lucere-python/issues/60)) ([707782b](https://github.com/jc-nana/lucere-python/commit/707782b546b2d9c12028ce78654d66dff923dc1a))
* **internal:** properly set __pydantic_private__ ([#62](https://github.com/jc-nana/lucere-python/issues/62)) ([164d27d](https://github.com/jc-nana/lucere-python/commit/164d27d9791ba0a0fbbb29af5ebfc5e320422c6d))
* **internal:** remove extra empty newlines ([#67](https://github.com/jc-nana/lucere-python/issues/67)) ([c876361](https://github.com/jc-nana/lucere-python/commit/c876361ee558bfc779ae072fef6f3cebccae5fa2))
* **internal:** remove unused http client options forwarding ([#65](https://github.com/jc-nana/lucere-python/issues/65)) ([bed064d](https://github.com/jc-nana/lucere-python/commit/bed064dcdbf25d21fe66663af8830ee35fba1706))


### Documentation

* update URLs from stainlessapi.com to stainless.com ([#63](https://github.com/jc-nana/lucere-python/issues/63)) ([09779dd](https://github.com/jc-nana/lucere-python/commit/09779ddceb31f097333a7b48578740d072712dd5))

## 0.1.0-alpha.6 (2025-02-21)

Full Changelog: [v0.1.0-alpha.5...v0.1.0-alpha.6](https://github.com/jc-nana/lucere-python/compare/v0.1.0-alpha.5...v0.1.0-alpha.6)

### Features

* **client:** allow passing `NotGiven` for body ([#57](https://github.com/jc-nana/lucere-python/issues/57)) ([c69ebd5](https://github.com/jc-nana/lucere-python/commit/c69ebd54cd52329189791b0bbcf7a07ee625f495))


### Bug Fixes

* **client:** mark some request bodies as optional ([c69ebd5](https://github.com/jc-nana/lucere-python/commit/c69ebd54cd52329189791b0bbcf7a07ee625f495))

## 0.1.0-alpha.5 (2025-02-14)

Full Changelog: [v0.1.0-alpha.4...v0.1.0-alpha.5](https://github.com/jc-nana/lucere-python/compare/v0.1.0-alpha.4...v0.1.0-alpha.5)

### Features

* **client:** send `X-Stainless-Read-Timeout` header ([#51](https://github.com/jc-nana/lucere-python/issues/51)) ([26c6baa](https://github.com/jc-nana/lucere-python/commit/26c6baa2e3773790bc6cdfd3084314a1ed264147))


### Bug Fixes

* asyncify on non-asyncio runtimes ([#55](https://github.com/jc-nana/lucere-python/issues/55)) ([170f0bf](https://github.com/jc-nana/lucere-python/commit/170f0bf4d6aceeb6fddaaa9b28d79f0e5239f085))


### Chores

* **internal:** bummp ruff dependency ([#50](https://github.com/jc-nana/lucere-python/issues/50)) ([810b421](https://github.com/jc-nana/lucere-python/commit/810b4215b3b435f8e17cd65aa69e86dd080f5c0d))
* **internal:** change default timeout to an int ([#49](https://github.com/jc-nana/lucere-python/issues/49)) ([6da8fbc](https://github.com/jc-nana/lucere-python/commit/6da8fbc9d3dc9f47d9ad5e0886445efd00d2f280))
* **internal:** codegen related update ([#47](https://github.com/jc-nana/lucere-python/issues/47)) ([8d20908](https://github.com/jc-nana/lucere-python/commit/8d209083fa8cb06b84f8a842167b3195ec0dd26f))
* **internal:** fix type traversing dictionary params ([#52](https://github.com/jc-nana/lucere-python/issues/52)) ([2b488cc](https://github.com/jc-nana/lucere-python/commit/2b488cc8a4cd680498bfb0d40ba3d31c47dbee94))
* **internal:** minor type handling changes ([#53](https://github.com/jc-nana/lucere-python/issues/53)) ([2898846](https://github.com/jc-nana/lucere-python/commit/28988462a91dcae88c516ff1e9a4c2a5da960043))
* **internal:** update client tests ([#54](https://github.com/jc-nana/lucere-python/issues/54)) ([1f7f67e](https://github.com/jc-nana/lucere-python/commit/1f7f67e9b3c08cd0a4202c2f4568d415bd985b2c))

## 0.1.0-alpha.4 (2025-01-17)

Full Changelog: [v0.1.0-alpha.3...v0.1.0-alpha.4](https://github.com/jc-nana/lucere-python/compare/v0.1.0-alpha.3...v0.1.0-alpha.4)

### Bug Fixes

* **client:** compat with new httpx 0.28.0 release ([#24](https://github.com/jc-nana/lucere-python/issues/24)) ([2270a34](https://github.com/jc-nana/lucere-python/commit/2270a34688cdc7706cb8d4de01a72cbffa256063))
* **client:** only call .close() when needed ([#41](https://github.com/jc-nana/lucere-python/issues/41)) ([57d549f](https://github.com/jc-nana/lucere-python/commit/57d549f42930e67c9942608010d7c9cbc4d9e745))
* correctly handle deserialising `cls` fields ([#44](https://github.com/jc-nana/lucere-python/issues/44)) ([b90f808](https://github.com/jc-nana/lucere-python/commit/b90f8089847bbcdf5503f21ea1746a8de2af24b9))


### Chores

* add missing isclass check ([#39](https://github.com/jc-nana/lucere-python/issues/39)) ([7678f1c](https://github.com/jc-nana/lucere-python/commit/7678f1c2a0ed4cc08e95ca696160db72009d262b))
* **internal:** add support for TypeAliasType ([#30](https://github.com/jc-nana/lucere-python/issues/30)) ([5aef021](https://github.com/jc-nana/lucere-python/commit/5aef021d2ac8ab908188a2e715965bed2b77d9ff))
* **internal:** bump httpx dependency ([#40](https://github.com/jc-nana/lucere-python/issues/40)) ([cccea44](https://github.com/jc-nana/lucere-python/commit/cccea4447906ce7c37947c7d01714a31a46c7581))
* **internal:** bump pydantic dependency ([#27](https://github.com/jc-nana/lucere-python/issues/27)) ([2517a29](https://github.com/jc-nana/lucere-python/commit/2517a2998f84acc0a43c37ae2b1c52df5d44edb6))
* **internal:** bump pyright ([#25](https://github.com/jc-nana/lucere-python/issues/25)) ([8024934](https://github.com/jc-nana/lucere-python/commit/802493440ef0622500331d294d5ca26075d07792))
* **internal:** bump pyright ([#29](https://github.com/jc-nana/lucere-python/issues/29)) ([4668534](https://github.com/jc-nana/lucere-python/commit/46685341c42af3b4e773d60860b32768f6eca4a6))
* **internal:** codegen related update ([#31](https://github.com/jc-nana/lucere-python/issues/31)) ([e987d16](https://github.com/jc-nana/lucere-python/commit/e987d16a07ad3bde6ad60f57698ea71c5ea86573))
* **internal:** codegen related update ([#32](https://github.com/jc-nana/lucere-python/issues/32)) ([f0077fd](https://github.com/jc-nana/lucere-python/commit/f0077fdaf69ab20cd933613d8742e41165e2b37d))
* **internal:** codegen related update ([#34](https://github.com/jc-nana/lucere-python/issues/34)) ([a8de547](https://github.com/jc-nana/lucere-python/commit/a8de547f1f43b7237bed73657b039b108fb147eb))
* **internal:** codegen related update ([#35](https://github.com/jc-nana/lucere-python/issues/35)) ([33c72c8](https://github.com/jc-nana/lucere-python/commit/33c72c81ae66fa08a0cffe1f179614a9ebf08568))
* **internal:** codegen related update ([#38](https://github.com/jc-nana/lucere-python/issues/38)) ([bfe16fa](https://github.com/jc-nana/lucere-python/commit/bfe16fad6c7ff1e5f5d0e9353dc4c06a34e6977f))
* **internal:** codegen related update ([#43](https://github.com/jc-nana/lucere-python/issues/43)) ([c5f424a](https://github.com/jc-nana/lucere-python/commit/c5f424aff9d12a2912f82b303ef64ec317104517))
* **internal:** codegen related update ([#45](https://github.com/jc-nana/lucere-python/issues/45)) ([28dd94d](https://github.com/jc-nana/lucere-python/commit/28dd94d4713b78b102fd919ce2541ea2fa54d8ea))
* **internal:** exclude mypy from running on tests ([#23](https://github.com/jc-nana/lucere-python/issues/23)) ([aa50586](https://github.com/jc-nana/lucere-python/commit/aa50586c68860081401e161808148e016b350e93))
* **internal:** fix compat model_dump method when warnings are passed ([#20](https://github.com/jc-nana/lucere-python/issues/20)) ([b33718f](https://github.com/jc-nana/lucere-python/commit/b33718fae22ec504962bde2b768d5aad2e086a3b))
* **internal:** fix some typos ([#37](https://github.com/jc-nana/lucere-python/issues/37)) ([3ca2a6e](https://github.com/jc-nana/lucere-python/commit/3ca2a6e3574bf76683acec31207081089706acc6))
* **internal:** updated imports ([#33](https://github.com/jc-nana/lucere-python/issues/33)) ([ff7eacd](https://github.com/jc-nana/lucere-python/commit/ff7eacd06cd89092818cd19bba7654be58b922e5))
* make the `Omit` type public ([#26](https://github.com/jc-nana/lucere-python/issues/26)) ([7eba950](https://github.com/jc-nana/lucere-python/commit/7eba950fde132a56b6e1e8aa2ee9d984750e781f))
* rebuild project due to codegen change ([#15](https://github.com/jc-nana/lucere-python/issues/15)) ([1c48dd0](https://github.com/jc-nana/lucere-python/commit/1c48dd0eb9883af41a334d84b0cdb095de206b69))
* rebuild project due to codegen change ([#17](https://github.com/jc-nana/lucere-python/issues/17)) ([7dc29ab](https://github.com/jc-nana/lucere-python/commit/7dc29abd07b6db08dbac3a08a70fd6f32c3f1360))
* rebuild project due to codegen change ([#18](https://github.com/jc-nana/lucere-python/issues/18)) ([77cecf0](https://github.com/jc-nana/lucere-python/commit/77cecf048f4a3f438d28b50d74771d390c41f6d6))
* rebuild project due to codegen change ([#19](https://github.com/jc-nana/lucere-python/issues/19)) ([33713f1](https://github.com/jc-nana/lucere-python/commit/33713f1c475dcc442c3effe185bfd43424313f3d))
* remove now unused `cached-property` dep ([#22](https://github.com/jc-nana/lucere-python/issues/22)) ([449460b](https://github.com/jc-nana/lucere-python/commit/449460b4653f15ca1f1820ecdc3e22ffab9dfee2))


### Documentation

* add info log level to readme ([#21](https://github.com/jc-nana/lucere-python/issues/21)) ([7a93411](https://github.com/jc-nana/lucere-python/commit/7a934116b1a7bd7ad42529feda8215a8e31d9a0b))
* fix typos ([#42](https://github.com/jc-nana/lucere-python/issues/42)) ([8bfc732](https://github.com/jc-nana/lucere-python/commit/8bfc732a095a783a1c33c502dc84163495063f80))
* **readme:** example snippet for client context manager ([#36](https://github.com/jc-nana/lucere-python/issues/36)) ([2cd730c](https://github.com/jc-nana/lucere-python/commit/2cd730c46c0bc93dbba342050743b4d5335dc2c4))
* **readme:** fix http client proxies example ([#28](https://github.com/jc-nana/lucere-python/issues/28)) ([1365d40](https://github.com/jc-nana/lucere-python/commit/1365d40e19906497a748c0f3214f3cff05b82ccd))

## 0.1.0-alpha.3 (2024-06-19)

Full Changelog: [v0.1.0-alpha.2...v0.1.0-alpha.3](https://github.com/jc-nana/lucere-python/compare/v0.1.0-alpha.2...v0.1.0-alpha.3)

### Features

* **api:** update via SDK Studio ([#12](https://github.com/jc-nana/lucere-python/issues/12)) ([d8fb578](https://github.com/jc-nana/lucere-python/commit/d8fb578fea9a4ec7534915b842f3dbbbf28399b1))

## 0.1.0-alpha.2 (2024-06-18)

Full Changelog: [v0.1.0-alpha.1...v0.1.0-alpha.2](https://github.com/jc-nana/lucere-python/compare/v0.1.0-alpha.1...v0.1.0-alpha.2)

### Features

* **api:** OpenAPI spec update via Stainless API ([4b24c82](https://github.com/jc-nana/lucere-python/commit/4b24c82d103c1000bc6df0fbacb204256b3d6eee))
* **api:** OpenAPI spec update via Stainless API ([8448fba](https://github.com/jc-nana/lucere-python/commit/8448fbaf5fd561800c7d2bee71d77cb3a441e8f2))
* **api:** OpenAPI spec update via Stainless API ([#7](https://github.com/jc-nana/lucere-python/issues/7)) ([f20a45f](https://github.com/jc-nana/lucere-python/commit/f20a45fa3d6c84fcd7e86f4da51a961e0bcf5f1b))
* **api:** update via SDK Studio ([110ff53](https://github.com/jc-nana/lucere-python/commit/110ff53b5df87d32a1dcf91e550b32625f0f29df))


### Chores

* go live ([#9](https://github.com/jc-nana/lucere-python/issues/9)) ([e557898](https://github.com/jc-nana/lucere-python/commit/e557898fb8c2fef07a20c1029a7bd732f4d0348b))

## 0.1.0-alpha.1 (2024-06-18)

Full Changelog: [v0.0.1-alpha.1...v0.1.0-alpha.1](https://github.com/jc-nana/lucere-python/compare/v0.0.1-alpha.1...v0.1.0-alpha.1)

### Features

* **api:** update via SDK Studio ([#4](https://github.com/jc-nana/lucere-python/issues/4)) ([d508e5b](https://github.com/jc-nana/lucere-python/commit/d508e5b81a4b3f8cdf12c504fa322f4d02599c5d))

## 0.0.1-alpha.1 (2024-06-18)

Full Changelog: [v0.0.1-alpha.0...v0.0.1-alpha.1](https://github.com/jc-nana/lucere-python/compare/v0.0.1-alpha.0...v0.0.1-alpha.1)

### Chores

* go live ([#2](https://github.com/jc-nana/lucere-python/issues/2)) ([c2a17cf](https://github.com/jc-nana/lucere-python/commit/c2a17cf19cf973d991f8bc9b6d9f15b90ecc350b))
* update SDK settings ([92e9755](https://github.com/jc-nana/lucere-python/commit/92e97553066af06d2491d3a31d11474662bd13ef))
* update SDK settings ([757707a](https://github.com/jc-nana/lucere-python/commit/757707a8792f0f2952517140b94fc9cf2e5f3ca2))
