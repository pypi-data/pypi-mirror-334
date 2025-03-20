import sys

from get_pod_logs import get_nebari_pod_logs_tool


def main():
    """Test the get_nebari_pod_logs_tool function with a specific pod."""
    pod_name = "nebari-grafana-74874bd867-67t7c"

    # Parse command line arguments for container name
    container = None
    if len(sys.argv) > 1:
        container = sys.argv[1]

    # Get logs for the last 10 minutes by default
    logs = get_nebari_pod_logs_tool(pod_names=[pod_name], container=container)

    container_msg = f" (container: {container})" if container else ""
    print(f"Logs for {pod_name}{container_msg}:")
    print("=" * 50)
    print(logs)
    print("=" * 50)


if __name__ == "__main__":
    main()
