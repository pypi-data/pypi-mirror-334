import importlib.resources as pkg_resources
import os


def get_installed_graph_descriptions_path():
    package_name = 'fhir_aggregator_client'
    resource_path = 'graph-definitions'
    try:
        print(pkg_resources.files(package_name))
        resource = pkg_resources.files(package_name).joinpath(resource_path)
        if resource.is_dir():
            return str(resource)
        else:
            raise FileNotFoundError(f"{resource_path} directory not found in the installed package.")
    except Exception as e:
        raise RuntimeError(f"Error locating {resource_path} directory: {e}")


def test_installed_graph_definitions():
    graph_descriptions_path = get_installed_graph_descriptions_path()

    # Check if the graph_descriptions directory exists
    assert os.path.isdir(graph_descriptions_path), f"graph_descriptions directory {graph_descriptions_path} is not installed"
