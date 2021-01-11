# Changelog

## [0.0.8](https://github.com/T-Systems-MMS/ansible-collection-letsencrypt/tree/0.0.8) (2021-01-11)

[Full Changelog](https://github.com/T-Systems-MMS/ansible-collection-letsencrypt/compare/0.0.7...0.0.8)

**Closed issues:**

- Integration Tests for role [\#3](https://github.com/T-Systems-MMS/ansible-collection-letsencrypt/issues/3)

**Merged pull requests:**

- fix galaxy-release action [\#29](https://github.com/T-Systems-MMS/ansible-collection-letsencrypt/pull/29) ([rndmh3ro](https://github.com/rndmh3ro))
- adjust variable naming in example files and readme [\#27](https://github.com/T-Systems-MMS/ansible-collection-letsencrypt/pull/27) ([avalor1](https://github.com/avalor1))
- Create runtime.yml [\#26](https://github.com/T-Systems-MMS/ansible-collection-letsencrypt/pull/26) ([rndmh3ro](https://github.com/rndmh3ro))
- Create LICENSE [\#25](https://github.com/T-Systems-MMS/ansible-collection-letsencrypt/pull/25) ([rndmh3ro](https://github.com/rndmh3ro))
- run tests on a schedule [\#24](https://github.com/T-Systems-MMS/ansible-collection-letsencrypt/pull/24) ([rndmh3ro](https://github.com/rndmh3ro))
- build integration tests [\#23](https://github.com/T-Systems-MMS/ansible-collection-letsencrypt/pull/23) ([rndmh3ro](https://github.com/rndmh3ro))

## [0.0.7](https://github.com/T-Systems-MMS/ansible-collection-letsencrypt/tree/0.0.7) (2020-12-15)

[Full Changelog](https://github.com/T-Systems-MMS/ansible-collection-letsencrypt/compare/0.0.6...0.0.7)

**Fixed bugs:**

- fix broken AutoDNS wildcard creation \#20 [\#21](https://github.com/T-Systems-MMS/ansible-collection-letsencrypt/pull/21) ([avalor1](https://github.com/avalor1))

**Closed issues:**

- creation of wildcard certificates with autodns challenge not working with release 0.0.5 [\#20](https://github.com/T-Systems-MMS/ansible-collection-letsencrypt/issues/20)

## [0.0.6](https://github.com/T-Systems-MMS/ansible-collection-letsencrypt/tree/0.0.6) (2020-12-15)

[Full Changelog](https://github.com/T-Systems-MMS/ansible-collection-letsencrypt/compare/0.0.5...0.0.6)

**Implemented enhancements:**

- Add Hetzner DNS as letsencrypt\_dns\_provider [\#22](https://github.com/T-Systems-MMS/ansible-collection-letsencrypt/pull/22) ([xobtoor](https://github.com/xobtoor))

## [0.0.5](https://github.com/T-Systems-MMS/ansible-collection-letsencrypt/tree/0.0.5) (2020-12-09)

[Full Changelog](https://github.com/T-Systems-MMS/ansible-collection-letsencrypt/compare/0.0.4...0.0.5)

**Implemented enhancements:**

- Push to Galaxy Fails [\#13](https://github.com/T-Systems-MMS/ansible-collection-letsencrypt/issues/13)
- add second checkout to solve race condition \(version gets updated but… [\#15](https://github.com/T-Systems-MMS/ansible-collection-letsencrypt/pull/15) ([avalor1](https://github.com/avalor1))

**Closed issues:**

- subject\_alt\_name not optional [\#9](https://github.com/T-Systems-MMS/ansible-collection-letsencrypt/issues/9)

**Merged pull requests:**

- fix ansible error if group is empty [\#19](https://github.com/T-Systems-MMS/ansible-collection-letsencrypt/pull/19) ([avalor1](https://github.com/avalor1))
- remove common\_name variable [\#18](https://github.com/T-Systems-MMS/ansible-collection-letsencrypt/pull/18) ([avalor1](https://github.com/avalor1))
- remove letsencrypt\_create\_private\_keys variable from examples [\#17](https://github.com/T-Systems-MMS/ansible-collection-letsencrypt/pull/17) ([avalor1](https://github.com/avalor1))

## [0.0.4](https://github.com/T-Systems-MMS/ansible-collection-letsencrypt/tree/0.0.4) (2020-11-12)

[Full Changelog](https://github.com/T-Systems-MMS/ansible-collection-letsencrypt/compare/0.0.3...0.0.4)

**Implemented enhancements:**

- add description of force\_renewal variable [\#12](https://github.com/T-Systems-MMS/ansible-collection-letsencrypt/pull/12) ([avalor1](https://github.com/avalor1))

**Merged pull requests:**

- update checkout version for release workflow [\#11](https://github.com/T-Systems-MMS/ansible-collection-letsencrypt/pull/11) ([avalor1](https://github.com/avalor1))
- update checkout version in galaxy push workflow [\#10](https://github.com/T-Systems-MMS/ansible-collection-letsencrypt/pull/10) ([avalor1](https://github.com/avalor1))

## [0.0.3](https://github.com/T-Systems-MMS/ansible-collection-letsencrypt/tree/0.0.3) (2020-11-12)

[Full Changelog](https://github.com/T-Systems-MMS/ansible-collection-letsencrypt/compare/0.0.2...0.0.3)

**Closed issues:**

- Remove unwanted files from release-tarball  [\#4](https://github.com/T-Systems-MMS/ansible-collection-letsencrypt/issues/4)

**Merged pull requests:**

- Add Azure dns provider challenge [\#8](https://github.com/T-Systems-MMS/ansible-collection-letsencrypt/pull/8) ([michaelamattes](https://github.com/michaelamattes))

## [0.0.2](https://github.com/T-Systems-MMS/ansible-collection-letsencrypt/tree/0.0.2) (2020-11-06)

[Full Changelog](https://github.com/T-Systems-MMS/ansible-collection-letsencrypt/compare/0.0.1...0.0.2)

**Merged pull requests:**

- remove variable letsencrypt\_create\_private\_keys [\#7](https://github.com/T-Systems-MMS/ansible-collection-letsencrypt/pull/7) ([avalor1](https://github.com/avalor1))
- add build\_ignore to filter unwanted files from release-tarball [\#6](https://github.com/T-Systems-MMS/ansible-collection-letsencrypt/pull/6) ([avalor1](https://github.com/avalor1))

## [0.0.1](https://github.com/T-Systems-MMS/ansible-collection-letsencrypt/tree/0.0.1) (2020-11-04)

[Full Changelog](https://github.com/T-Systems-MMS/ansible-collection-letsencrypt/compare/6c0445f6769360d1b8ea12df58483ac4a8b602f3...0.0.1)

**Merged pull requests:**

- Workflows [\#2](https://github.com/T-Systems-MMS/ansible-collection-letsencrypt/pull/2) ([avalor1](https://github.com/avalor1))
- add Workflows [\#1](https://github.com/T-Systems-MMS/ansible-collection-letsencrypt/pull/1) ([avalor1](https://github.com/avalor1))



\* *This Changelog was automatically generated by [github_changelog_generator](https://github.com/github-changelog-generator/github-changelog-generator)*
