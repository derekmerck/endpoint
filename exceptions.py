class EndpointException(Exception):
    pass


class EndpointHealthException(EndpointException):
    """Endpoint failed to pass health check"""
    pass


class EndpointValueException(EndpointException, ValueError):
    """Endpoint request using the wrong value"""
    pass


class EndpointTypeException(EndpointException, TypeError):
    """Endpoint request using the wrong data type"""
    pass


class EndpointRuntimeException(EndpointException, RuntimeError):
    """Endpoint failed to handle a request"""
    pass


class EndpointFactoryException(EndpointException, RuntimeError):
    """Endpoint factory failed to instantiate object"""
    pass
