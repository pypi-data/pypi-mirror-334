import pathlib

import kubernetes.client
import kubernetes.client.exceptions
import kubernetes.config
from _nebari.config import read_configuration
from loguru import logger


def get_nebari_pod_logs_tool(
    pod_names: list[str],
    since_minutes: int = 10,
    namespace: str = "dev",
    containers: str = None,
) -> dict:
    """
    Retrieve logs from specified Nebari pods.  Doesn't support wildcard or regex.

    Call get_nebari_pods_tool before using this tool to get a list of pod names.

    Be cautious when using this tool with a large number of pods or a long time range, as it may fill up the context window.

    Args:
        pod_names (list[str]): List of pod names to retrieve logs from
        since_minutes (int, optional): Time range in minutes to limit log retrieval.
                                      Defaults to 10 minutes.
        namespace (str, optional): Kubernetes namespace. Defaults to "dev".
        container (str, optional): Container name to get logs from. If None, gets logs from all containers.

    Returns:
        dict: Dictionary mapping pod names to their logs or error messages.
              Format: {pod_name: log_content_or_error_message}

    Example:
        >>> logs = get_pod_logs_tool(['jupyterhub-0', 'traefik-7d8977f88d-lt5wb'])
        >>> logs['jupyterhub-0'][:50]
        '2023-04-05 12:34:56.789 INFO: JupyterHub starting...'

    Raises:
        kubernetes.config.config_exception.ConfigException: If kube config cannot be loaded
    """
    kubernetes.config.kube_config.load_kube_config()

    v1 = kubernetes.client.CoreV1Api()

    logs = {}
    for pod_name in pod_names:
        try:
            logs[pod_name] = dict()

            if containers is None:
                containers = [
                    c.name
                    for c in v1.read_namespaced_pod(
                        name=pod_name, namespace=namespace
                    ).spec.containers
                ]

            for container in containers:
                logs[pod_name][container] = v1.read_namespaced_pod_log(
                    name=pod_name,
                    namespace=namespace,
                    since_seconds=since_minutes * 60,
                    container=container,
                )
        except kubernetes.client.exceptions.ApiException as e:
            logs[pod_name] = f"Failed to retrieve logs: {e.reason}"
            logger.error(f"Failed to retrieve logs for pod {pod_name}: {e}")

    return str(logs)


def make_get_nebari_pod_names_tool(config_filepath: pathlib.Path) -> str:
    def get_nebari_pod_names_tool():
        """
        Retrieve a list of all pods in the Nebari namespace.

        Returns:
            str: A formatted string listing all pods and their status in the Nebari
                namespace. Format: "<pod_name> <status_phase>" with each pod on a
                new line.

        Example:
            >>> get_nebari_pods_tool()
            'jupyterhub-0 Running
            traefik-7d8977f88d-lt5wb Running
            user-scheduler-0 Running'

        Raises:
            FileNotFoundError: If the configuration file cannot be found
            ValueError: If the namespace cannot be determined from config
        """
        return get_nebari_pod_names(config_filepath)

    return get_nebari_pod_names_tool


# Helper functions
def get_nebari_pod_names(config_filepath: pathlib.Path) -> str:
    """
    Retrieve a list of all pods in the Nebari namespace.

    This function reads the Nebari configuration to determine the namespace,
    then retrieves information about all pods in that namespace.
    It's designed to be used as a tool by the diagnostic agent.

    Returns:
        str: A formatted string listing all pods and their status in the Nebari
             namespace. Format: "<pod_name> <status_phase>" with each pod on a
             new line.

    Example:
        >>> get_nebari_pod_names()
        'jupyterhub-0 Running
        traefik-7d8977f88d-lt5wb Running
        user-scheduler-0 Running'

    Raises:
        FileNotFoundError: If the configuration file cannot be found
        ValueError: If the namespace cannot be determined from config
    """
    from nebari.plugins import nebari_plugin_manager

    config_schema = nebari_plugin_manager.config_schema
    namespace = read_configuration(config_filepath, config_schema).namespace

    return get_pods(namespace)


def get_pods(namespace: str) -> str:
    """
    Retrieve and format a list of Kubernetes pods in the specified namespace.

    Args:
        namespace (str): The Kubernetes namespace to query for pods

    Returns:
        str: A newline-separated string of pod names and their current status phases.
             Format: "<pod_name> <status_phase>"

    Example:
        >>> get_pods("nebari")
        'jupyterhub-0 Running
        traefik-7d8977f88d-lt5wb Running
        user-scheduler-0 Running'
    """
    kubernetes.config.kube_config.load_kube_config()

    v1 = kubernetes.client.CoreV1Api()

    pods = v1.list_namespaced_pod(namespace=namespace)
    pod_dict = pods.to_dict()
    pod_names = "\n".join(
        [f"{p['metadata']['name']} {p['status']['phase']}" for p in pod_dict["items"]]
    )
    return pod_names


if __name__ == "__main__":
    logs = get_nebari_pod_logs_tool(["nebari-grafana-74874bd867-67t7c"])
    print(logs)
