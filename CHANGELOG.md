# Changelog

## [0.2.0](https://github.com/nomios-opensource/yapyang/compare/v0.1.0...v0.2.0) (2024-08-14)


### ⚠ BREAKING CHANGES

* add type annotation check ([#5](https://github.com/nomios-opensource/yapyang/issues/5))

### Features

* add auto node identifier derived from class name ([ef58234](https://github.com/nomios-opensource/yapyang/commit/ef58234b355dcf5499b5a3fead62a473a7d70f01))
* add type annotation check ([#5](https://github.com/nomios-opensource/yapyang/issues/5)) ([c72a2b9](https://github.com/nomios-opensource/yapyang/commit/c72a2b9766e2aa4508fe1de0e6da265adb4bb639))
* implement YANG leaf list node mvp ([2c817ca](https://github.com/nomios-opensource/yapyang/commit/2c817ca0b52efc79021b2c7de15df3cda909b7d4))


### Bug Fixes

* change method of calling _cls_meta_args_resolver ([85e8d84](https://github.com/nomios-opensource/yapyang/commit/85e8d84b38067a102b127dc97693a2b5d1e1bec0))


### Documentation

* add mkdocs ([e886dd1](https://github.com/nomios-opensource/yapyang/commit/e886dd177a33eeed38501cf4b71996406c7936e7))
* add quick start to README.md ([37b0959](https://github.com/nomios-opensource/yapyang/commit/37b095938938c2f934e2566e990f7213b801a185))
* add shields to README.md ([5ba7700](https://github.com/nomios-opensource/yapyang/commit/5ba7700d8943adf97e9fdba76c18e884bc0275c3))
* format quick start code blocks ([f3bae97](https://github.com/nomios-opensource/yapyang/commit/f3bae97674ce3d02c0ea21a5c95f4f661cd7e12e))

## 0.1.0 (2024-07-26)


### Features

* add metadata wrapper for YANG model fields ([a9a21ea](https://github.com/nomios-opensource/yapyang/commit/a9a21eafd9f41fc09538f52a91acfbd063e12952))
* add XML serialization for Module, Container, List, Leaf nodes ([149043f](https://github.com/nomios-opensource/yapyang/commit/149043fc3ed2928f37cb0f356dc289c50bd1f96a))
* added initializer for ModuleNode ([44c65fe](https://github.com/nomios-opensource/yapyang/commit/44c65fe72f144f6a320427e13b3eb6ba5d9c0a76))
* implement YANG list node MVP ([b43c9fc](https://github.com/nomios-opensource/yapyang/commit/b43c9fcf00b8409b4e03d98e35c12e849d0357c1))
* prevent YANG nodes from direct instantiation ([3473442](https://github.com/nomios-opensource/yapyang/commit/34734426faa8a5cee1438dec7b7e4b05050f07bf))
* treat dunder cls attributes as metadata ([ac4ecf1](https://github.com/nomios-opensource/yapyang/commit/ac4ecf1ef65a601c9fa00f24fa2f24c39da72381))


### Bug Fixes

* add support for Python 3.8 ([7ac187b](https://github.com/nomios-opensource/yapyang/commit/7ac187ba34a1b6fc9fd9571d759efbc5a3954b33))
* added type annotations and renamed args ([b54dc35](https://github.com/nomios-opensource/yapyang/commit/b54dc351f2c8e727b803b81c5aa68b34284d6ce0))
* moved package version ([0b8d890](https://github.com/nomios-opensource/yapyang/commit/0b8d890ccbfb6bce03b8b645a3adb1b06a59e3d5))


### Documentation

* add summary to README.md ([abeaf49](https://github.com/nomios-opensource/yapyang/commit/abeaf497749731a1c8a9eaf3ddb63fa1426dc11f))
* added ruff and pytest options ([5bec3b1](https://github.com/nomios-opensource/yapyang/commit/5bec3b17338fd02a8e89ad6a819810dae6207bb1))
