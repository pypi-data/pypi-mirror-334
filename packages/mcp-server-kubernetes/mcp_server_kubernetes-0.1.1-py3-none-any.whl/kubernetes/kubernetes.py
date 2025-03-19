from subprocess import check_output
from typing import Optional
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("kubernetes_core")

################################
# Define the first kubernetes tool "kubectl_describe"
################################
@mcp.tool()
def kubectl_describe(kind: str, name: str, namespace: Optional[str] = None):
    """Run kubectl describe <kind> <name> -n <namespace>"""
    if namespace:
        command = f"kubectl describe {kind} {name} -n {namespace}"
    else:
        command = f"kubectl describe {kind} {name}"
    output = check_output(command.split()).decode()
    return output

@mcp.tool()
def kubectl_get_by_name(name: str):
    """Example 2: Get a Kubernetes resource by its name."""
    command = f"kubectl get {name}"
    output = check_output(command.split()).decode()
    return output

@mcp.tool()
def kubectl_exec_into_pod(podname: str, containername: str, command: str, namespace: Optional[str] = None):
    """Example 3: Execute a command in a specific container within a pod."""
    if namespace:
        exec_command = f"kubectl exec {podname} -c {containername} -n {namespace} -- {command}"
    else:
        exec_command = f"kubectl exec {podname} -c {containername} -- {command}"
    output = check_output(exec_command.split()).decode()
    return output

@mcp.tool()
def kubectl_get_by_kind_in_namespace(kind: str, namespace: str):
    """Example 4: Get Kubernetes resources of a certain kind in a specific namespace."""
    command = f"kubectl get {kind} -n {namespace}"
    output = check_output(command.split()).decode()
    return output

@mcp.tool()
def kubectl_previous_logs(pod_name: str, namespace: Optional[str] = None):
    """Run `kubectl logs --previous` on a single Kubernetes pod. 
    Used to fetch logs for a pod that crashed and see logs from before the crash.
    Never give a deployment name or a resource that is not a pod.
    """
    if namespace:
        command = f"kubectl logs {pod_name} -n {namespace} --previous"
    else:
        command = f"kubectl logs {pod_name} --previous"
    output = check_output(command.split()).decode()
    return output


def main():
    mcp.run(transport='stdio')

if __name__ == "__main__":
    main()
