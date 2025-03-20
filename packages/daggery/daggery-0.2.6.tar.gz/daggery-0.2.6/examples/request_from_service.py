# examples/request_from_service.py
import requests

from daggery.description import DAGDescription, Operation, OperationSequence
from examples.fastapi_service import EvaluateRequest


def main():
    service_url = "http://localhost:8001/evaluate"

    # Example 1: Simple string-based operation sequence
    simple_request = EvaluateRequest(
        name="simple_chain", value=5, operations="foo >> bar >> baz"
    )

    response = requests.post(service_url, json=simple_request.model_dump())
    if response.status_code == 200:
        print("String-based request result:", response.json())
    else:
        print("Error:", response.text)

    # Example 2: Structured DAGDescription with argument mappings
    structured_ops = OperationSequence(
        ops=(
            Operation(name="foo", op_name="foo", children=("bar",)),
            Operation(name="bar", op_name="bar", children=("baz",)),
            Operation(name="baz", op_name="baz"),
        )
    )

    complex_request = EvaluateRequest(
        name="structured_dag",
        value=5,
        operations=DAGDescription(operations=structured_ops),
    )

    response = requests.post(service_url, json=complex_request.model_dump())
    if response.status_code == 200:
        print("Structured request result:", response.json())
    else:
        print("Error:", response.text)


if __name__ == "__main__":
    main()

# To run the service first:
# uvicorn examples.fastapi_service:app --port 8001 --reload
