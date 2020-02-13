workspace(name = "bark_project")

load("@bazel_tools//tools/build_defs/repo:http.bzl", "http_archive", "http_file")
load("@bazel_tools//tools/build_defs/repo:git.bzl", "git_repository")


# ---- BARK Internal Dependencies ----------------
load("@bark_project//tools:deps.bzl", "bark_dependencies")
bark_dependencies()


load("@com_github_nelhage_rules_boost//:boost/boost.bzl", "boost_deps")
boost_deps()
# -------------------------------------------------



# ------ Planner UCT ------------------------------
git_repository(
  name = "planner_uct",
  branch="master",
  remote = "https://github.com/bark-simulator/planner-mcts"
)
load("@planner_uct//util:deps.bzl", "planner_uct_rules_dependencies")
planner_uct_rules_dependencies()
# --------------------------------------------------



# ------ Planner BARK-ML ---------------------------
git_repository(
  name = "bark_ml",
  branch="master",
  remote = "https://github.com/bark-simulator/bark-ml"
)

load("@bark_ml//utils:dependencies.bzl", "load_bark")
load_bark()
# --------------------------------------------------



# -------- Benchmark Database -----------------------
git_repository(
  name = "benchmark_database",
  commit="436e665360daac6ac19285b2aab64bb27a2bc02d",
  remote = "https://github.com/bark-simulator/benchmark-database"
)

load("@benchmark_database//util:deps.bzl", "benchmark_database_dependencies")
load("@benchmark_database//load:load.bzl", "benchmark_database_release")
benchmark_database_dependencies()
benchmark_database_release()
# --------------------------------------------------