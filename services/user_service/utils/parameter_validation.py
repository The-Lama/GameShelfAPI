import logging
from functools import wraps

from flask import jsonify, request

logger = logging.getLogger(__name__)


def validate_parameter(parameter: str, parameter_type: type) -> type:
    """
    Validate that the parameter can be converted to the specified type.

    Args:
        parameter (str): The parameter value to be validated.
        parameter_type (type): The type to which the parameter should be converted.

    Returns:
        The parameter converted to parameter_type.

    Raises:
        ValueError: If the parameter cannot be converted to parameter_type.
    """
    try:
        converted_parameter = parameter_type(parameter)
        return converted_parameter
    except ValueError as e:
        logger.warning(
            f"Invalid parameter '{parameter}' for type {parameter_type.__name__}: {e}"
        )
        raise ValueError(f"parameter must be of type {parameter_type.__name__}") from e


def validate_parameters(source: str, *parameters):
    """
    Validate parameters in a request query or JSON body as decorator.

    Args:
        source (str): The source of the parameters ("query" or "json")
        *parameters: A variable-length tuple of required parameters.
                     Each parameter should be specified as a tuple:
                     (parameter_name (str), parameter_type (type))

    Returns:
        function: The wrapped view function with the validated parameters added to kwargs.
    """

    def decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            if source == "query":
                data = request.args
            elif source == "json":
                data = request.get_json() or {}
            else:
                raise ValueError(f"Unsupported parameter source: {source}")

            validated_parameters = {}
            for parameter_name, parameter_type in parameters:
                value = data.get(parameter_name)

                if value is None:
                    logger.warning(f"Missing parameter for {parameter_name}.")
                    return jsonify({"error": f"{parameter_name} is required"}), 400

                try:
                    validated_parameters[parameter_name] = validate_parameter(
                        value, parameter_type
                    )
                except ValueError as e:
                    return jsonify({"error": str(e)}), 400

            kwargs.update(validated_parameters)
            return function(*args, **kwargs)

        return wrapper

    return decorator


def validate_query_parameters(*parameters):
    """Validate query parameters in GET requests."""
    return validate_parameters("query", *parameters)


def validate_json_parameters(*parameters):
    """Validate query parameters in POST requests."""
    return validate_parameters("json", *parameters)
