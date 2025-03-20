# Changelog

## 0.4.2 (2025-03-17)

Full Changelog: [v0.4.1...v0.4.2](https://github.com/SigmaEf5ect/sigma-sdk-python/compare/v0.4.1...v0.4.2)

### Bug Fixes

* **ci:** ensure pip is always available ([#41](https://github.com/SigmaEf5ect/sigma-sdk-python/issues/41)) ([06cf89d](https://github.com/SigmaEf5ect/sigma-sdk-python/commit/06cf89d546387a5b227f82b58de6caac8ea1e3dd))
* **ci:** remove publishing patch ([#43](https://github.com/SigmaEf5ect/sigma-sdk-python/issues/43)) ([cf0fc63](https://github.com/SigmaEf5ect/sigma-sdk-python/commit/cf0fc63a80126a20a17d0f573148fd44949ad9bc))

## 0.4.1 (2025-03-15)

Full Changelog: [v0.4.0...v0.4.1](https://github.com/SigmaEf5ect/sigma-sdk-python/compare/v0.4.0...v0.4.1)

### Bug Fixes

* **types:** handle more discriminated union shapes ([#39](https://github.com/SigmaEf5ect/sigma-sdk-python/issues/39)) ([55a22b3](https://github.com/SigmaEf5ect/sigma-sdk-python/commit/55a22b3d9628535a44fee23889a65cae9fc50674))


### Chores

* **docs:** update client docstring ([#33](https://github.com/SigmaEf5ect/sigma-sdk-python/issues/33)) ([7899368](https://github.com/SigmaEf5ect/sigma-sdk-python/commit/7899368ef9cc1759e24b4d31e024542ab9db881a))
* **internal:** bump rye to 0.44.0 ([#38](https://github.com/SigmaEf5ect/sigma-sdk-python/issues/38)) ([902a781](https://github.com/SigmaEf5ect/sigma-sdk-python/commit/902a7811a1e08e61956ddced70a7a4f1bf407bce))
* **internal:** codegen related update ([#37](https://github.com/SigmaEf5ect/sigma-sdk-python/issues/37)) ([6adca0f](https://github.com/SigmaEf5ect/sigma-sdk-python/commit/6adca0f856aa41ec4239eceb7d3b5e956ce9b943))
* **internal:** properly set __pydantic_private__ ([#30](https://github.com/SigmaEf5ect/sigma-sdk-python/issues/30)) ([c64d1fb](https://github.com/SigmaEf5ect/sigma-sdk-python/commit/c64d1fb8d4b3db9e50b08df773c49884e3d1877f))
* **internal:** remove extra empty newlines ([#36](https://github.com/SigmaEf5ect/sigma-sdk-python/issues/36)) ([41854fd](https://github.com/SigmaEf5ect/sigma-sdk-python/commit/41854fdbf818cb41c8ab2e0162106f1d00aaa2e5))
* **internal:** remove unused http client options forwarding ([#34](https://github.com/SigmaEf5ect/sigma-sdk-python/issues/34)) ([583c45b](https://github.com/SigmaEf5ect/sigma-sdk-python/commit/583c45b5c68303a9a09158192522c3fe5ae5886c))


### Documentation

* update URLs from stainlessapi.com to stainless.com ([#32](https://github.com/SigmaEf5ect/sigma-sdk-python/issues/32)) ([559ddde](https://github.com/SigmaEf5ect/sigma-sdk-python/commit/559dddefe42ba19e1b6aa4e333fc5cd4cf6bf322))

## 0.4.0 (2025-02-24)

Full Changelog: [v0.3.0...v0.4.0](https://github.com/SigmaEf5ect/sigma-sdk-python/compare/v0.3.0...v0.4.0)

### Features

* **api:** api update ([#28](https://github.com/SigmaEf5ect/sigma-sdk-python/issues/28)) ([7809e79](https://github.com/SigmaEf5ect/sigma-sdk-python/commit/7809e79ba55bb3b75c53cdc17b2f7ab40a364a7f))


### Chores

* **internal:** fix devcontainers setup ([#26](https://github.com/SigmaEf5ect/sigma-sdk-python/issues/26)) ([5937580](https://github.com/SigmaEf5ect/sigma-sdk-python/commit/5937580009ce2f08dc851e1303aaac678abbe9e6))

## 0.3.0 (2025-02-21)

Full Changelog: [v0.2.0...v0.3.0](https://github.com/SigmaEf5ect/sigma-sdk-python/compare/v0.2.0...v0.3.0)

### Features

* **client:** allow passing `NotGiven` for body ([#23](https://github.com/SigmaEf5ect/sigma-sdk-python/issues/23)) ([5206aea](https://github.com/SigmaEf5ect/sigma-sdk-python/commit/5206aea5288d86d1165e1cf2be1e0c5b04437f60))


### Bug Fixes

* **client:** mark some request bodies as optional ([5206aea](https://github.com/SigmaEf5ect/sigma-sdk-python/commit/5206aea5288d86d1165e1cf2be1e0c5b04437f60))

## 0.2.0 (2025-02-14)

Full Changelog: [v0.1.1...v0.2.0](https://github.com/SigmaEf5ect/sigma-sdk-python/compare/v0.1.1...v0.2.0)

### Features

* **client:** send `X-Stainless-Read-Timeout` header ([#18](https://github.com/SigmaEf5ect/sigma-sdk-python/issues/18)) ([7390988](https://github.com/SigmaEf5ect/sigma-sdk-python/commit/73909887d03bc31ab1de57a5bed8ff17fe2ebcaf))


### Bug Fixes

* asyncify on non-asyncio runtimes ([#21](https://github.com/SigmaEf5ect/sigma-sdk-python/issues/21)) ([a23a73c](https://github.com/SigmaEf5ect/sigma-sdk-python/commit/a23a73cbf896b5b67f8205b65d93ea8d126ec580))


### Chores

* **internal:** bummp ruff dependency ([#17](https://github.com/SigmaEf5ect/sigma-sdk-python/issues/17)) ([aaf96ed](https://github.com/SigmaEf5ect/sigma-sdk-python/commit/aaf96ed10e589e8c7ce9abaf901b0a81a7274778))
* **internal:** change default timeout to an int ([#16](https://github.com/SigmaEf5ect/sigma-sdk-python/issues/16)) ([feddf16](https://github.com/SigmaEf5ect/sigma-sdk-python/commit/feddf163d12fe0ae96c0fa8d23b0b7534f5a6bf1))
* **internal:** fix type traversing dictionary params ([#19](https://github.com/SigmaEf5ect/sigma-sdk-python/issues/19)) ([acd93c0](https://github.com/SigmaEf5ect/sigma-sdk-python/commit/acd93c090fc7678a6410f98a27ecc55e3221453e))
* **internal:** minor formatting changes ([#14](https://github.com/SigmaEf5ect/sigma-sdk-python/issues/14)) ([eaa08a9](https://github.com/SigmaEf5ect/sigma-sdk-python/commit/eaa08a939ebf374ea8961b21745601d0fdcaf679))

## 0.1.1 (2025-01-22)

Full Changelog: [v0.1.0...v0.1.1](https://github.com/SigmaEf5ect/sigma-sdk-python/compare/v0.1.0...v0.1.1)

### Bug Fixes

* **tests:** make test_get_platform less flaky ([#10](https://github.com/SigmaEf5ect/sigma-sdk-python/issues/10)) ([b57a3f5](https://github.com/SigmaEf5ect/sigma-sdk-python/commit/b57a3f5d8a3e85653fe62ae8b97ff4d2135dc54e))


### Chores

* **internal:** avoid pytest-asyncio deprecation warning ([#11](https://github.com/SigmaEf5ect/sigma-sdk-python/issues/11)) ([cf8f570](https://github.com/SigmaEf5ect/sigma-sdk-python/commit/cf8f5703d338c7d8cbfaba7817170f8227ce9b00))
* **internal:** codegen related update ([#12](https://github.com/SigmaEf5ect/sigma-sdk-python/issues/12)) ([767bb89](https://github.com/SigmaEf5ect/sigma-sdk-python/commit/767bb89ece9430cfe0d46f03c14e2a85092f4b0a))
* **internal:** codegen related update ([#7](https://github.com/SigmaEf5ect/sigma-sdk-python/issues/7)) ([1f84d5d](https://github.com/SigmaEf5ect/sigma-sdk-python/commit/1f84d5dcd5b094379bacca0d2ad5b42a3e12ec1c))


### Documentation

* **raw responses:** fix duplicate `the` ([#9](https://github.com/SigmaEf5ect/sigma-sdk-python/issues/9)) ([41a75d9](https://github.com/SigmaEf5ect/sigma-sdk-python/commit/41a75d9f2b4fa2ad20eb86786aab623079aecab3))

## 0.1.0 (2025-01-10)

Full Changelog: [v0.0.1...v0.1.0](https://github.com/SigmaEf5ect/sigma-sdk-python/compare/v0.0.1...v0.1.0)

### Features

* **api:** update via SDK Studio ([#4](https://github.com/SigmaEf5ect/sigma-sdk-python/issues/4)) ([f4fed85](https://github.com/SigmaEf5ect/sigma-sdk-python/commit/f4fed85f8573cbd8deabb6df3d31b8329e9f8937))

## 0.0.1 (2025-01-10)

Full Changelog: [v0.0.1-alpha.0...v0.0.1](https://github.com/SigmaEf5ect/sigma-sdk-python/compare/v0.0.1-alpha.0...v0.0.1)

### Chores

* go live ([bf4c93b](https://github.com/SigmaEf5ect/sigma-sdk-python/commit/bf4c93b2d494b045ee12abbef4c4b41352273113))
* update SDK settings ([#2](https://github.com/SigmaEf5ect/sigma-sdk-python/issues/2)) ([ffef085](https://github.com/SigmaEf5ect/sigma-sdk-python/commit/ffef0859dcb7380acb7ede0c418816cd7166a10c))
