# Installs executable dependencies on the CI before running tests.

cargo install --debug --locked swh_graph_topology --version 6.3.0

cargo install --debug --locked swh-provenance-db-build --git https://gitlab.softwareheritage.org/swh/devel/swh-provenance.git --rev eda122d8cc156aab4a7fc888455341add2dc27c6
